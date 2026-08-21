import sqlite3 as sqlite

def initialiseVelocityFunctionTable():
    """Creates table in fluids database to store velocity functions and sets up prebuilt functions"""
    with sqlite.Connection("fluids.db") as conn:
        conn.cursor().executescript("""CREATE TABLE IF NOT EXISTS velocity_function (
                    written TEXT UNIQUE,
                    exponential INTEGER,
                    magnitude TEXT,
                    argument TEXT);

                    INSERT or IGNORE INTO velocity_function VALUES ("tunnel", 1, "1", "i*pi");
                    INSERT or IGNORE INTO velocity_function VALUES ("vortex", 1, "1", "i*pi*-0.25");
                    INSERT or IGNORE INTO velocity_function VALUES ("falling", 1, "1", "i*pi*0.5");
                    """)
        conn.commit()


def searchVelocityFunction(function : str, include_name : bool = False):
    """Searches the velocity function table with written attribute as criteria"""
    with sqlite.Connection("fluids.db") as conn:
        function_data = conn.cursor().execute("""SELECT * FROM velocity_function WHERE written = (?) """, (function,)).fetchone()
        conn.commit()
    if not function_data:
        return False
    if not include_name:
        return function_data[1:]
    return function_data


def saveVelocityFunction(function : str):
    """Adds a new velocity function to the table"""
    if "e" in function: 
        magnitude = function[:function.index("e")]
        if "*" in function or "/" in function:
            try: 
                argument = function[function.index("i"):function.index(")")]
            except ValueError:
                argument = function[function.index("i"):]
        else:
            argument = 0
        
        with sqlite.Connection("fluids.db") as conn:
            conn.cursor().execute("""INSERT or IGNORE INTO velocity_function VALUES (?,?,?,?)""",
            (function, 1, magnitude, argument))



def initialiseBodyTable():
    """Creates table in fluids database to store body properties and sets up preset bodies"""
    with sqlite.Connection("fluids.db") as conn:
        conn.cursor().executescript("""CREATE TABLE IF NOT EXISTS body
        (num INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        path TEXT,
        fixed INTEGER,
        mass REAL,
        display_scale_factor REAL);
        
        INSERT or IGNORE INTO body VALUES (1, "circle", "images\\body\\circle.png", 0, 10.0, 0.9);
        INSERT or IGNORE INTO body VALUES (2, "square", "images\\body\\square.png", 0, 10.0, 0.9);
        INSERT or IGNORE INTO body VALUES (3, "airfoil", "images\\body\\airfoil.png", 1, 0.0, 1.1);
        INSERT or IGNORE INTO body VALUES (4, "f1 car", "images\\body\\car.png", 1, 0.0, 1.1);
        INSERT or IGNORE INTO body VALUES (5, "regan", "images\\body\\regan.png", 0, 100.0, 0.85);
        INSERT or IGNORE INTO body VALUES (6, "rod", "images\\body\\rod.png", 0, 10.0, 0.9)""")
        conn.commit()

def getBodyProperties(index : int):
    """Returns the properties of an object of a given index"""
    with sqlite.Connection("fluids.db") as conn:
        return conn.cursor().execute("""SELECT * FROM body WHERE num = ?""", (index,)).fetchone()[1:]
