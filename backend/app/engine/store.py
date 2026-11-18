"""SQLite snapshots and append-only message/version/execution records."""
import hashlib
import json
import sqlite3
from pathlib import Path
from backend.app.schemas.plan import now

class PlanningStore:
    def __init__(self, database_path: str = ":memory:"):
        if database_path != ":memory:":
            Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(database_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.connection.executescript("""
        PRAGMA foreign_keys=ON;
        CREATE TABLE IF NOT EXISTS engine_state(id INTEGER PRIMARY KEY CHECK(id=1), payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS plan_versions(id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL,
            summary TEXT NOT NULL, affected_areas TEXT NOT NULL, snapshot TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS original_messages(id INTEGER PRIMARY KEY AUTOINCREMENT, digest TEXT UNIQUE,
            payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS executions(id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL,
            payload TEXT NOT NULL);
        """)
        self.connection.commit()

    def load(self):
        row = self.connection.execute("SELECT payload FROM engine_state WHERE id=1").fetchone()
        return json.loads(row[0]) if row else None

    def save(self, state: dict, summary: str, areas: list[str], version: bool = False, execution: dict | None = None):
        with self.connection:
            if version:
                cursor = self.connection.execute("INSERT INTO plan_versions(timestamp,summary,affected_areas,snapshot) VALUES(?,?,?,?)",
                                                 (now(), summary, json.dumps(areas), json.dumps(state)))
                state["plan"]["version"] = cursor.lastrowid
                self.connection.execute("UPDATE plan_versions SET snapshot=? WHERE id=?", (json.dumps(state), cursor.lastrowid))
            self.connection.execute("INSERT INTO engine_state(id,payload) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload", (json.dumps(state),))
            for message in state.get("messages", []):
                digest = hashlib.sha256(message.get("raw", message["text"]).encode()).hexdigest()
                self.connection.execute("INSERT OR IGNORE INTO original_messages(digest,payload) VALUES(?,?)", (digest, json.dumps(message)))
            if execution:
                self.connection.execute("INSERT INTO executions(timestamp,payload) VALUES(?,?)", (now(), json.dumps(execution)))
        return state["plan"].get("version", 0)

    def history(self):
        return [{"version": row["id"], "timestamp": row["timestamp"], "summary": row["summary"],
                 "affected_areas": json.loads(row["affected_areas"])} for row in
                self.connection.execute("SELECT id,timestamp,summary,affected_areas FROM plan_versions ORDER BY id DESC LIMIT 200")]

    def version(self, identifier: int):
        row = self.connection.execute("SELECT snapshot FROM plan_versions WHERE id=?", (identifier,)).fetchone()
        return json.loads(row[0]) if row else None

    def executions(self):
        return [json.loads(row[0]) for row in self.connection.execute("SELECT payload FROM executions ORDER BY id DESC LIMIT 100")]

