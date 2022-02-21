import sqlite3

# Connect to SQLite DB
conn = sqlite3.connect("test.db")

with conn:
    # Create Cursor from connection object
    cur = conn.cursor()
     
    # Put SQL Query
    cur.execute("CREATE TABLE \
                 customer(id integer primary key autoincrement, \
                          name text not null, category integer, \
                          region text);")

    cur.execute("INSERT INTO customer(name, category, region)\
                 VALUES ('cbchoi', 1, 'Daejeon');")
    
    cur.execute("SELECT name FROM customer WHERE category = 1;")

    for row in cur.fetchall():
       print(row)
    
    # Reflect to Database
    conn.commit()