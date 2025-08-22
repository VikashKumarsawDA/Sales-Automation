import sqlite3

def generate():
    conobj = sqlite3.connect(database='sales.sqlite')
    curobj=conobj.cursor()
    query='''create table if not exists users(
        UserID integer primary key autoincrement,
        UserName text,
        UserEmail text,
        UserMob text,
        UserAddress text,
        UserPassword text,
        UserPurchase float,
        UserOpenDate text
        )
        '''
    curobj.execute(query)
    # Set AUTOINCREMENT starting value to 10000 so next UserID will be 10001
    curobj.execute('INSERT OR IGNORE INTO sqlite_sequence(name, seq) VALUES("users", 10000)')
    conobj.close()