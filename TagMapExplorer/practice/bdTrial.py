import sqlite3

conn = sqlite3.connect('example.db')

c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    age INTEGER NOT NULL
)
''')

conn.commit()
conn.close()

conn = sqlite3.connect('example.db')

c = conn.cursor()

c.execute('''
INSERT INTO users (username, password, age) VALUES ('john_doe', 'password123', 3)''')

conn.commit()

c.execute('''SELECT AVG(age) FROM users''')

average_age = c.fetchall()[0][0]

print(average_age)

conn.close()