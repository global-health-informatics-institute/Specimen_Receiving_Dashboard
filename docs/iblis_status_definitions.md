# IBLIS STATUS DEFINITIONS
- derived from the the actual test function in the
the status for a specimen is defined using 2 values from the iblis json object
    use keys "status" and "order_status"
    order_status - specimen level state, as in 'track where the sample is'
    status - for test level state of the specimen specimen


# `actual_status` Function Documentation

## Purpose
The `actual_status` function determines a human-readable status for a lab specimen or test based on two inputs:
- `specimen_status`: The status of the specimen (sample).
- `test_status`: The status of the test performed on the specimen.

The function **prioritizes test status** over specimen status:
1. If a valid `test_status` is provided, its mapped status is returned.
2. Otherwise, it falls back to the mapped `specimen_status`.
3. If neither status is recognized, `"Unknown"` is returned.

---

## Constants

### Specimen Statuses
| Specimen Status Key          | Human-Readable Value |
|------------------------------|----------------------|
| `specimen-not-collected`     | Specimen Received    |
| `specimen-accepted`          | Specimen Received    |
| `specimen-rejected`          | Rejected             |

---

### Test Statuses
| Test Status Key | Human-Readable Value   |
|-----------------|-----------------------|
| `pending`       | Specimen Received     |
| `started`       | Being Analyzed        |
| `completed`     | Pending Verification  |
| `verified`      | Analysis Complete     |
| `voided`        | Not Done              |
| `not-done`      | Not Done              |
| `rejected`      | Rejected              |

---

## Function Definition

```python
def actual_status(specimen_status, test_status):
    return TEST_STATUSES.get(test_status, SPECIMEN_STATUSES.get(specimen_status, "Unknown"))
```

---

### Parameters
| Name             | Type   | Description                                      |
|------------------|--------|--------------------------------------------------|
| `specimen_status`| `str`  | Key representing the status of the specimen.     |
| `test_status`    | `str`  | Key representing the status of the test.         |

---

### Returns
| Type  | Description                                                        |
|-------|--------------------------------------------------------------------|
| `str` | The corresponding human-readable status, or `"Unknown"` if not found.|

---

## Decision Logic
1. Check if `test_status` is in `TEST_STATUSES`:
   - If found, return the mapped value.
2. Else, check if `specimen_status` is in `SPECIMEN_STATUSES`:
   - If found, return the mapped value.
3. Else, return `"Unknown"`.

---

## Behavior Table

This table shows the result of `actual_status(specimen_status, test_status)` for all combinations of `SPECIMEN_STATUSES` and `TEST_STATUSES` values.  
(`–` means that parameter is `None` or invalid.)

| Specimen Status Key       | Test Status Key     | Result                |
|---------------------------|--------------------|----------------------|
| specimen-not-collected    | pending            | Specimen Received    |
| specimen-not-collected    | started            | Being Analyzed       |
| specimen-not-collected    | completed          | Pending Verification |
| specimen-not-collected    | verified           | Analysis Complete    |
| specimen-not-collected    | voided             | Not Done             |
| specimen-not-collected    | not-done           | Not Done             |
| specimen-not-collected    | rejected           | Rejected             |
| specimen-not-collected    | –                  | Specimen Received    |
| specimen-accepted         | pending            | Specimen Received    |
| specimen-accepted         | started            | Being Analyzed       |
| specimen-accepted         | completed          | Pending Verification |
| specimen-accepted         | verified           | Analysis Complete    |
| specimen-accepted         | voided             | Not Done             |
| specimen-accepted         | not-done           | Not Done             |
| specimen-accepted         | rejected           | Rejected             |
| specimen-accepted         | –                  | Specimen Received    |
| specimen-rejected         | pending            | Specimen Received    |
| specimen-rejected         | started            | Being Analyzed       |
| specimen-rejected         | completed          | Pending Verification |
| specimen-rejected         | verified           | Analysis Complete    |
| specimen-rejected         | voided             | Not Done             |
| specimen-rejected         | not-done           | Not Done             |
| specimen-rejected         | rejected           | Rejected             |
| specimen-rejected         | –                  | Rejected             |
| –                         | pending            | Specimen Received    |
| –                         | started            | Being Analyzed       |
| –                         | completed          | Pending Verification |
| –                         | verified           | Analysis Complete    |
| –                         | voided             | Not Done             |
| –                         | not-done           | Not Done             |
| –                         | rejected           | Rejected             |
| –                         | –                  | Unknown              |

---

## Key Takeaways
- **Test status overrides specimen status** if present.
- If there’s **no test status**, the function falls back to specimen status.
- If both are invalid or missing, the function returns `"Unknown"`.
