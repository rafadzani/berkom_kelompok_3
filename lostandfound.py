import csv
from datetime import datetime
# Program Lost and Found ITB Jatinangor
# Berfungsi untuk membantu civitas ITB melaporkan dan mencari barang hilang maupun barang temuan

# PROGRAM UTAMA
def main():
    # Menjalankan tampilan utama Lost and Found

    # KAMUS LOKAL
    # database_user : list of dict
    # data_utama_user : list atau bool
    # indeks_user : int
    # email, nama, pilihan : str
    # login_berhasil : bool

    print("===================================================")
    print("       LOST AND FOUND ITB JATINANGOR")
    print("===================================================")

    # Membaca database pengguna saat program dimulai
    database_user = ambil_data("users.csv")

    while True:
        print("\n================ MENU UTAMA =================")
        print("1. Sign In")
        print("2. Sign Up")
        print("3. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            # Proses Sign In
            login_berhasil = False

            while True:
                data_utama_user = cek_user(database_user)

                if data_utama_user != False:
                    indeks_user = data_utama_user[1]
                    email = data_utama_user[2]
                    nama = data_utama_user[3]

                    if cek_password(database_user, indeks_user):
                        print("\nLogin berhasil!")
                        print("Selamat datang,", nama)
                        login_berhasil = True
                        break
                    else:
                        break

                else:
                    print("\nApa yang ingin anda lakukan?")
                    print("1. Masukkan email ulang")
                    print("2. Sign Up")
                    print("3. Kembali ke menu utama")

                    pilihan_email = input("Pilih menu: ")

                    if pilihan_email == "1":
                        continue   # minta ulang email
                    elif pilihan_email == "2":
                        if daftar_user(database_user):
                            simpan_data("users.csv", database_user)
                        break      # setelah daftar, balik ke menu utama
                    elif pilihan_email == "3":
                        break      # balik ke menu utama
                    else:
                        print("Pilihan tidak valid! Masukkan angka 1-3.")

            if login_berhasil:
                print("===================================================")
                print("Anda berhasil masuk ke sistem Lost and Found.")
                print("===================================================")

                while True:
                    print(f"Apa yang ingin anda lakukan, {nama} :")
                    print("1. Melaporkan barang temuan")
                    print("2. Melaporkan kehilangan barang")
                    print("3. Cek status barang")
                    print("4. Cek Leaderboard")
                    print("5. Keluar dari menu ini")
                    
                    pilihan_menu = input("Pilih menu: ")
                    
                    if pilihan_menu == "1":
                        print("===================================================")
                        print("Laporan Barang Temuan")
                        print("===================================================")
                    
                    elif pilihan_menu == "2":
                        print("===================================================")
                        print("Laporan Barang Hilang")
                        print("===================================================")
                    
                    elif pilihan_menu == "3":
                        print("===================================================")
                        print("Status Barang Hilang")
                        print("===================================================")
                    
                    elif pilihan_menu == "4":
                        print("===================================================")
                        print("Leaderboard Poin")
                        print("===================================================")
                    
                    elif pilihan_menu == "5":
                        break
                    
                    else:
                        print("pilihan tidak valid")

        elif pilihan == "2":
            # Proses Sign Up
            if daftar_user(database_user):
               simpan_data("users.csv", database_user)

        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan Lost and Found ITB!")
            break

        else:
            print("Pilihan tidak valid! Masukkan angka 1-3.")

#subprogram
def ambil_data(filename):
  # Membaca file CSV dan mengambil datanya
  # KAMUS LOKAL
  # filename : str; pembaca : DictReader
  with open(filename, mode="r", encoding="utf-8-sig") as file:
    pembaca = csv.DictReader(file)
    return [row for row in pembaca]

def daftar_user(database):
    # Mendaftarkan pengguna baru ke dalam database
    # KAMUS LOKAL
    # database : list of dict; nama, email, password, no_hp : str; sudah_ada : bool; i : int

    # Mencari slot kosong dalam database
    for i in range(len(database)):
        if database[i]["user_id"] == "":

            nama = input("Masukkan nama lengkap: ")
            while nama == "":
                nama = input("Nama tidak boleh kosong! Masukkan nama: ")

            # Memeriksa email agar tidak terdaftar dua kali
            while True:
                email = input("Masukkan email: ").strip()

                if email == "":
                    print("Email tidak boleh kosong!")
                else:
                    sudah_ada = False

                    for data in database:
                        if data["email"].lower() == email.lower():
                            sudah_ada = True
                            break

                    if sudah_ada == False:
                        break

                    print("Email sudah terdaftar!")

            password = input("Masukkan password: ")
            while password == "":
                password = input("Password tidak boleh kosong! Masukkan password: ")

            no_hp = input("Masukkan nomor handphone: ")
            while no_hp == "":
                no_hp = input("Nomor handphone tidak boleh kosong! Masukkan nomor handphone: ")

            # Mengisi slot kosong dengan data pengguna baru
            database[i] = {
                "nomor": str(i + 1),
                "user_id": "U" + str(i + 1).zfill(3),
                "nama": nama,
                "email": email,
                "password": password,
                "no_hp": no_hp,
                "poin": "0"
            }

            print("\nRegistrasi berhasil!")
            print("Akun anda berhasil didaftarkan.")
            print("Silahkan login kembali dengan akun yang sudah anda buat")
            return True

    print("Database pengguna sudah penuh!")
    return False

def simpan_data(filename, database):
    # Menyimpan perubahan data ke dalam file CSV

    # KAMUS LOKAL
    # filename : str; database : list of dict; penulis : DictWriter

    if len(database) == 0:
        print("Database kosong, tidak ada data yang disimpan!")
        return False

    with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
        penulis = csv.DictWriter(file, fieldnames=database[0].keys())
        penulis.writeheader()
        penulis.writerows(database)

    return True

def cek_user(database):
  # Meminta input username lalu mencocokkannya dengan database
  # KAMUS LOKAL
  # 
  email = input("Masukkan email anda: ")
  for i in range(len(database)):
    if database[i]["email"] == email and email != "":
      nama_user = database[i]["nama"]
      return [True, i, email, nama_user]
  print("Email tidak terdaftar!")
  return False

def cek_password(database, indeks):
  # Meminta input password lalu mencocokkannya dengan database
  # KAMUS LOKAL
  # database : list of dict; indeks, kesempatan : int; password : str
  for kesempatan in range(3):   # User diberi 3 kali percobaan/kesempatan
    password = input("Masukkan password: ")
    if password == database[indeks]["password"]:
      return True
    print("Password salah!")
  print("Anda sudah salah 3 kali!\nSilahkan login ulang\nApabila Lupa, Hubungi admin untuk mengganti password")
  return False

def form_temuan(nama, barang):
  # Meminta input password lalu mencocokkannya dengan database
  # KAMUS LOKAL
  # database : list of dict; indeks, kesempatan : int; password : str

    main()