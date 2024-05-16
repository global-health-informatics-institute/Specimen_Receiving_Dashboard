DROP TABLE IF EXISTS specimens;

CREATE TABLE specimens (
	specimen_id INTEGER PRIMARY KEY AUTOINCREMENT,
	accession_number TEXT NOT NULL,
	status TEXT NOT NULL,
	type TEXT NOT NULL,
	department TEXT NOT NULL,
	time_registered TIMESTAMP NOT NULL,
	time_received TIMESTAMP
);
