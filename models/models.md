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
