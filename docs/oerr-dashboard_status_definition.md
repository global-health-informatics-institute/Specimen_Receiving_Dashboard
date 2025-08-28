# OERR DASHBOARD
- briefly defines a mapping of the actual_status(order_status,test_status) and the key value in the tab
- actual status utilizes: map_lims_to_oerr_dashboard_status(lims_test_status, lims_specimen_status)

  | actual status             | definition         | specimen value       |
  |---------------------------|--------------------|----------------------|
  | Specimen Received         | registered         | 1                    |
  | Being Analyzed            | in progress        | 3                    |
  | Pending Verification      | pending auth       | 4                    |
  | Analysis Complete         | completed          | 5                    |
  | Not Done                  | rejected           | 0                    |
  | Rejected                  | rejected           | 0                    |


- defining a mapping of a success request from the endpoint 'scan_sample' 
  | scan_sample               | definition         | specimen value       |
  |---------------------------|--------------------|----------------------|
  | Sample Scanned            | received           | 2                    |
