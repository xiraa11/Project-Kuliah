from typing import List
from datetime import datetime
from colorama import Fore
import pandas as pd
import os

users = []
kategoris = [
    {"id": 1, "nama_kategori": "Elektronik"},
    {"id": 2, "nama_kategori": "Pakaian"},
    {"id": 3, "nama_kategori": "Makanan"},
    {"id": 4, "nama_kategori": "Peralatan Rumah Tangga"},
]
barangs = []
pesanans = []
keranjangs = []
# cihuyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
curr_user = None

class User:
    idm = 1
    def __init__(self, nama, password, alamat=None, role="pembeli"):
        self.id = User.idm
        User.idm += 1
        self.nama = nama
        self.password = password
        self.alamat = alamat
        self.role = role

class Barang:
    idm = 1
    def __init__(self, nama, deskripsi, harga, quantity, kategori_id, nama_kategori, penjual_id):
        self.id = Barang.idm
        Barang.idm += 1
        self.nama = nama
        self.deskripsi = deskripsi
        self.harga = harga
        self.quantity = quantity
        self.kategori_id = kategori_id
        self.nama_kategori = nama_kategori 
        self.penjual_id = penjual_id

class Orders:
    idm = 1
    def __init__(self, user_id, total_harga, status, tanggal):
        self.id = Orders.idm
        Orders.idm += 1
        self.user_id = user_id
        self.total_harga = total_harga
        self.status = status
        self.tanggal = tanggal

class Keranjang:
    idm = 1
    def __init__(self, user_id, barang_id, quantity):
        self.id = Keranjang.idm
        Keranjang.idm += 1
        self.user_id = user_id
        self.barang_id = barang_id
        self.quantity = quantity

def register_user():
    try:
        print(Fore.LIGHTWHITE_EX)
        print("\n=== Register User ===")
        nama = input("Nama: ").strip()
        password = input("Password: ").strip()
        alamat = input("Alamat : ").strip()
        role = input("""Pilih Role: 
        (1) Penjual
        (2) Pembeli
        """).strip()
        
        if role == "1":
            role = "penjual"
        else :
            role = "pembeli"

        if any(user.nama == nama for user in users):
            os.system("cls")
            print(Fore.LIGHTRED_EX)
            print("==========================================")
            print("       Error: Nama sudah digunakan.       ")
            print("==========================================")
            return register_user()

        user = User(nama=nama, password=password, alamat=alamat, role=role)
        users.append(user)
        
        os.system("cls")
        print(Fore.LIGHTGREEN_EX)
        print("==========================================")
        print(f" User {nama} berhasil terdaftar dengan ID {user.id}. ")
        print("==========================================")
    
    except Exception as e:
        os.system("cls")
        print(Fore.LIGHTRED_EX)
        print("==========================================")
        print(f"         Error pas register: {e}         ")
        print("==========================================")
        return register_user()


def login_user():
    global curr_user
    percobaan = 0
    max_percobaan = 3
    while percobaan < max_percobaan:
        try:
            print(Fore.LIGHTWHITE_EX)
            if percobaan > 0:
                print(Fore.LIGHTRED_EX)
                print("==========================================")
                print(f" Error: Login gagal. Coba lagi ({max_percobaan -
                percobaan} kali).")
                print("==========================================")

            print(Fore.LIGHTWHITE_EX)
            print("\n=== Login User ===")
            nama = input("Nama: ").strip()
            password = input("Password: ").strip()

            user = next((u for u in users if u.nama == nama and u.password == password), None)
            
            if user:
                curr_user = user
                os.system("cls")
                print(Fore.LIGHTGREEN_EX)
                print("==========================================")
                print(f"   Login berhasil sebagai {curr_user.nama} ({curr_user.role}).   ")
                print("==========================================")
                return

            else:
                os.system("cls")
                print(Fore.LIGHTRED_EX)
                print("=================================================================================")
                print("                         Error: Nama atau password salah.                        ")
                print("=================================================================================")
                percobaan +=1

        except Exception as e:
            os.system("cls")
            print(Fore.LIGHTRED_EX)
            print("==========================================")
            print(f"          Error pas login: {e}           ")
            print("==========================================")
            percobaan =+ 1
    punya = int(input(Fore.LIGHTRED_EX + """Terlalu Banyak Percobaan, Jika Belum Punya akun silakan Buat Akun Terlebih Dahulu
    1. Buat Akun
    2. Keluar
    """))
    
    if punya == 1:
        return register_user()
    else :
        exit()

def logout_user():
    global curr_user
    if curr_user:
        os.system("cls")
        print(Fore.LIGHTRED_EX)
        print("==========================================")
        print(f"   User {curr_user.nama} berhasil logout.   ")
        print("==========================================")
        curr_user = None
    else:
        print(Fore.LIGHTBLUE_EX)
        print("==========================================")
        print("     Tidak ada user yang sedang login.    ")
        print("==========================================")
        return

def create_barang():
    try:
        if not curr_user or curr_user.role != "penjual":
            print(Fore.LIGHTRED_EX + "Error: Hanya penjual yang dapat menambah barang.")
            return

        print(Fore.LIGHTWHITE_EX)
        print("\n=== Tambah Barang ===")
        
        if not barangs:
            barang_id = 1
        else:
            barang_id = max(b.id for b in barangs) - 1
            
        nama = input("Nama Barang: ").strip()
        if not nama:
            print(Fore.LIGHTRED_EX + "Error: Nama barang tidak boleh kosong.")
            return create_barang()

        deskripsi = input("Deskripsi Barang: ").strip()
        if not deskripsi:
            print(Fore.LIGHTRED_EX + "Error: Deskripsi barang tidak boleh kosong.")
            return create_barang()
        
        try:
            harga = input("Harga Barang: ").strip()
            harga = int(harga) if harga else 0
        except ValueError:
            print(Fore.LIGHTRED_EX + "Error: Harga harus berupa angka.")
            return create_barang()
        
        try:
            quantity = input("Jumlah Barang: ").strip()
            quantity = int(quantity) if quantity else 1
        except ValueError:
            print(Fore.LIGHTRED_EX + "Error: Jumlah barang harus berupa angka.")
            return create_barang()
        
        os.system("cls")
        print(Fore.LIGHTYELLOW_EX)
        print("\n==========================================")
        print("           Kategori Barang                ")
        print("==========================================")
        print("   1       Elektronik                     ")
        print("   2       Pakaian                        ")
        print("   3       Makanan                        ")
        print("   4       Peralatan Rumah Tangga         ")
        print("------------------------------------------")
        
        kategori_id = input("Kategori ID: ").strip()
        if not kategori_id.isdigit():
            print(Fore.LIGHTRED_EX)
            print("\n==========================================")
            print("  Error: Kategori ID harus berupa angka.  ")
            print("==========================================")
            return create_barang()
        
        kategori_id = int(kategori_id)
        
        kategori_nama = None
        if kategori_id == 1:
            nama_kategori = "Elektronik"
        elif kategori_id == 2:
            nama_kategori = "Pakaian"
        elif kategori_id == 3:
            nama_kategori = "Makanan"
        elif kategori_id == 4:
            nama_kategori = "Peralatan Rumah Tangga"
        else:
            print(Fore.LIGHTRED_EX)
            print("==========================================")
            print("      Error: Kategori ID tidak valid.     ")
            print("==========================================")
            return create_barang()
        
        barang_baru = Barang(
            penjual_id=curr_user.id,
            nama=nama,
            deskripsi=deskripsi,
            harga=harga,
            quantity=quantity,
            kategori_id=kategori_id,
            nama_kategori=nama_kategori,
        )
        barangs.append(barang_baru)
        
        os.system("cls")
        print(Fore.LIGHTGREEN_EX)
        print("===============================================================================")
        print(f"  Barang '{nama}' berhasil ditambahkan dengan ID {barang_baru.id} ke dalam kategori {nama_kategori}.  ")
        print("===============================================================================")
    
    except Exception as e:
        print(Fore.LIGHTRED_EX)
        print("==========================================")
        print(f"      Error pas membuat barang: {e}      ")
        print("==========================================")
        return create_barang()


def read_barang():
    if not barangs:
        os.system("cls")
        print(Fore.LIGHTYELLOW_EX)
        print("\n==========================================")
        print("              Daftar Barang               ")
        print("==========================================")
        print("      Tidak ada barang yang tersedia      ")
        print("------------------------------------------")
        return

    os.system("cls")
    
    df = pd.DataFrame([vars(barang) for barang in barangs])
    df = df.reset_index(drop=True)
    df.index += 1
    
    pd.set_option('display.colheader_justify', 'center')
    
    print(Fore.LIGHTYELLOW_EX + "\n=========================================================================================================")
    print("                                              Daftar Barang.                                             ")
    print("=========================================================================================================")
    print(Fore.LIGHTWHITE_EX)
    print(df.to_string(index=False))
    print(Fore.LIGHTYELLOW_EX + "---------------------------------------------------------------------------------------------------------")

    print(Fore.LIGHTYELLOW_EX + "\n==========================================")
    print("               Pilih Cara Urutkan                 ")
    print("==========================================")
    print("1. Berdasarkan Kategori       ")
    print("2. Berdasarkan Harga Terkecil ")
    print("3. Berdasarkan Harga Terbesar ")
    print("4. Tetap Berdasarkan Index    ")
    print("------------------------------------------")
    
    try:
        # Meminta input pengguna
        pilih = int(input(Fore.LIGHTWHITE_EX + "Masukkan pilihan (1-4): ").strip())

        # Sorting sesuai pilihan pengguna
        if pilih == 1:
            df = df.sort_values(by="kategori_id", ascending=True)
        elif pilih == 2:
            df = df.sort_values(by="harga", ascending=True)  # Harga termurah
        elif pilih == 3:
            df = df.sort_values(by="harga", ascending=False)  # Harga termahal
        elif pilih == 4:
            pass  # Tidak ada perubahan untuk index (default)
        else:
            print(Fore.LIGHTRED_EX + "Pilihan tidak valid. Menampilkan default (Index).")

        os.system("cls")
        print(Fore.LIGHTYELLOW_EX + "\n=========================================================================================================")
        print("                                              Daftar Barang.                                             ")
        print("=========================================================================================================")
        print(Fore.LIGHTWHITE_EX)
        print(df.to_string(index=False))
        print(Fore.LIGHTYELLOW_EX + "---------------------------------------------------------------------------------------------------------")

    except ValueError:
        print(Fore.LIGHTRED_EX + "Input tidak valid. Mohon masukkan angka 1-4.")

def update_barang():
    try:
        if not curr_user or curr_user.role != "penjual":
            print(Fore.LIGHTRED_EX + "Error: Hanya penjual yang dapat mengubah barang.")
            return

        read_barang()
        print(Fore.LIGHTWHITE_EX)
        
        barang_id = input("Masukkan ID Barang yang ingin diubah: ").strip()
        if not barang_id.isdigit():
            print(Fore.LIGHTRED_EX + "Error: ID barang harus berupa angka.")
            return

        barang_id = int(barang_id)
        barang = next((b for b in barangs if b.id == barang_id and b.penjual_id == curr_user.id), None)
        
        if not barang:
            print(Fore.LIGHTRED_EX + "Error: Barang tidak ditemukan atau bukan milik Anda.")
            return
        
        nama = input(f"Nama ({barang.nama}): ").strip()
        barang.nama = nama or barang.nama

        deskripsi = input(f"Deskripsi ({barang.deskripsi}): ").strip()
        barang.deskripsi = deskripsi or barang.deskripsi
        
        try:
            harga = input(f"Harga ({barang.harga}): ").strip()
            barang.harga = int(harga) if harga else barang.harga
        except ValueError:
            print(Fore.LIGHTRED_EX + "Error: Harga harus berupa angka.")
            return
        
        try:
            quantity = input(f"Quantity ({barang.quantity}): ").strip()
            barang.quantity = int(quantity) if quantity else barang.quantity
        except ValueError:
            print(Fore.LIGHTRED_EX + "Error: Quantity harus berupa angka.")
            return
        
        try:
            kategori_id = input(f"kategori_id ({barang.kategori_id}): ").strip()
            kategori_id = int(kategori_id) if kategori_id else barang.kategori_id
            if kategori_id == 1:
                barang.nama_kategori = "Elektronik"
            elif kategori_id == 2:
                barang.nama_kategori = "Pakaian"
            elif kategori_id == 3:
                barang.nama_kategori = "Makanan"
            elif kategori_id == 4:
                barang.nama_kategori = "Peralatan Rumah Tangga"
            else:
                print(Fore.LIGHTRED_EX + "Error: Kategori ID tidak valid.")
                return
            barang.kategori_id = kategori_id
        except ValueError:
            print(Fore.LIGHTRED_EX + "Error: ID Kategori harus berupa angka.")
            return

            
        os.system("cls")
        print(Fore.LIGHTGREEN_EX)
        print("======================================================")
        print(f"        Barang dengan ID {barang.id} berhasil diperbarui.        ")
        print("======================================================")
    except Exception as e:
        print(Fore.LIGHTRED_EX)
        print("==========================================")
        print(f"      Error pas mengubah barang: {e}     ")
        print("==========================================")

def delete_barang():
    try:
        if not curr_user or curr_user.role != "penjual":
            print("Error: Hanya penjual yang dapat menghapus barang.")
            return

        read_barang()
        print(Fore.LIGHTWHITE_EX)
        
        barang_id = input("Masukkan ID Barang yang ingin dihapus: ").strip()
        if not barang_id.isdigit():
            print(Fore.LIGHTRED_EX + "Error: ID barang harus berupa angka.")
            return
        
        barang_id = int(barang_id)
        barang = next((b for b in barangs if b.id == barang_id and b.penjual_id == curr_user.id), None)

        if not barang:
            print(Fore.LIGHTRED_EX + "Error: Barang tidak ditemukan atau bukan milik Anda.")
            return

        barangs.remove(barang)
        
        for i, b in enumerate(barangs):
            b.id = i + 1
                   
        os.system("cls")
        print(Fore.LIGHTGREEN_EX)
        print("==========================================")
        print(f"   Barang dengan ID {barang.id} berhasil dihapus.   ")
        print("==========================================")
    
    except Exception as e:
        print(Fore.LIGHTRED_EX)
        print("==========================================")
        print(f"     Error pas menghapus barang: {e}     ")
        print("==========================================")

def checkout():
    try:
        if not curr_user or curr_user.role != "pembeli":
            print("Error: Hanya pembeli yang dapat checkout.")
            return

        userkeran = [k for k in keranjangs if k.user_id == curr_user.id]
        if not userkeran:
            print(Fore.LIGHTWHITE_EX + "==========================================")
            print(Fore.LIGHTRED_EX + "             Keranjang kosong.            ")
            print(Fore.LIGHTWHITE_EX + "==========================================")
            return
        
        print(Fore.LIGHTMAGENTA_EX + "\n==========================================")
        print(Fore.LIGHTWHITE_EX + "             Keranjang Belanja            ")
        print(Fore.LIGHTMAGENTA_EX + "==========================================")
        for i, keranitem in enumerate(userkeran, 1):
            barang = next((b for b in barangs if b.id == keranitem.barang_id), None)
            if barang:
                print(f"| {i}. {barang.nama} - Harga: {barang.harga} - Quantity: {keranitem.quantity} |")
            else:
                print(f"| {i}. Barang dengan ID {keranitem.barang_id} tidak ditemukan. |")

        pilh = input(Fore.LIGHTWHITE_EX + "\nPilih index barang yang ingin di-checkout (misal: 1,2,3): ").strip()
        piliha = [int(i) - 1 for i in pilh.split(",") if i.isdigit()]

        terpil = [userkeran[i] for i in piliha if i < len(userkeran)]

        if not terpil:
            os.system("cls")
            print(Fore.LIGHTWHITE_EX + "==========================================")
            print(Fore.LIGHTRED_EX + "Tidak ada barang yang dipilih untuk checkout.")
            print(Fore.LIGHTWHITE_EX + "==========================================")
            return checkout()

        total_harga = sum(next((b.harga * k.quantity for b in barangs if b.id == k.barang_id), 0) for k in terpil)
        print(Fore.LIGHTBLUE_EX + "==========================================")
        print(f"\nTotal Harga: {total_harga}")
        print("==========================================")
        confirm = input(
            Fore.LIGHTWHITE_EX + "\nApakah Anda yakin ingin melanjutkan checkout? " +
            Fore.LIGHTGREEN_EX + "Y" + Fore.LIGHTWHITE_EX + "/" +
            Fore.LIGHTRED_EX + "N" + Fore.LIGHTWHITE_EX + " :"
        ).strip().lower()

        if confirm == 'y':
            pesanans.append(Orders(curr_user.id, total_harga, "pending", datetime.now()))
            keranjangs[:] = [k for k in keranjangs if k.user_id != curr_user.id or k not in terpil]
            print(Fore.LIGHTGREEN_EX)
            print("==========================================")
            print("            Checkout Berhasil!            ")
            print("==========================================")
        else:
            os.system("cls")
            print(Fore.LIGHTRED_EX)
            print("==========================================")
            print("           Checkout Dibatalkan!           ")
            print("==========================================")
            
    except Exception as e:
        print(Fore.LIGHTRED_EX)
        print("==========================================")
        print(f"         Error saat checkout: {e}        ")
        print("==========================================")
    
def list_keran():
    try:
        if not curr_user or curr_user.role != "pembeli":
            print("Error: Hanya pembeli yang dapat melihat keranjang.")
            return

        userkeran = [k for k in keranjangs if k.user_id == curr_user.id]
        if not userkeran:
            os.system("cls")
            print(Fore.LIGHTWHITE_EX + "==========================================")
            print(Fore.LIGHTRED_EX + "             Keranjang kosong.            ")
            print(Fore.LIGHTWHITE_EX + "==========================================")
            return

        os.system("cls")
        print(Fore.LIGHTWHITE_EX + "\n==========================================")
        print(Fore.LIGHTBLUE_EX + "             Daftar Keranjang            ")
        print(Fore.LIGHTWHITE_EX + "==========================================")
        
        for i, keranitem in enumerate(userkeran, 1):
            barang = next((b for b in barangs if b.id == keranitem.barang_id), None)
            if barang:
                print(f"{i}. {barang.nama} - Harga: {barang.harga} - Quantity: {keranitem.quantity}")
            else:
                print(f"{i}. Barang dengan ID {keranitem.barang_id} tidak ditemukan.")

        action = input("\nPilih aksi: \n1. Lanjutkan Checkout \n2. Hapus Barang \n3. Kembali ke Menu\nPilih: ").strip()
        
        if action == "1":
            checkout()  # Proceed to checkout
        elif action == "2":
            delete_from_cart(userkeran)  # Allow item removal
        elif action == "3":
            return
        else:
            os.system("cls")
            print(Fore.LIGHTRED_EX)
            print("==========================================")
            print("            Aksi tidak valid.             ")
            print("==========================================")
            
    except Exception as e:
        os.system("cls")
        print(Fore.LIGHTRED_EX)
        print("==========================================")
        print(f"  Error saat menampilkan keranjang: {e}  ")
        print("==========================================")

def delete_from_cart():
    try:
        userkeran = [k for k in keranjangs if k.user_id == curr_user.id]
        if not userkeran:
            os.system("cls")
            print(Fore.LIGHTWHITE_EX + "==========================================")
            print(Fore.LIGHTRED_EX + "             Keranjang kosong.            ")
            print(Fore.LIGHTWHITE_EX + "==========================================")
            return

        os.system("cls")
        print(Fore.LIGHTWHITE_EX + "\n==========================================")
        print(Fore.LIGHTBLUE_EX + "             Daftar Keranjang            ")
        print(Fore.LIGHTWHITE_EX + "==========================================")
        
        for i, keranitem in enumerate(userkeran, 1):
            barang = next((b for b in barangs if b.id == keranitem.barang_id), None)
            if barang:
                print(f"| {i}. {barang.nama} - Harga: {barang.harga} - Quantity: {keranitem.quantity} |")

        item_to_remove = int(input("Masukkan nomor barang yang ingin dihapus dari keranjang: "))
        if 1 <= item_to_remove <= len(userkeran):
            keranitem = userkeran[item_to_remove - 1]
            keranjangs.remove(keranitem)
            os.system("cls")
            print(Fore.LIGHTGREEN_EX)
            print("============================================")
            print(f"  Barang {keranitem.barang_id} berhasil dihapus dari keranjang.")
            print("============================================")
            
        else:
            os.system("cls")
            print(Fore.LIGHTRED_EX)
            print("==========================================")
            print("         Nomor barang tidak valid.        ")
            print("==========================================")
            
    except ValueError:
        os.system("cls")
        print(Fore.LIGHTRED_EX)
        print("==========================================")
        print("            Input tidak valid.            ")
        print("==========================================")
        
    except Exception as e:
        os.system("cls")
        print(Fore.LIGHTRED_EX)
        print("==========================================")
        print(f"  Error saat menghapus barang dari keranjang: {e}  ")
        print("==========================================")

#Karel
def add_keran():
    try:
        if not curr_user or curr_user.role != "pembeli":
            print("Error: Hanya pembeli yang dapat menambah barang ke keranjang.")
            return

        read_barang()
        print(Fore.LIGHTWHITE_EX)
        barang_ids = input("Masukkan ID barang yang ingin ditambahkan (pisahkan dengan spasi): ").split()
        quantities = input("Masukkan jumlah barang (sesuai urutan, pisahkan dengan spasi): ").split()

        if len(barang_ids) != len(quantities):
            raise ValueError(Fore.LIGHTRED_EX + "Jumlah barang dan jumlah yang dimasukkan tidak sesuai.")

        for barang_id, quantity in zip(barang_ids, quantities):
            try:
                barang = next((b for b in barangs if b.id == int(barang_id)), None)
                if not barang:
                    os.system("cls")
                    print(Fore.LIGHTRED_EX)
                    print("==========================================")
                    print(f"   Barang dengan ID '{barang_id}' tidak ditemukan.   ")
                    print("==========================================")
                    continue
                
                qty = int(quantity)
                if qty <= 0 or qty > barang.quantity:
                    os.system("cls")
                    print(Fore.LIGHTRED_EX)
                    print("==========================================")
                    print(f" Quantity {qty} tidak valid untuk barang {barang.nama}.  ")
                    print("==========================================")
                    continue
                
                keranjangs.append(Keranjang(curr_user.id, barang.id, qty))
                
                os.system("cls")
                print(Fore.LIGHTGREEN_EX)
                print("=====================================================")
                print(f"   Barang {barang.nama} berhasil ditambahkan ke keranjang.  ")
                print("=====================================================")
                
            except ValueError:
                os.system("cls")
                print(Fore.LIGHTRED_EX)
                print("==========================================")
                print(f"  ID barang {barang_id} tidak valid.  ")
                print("==========================================")
                
    except Exception as e:
        os.system("cls")
        print(Fore.LIGHTRED_EX)
        print("==========================================")
        print(f"  Error saat menambah ke keranjang: {e}  ")
        print("==========================================")

def list_order():
    try:
        if not curr_user or curr_user.role != "pembeli":
            print("Error: Hanya pembeli yang dapat melihat daftar pesanan.")
            return

        user_orders = [order for order in pesanans if order.user_id == curr_user.id]
        if not user_orders:
            os.system("cls")
            print(Fore.LIGHTWHITE_EX + "==========================================")
            print(Fore.LIGHTBLUE_EX + "             Belum Ada Pesanan.            ")
            print(Fore.LIGHTWHITE_EX + "==========================================")
            return

        os.system("cls")
        print(Fore.LIGHTBLUE_EX + "=========================================================================================================")
        print(Fore.LIGHTWHITE_EX + "                                             Daftar Pesanan.                                            ")
        print(Fore.LIGHTBLUE_EX + "=========================================================================================================")
        
        
        for i, order in enumerate(user_orders, 1):
            print(f"| {i}. ID Pesanan: {order.id} - Total Harga: {order.total_harga} - Status: {order.status} - Tanggal: {order.tanggal} |")
    except Exception as e:
        os.system("cls")
        print(Fore.LIGHTWHITE_EX)
        print("==========================================")
        print(f" Error saat menampilkan daftar pesanan: {e} ")
        print("==========================================")

def menu():
    print(Fore.LIGHTWHITE_EX);
    print("==========================================")
    print("           Terminal E-commerce App        ")
    print("==========================================")
    print("   1       Register User                  ")
    print("   2       Login User                     ")
    print("   3       Exit Program                   ")
    print("------------------------------------------")

def menu_penjual():
    print(Fore.LIGHTGREEN_EX + "==========================================")
    print(Fore.LIGHTWHITE_EX + "           Terminal E-commerce App        ")
    print(Fore.LIGHTGREEN_EX + "==========================================")
    print(Fore.LIGHTWHITE_EX + "               ROLE : Penjual             ")
    print(Fore.LIGHTGREEN_EX + "==========================================")
    print(Fore.LIGHTWHITE_EX + "   1       Tambah Barang                  ")
    print("   2       Daftar Barang                  ")
    print("   3       Update Barang                  ")
    print("   4       Delete Barang                  ")
    print("   5       Log Out                        ")
    print("   6       Exit                           ")
    print(Fore.LIGHTGREEN_EX + "------------------------------------------")

def menu_pembeli():
    print(Fore.LIGHTYELLOW_EX + "==========================================")
    print(Fore.LIGHTWHITE_EX + "           Terminal E-commerce App        ")
    print(Fore.LIGHTYELLOW_EX + "==========================================")
    print(Fore.LIGHTWHITE_EX + "               ROLE : Pembeli             ")
    print(Fore.LIGHTYELLOW_EX + "==========================================")
    print(Fore.LIGHTWHITE_EX + "   1       Daftar Barang                  ")
    print("   2       Tambah Barang ke Keranjang     ")
    print("   3       Daftar Keranjang               ")
    print("   4       Hapus  Keranjang               ")
    print("   5       Check Out                      ")
    print("   6       Riwayat Pesanan                ")
    print("   7       Log Out                        ")
    print("   8       Exit                           ")
    print(Fore.LIGHTYELLOW_EX + "------------------------------------------")

def main():
    while True:
        if not curr_user:
            menu()
            pilihan = input(Fore.LIGHTWHITE_EX + "Pilih menu: ").strip()
            if pilihan == "1":
                register_user()
            elif pilihan == "2":
                login_user()
            elif pilihan == "3":
                print(Fore.LIGHTRED_EX + "\nProgram Closed\nThanks for using this program, Goodbye!")
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
        else:
            # Penanganan setelah login
            if curr_user.role == "penjual":
                while True:
                    menu_penjual()
                    pilihan = input(Fore.LIGHTWHITE_EX + "Pilih menu: ").strip()
                    if pilihan == "1":
                        create_barang()
                    elif pilihan == "2":
                        read_barang()
                    elif pilihan == "3":
                        update_barang()
                    elif pilihan == "4":
                        delete_barang()
                    elif pilihan == "5":
                        logout_user()
                        break # Kembali ke menu utama
                    elif pilihan == "6":
                        print(Fore.LIGHTRED_EX + "\nProgram Closed\nThanks for using this program, Goodbye!")
                        return  # Keluar dari program
                      
                    else:
                        print("Pilihan tidak valid. Silakan coba lagi.")

            elif curr_user.role == "pembeli":
                while True:
                    menu_pembeli()
                    pilihan = input(Fore.LIGHTWHITE_EX + "Pilih menu: ").strip()
                    if pilihan == "1":
                        read_barang()
                    elif pilihan == "2":
                        add_keran()
                    elif pilihan == "3":
                        list_keran()
                    elif pilihan == "4":
                        delete_from_cart()
                    elif pilihan == "5":
                        checkout()
                    elif pilihan == "6":
                        list_order()
                    elif pilihan == "7":
                        logout_user()
                        break
                    elif pilihan == "8":
                        print(Fore.LIGHTRED_EX + "\nProgram Closed\nThanks for using this program, Goodbye!")
                        return

                    else:
                        print(Fore.LIGHTRED_EX + "Pilihan tidak valid. Silakan coba lagi.")


main()


    
