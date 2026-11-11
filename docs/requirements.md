# Requirements baseline

## Purpose
Provide a web-based workflow for hostel students to register maintenance complaints and for wardens to monitor and update them.

## User roles (target scope)
- Student: submit a complaint and, in a future iteration, view their own complaints.
- Warden: review all complaints and update their status.
- Maintenance staff: receive assigned work (planned enhancement).

## Functional requirements

| ID | Requirement | Baseline |
|---|---|---|
| FR-01 | Capture student name, complaint category and description | Implemented in prototype |
| FR-02 | Reject missing complaint fields | Basic server-side validation implemented |
| FR-03 | Set new complaints to Pending | Implemented in prototype |
| FR-04 | Display complaints in a warden dashboard | Implemented in prototype |
| FR-05 | Update status among Pending, In Progress and Resolved | Implemented in prototype |
| FR-06 | Show total and status-wise complaint counts | Implemented in prototype |
| FR-07 | Persist complaint records across restarts | Planned: SQLite |
| FR-08 | Authenticate students and wardens | Planned |
| FR-09 | Restrict warden operations by role | Planned |
| FR-10 | Assign complaints to maintenance staff | Planned |
| FR-11 | Provide AI-assisted category/priority suggestions | Optional proposed feature |

## Non-functional requirements
- Validate input on the server.
- Render user-provided content with template autoescaping.
- Keep secrets out of source control.
- Provide repeatable automated tests.
- Document known limitations and setup steps.

## Current limitations
The initial prototype uses a Python list for complaint storage. Data is lost when the server process stops. The prototype does not currently implement login, role-based access, staff assignment, a database, or an AI model. Those items are tracked as future work rather than completed capabilities.
