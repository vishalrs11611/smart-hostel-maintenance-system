# Test cases

| ID | Scenario | Expected result |
|---|---|---|
| TC-01 | Open dashboard with no complaints | Dashboard renders and shows empty state |
| TC-02 | Submit complete valid complaint | Complaint is added with Pending status |
| TC-03 | Omit student name | Request is rejected |
| TC-04 | Omit category | Request is rejected |
| TC-05 | Omit description | Request is rejected |
| TC-06 | Submit whitespace-only student name | Request is rejected |
| TC-07 | Submit a category outside the allow-list | Request is rejected |
| TC-08 | Update a complaint to In Progress | Status is updated |
| TC-09 | Submit an unsupported status | Request is rejected and status remains unchanged |
| TC-10 | Update a non-existent complaint index | 404 is returned |

## Execution

Run the automated suite from the repository root:

```bash
python -m pip install -r requirements.txt
pytest -q
```

Record the actual result, environment, and date after executing the tests. Do not mark a test as passed solely because it is listed here.
