import sqlite3 as sqlite


def initialiseFlowTable():
    with sqlite.Connection("fluid.db") as conn:
        conn.executescript("""CREATE TABLE IF NOT EXISTS flow 
        (
        flowID INTEGER PRIMARY KEY,
        flowName TEXT,
        velocityFunction TEXT,
        startX INTEGER,
        startY INTEGER
        );
        
        INSERT OR IGNORE INTO flow VALUES (1, "point_source", "(z)/(|z|**2)", 775, 450);
        INSERT OR IGNORE INTO flow VALUES (2, "vortex", "(i*z)/(|z|**2)", -1, -1);
        INSERT OR IGNORE INTO flow VALUES (3, "doublet", "-1*(z**2)/(|z|**4)", -1, 450); """)
        conn.commit()
