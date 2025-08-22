import sqlite3

def create_chat_table():
    """
    Creates the admin_chat table if it does not exist.
    Columns:
        id        : Auto-increment primary key
        timestamp : Text, stores message timestamp
        sender    : Text, 'Admin' or 'System'
        message   : Text, the message content
    """
    con = sqlite3.connect('sales.sqlite')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS admin_chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            sender TEXT,
            message TEXT
        )
    ''')
    con.commit()
    con.close()

# Optional: run immediately if this file is executed directly
if __name__ == "__main__":
    create_chat_table()
    print("admin_chat table created (if it did not exist).")
