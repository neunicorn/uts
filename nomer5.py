import re
import sqlite3
import os
from tabulate import tabulate

conn = sqlite3.connect("nomer5.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE if not exists history(
    id INTEGER PRIMARY KEY,
    kata TEXT not null,
    history_nilai INTEGER NOT NULL,
    tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)""")

conn.commit()

solve = lambda s : max([sum([ord(letter)-ord('a')+1 for letter in consOnly]) for consOnly in re.split("a|e|i|o|u",s)])

def insert_values(x):
    cur.execute("INSERT INTO history(kata, history_nilai) VALUES(?,?)", x)
    conn.commit()

def input_values():
    print("===== Menghitung consonant values =====")
    variable = input("masukkan kata: ")
    print("panjang consonant pada kata " + variable + " adalah: " + str(solve(variable)))
    history_input = int(solve(variable))
    insert_data = (variable, history_input)
    insert_values(insert_data)

def history5():
    with conn:
        cur.execute("SELECT * FROM history")
        history55 = cur.fetchall()

    print(tabulate(history55, headers=["No", "Kata", "Max Value",  "Date"]))

def  main5():
    print("===== Menghitung consonant values =====")
    print("1. input data")
    print("2. history")
    choise = input("pilih: ")

    if choise == "1":
        os.system("cls")
        input_values()
    elif choise == "2":
        history5()


main5()

conn.close()

# print(solve("zodiacs")) # output : 26
# print(solve("chruschtschov")) # output : 80
# print(solve("rhythm")) # output : 92