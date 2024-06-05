**config.py**:
--Stand alone to app.py
--Contains app configurations and should be redefined manually

**dbsetup**:
--first to be run... defines the schema for the sqlite and SQL
--every data functions is defined in a nameCorresponding model file

**view.py**:
--creates a Join view for all values we need

**Intermediate**:
--only executed on first run + new values(Implemented for testing)