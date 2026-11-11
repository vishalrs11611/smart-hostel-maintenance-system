# Test cases

| ID | Scenario | Expected result |
|---|---|---|
| TC-01 | Open dashboard with no complaints | Dashboard renders and shows empty state |
| TC-02 | Submit complete valid complaint | Complaint is stored with Pending status |
| TC-03 | Omit student name | Request is rejected |
| TC-04 | Omit category | Request is rejected |
| TC-05 | Omit description | Request is rejected |
| TC-06 | Submit whitespace-only student name | Request is rejected |
| TC-07 | Submit a category outside the allow-list | Request is rejected |
| TC-08 | Update a complaint to In Progress | Database status is updated |
| TC-09 | Submit an unsupported status | Request is rejected and status remains unchanged |
| TC-10 | Update a non-existent complaint ID | 404 is returned |
| TC-11 | Register a complaint and make a separate request | Complaint remains visible |
| TC-12 | Register multiple complaints and update one by ID | Only the selected database record changes |
| TC-13 | Dashboard status counts after updates | Counts match the database records |

## Execution

Run the automated suite from the repository root:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

The test fixture configures a separate temporary SQLite database. Record the actual CI result and date after the workflow completes.
