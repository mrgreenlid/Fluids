import sqlite3 as sqlite

def initialiseFlowTable():
    with sqlite.Connection("fluid.db") as conn:
        conn.cursor().executescript("""CREATE TABLE IF NOT EXISTS flow 
        (
        flowID INTEGER PRIMARY KEY,
        flowName TEXT UNIQUE,
        velocityFunction TEXT,
        clockScalar INTEGER
        );
        
        INSERT OR IGNORE INTO flow VALUES (1, "point_source", "(z)/(|z|**2)",10000);
        INSERT OR IGNORE INTO flow VALUES (2, "vortex", "(i*z)/(|z|**2)", 10000);
        INSERT OR IGNORE INTO flow VALUES (3, "doublet", "-1*(z**2)/(|z|**4)", 1000000); """)
        conn.commit()

def getFlowAttributes(flow_name : str):
    with sqlite.Connection("fluid.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * from flow WHERE flowName = ?""", (flow_name,))
        attributes = cursor.fetchone()[2:]
        conn.commit()
    return attributes