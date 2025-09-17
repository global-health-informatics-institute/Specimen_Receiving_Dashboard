LIMS_TEST_STATUS_REFERENCE = {
  # from the iblis json, root key 'status'
  "pending": "Specimen Received",
  "started": "Being Analyzed",
  "completed": "Pending Verification",
  "verified": "Analysis Complete",
  "voided": "Not Done",
  "not-done": "Not Done",
  "rejected": "Rejected"
}

LIMS_SPECIMEN_STATUS_REFERENCE = {
  # from the lims json, root key 'order_status'
  "specimen-not-collected" :"Specimen Received",
  "specimen-accepted" : "Specimen Received",
  "specimen-rejected" : "Rejected"
}

OERR_DASHBOARD_TEST_STATUSES = {
  "pending": 1,
  "started": 3,
  "completed": 4,
  "verified": 5,
  "missing": 9,
  "voided": 0,
  "not-done": 0,
  "rejected": 0
}

OERR_DASHBOARD_SPECIMEN_STATUSES = {
  "specimen-not-collected" : 1,
  "specimen-accepted" : 1,
  # "specimen-accepted - 1" -> "specimen-accepted - 2": 
  # this was initially 2, but was changed to 1 because it does not fulfil 'received in the lab' rather 'registered on the reception'
  "specimen-rejected" : 0
}

OERR_DASHBOARD_STATUSES_REFERENCE= {
    "received": 2,
    "registered": 1,
    "in_progress": 3,
    "pending_auth": 4,
    "completed": 5,
    "rejected": 0
}


WEEKLY_LABEL_REFERENCE = {
    "weekly_count_registered" : 1,
    "weekly_count_received" : 2,
    "weekly_count_progress" : 3,
    "weekly_count_pending": 4,
    "weekly_count_complete": 5,
    "weekly_count_rejected": 0,
}


MONTHLY_LABEL_REFERENCE = {
    "monthly_count_registered" : 1,
    "monthly_count_received" : 2,
    "monthly_count_progress" : 3,
    "monthly_count_pending": 4,
    "monthly_count_complete": 5,
    "monthly_count_rejected": 0,
}

DEPARTMENT_REFERENCE = {
    1: ["OPD2","MSS","4A","4B","MHDU","DIALYSIS UNIT"],
    2: ["UNDER 5","CWA","CWB","CWC","CW HDU"],
    3: ["CASUALTY","1A","1B","2B","3A","3B","SHDU","THEATRE"],
    4: ["LABOUR","POSTNATAL WARD","ANTENATAL WARD","EM OPD","EMHDU","EM NURSERY","GYNAE"],
    5: ["ICU","OPD1","EYE","DENTAL"]
  }


def map_lims_to_oerr_dashboard_status(lims_test_status, lims_specimen_status):
    # map the test status first
    if lims_test_status in OERR_DASHBOARD_TEST_STATUSES:
        return OERR_DASHBOARD_TEST_STATUSES[lims_test_status]

    if lims_specimen_status in OERR_DASHBOARD_SPECIMEN_STATUSES:
        return OERR_DASHBOARD_SPECIMEN_STATUSES[lims_specimen_status]
    
    # return missing
    return 9
   