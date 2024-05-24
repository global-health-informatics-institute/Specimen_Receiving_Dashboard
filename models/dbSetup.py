import sqlite3
def dbSetup():
    # DB connection
    conn = sqlite3.connect('models/intermediateDB.db')


    # cursor Object
    cursor = conn.cursor()

    # Table Definition
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tests (
        testID INTEGER PRIMARY KEY AUTOINCREMENT,
        assertionNumber INTEGER NOT NULL,
        testType TEXT NOT NULL,
        testStatus TEXT NOT NULL,
        writeTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weeklySummary (
        weeklySummaryID INTEGER PRIMARY KEY AUTOINCREMENT,
        totalRegistered INTEGER NOT NULL,
        totalReceived INTEGER NOT NULL,
        totalInprogress INTEGER NOT NULL,
        totalPendingAuth INTEGER NOT NULL,
        totalCompleted INTEGER NOT NULL,
        writeTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS monthlySummary (
        monthlySummaryID INTEGER PRIMARY KEY AUTOINCREMENT,
        totalRegistered INTEGER NOT NULL,
        totalReceived INTEGER NOT NULL,
        totalInprogress INTEGER NOT NULL,
        totalPendingAuth INTEGER NOT NULL,
        totalCompleted INTEGER NOT NULL,
        writeTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()

    conn.close()
