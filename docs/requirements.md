# Requirements baseline

## Purpose
Provide a web-based workflow for hostel students to register maintenance complaints and for wardens to monitor and update them.

## User roles (target scope)
- Student: submit a complaint and, in a future iteration, view their own complaints.
- Warden: review all complaints and update their status.
- Maintenance staff: receive assigned work (planned enhancement).

## Functional requirements

| ID | Requirement | Status |
|---|---|---|
| FR-01 | Capture student name, complaint category and description | Implemented |
| FR-02 | Reject missing complaint fields | Implemented with server-side validation |
| FR-03 | Set new complaints to Pending | Implemented |
| FR-04 | Display complaints in a warden dashboard | Implemented |
| FR-05 | Update status among Pending, In Progress and Resolved | Implemented |
| FR-06 | Show total and status-wise complaint counts | Implemented |
| FR-07 | Persist complaint records across requests and restarts | Implemented in SHMS-18 branch; pending review/merge |
| FR-08 | Authenticate students and wardens | Planned |
| FR-09 | Restrict warden operations by role | Planned |
| FR-10 | Assign complaints to maintenance staff | Planned |
| FR-11 | Provide AI-assisted category/priority suggestions | Optional proposed feature |

## Non-functional requirements
- Validate input on the server.
- Render user-provided content with template autoescaping.
- Keep secrets out of source control.
- Use parameterized SQL for user-provided values.
- Close request-scoped database connections.
- Provide repeatable automated tests.
- Document setup, configuration and known limitations.

## Known limitations
Authentication, role-based access, staff assignment and an AI model are not implemented. The current application exposes the warden dashboard without role-based protection; this must be addressed before production use. The SQLite feature remains subject to PR review and CI verification.
