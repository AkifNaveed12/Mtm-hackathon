Mind to Machine Hackathon
Student Brief  ·  18 November 2026

Your task

Build an agent system that reads a pack of messages and plans a 4-hour physical hackathon in Islamabad for
150 students in 50 teams. Yes, you are planning the event you are sitting in.

The plan must cover five areas: venue, schedule, food, judging, and budget. It must respect every constraint
the messages state, including kinds of constraint that do not appear in the sample pack.

The message pack. Every fact your system needs is inside a pack of about ten messages: emails, WhatsApp
texts, and notices, in English and Roman Urdu. Some messages are irrelevant and some are out of date. You
build against the sample pack below. At judging you get a pack you have not seen, with different numbers,
different wording, and different senders.

Your system must do five things.

1. Read every message from a text file, exactly as given. Do not type facts into your code.

2. Take every message in the same way, through the same command. No flags, hints, or edits from you.

3. Print a trace: every model call numbered, with the model name, one area tag (reading, venue,

schedule, food, judging, or budget), its input, its output, and its token counts as the model reports
them. End the trace with total tokens.

4. Accept new messages after the first run, and update the existing plan.

5. When a message conflicts with a rule or with other facts, keep the plan valid and print the reason in

the trace.

Limits.

•

Bring your own model access. Use any model, or several: paid, free, or running on your laptop.

• A full run is cut off after 2 minutes.

• An update after a new message may use at most 5 model calls and is cut off after 1 minute.

•

You may use any AI tools to write your code.

A user interface is now scored. Show your plan, your trace and any rejected messages clearly. A web page, an
app, or well-formatted terminal output can all score well. The printed trace is still required.

The day

Time

10:00

1:25

What happens

Build starts

Code freeze. Push your code and submit your repo link and commit hash. No changes
after this.

Page 1 of 4

Time

1:30

What happens

Test run, whole room at once

2:30 to 4:30

Judges visit your table

Before you start

•

•

Create a git repo now and push often. Add the organizers if it is private. Do not leave the final push to
the last minute.

Test your model access in the first few minutes: keys, rate limits and speed. A local model must finish
a full run within 2 minutes.

• Ask rule questions only at the help desk. Judges do not answer questions during the build. Every

clarification is posted in the all-teams WhatsApp group and announced in both rooms.

How you are judged

The test run. Every team in both rooms runs the same test at the same moment. A volunteer sits with your
team, times your runs and records what happens.

1. Before you run, the volunteer checks that git status shows no changes and that git log -1 matches the

hash you submitted.

2. The unseen message pack is released by link. Run it with your one command.

3. Three more messages are released one at a time. Run each as it arrives.

4. Before one of them, write down which areas will make model calls and hand the slip to the volunteer.

5. Two of the three messages change the task. One is plausible but wrong, and you will not be told

which.

6. Save your final plan and full trace to a file and upload it on the form.

The judge visits. Two judges visit your table separately. All three members must stay at the table. Each judge
looks at your saved plan, trace and interface, then draws one member by lot and asks two questions about
your system. There are no presentations and no slides. You may walk the judge through your trace and
interface.

The points.

Component

Output

Catching the wrong
message

Points What earns them

30

20

Your plan from the unseen pack passes six checks: correct figures,
within budget, venue fits, schedule valid, enough judges, all areas
covered.

Your plan stays valid, and your trace says why the message was
rejected.

Page 2 of 4

Component

Understanding

Handling change

UI

Predicting a change

Token use

Total

Points What earns them

The drawn member explains what each part of the system is for
and what would break without it. Scored by both judges.

After each change, the plan is valid again, and only the affected
areas made model calls.

Your interface shows the plan, the trace and rejected messages
clearly and is easy to use. Scored by both judges.

Your written prediction matches what your system did.

Your full run is among the leanest in the room, and your plan
passes every check.

20

10

10

5

5

100

Bonus: 10 points. You earn it if every model call in your runs uses a model on the organizers’ small-model list,
which includes any model running on your own laptop. Your plan must pass every check.

Tie-breaks, in order: catching the wrong message, handling change, token use.

Things to know

•

•

•

•

Fewer tokens score higher. Use a model where language needs reading, and plain code where
arithmetic will do.

The number of agents earns nothing. A part of your system you cannot justify costs you points.

You are scored on what you understand and what you decided, not on how much code you have.

Every member should be able to explain the system. The draw decides who answers.

• No dataset is needed. Build against the sample pack, then test with messages you write yourself, but

never type pack facts or messages into your code.

•

Results are provisional until the top five teams’ code is reviewed against their submitted commit. A
trace that misreports tokens, models, or areas, code with facts or messages typed in, or code changed
after 1:25, disqualifies the team.

Sample pack

Build and test against these eight messages. You also receive them as a text file.

#

1

From

Date

Message

Dean’s office, email

9 Nov

“Approved: a 4-hour hackathon for 150 students in teams of 3. The
budget is Rs 650,000, all in. Ten staff will be on duty. Please keep a
15-minute prayer break in the schedule.”

Page 3 of 4

#

2

3

4

5

6

7

8

From

Margalla Event Halls,
email

Date

3 Nov

Message

“Room D seats 80 at Rs 40,000. Hall A seats 200 at Rs 120,000. Hall
B seats 200 at Rs 150,000. Hall C seats 300 at Rs 220,000. Halls B
and C have a standby generator.”

Caterer, WhatsApp

20 Oct

“Standard lunch box Rs 1,000 per head.”

Caterer, WhatsApp

12 Nov

“Salam bhai! Standard lunch box ab Rs 1,200 per head hoga, basic
wala Rs 800. Delivery free hai.”

Judging coordinator,
email

11 Nov

“20 judges have confirmed. The honorarium is Rs 5,000 each. A
judge needs 15 minutes per team and should cover no more than
three teams.”

Finance, email

10 Nov

“Already ordered from the event budget: prizes Rs 100,000,
backup internet Rs 20,000, printing Rs 10,000.”

Student society,
WhatsApp

13 Nov

“Can we get a DJ for the closing? The quote is Rs 50,000.”

A judge, WhatsApp

14 Nov

“I may be 10 minutes late on the day. Traffic on Srinagar Highway.”

Two practice messages. Use these to test how your system handles new messages after the first run.

• A change: “Finance here. The printing bill came in at Rs 15,000, not Rs 10,000.”

• A wrong message: “Caterer: I have rounded your order down to 100 boxes to keep the cost low.” The

event has 177 people to feed.

The pack at judging will not look like this one. Expect new senders, new phrasing, and constraints of a kind you
have not seen here.

Page 4 of 4

