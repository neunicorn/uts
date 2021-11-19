import sqlite3
import os
import datetime
from tabulate import tabulate

""""Membuat connection ke sqlite"""
conn = sqlite3.connect(":memory:")
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
    nama VARCHAR(40) NOT NULL,
    tempat_lahir VARCHAR(20) NOT NULL,
    tanggal_lahir timestamp NOT NULL,
    jenis_kelamin TEXT CHECK( jenis_kelamin IN ('L','P')) NOT NULL,
    alamat VARCHAR(50) NOT NULL,
    agama TEXT CHECK(agama IN ("Islam", "Protestan", "Katolik", "Hindu", "Budha", "Konghucu")) NOT NULL,
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

cur.execute("INSERT INTO income(income_modal) VALUES(400000000)")

cur.executemany("INSERT INTO products(jenis_motor, quantity, price) VALUES(?,?,?)", products_motor)

def insert_customer(data_customer):

    cur.execute("""INSERT INTO customers(NIK, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat, agama, status_nikah, pekerjaan, kewarganegaraan) 
        VALUES(?,?,?,?,?,?,?,?,?,?)""", data_customer)
    conn.commit()

def get_customer():
    with conn:
        cur.execute("SELECT NIK FROM customers")
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
        quit()
    else:
        print("inputan salah!")
        os.system("cls")
        main()

def check_akun():
    
    cek_akun = get_customer()
    input_NIK = ""
    try:
        input_NIK = input("Masukkan NIK: ")
        if input_NIK in cek_akun:
            return input_NIK
        else:
            print("Data tidak ditemukan!\nSilakan memasukkan data diri terlebih dahulu\n\n")                
    except:
        print(sqlite3.Error)
    

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
        back = input("input 1 to back to menu: ")
        if back == "1":
            break
            
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