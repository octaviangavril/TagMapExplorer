import sqlite3


def setup_test_db():
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS users')

    cur.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
    ''')

    cur.executemany('INSERT INTO users (name, age) VALUES (?, ?)', [
                    ('john_doe', 3),
                    ('jane_doe', 5),
                    ('joe_doe', 7)
                    ])

    conn.commit()
    conn.close()
    print("Test database setup completed.")


if __name__ == "__main__":
    setup_test_db()