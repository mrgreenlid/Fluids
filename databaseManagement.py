import sqlite3 as sqlite

def initialiseFlowTable():
    with sqlite.Connection("fluid.db") as conn:
        conn.cursor().executescript("""CREATE TABLE IF NOT EXISTS flow 
        (
        flowName TEXT UNIQUE,
        velocity_function TEXT,
        displacement_scalar INTEGER
        );
        
        INSERT OR IGNORE INTO flow VALUES ("point_source", "(z)/(|z|**2)", 10000);
        INSERT OR IGNORE INTO flow VALUES ("vortex", "(i*z)/(|z|**2)", 10000);
        INSERT OR IGNORE INTO flow VALUES ("doublet", "(z**2)/(|z|**4)", 10000000);""")
        conn.commit()

def getFlowAttributes(flow_name : str):
    with sqlite.Connection("fluid.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * from flow WHERE flowName = ?""", (flow_name,))
        attributes = cursor.fetchone()
        conn.commit()
    return attributes