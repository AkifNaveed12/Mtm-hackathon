import { type ReactNode, useEffect, useRef } from "react";

// Adapted from the local ui-library table, plain-card, button-actions and dialog bundles.
// Native semantics keep these operational views small, keyboard accessible and dependency free.
export function Icon({
  name,
  size = 18,
  className = "",
}: {
  name: string;
  size?: number;
  className?: string;
}) {
  const paths: Record<string, ReactNode> = {
    dashboard: (
      <>
        <rect x="3" y="3" width="7" height="7" rx="1" />
        <rect x="14" y="3" width="7" height="7" rx="1" />
        <rect x="3" y="14" width="7" height="7" rx="1" />
        <rect x="14" y="14" width="7" height="7" rx="1" />
      </>
    ),
    messages: (
      <>
        <path d="M21 15a3 3 0 0 1-3 3H8l-5 4V6a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3Z" />
        <path d="M7 8h10M7 12h7" />
      </>
    ),
    venue: (
      <>
        <path d="M20 10c0 6-8 11-8 11S4 16 4 10a8 8 0 1 1 16 0Z" />
        <circle cx="12" cy="10" r="2.5" />
      </>
    ),
    schedule: (
      <>
        <rect x="3" y="5" width="18" height="16" rx="2" />
        <path d="M16 3v4M8 3v4M3 11h18M8 15h3M14 15h2" />
      </>
    ),
    judging: (
      <>
        <circle cx="9" cy="7" r="3" />
        <path d="M3 21v-3a6 6 0 0 1 12 0v3M16 4a3 3 0 0 1 0 6M18 15a5 5 0 0 1 3 5" />
      </>
    ),
    food: (
      <>
        <path d="M5 3v6a3 3 0 0 0 6 0V3M8 3v18M20 3c-4 3-4 9 0 9V3Zm0 9v9" />
      </>
    ),
    budget: (
      <>
        <rect x="3" y="5" width="18" height="15" rx="2" />
        <path d="M3 9h18M16 15h2M7 3v2" />
      </>
    ),
    trace: (
      <>
        <path d="m8 5-6 7 6 7m8-14 6 7-6 7m-3-17-2 20" />
      </>
    ),
    rejected: (
      <>
        <path d="m12 3 10 18H2L12 3Z" />
        <path d="M12 9v4m0 4h.01" />
      </>
    ),
    history: (
      <>
        <path d="M3 11a9 9 0 1 1 2 7M3 4v7h7M12 7v5l4 2" />
      </>
    ),
    whatsapp: (
      <>
        <path d="M21 11a9 9 0 0 1-9 10 9 9 0 0 1-4-.9L3 22l1.9-5A9 9 0 1 1 21 11Z" />
        <path d="M8 7c0 5 4 9 8 9l1-3-3-1-1 1-2-2 1-1-1-3Z" />
      </>
    ),
    play: <path d="m8 4 13 8-13 8V4Z" />,
    upload: (
      <>
        <path d="m7 8 5-5 5 5m-5-5v13M4 16v5h16v-5" />
      </>
    ),
    download: (
      <>
        <path d="m7 11 5 5 5-5m-5 5V3M4 16v5h16v-5" />
      </>
    ),
    refresh: (
      <>
        <path d="M20 7a8 8 0 1 0 1 8M20 3v5h-5" />
      </>
    ),
    check: <path d="m5 12 4 4L20 5" />,
    close: <path d="m6 6 12 12M6 18 18 6" />,
    menu: <path d="M3 6h18M3 12h18M3 18h18" />,
    arrow: <path d="M4 12h16m-6-6 6 6-6 6" />,
    sun: (
      <>
        <circle cx="12" cy="12" r="4" />
        <path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1 1m12 12 1 1M5 19l1-1M18 6l1-1" />
      </>
    ),
    search: (
      <>
        <circle cx="10" cy="10" r="6" />
        <path d="m15 15 6 6" />
      </>
    ),
    clock: (
      <>
        <circle cx="12" cy="12" r="9" />
        <path d="M12 7v5l3 2" />
      </>
    ),
    shield: (
      <>
        <path d="M12 2 3 6v6c0 6 9 10 9 10s9-4 9-10V6L12 2Z" />
        <path d="m8 12 3 3 5-6" />
      </>
    ),
    bolt: <path d="m13 2-9 12h7l-1 8 10-13h-7l1-7Z" />,
  };
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      className={className}
    >
      {paths[name] || paths.dashboard}
    </svg>
  );
}

export function Badge({
  children,
  tone = "muted",
}: {
  children: ReactNode;
  tone?: "muted" | "success" | "warning" | "danger" | "accent" | "airforce" | "purple";
}) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}
export function Panel({
  title,
  subtitle,
  action,
  children,
  className = "",
  noPadding = false,
}: {
  title: string;
  subtitle?: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
  noPadding?: boolean;
}) {
  return (
    <section className={`panel ${className}`}>
      <div className="panel-header">
        <div>
          <h2 className="text-[15px] font-semibold">{title}</h2>
          {subtitle ? (
            <p className="mt-1 text-xs text-muted">{subtitle}</p>
          ) : null}
        </div>
        {action}
      </div>
      <div className={noPadding ? "" : "panel-body"}>{children}</div>
    </section>
  );
}
export function Empty({
  title = "No plan yet",
  text = "Import a message pack to generate your first event plan.",
  action,
}: {
  title?: string;
  text?: string;
  action?: ReactNode;
}) {
  return (
    <div className="py-14 px-5 text-center">
      <div className="mx-auto mb-4 grid h-12 w-12 place-items-center rounded-xl border border-line bg-elevated text-accent">
        <Icon name="messages" size={23} />
      </div>
      <h3 className="font-semibold">{title}</h3>
      <p className="mx-auto mt-2 max-w-md text-sm text-muted">{text}</p>
      {action ? <div className="mt-5">{action}</div> : null}
    </div>
  );
}
export function Stat({
  label,
  value,
  note,
  icon,
  tone,
}: {
  label: string;
  value: ReactNode;
  note?: string;
  icon?: string;
  tone?: string;
}) {
  return (
    <div className="panel p-5">
      <div className="mb-4 flex items-center justify-between gap-3 text-xs text-muted">
        <span>{label}</span>
        {icon ? <Icon name={icon} size={17} /> : null}
      </div>
      <div className={`stat-value ${tone || ""}`}>{value}</div>
      {note ? <p className="mt-2 text-[11px] text-muted">{note}</p> : null}
    </div>
  );
}
export function Table({
  headers,
  rows,
  caption,
}: {
  headers: string[];
  rows: ReactNode[][];
  caption?: string;
}) {
  return (
    <div className="scroll-table">
      <table className="data-table">
        {caption ? <caption>{caption}</caption> : null}
        <thead>
          <tr>
            {headers.map((header) => (
              <th key={header} scope="col">
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.length ? (
            rows.map((row, index) => (
              <tr key={index}>
                {row.map((cell, i) => (
                  <td key={i}>{cell}</td>
                ))}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={headers.length} className="text-center text-muted">
                No records available.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
export function Modal({
  title,
  children,
  onClose,
  footer,
}: {
  title: string;
  children: ReactNode;
  onClose: () => void;
  footer?: ReactNode;
}) {
  const dialog = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const element = dialog.current;
    element?.showModal();
    return () => element?.close();
  }, []);
  return (
    <dialog
      ref={dialog}
      onCancel={onClose}
      className="modal panel m-auto p-0 text-foreground backdrop:bg-black/70"
      aria-label={title}
    >
      <div className="panel-header">
        <h2 className="text-lg font-semibold">{title}</h2>
        <button className="btn" onClick={onClose} aria-label="Close dialog">
          <Icon name="close" />
        </button>
      </div>
      <div className="panel-body">{children}</div>
      {footer ? (
        <div className="flex justify-end gap-3 border-t border-line p-5">
          {footer}
        </div>
      ) : null}
    </dialog>
  );
}
