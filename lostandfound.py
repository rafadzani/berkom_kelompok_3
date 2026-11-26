import csv
from datetime import datetime
# Program Lost and Found ITB Jatinangor
# Berfungsi untuk membantu civitas ITB melaporkan dan mencari barang hilang maupun barang temuan

# PROGRAM UTAMA
def main():
    # Menjalankan tampilan utama Lost and Found

    # KAMUS LOKAL
    # database_user, database_hilang, database_temuan : list of dict
    # data_utama_user : list atau bool
    # indeks_user : int
    # email, nama, id_user, pilihan, pilihan_menu : str
    # login_berhasil : bool

    print("=======================================================")
    print("            LOST AND FOUND ITB JATINANGOR")
    print("=======================================================")
    print("Selamat datang di program lost and found ITB Jatinangor")

    # Membaca seluruh database CSV saat program dimulai
    database_user = ambil_data("users.csv")
    database_hilang = ambil_data("baranghilang.csv")
    database_temuan = ambil_data("barangtemuan.csv")
    database_kategori = ambil_data("kategori.csv")

    while True:
        print("\n================ MENU UTAMA =================")
        print("1. Sign In dengan akun yang sudah ada")
        print("2. Sign Up jika belum memiliki akun")
        print("3. Keluar dari program ini")

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
                    print(f"\nApa yang ingin anda lakukan, {nama} :")
                    print("1. Melaporkan barang temuan")
                    print("2. Melaporkan kehilangan barang")
                    print("3. Cek status barang")
                    print("4. Cek Leaderboard")
                    print("5. Keluar dari menu ini")
                    
                    pilihan_menu = input("Pilih menu: ")
                    
                    if pilihan_menu == "1":
                        lapor_barang_temuan(database_temuan, database_hilang, database_user, indeks_user, database_kategori)
                        lanjut = input("Apakah ada yang ingin anda lakukan lagi (y/n) ? : ")
                        if lanjut == "n":
                            break
                    
                    elif pilihan_menu == "2":
                        if lapor_barang_hilang(database_hilang, id_user, database_kategori):
                            simpan_data("baranghilang.csv", database_hilang)
                        lanjut = input("Apakah ada yang ingin anda lakukan lagi (y/n) ? : ")
                        if lanjut == "n":
                            break
                    
                    elif pilihan_menu == "3":
                        cek_status(database_hilang, database_temuan, id_user)

                        lanjut = input("Apakah ada yang ingin anda lakukan lagi (y/n) ? : ")
                        if lanjut == "n":
                            break
                    
                    elif pilihan_menu == "4":
                        cetak_leaderboard(database_user)
                        lanjut = input("Apakah ada yang ingin anda lakukan lagi (y/n) ? : ")
                        if lanjut == "n":
                            break

                    elif pilihan_menu == "5":
                        print("Keluar dari menu ini ...")
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

def lapor_barang_hilang(database_hilang, id_pelapor, database_kategori):
    # Menambahkan laporan barang hilang baru ke dalam slot kosong database_hilang
    # KAMUS LOKAL
    # database_hilang : list of dict
    # id_pelapor, nama_barang, kategori, warna, lokasi, waktu, catatan, bounty : str
    # i : int

    print("\n================ LAPOR BARANG HILANG ================")

    # Mencari slot kosong dalam database_hilang
    for i in range(len(database_hilang)):
        if database_hilang[i]["id_barang"] == "":

            nama_barang = input("Masukkan nama barang: ").strip()
            while nama_barang == "":
                nama_barang = input("Nama barang tidak boleh kosong! Masukkan nama barang: ").strip()

            kategori = pilih_kategori(database_kategori)

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

            # Mengisi slot kosong dengan laporan baru
            database_hilang[i] = {
                "nomor": str(i + 1),
                "id_barang": "H" + str(i + 1).zfill(3),
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

            print("\nLaporan barang hilang berhasil ditambahkan!")
            print(f"ID Barang : {database_hilang[i]['id_barang']}")
            print(f"Status    : {database_hilang[i]['status']}")
            return True

    print("Database barang hilang sudah penuh!")
    return False

def lapor_barang_temuan(database_temuan, database_hilang, database_user, indeks_user, database_kategori):
    # Melaporkan barang temuan, mencocokkan dengan barang hilang, dan memberi poin bounty
    # KAMUS LOKAL
    # database_temuan, database_hilang, database_user : list of dict
    # indeks_kandidat : list of int
    # indeks_user, jumlah_kandidat, pilihan, idx_hilang, bounty, poin_sekarang, i : int
    # id_pelapor, nama_barang, kategori, warna, lokasi, waktu, catatan, konfirmasi : str
    # cocok_nama, cocok_kategori, cocok_warna : bool
    # barang_target : dict

    print("\n================ LAPOR BARANG TEMUAN ================")
    id_pelapor = database_user[indeks_user]["user_id"]

    nama_barang = input("Masukkan nama barang yang ditemukan: ").strip()
    while nama_barang == "":
        nama_barang = input("Nama barang tidak boleh kosong! Masukkan nama barang: ").strip()

    kategori = pilih_kategori(database_kategori)

    warna = input("Masukkan warna barang: ").strip()
    while warna == "":
        warna = input("Warna tidak boleh kosong! Masukkan warna: ").strip()

    lokasi = input("Masukkan lokasi ditemukan: ").strip()
    while lokasi == "":
        lokasi = input("Lokasi tidak boleh kosong! Masukkan lokasi: ").strip()

    waktu = input("Masukkan waktu ditemukan (kosongkan untuk waktu sekarang): ").strip()
    if waktu == "":
        waktu = datetime.now().strftime("%d-%m-%Y %H:%M")

    catatan = input("Masukkan catatan/ciri khusus barang: ").strip()
    if catatan == "":
        catatan = "-"

    # Mencocokkan dengan daftar barang hilang menggunakan array statis
    indeks_kandidat = [-1] * len(database_hilang)
    jumlah_kandidat = 0

    for i in range(len(database_hilang)):
        item = database_hilang[i]
        if item["id_barang"] != "" and item["status"] == "Belum Ditemukan":
            cocok_nama = (nama_barang.lower() in item["nama_barang"].lower()) or (item["nama_barang"].lower() in nama_barang.lower())
            cocok_kategori = kategori.lower() == item["kategori"].lower()
            cocok_warna = warna.lower() == item["warna"].lower()

            if cocok_nama or (cocok_kategori and cocok_warna):
                indeks_kandidat[jumlah_kandidat] = i
                jumlah_kandidat += 1

    if jumlah_kandidat > 0:
        print("\n[!] Ditemukan laporan barang hilang yang mirip di sistem:")
        for i in range(jumlah_kandidat):
            item = database_hilang[indeks_kandidat[i]]
            print(f"{i + 1}. [{item['id_barang']}] {item['nama_barang']} | "
                  f"Warna: {item['warna']} | Lokasi hilang: {item['lokasi']} | "
                  f"Ciri: {item['catatan']} | Bounty: {item['bounty']} poin")

        konfirmasi = input("\nApakah barang yang Anda temukan cocok dengan salah satu daftar di atas? (y/n): ").strip().lower()
        if konfirmasi == "y":
            pilihan = input("Masukkan nomor urut barang yang cocok: ").strip()
            while not pilihan.isdigit() or int(pilihan) < 1 or int(pilihan) > jumlah_kandidat:
                pilihan = input("Nomor tidak valid! Masukkan nomor urut yang sesuai: ").strip()

            idx_hilang = indeks_kandidat[int(pilihan) - 1]
            barang_target = database_hilang[idx_hilang]
            barang_target["status"] = "Sudah Ditemukan"

            # Menambahkan poin bounty ke akun penemu
            bounty = int(barang_target["bounty"])
            poin_sekarang = int(database_user[indeks_user]["poin"])
            database_user[indeks_user]["poin"] = str(poin_sekarang + bounty)

            # Mencari kontak pemilik barang
            nama_pemilik = "Tidak diketahui"
            hp_pemilik = "-"
            email_pemilik = "-"
            for user in database_user:
                if user["user_id"] == barang_target["id_pelapor"]:
                    nama_pemilik = user["nama"]
                    hp_pemilik = user["no_hp"]
                    email_pemilik = user["email"]
                    break

            simpan_data("baranghilang.csv", database_hilang)
            simpan_data("users.csv", database_user)

            print("\n=== KECOCOKAN TERKONFIRMASI ===")
            print(f"Status barang [{barang_target['id_barang']}] diperbarui menjadi: Sudah Ditemukan")
            print("Silakan hubungi pemilik untuk pengembalian barang:")
            print(f"- Nama  : {nama_pemilik}")
            print(f"- No HP : {hp_pemilik}")
            print(f"- Email : {email_pemilik}")
            print(f"Selamat! Anda mendapatkan +{bounty} poin bounty.")
            return True

    # Jika tidak ada yang cocok, cari slot kosong di database_temuan
    for i in range(len(database_temuan)):
        if database_temuan[i]["id_barang"] == "":
            database_temuan[i] = {
                "nomor": str(i + 1),
                "id_barang": "T" + str(i + 1).zfill(3),
                "id_pelapor": id_pelapor,
                "nama_barang": nama_barang,
                "kategori": kategori,
                "warna": warna,
                "lokasi": lokasi,
                "waktu": waktu,
                "catatan": catatan,
                "status": "Belum Diklaim"
            }

            simpan_data("barangtemuan.csv", database_temuan)
            print("\nLaporan barang temuan berhasil ditambahkan!")
            print(f"ID Barang : {database_temuan[i]['id_barang']}")
            print(f"Status    : {database_temuan[i]['status']}")
            return True

    print("Database barang temuan sudah penuh!")
    return False

def pilih_kategori(database_kategori):
    # Memilih kategori barang berdasarkan kategori.csv

    print("\nPilih kategori barang:")

    for i in range(len(database_kategori)):
        print(f"{i + 1}. {database_kategori[i]['kategori']}")

    pilihan = input("Masukkan nomor kategori: ")

    while not pilihan.isdigit() or int(pilihan) < 1 or int(pilihan) > len(database_kategori):
        pilihan = input("Pilihan tidak valid! Masukkan nomor kategori: ")

    kategori = database_kategori[int(pilihan) - 1]["kategori"]

    return kategori

def cek_status(database_hilang, database_temuan, id_user):
    print("\n============= STATUS BARANG ANDA =============")

    print("\n----Laporan Barang Hilang ----")
    ada_hilang = False
    for i in range(len(database_hilang)):
        item = database_hilang[i]
        if item["id_pelapor"] == id_user and item["id_barang"] != "":
            ada_hilang = True
            print(f"[{item['id_barang']}] {item['nama_barang']} ({item['kategori']}, {item['warna']}) | "
                  f"Lokasi: {item['lokasi']} | Waktu: {item['waktu']} | "
                  f"Bounty: {item['bounty']} poin | Status: {item['status']}")

    if not ada_hilang:
        print("Belum ada laporang barang hilang")
    
    print("\n----Laporan Barang Temuan ----")
    ada_temuan = False
    for i in range(len(database_temuan)):
        item = database_temuan[i]
        if item["id_pelapor"] == id_user and item["id_barang"] != "":
            ada_temuan = True
            print(f"[{item['id_barang']}] {item['nama_barang']} ({item['kategori']}, {item['warna']}) | "
                  f"Lokasi: {item['lokasi']} | Waktu: {item['waktu']} | Status: {item['status']}")
        
    if not ada_temuan:
        print("Belum ada laporang barang temuan")
            


def cetak_leaderboard(database_user):
    print("\n============= LEADERBOARD BOUNTY =============")
    indeks_aktif = [-1 for i in range(len(database_user))]
    jumlah_user = 0

    for i in range(len(database_user)):
        if database_user[i]["user_id"] != "":
            indeks_aktif[jumlah_user] = i
            jumlah_user += 1
        
    if jumlah_user == 0:
        print("Belum ada pengguna terdaftar.")
        return

    # Sortir dari poin tertinggi ke terendah
    for i in range(jumlah_user - 1):
        indeks_max = i
        for j in range(i + 1, jumlah_user):
            poin_j = int(database_user[indeks_aktif[j]]["poin"])
            poin_max = int(database_user[indeks_aktif[indeks_max]]["poin"])
            if poin_j > poin_max:
                indeks_max = j

        if indeks_max != i:
            temp = indeks_aktif[i]
            indeks_aktif[i] = indeks_aktif[indeks_max]
            indeks_aktif[indeks_max] = temp

    print("Peringkat / Nama / Poin")
    print("=" * 40)
    for i in range(jumlah_user):
        user = database_user[indeks_aktif[i]]
        print(f"{i + 1} / {user["nama"]} / {user["poin"]}")



main()
