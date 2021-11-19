import sqlite3
import os
import datetime
import re
from tabulate import tabulate

def mainProgram():
    print("===== UTS SDA STUDI KASUS =====\n")
    print("1. Case1")
    print("2. Case3")
    print("3. Case5")
    print("0. Quit")

    pilih_main_program = input("pilih case: ")

    if pilih_main_program == "1":
        os.system("cls")
        case1()
    elif pilih_main_program == "2":
        os.system("cls")
        case3()
    elif pilih_main_program == "3":
        os.system("cls")
        case5()
    elif pilih_main_program == 0:
        quit()

def case1():
    """"Membuat connection ke sqlite"""
    conn = sqlite3.connect("databases.db")
    cur = conn.cursor()

    products_motor = [("Revo F1 110", 30, 12500000),
                    ("New Supra X 125 F1", 30, 18500000),
                    ("New Beat F1", 20, 12000000),
                    ("Vega ZR", 10, 13500000),
                    ("Jupiter Z", 20, 14000000),
                    ("Jupiter MX", 15, 17000000),
                    ("Satria FU 150", 10, 19500000),
                    ("Shogun R 125", 5, 14000000)
    ]

    """"membuat table """
    cur.execute("""create table if not exists products(
        id INTEGER PRIMARY KEY,
        jenis_motor TEXT,
        quantity INTEGER,
        price INTEGER
    )""")

    cur.execute("""create table IF NOT EXISTS customers(
        NIK TEXT PRIMARY KEY,
        nama VARCHAR(50) NOT NULL,
        tempat_lahir VARCHAR(20) NOT NULL,
        tanggal_lahir timestamp NOT NULL,
        jenis_kelamin TEXT CHECK( jenis_kelamin IN ('L','P')) NOT NULL,
        alamat VARCHAR(50) NOT NULL,
        agama TEXT NOT NULL,
        status_nikah TEXT CHECK (status_nikah IN ("sudah", "belum")) NOT NULL,
        pekerjaan VARCHAR(30) NOT NULL,
        kewarganegaraan TEXT CHECK (kewarganegaraan IN ("WNI", "WNA")) NOT NULL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS income(
        id INTEGER PRIMARY KEY,
        income_modal INTEGER NOT NULL DEFAULT 400000000,
        tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY,
        NIK_customer TEXT NOT NULL,
        id_products INTEGER NOT NULL,
        quantities INTEGER NOT NULL,
        total INTEGER NOT NULL,
        tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (NIK_customer) REFERENCES customers(NIK),
        FOREIGN KEY (id_products) REFERENCES products(id)
    )""")

    conn.commit()

    pemasukan = cur.execute("SELECT * FROM income").fetchall()
    if pemasukan == []:
        cur.execute("INSERT INTO income(income_modal) VALUES(400000000)")
        conn.commit()
    else:
        pass

    product = cur.execute("SELECT * FROM products").fetchall()
    if product == []:
        cur.executemany("INSERT INTO products(jenis_motor, quantity, price) VALUES(?,?,?)", products_motor)
        conn.commit()
    else:
        pass

    def insert_customer(data_customer):

        cur.execute("""INSERT INTO customers(NIK, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat, agama, status_nikah, pekerjaan, kewarganegaraan) 
            VALUES(?,?,?,?,?,?,?,?,?,?)""", data_customer)
        conn.commit()

    def get_customer():
        with conn:
            cur.execute("SELECT * FROM customers")
        return cur.fetchall()

    def get_products():
        with conn:
            cur.execute("select * from products")
        return cur.fetchall()

    def update_products(quantity, id):
        with conn:
            cur.execute(f"""UPDATE products set quantity = quantity - {quantity} where id = {id}""")

    def insert_orders(order):
        with conn:
            cur.execute("INSERT INTO orders(NIK_customer, id_products, quantities, total) VALUES(?,?, ?, ?)", order)

    def get_order():
        with conn:
            cur.execute("SELECT * FROM orders")
        return cur.fetchall()

    def update_income(x):
        with conn:
            cur.execute(f"UPDATE income set income_modal = income_modal + {x} where id = 1")

    def get_income():
        with conn:
            cur.execute("SELECT income_modal FROM income")
        return cur.fetchall()

    def main():

        print("\t========== PT. XYZ Otomotif ==========\n")
        print("\t1. Beli")
        print("\t2. Riwayat penjualan")
        print("\t3. Pemasukkan")
        print("\t0. Quit")
        pilih = input("pilih: ")

        if pilih == "1":
            os.system("cls")
            payment()
        elif pilih == "2":
            os.system("cls")
            history()
        elif pilih == "3":
            os.system("cls")
            income()
        elif pilih == "0":
            conn.close()
            os.system("cls")
            mainProgram()
        else:
            print("inputan salah!")
            os.system("cls")
            main()

    def check_akun():
        
        cek_akun = get_customer()
        input_NIK = input("Masukkan NIK: ")
        if cur.execute(f"SELECT NIK from customers where NIK = {input_NIK}").fetchone() :
            return input_NIK
        else:
            print("Data tidak ditemukan!\nSilakan memasukkan data diri terlebih dahulu\n\n")                


    def login():
        print()
        print("\t========== PT. XYZ Otomotif ==========\n")
        print("Apakah pembeli merupakan customer baru?(y/n)")
        customer_baru = input("y untuk ya dan n untuk tidak: ")
        if customer_baru == "y":
            os.system("cls")
            nik_baru = buat_akun()
            return nik_baru
        elif customer_baru == "n":
            check = check_akun()
            print(check)
            print()
            if check == None:
                nik_baru = buat_akun()
                return nik_baru
            else:
                return check
        else:
            os.system("cls")
            login()
            

    def buat_akun():
        print()
        while(True):
        
            print("\t========== PT. XYZ Otomotif ==========\n")
            print("\tmemasukkan identitas diri")
            NIK = input("NIK: ")
            nama = input("nama: ")
            tempat_lahir = input("tempat lahir: ")
            tanggal_lahir = input ("tanggal lahir(YYYY-MM-DD): ")
            jenis_kelamin = input("Jenis Kelamin(L/P): ")
            alamat = input("alamat: ")
            agama = input("Agama: ")
            status_nikah = input("status nikah(sudah/belum): ")
            pekerjaan = input("pekerjaan: ")
            kewarganegaraan = input("Kewarganegaraan(WNI/WNA): ")

            data_customer = (NIK, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat, agama, status_nikah, pekerjaan, kewarganegaraan)

            print()

            print("NIK\t\t: "  + NIK+
                "\nNama\t\t:"+ nama+
                "\nTTL\t\t: " + tempat_lahir +", " + tanggal_lahir+
                "\nJK\t\t: " + jenis_kelamin+
                "\nAlamat\t\t: "+alamat+
                "\nAgama\t\t: "+agama+
                "\nStatus Nikah\t: "+status_nikah+
                "\npekerjaan\t: "+pekerjaan+
                "\nwarganegara\t: " +kewarganegaraan
            )
            cek = input("apakah data anda sudah benar(y/n)?")
            if cek == "y":
                try:
                    insert_customer(data_customer)
                    break
                except:
                    os.system("cls")
                    print("data yang anda input salah!")
                    print("Silahkan input ulang!")
                    print()
            elif cek == "n":
                os.system("cls")
            else:
                os.system("cls")

        return NIK

    def payment():
        NIK = login()
        print("NIK: "  + NIK)
        total = 0
        print("\t========== PT. XYZ Otomotif ==========\n")
        product = get_products()
        print(tabulate(product, headers=["No", "Jenis Motor", "Quantity", "Price"]))
        print()
        print()
        while(True):

            while(True):
                pilih_product = int(input("pilih(id): "))
                if pilih_product in range(1, 9):
                    break
                else:
                    print("Pilihan anda tidak tersedia!")

            cur.execute(f"Select jenis_motor, price from products where id= {pilih_product}")
            buffer_product = cur.fetchall()
            conn.commit()

            motor = buffer_product[0][0]
            harga = buffer_product[0][1]


            print("Jenis Motor: " + str(motor) + "\tharga: " + str(harga)) 
            kuantitas = int(input("Berapa banyak motor yang akan dibeli: "))
            harga *= kuantitas
            print("Jenis Motor: " + str(motor) + "\nKuantitas: " + str(kuantitas) + "\tharga: " + str(harga))
            total += harga

            order = (NIK, pilih_product, kuantitas, harga)

            update_products(kuantitas, pilih_product)
            insert_orders(order)
            
            beli_lagi = ""
            print()
            beli_lagi = input("apakah anda ingin membeli motor lain?(y/n): ")

            if beli_lagi == "y":
                pass
            elif beli_lagi == "n":
                break
        
        print("Total: " + str(total))
        update_income(total)

        while(True):
            bayar = int(input("input uang jumlah bayar: "))
            if bayar < total:
                print("Uang anda tidak cukup!")
            elif bayar >= total:
                break
        
        kembalian = bayar - total
        print(f"Kembalian: {kembalian}")

        flow_program = input("Apakah anda ingin membeli lagi?(y/n)")
        if flow_program == "y":
            payment()
        elif flow_program == "n":
            main()

    
    def history():
        with conn:
            cur.execute("""SELECT orders.id, customers.nama, orders.tanggal, products.jenis_motor, orders.quantities, orders.total from orders
            JOIN customers ON customers.NIK = orders.NIK_customer
            JOIN products ON products.id = orders.id_products""")
            history_order = cur.fetchall()

        print(tabulate(history_order, headers=["No", "Pembeli", "Tanggal", "Jenis Motor", "Kuantitas", "Harga"]))

        print("\n\n\n")
        while(True):
            back = input("input 1 to back to menu or 2 to pop data:  ")
            if back == "1":
                break

            elif back == "2":
                cur.execute("delete from orders where id = (SELECT MAX(id) FROM orders)")
                print("Data terakhir berhasil di hapus(pop)")
                enter = input("press enter to continue...")
                os.system("cls")
                history()

            else:
                pass
        os.system("cls")
        main()

    def income():
        print("Pendapatan PT. XYZ Otomotif\n\n")
        pendapatan = get_income()
        for i in pendapatan:
            print("Pendapatan: " + str(i[0]))

        print("press 1 to continue to menu: ")
        while(True):
            i = input()
            if i == "1":
                break
                
            else:
                pass
        os.system("cls")
        main()


    main()
    conn.close()

def case3():
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
        if(inputMenu == "1"):
            os.system("cls")
            input_data()
        elif inputMenu == "2":
            os.system("cls")
            print("\t====== HISTORY =======\n")
            history()
        elif inputMenu == "0":
            os.system("cls")
            mainProgram()
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
        print()
        print()
        print("1. Back to menu\n2. Pop data:")
        backMenu = input("input: ")
        if backMenu == "1":
            os.system("cls")
            main()
        elif backMenu == "2":
            cursor.execute("DELETE FROM numberone WHERE id = (SELECT MAX(id) FROM numberone)")
            conn.commit()
            print("Data berhasil di pop")
            back = input("press enter to back to history..")
            os.system("cls")
            history()
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

def case5():
        
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

        print("enter to back to main menu...")
        back_to_main_menu = input()
        main5()

    def history5():
        with conn:
            cur.execute("SELECT * FROM history")
            history55 = cur.fetchall()

        print(tabulate(history55, headers=["No", "Kata", "Max Value",  "Date"]))
        print("1. Back to menu\n2. Pop data")
        back_main_menu = input("input: ")
        if back_main_menu == "1":
            os.system("cls")
            main5()
        elif back_main_menu == "2":
            cur.execute("DELETE FROM history WHERE id = (SELECT MAX(id) FROM history)")
            conn.commit()

            print("data berhasil di pop")
            backk = input("press enter to back to history...")
            os.system("cls")
            history5()

    def  main5():
        print("===== Menghitung consonant values =====")
        print("1. input data")
        print("2. history")
        print("0. Quit")
        choise = input("pilih: ")

        if choise == "1":
            os.system("cls")
            input_values()
        elif choise == "2":
            history5()
        elif choise == "0":
            os.system("cls")
            mainProgram()


    main5()

    conn.close()

mainProgram()