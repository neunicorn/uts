import sqlite3

""""membuat koneksi ke sqlite"""
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

""""membuat table sqlite"""

cursor.execute("""create table history_table(
    id INTEGER PRIMARY KEY,
    history INTEGER,
    tanggal timestamp default current_timestamp
)""")

varcoba = [(2)]

cursor.execute("insert into history_table(history) values(?)", [(5)])

cursor.execute("select * from history_table")
x= cursor.fetchall()
print(x)

conn.commit()

conn.close()
