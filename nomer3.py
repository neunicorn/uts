import os
import datetime 
import sqlite3  
import tabulate
from tabulate import tabulate 

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

""""Block Code untuk membuat table dengan sqlite3"""
cursor.execute("""CREATE TABLE IF NOT EXISTS numberone (
   id INTEGER PRIMARY KEY,
   history INTEGER,
   tanggal timestamp default current_timestamp
)""")

def main():
    print("Menghitung nilai operasi dari a, b, c. Kemudian ditentukan nilai terbesar.")
    print("1. input data")
    print("2. history")
    print("0. quit")
    inputMenu = input("input: ")
    if(inputMenu is "1"):
        os.system("cls")
        input_data()
    elif inputMenu is "2":
        os.system("cls")
        print("\t====== HISTORY =======\n")
        history()
    elif inputMenu is "0":
        quit()
    else:
        os.system("cls")
        main()

def insert_value(x):
    
    cursor.execute("INSERT INTO numberone(history) VALUES(?)", [(x)])
    conn.commit()

def get_data():
    with conn:
        cursor.execute("select * from numberone")
    return cursor.fetchall()

def history():
    data_history = get_data()
    # print("id\tMax Value\t Date")
    print(tabulate(data_history, headers=["id", "Max Value", "Date"]))
    # for i in data_history:
    #     print(str(i[0]) + "\t"  + str(i[1]) + "\t   " + str(i[2]))
    
def maxValue(a, b, c):
    p = a + b + c 
    q = a + b * c 
    r = (a + b) * c    
    s = a * b + c 
    t = a * (b + c) 
    u = a * b * c
    listValue= [p,q, r, s, t, u]
    print("Nilai hasil operasi= "+str(listValue))
    print("Hasil perhitungan", end=": ")
    x=sorting(listValue)
    print("niliai max= ", x[len(x)-1])
    # print(max(listValue)) #bisa juga menggunkaan fungsi max

    return x

def sorting(li):
    for i in range(1, len(li)):
 
        key = li[i]
        j = i-1
        while j >=0 and key < li[j] :
                li[j+1] = li[j]
                j -= 1
        li[j+1] = key
    return li

def input_data():
    print("Menghitung nilai operasi dari a, b, c. Kemudian ditentukan nilai terbesar.")
    while(True):
        a = int(input("Masukkan nilai a = "))
        if a in range(1, 11):
            break
    while(True):
        b = int(input("Masukkan nilai b = "))
        if b in range(1, 11):
            break
    while(True):    
        c = int(input("Masukkan nilai c = "))
        if c in range(1, 11):
            break

    nilaiBalik=maxValue(a, b, c)
    insert_value(max(nilaiBalik))

    while(True):
        print("ingin menghitung lagi?(y/n)")
        lagi = input("y untuk ya, n untuk tidak: ")
        if lagi is "y" :
            os.system("cls")
            input_data()
        elif lagi is "n":
            os.system("cls")
            main()
        else:
            print("inputan salah\n\n")

main()

conn.close()