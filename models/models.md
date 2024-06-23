**config.py**:
- Stand alone to app.py
- Contains app configurations and should be redefined manually

**dbsetup**:
- first to be run... defines the schema for the sqlite and SQL
- every data functions is defined in a nameCorresponding model file


# UpdateEntries
- **iblis_connection**: from line 15-20, need external configurations
- **srs_connection**: from line 25 - 29, need further configarations
- will be called using `curl` 


# INSTRUCTIONS
- config the database end points in `models/config`
- config test type as short names for that screen`models/config`
- load the file (alone) `models/setUp`
- set up two cron jobs that log into `logs/clearTables.log`
    - one that clears weeklySummary and another monthlySummary