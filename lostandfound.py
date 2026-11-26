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
    database_hilang = ambil_data("baranghilang.csv")

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
                    id_user = database_user[indeks_user]["user_id"]

                    if cek_password(database_user, indeks_user):
                        print("\nLogin berhasil!")
                        print("Selamat datang,", nama)
                        login_berhasil = True
                        break
                    else:
                        break

                else:
                    print("Silakan masukkan email kembali.")

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
                        print("laporkan")
                    
                    elif pilihan_menu == "2":
                        if lapor_barang_hilang(database_hilang, id_user):
                            simpan_data("baranghilang.csv", database_hilang)
                    
                    elif pilihan_menu == "3":
                        print("berikut status barang anda")
                    
                    elif pilihan_menu == "4":
                        print("cetak leaderboard")
                    
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

def lapor_barang_hilang(database_hilang, id_pelapor):
    # Menambahkan laporan barang hilang baru ke dalam database_hilang
    # KAMUS LOKAL
    # database_hilang : list of dict
    # id_pelapor, nama_barang, kategori, warna, lokasi, waktu, catatan, bounty : str
    # nomor_baru, indeks_kosong : int
    # laporan_baru : dict

    print("\n================ LAPOR BARANG HILANG ================")

    nama_barang = input("Masukkan nama barang: ").strip()
    while nama_barang == "":
        nama_barang = input("Nama barang tidak boleh kosong! Masukkan nama barang: ").strip()

    kategori = input("Masukkan kategori (Elektronik/Alat Tulis/Botol Minum/Kartu/Lainnya): ").strip()
    while kategori == "":
        kategori = input("Kategori tidak boleh kosong! Masukkan kategori: ").strip()

    warna = input("Masukkan warna barang: ").strip()
    while warna == "":
        warna = input("Warna tidak boleh kosong! Masukkan warna: ").strip()

    lokasi = input("Masukkan perkiraan lokasi hilang: ").strip()
    while lokasi == "":
        lokasi = input("Lokasi tidak boleh kosong! Masukkan lokasi: ").strip()

    waktu = input("Masukkan perkiraan waktu hilang (kosongkan untuk waktu sekarang): ").strip()
    if waktu == "":
        waktu = datetime.now().strftime("%d-%m-%Y %H:%M")

    catatan = input("Masukkan catatan/ciri khusus barang: ").strip()
    if catatan == "":
        catatan = "-"

    bounty = input("Masukkan poin bounty untuk penemu (angka, contoh: 10): ").strip()
    while not bounty.isdigit():
        bounty = input("Bounty harus berupa angka! Masukkan poin bounty: ").strip()

    # Mencari slot kosong pada CSV (jika file sudah disiapkan nomornya seperti users.csv)
    indeks_kosong = -1
    for i in range(len(database_hilang)):
        if database_hilang[i]["id_barang"] == "":
            indeks_kosong = i
            break

    if indeks_kosong != -1:
        nomor_baru = indeks_kosong + 1
    else:
        nomor_baru = len(database_hilang) + 1

    laporan_baru = {
        "nomor": str(nomor_baru),
        "id_barang": "H" + str(nomor_baru).zfill(3),
        "id_pelapor": id_pelapor,
        "nama_barang": nama_barang,
        "kategori": kategori,
        "warna": warna,
        "lokasi": lokasi,
        "waktu": waktu,
        "catatan": catatan,
        "bounty": bounty,
        "status": "Belum Ditemukan"
    }

    if indeks_kosong != -1:
        database_hilang[indeks_kosong] = laporan_baru
    else:
        database_hilang.append(laporan_baru)

    print("\nLaporan barang hilang berhasil ditambahkan!")
    print(f"ID Barang : {laporan_baru['id_barang']}")
    print(f"Status    : {laporan_baru['status']}")
    return True

main()