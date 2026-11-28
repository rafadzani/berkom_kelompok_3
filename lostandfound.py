import csv
from datetime import datetime
# Program Lost and Found ITB Jatinangor
# Berfungsi untuk membantu civitas ITB melaporkan dan mencari barang hilang maupun barang temuan

# PROGRAM UTAMA
def main():
    # Menjalankan tampilan utama Lost and Found

    # KAMUS LOKAL
    # database_user, database_hilang, database_temuan, database_kategori : list of dict
    # data_utama_user : list atau None
    # indeks_user : int
    # nama, id_user, pilihan, pilihan_email, pilihan_menu : str
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

    # Program tidak bisa jalan kalau salah satu file hilang atau kosong
    if (len(database_user) == 0 or len(database_hilang) == 0 or len(database_temuan) == 0 or len(database_kategori) == 0):
        print("\nProgram tidak dapat dijalankan!")
        print("Pastikan users.csv, baranghilang.csv, barangtemuan.csv, dan kategori.csv")
        print("ada di folder yang sama dan berisi data awal.")
        return

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

                if data_utama_user is not None:
                    indeks_user = data_utama_user[1]
                    nama = data_utama_user[3]

                    if cek_password(database_user, indeks_user):
                        id_user = database_user[indeks_user]["user_id"]
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
                        if not tanya_lanjut():
                            break

                    elif pilihan_menu == "2":
                        lapor_barang_hilang(database_hilang, database_temuan, database_user, indeks_user, database_kategori)
                        if not tanya_lanjut():
                            break

                    elif pilihan_menu == "3":
                        cek_status(database_hilang, database_temuan, id_user)
                        if not tanya_lanjut():
                            break

                    elif pilihan_menu == "4":
                        cetak_leaderboard(database_user)
                        if not tanya_lanjut():
                            break

                    elif pilihan_menu == "5":
                        print("Keluar dari menu ini ...")
                        break

                    else:
                        print("Pilihan tidak valid! Masukkan angka 1-5.")

        elif pilihan == "2":
            # Proses Sign Up
            if daftar_user(database_user):
                simpan_data("users.csv", database_user)

        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan Lost and Found ITB!")
            break

        else:
            print("Pilihan tidak valid! Masukkan angka 1-3.")

# SUBPROGRAM
def ambil_data(filename):
    # Membaca file CSV dan mengambil datanya
    # Jika file tidak ditemukan, mengembalikan list kosong
    # KAMUS LOKAL
    # filename : str
    # file : file object; pembaca : DictReader
    try:
        with open(filename, mode="r", encoding="utf-8-sig") as file:
            pembaca = csv.DictReader(file)
            return [row for row in pembaca]
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan!")
        return []

def tanya_lanjut():
    # Menanyakan apakah user ingin melakukan hal lain (valid hanya y atau n)
    # Mengembalikan True jika user menjawab y, False jika n
    # KAMUS LOKAL
    # jawaban : str
    jawaban = input("Apakah ada yang ingin anda lakukan lagi (y/n) ? : ").strip().lower()
    while jawaban != "y" and jawaban != "n":
        jawaban = input("Pilihan tidak valid! Masukkan y atau n: ").strip().lower()
    return jawaban == "y"

def daftar_user(database):
    # Mendaftarkan pengguna baru ke dalam database
    # KAMUS LOKAL
    # database : list of dict
    # nama, email, password, no_hp : str
    # sudah_ada : bool
    # i : int
    # data : dict

    # Mencari slot kosong dalam database
    for i in range(len(database)):
        if database[i]["user_id"] == "":

            nama = input("Masukkan nama lengkap: ").strip()
            while nama == "":
                nama = input("Nama tidak boleh kosong! Masukkan nama: ").strip()

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

            no_hp = input("Masukkan nomor handphone: ").strip()
            while no_hp == "":
                no_hp = input("Nomor handphone tidak boleh kosong! Masukkan nomor handphone: ").strip()

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
    # Mengembalikan True jika berhasil, False jika database kosong
    # KAMUS LOKAL
    # filename : str
    # database : list of dict
    # file : file object; penulis : DictWriter

    if len(database) == 0:
        print("Database kosong, tidak ada data yang disimpan!")
        return False

    with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
        penulis = csv.DictWriter(file, fieldnames=database[0].keys())
        penulis.writeheader()
        penulis.writerows(database)

    return True

def cek_user(database):
    # Meminta input email lalu mencocokkannya dengan database (tidak case-sensitive)
    # Mengembalikan [True, indeks, email, nama] jika ketemu, None jika tidak
    # KAMUS LOKAL
    # database : list of dict
    # email : str
    # i : int
    email = input("Masukkan email anda: ").strip()
    for i in range(len(database)):
        if email != "" and database[i]["email"].lower() == email.lower():
            return [True, i, database[i]["email"], database[i]["nama"]]
    print("Email tidak terdaftar!")
    return None

def cek_password(database, indeks):
    # Meminta input password lalu mencocokkannya dengan database
    # KAMUS LOKAL
    # database : list of dict
    # indeks, kesempatan : int
    # password : str
    for kesempatan in range(3):   # User diberi 3 kali percobaan/kesempatan
        password = input("Masukkan password: ")
        if password == database[indeks]["password"]:
            return True
        print("Password salah!")
    print("Anda sudah salah 3 kali!\nSilahkan login ulang\nApabila Lupa, Hubungi admin untuk mengganti password")
    return False

def cari_kandidat(nama_barang, kategori, warna, database, status_dicari, id_pengecualian):
    # Mencari indeks barang di database yang mirip dengan barang yang baru dilaporkan
    # id_pengecualian = id pelapor sendiri, agar tidak mencocokkan barang miliknya sendiri
    # Mengembalikan (indeks_kandidat, jumlah)
    # KAMUS LOKAL
    # nama_barang, kategori, warna, status_dicari, id_pengecualian : str
    # database : list of dict
    # indeks_kandidat : list of int
    # jumlah, i : int
    # item : dict
    # cocok_nama, cocok_kategori, cocok_warna : bool

    indeks_kandidat = [-1] * len(database)
    jumlah = 0

    for i in range(len(database)):
        item = database[i]
        if (item["id_barang"] != ""
                and item["status"] == status_dicari
                and item["id_pelapor"] != id_pengecualian):

            cocok_nama = (nama_barang.lower() in item["nama_barang"].lower()) or \
                         (item["nama_barang"].lower() in nama_barang.lower())
            cocok_kategori = kategori.lower() == item["kategori"].lower()
            cocok_warna = warna.lower() == item["warna"].lower()

            # Kategori harus sama, lalu nama ATAU warna harus cocok
            if cocok_kategori and (cocok_nama or cocok_warna):
                indeks_kandidat[jumlah] = i
                jumlah += 1

    return indeks_kandidat, jumlah

def cari_kontak(database_user, user_id):
    # Mengembalikan data user (dict) berdasarkan user_id
    # Jika tidak ditemukan, mengembalikan dict cadangan
    # KAMUS LOKAL
    # database_user : list of dict
    # user_id : str
    # user : dict
    for user in database_user:
        if user["user_id"] == user_id:
            return user
    return {"nama": "Tidak diketahui", "no_hp": "-", "email": "-", "poin": "0"}

def tambah_barang_temuan(database_temuan, id_pelapor, nama_barang, kategori, warna, lokasi, waktu, catatan, status):
    # Mengisi slot kosong pertama di database_temuan dengan laporan baru
    # Mengembalikan indeks slot yang diisi, atau -1 jika database penuh
    # KAMUS LOKAL
    # database_temuan : list of dict
    # id_pelapor, nama_barang, kategori, warna, lokasi, waktu, catatan, status : str
    # i : int
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
                "status": status
            }
            return i
    return -1

def pilih_kategori(database_kategori):
    # Memilih kategori barang berdasarkan kategori.csv
    # Mengembalikan nama kategori yang dipilih
    # KAMUS LOKAL
    # database_kategori : list of dict
    # i : int
    # pilihan, kategori : str

    print("\nPilih kategori barang:")

    for i in range(len(database_kategori)):
        print(f"{i + 1}. {database_kategori[i]['kategori']}")

    pilihan = input("Masukkan nomor kategori: ").strip()

    while not pilihan.isdigit() or int(pilihan) < 1 or int(pilihan) > len(database_kategori):
        pilihan = input("Pilihan tidak valid! Masukkan nomor kategori: ").strip()

    kategori = database_kategori[int(pilihan) - 1]["kategori"]

    return kategori

def lapor_barang_hilang(database_hilang, database_temuan, database_user, indeks_user, database_kategori):
    # Menambahkan laporan barang hilang, lalu mengecek apakah sudah ada barang temuan yang mirip
    # KAMUS LOKAL
    # database_hilang, database_temuan, database_user, database_kategori : list of dict
    # indeks_kandidat : list of int
    # indeks_user, i, k, jumlah_kandidat, idx_temuan : int
    # id_pelapor, nama_barang, kategori, warna, lokasi, waktu, catatan, bounty : str
    # konfirmasi, pilihan : str
    # barang_temuan, penemu, t : dict

    print("\n================ LAPOR BARANG HILANG ================")
    id_pelapor = database_user[indeks_user]["user_id"]

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

            # Match balik ke database barang temuan
            indeks_kandidat, jumlah_kandidat = cari_kandidat(nama_barang, kategori, warna, database_temuan, "Belum Diklaim", id_pelapor)

            if jumlah_kandidat > 0:
                print("\n[!] Ada barang temuan yang mirip dengan barang Anda:")
                for k in range(jumlah_kandidat):
                    t = database_temuan[indeks_kandidat[k]]
                    print(f"{k + 1}. [{t['id_barang']}] {t['nama_barang']} | "
                          f"Warna: {t['warna']} | Lokasi ditemukan: {t['lokasi']} | "
                          f"Ciri: {t['catatan']}")

                konfirmasi = input("\nApakah salah satunya adalah barang Anda? (y/n): ").strip().lower()
                if konfirmasi == "y":
                    pilihan = input("Masukkan nomor urut barang yang cocok: ").strip()
                    while not pilihan.isdigit() or int(pilihan) < 1 or int(pilihan) > jumlah_kandidat:
                        pilihan = input("Nomor tidak valid! Masukkan nomor urut yang sesuai: ").strip()

                    idx_temuan = indeks_kandidat[int(pilihan) - 1]
                    barang_temuan = database_temuan[idx_temuan]

                    # Update status kedua barang
                    barang_temuan["status"] = "Sudah Diklaim"
                    database_hilang[i]["status"] = "Sudah Ditemukan"

                    # Poin bounty untuk si penemu
                    penemu = cari_kontak(database_user, barang_temuan["id_pelapor"])
                    penemu["poin"] = str(int(penemu["poin"]) + int(bounty))

                    simpan_data("barangtemuan.csv", database_temuan)
                    simpan_data("users.csv", database_user)

                    print("\n=== KECOCOKAN TERKONFIRMASI ===")
                    print("Silakan hubungi penemu untuk mengambil barang Anda:")
                    print(f"- Nama  : {penemu['nama']}")
                    print(f"- No HP : {penemu['no_hp']}")
                    print(f"- Email : {penemu['email']}")
                    print(f"Penemu mendapatkan +{bounty} poin bounty dari Anda.")

            simpan_data("baranghilang.csv", database_hilang)
            return True

    print("Database barang hilang sudah penuh!")
    return False

def lapor_barang_temuan(database_temuan, database_hilang, database_user, indeks_user, database_kategori):
    # Melaporkan barang temuan, mencocokkan dengan barang hilang, dan memberi poin bounty
    # KAMUS LOKAL
    # database_temuan, database_hilang, database_user, database_kategori : list of dict
    # indeks_kandidat : list of int
    # indeks_user, jumlah_kandidat, idx_hilang, idx_baru, bounty, poin_sekarang, i : int
    # id_pelapor, nama_barang, kategori, warna, lokasi, waktu, catatan : str
    # konfirmasi, pilihan, nama_pemilik, hp_pemilik, email_pemilik : str
    # item, barang_target, pemilik : dict

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

    # Mencocokkan dengan barang hilang milik orang lain
    indeks_kandidat, jumlah_kandidat = cari_kandidat(
        nama_barang, kategori, warna, database_hilang, "Belum Ditemukan", id_pelapor
    )

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
            pemilik = cari_kontak(database_user, barang_target["id_pelapor"])
            nama_pemilik = pemilik["nama"]
            hp_pemilik = pemilik["no_hp"]
            email_pemilik = pemilik["email"]

            # Mencatat laporan temuan ini agar muncul di "Cek status barang" penemu
            idx_baru = tambah_barang_temuan(database_temuan, id_pelapor, nama_barang, kategori,
                                            warna, lokasi, waktu, catatan, "Sudah Diklaim")
            if idx_baru != -1:
                simpan_data("barangtemuan.csv", database_temuan)

            simpan_data("baranghilang.csv", database_hilang)
            simpan_data("users.csv", database_user)

            print("\n=== KECOCOKAN TERKONFIRMASI ===")
            print(f"Status barang [{barang_target['id_barang']}] diperbarui menjadi: Sudah Ditemukan")
            print("Silakan hubungi pemilik untuk pengembalian barang:")
            print(f"- Nama  : {nama_pemilik}")
            print(f"- No HP : {hp_pemilik}")
            print(f"- Email : {email_pemilik}")
            print(f"Selamat! Anda mendapatkan +{bounty} poin bounty.")
            if idx_baru != -1:
                print(f"Laporan temuan anda tercatat dengan ID {database_temuan[idx_baru]['id_barang']}.")
            else:
                print("Catatan: database barang temuan penuh, laporan temuan anda tidak dicatat.")
            return True

    # Jika tidak ada yang cocok (atau user menjawab n), simpan sebagai barang temuan baru
    idx_baru = tambah_barang_temuan(database_temuan, id_pelapor, nama_barang, kategori,
                                    warna, lokasi, waktu, catatan, "Belum Diklaim")

    if idx_baru == -1:
        print("Database barang temuan sudah penuh!")
        return False

    simpan_data("barangtemuan.csv", database_temuan)
    print("\nLaporan barang temuan berhasil ditambahkan!")
    print(f"ID Barang : {database_temuan[idx_baru]['id_barang']}")
    print(f"Status    : {database_temuan[idx_baru]['status']}")
    return True

def cek_status(database_hilang, database_temuan, id_user):
    # Menampilkan semua laporan hilang dan temuan milik user yang sedang login
    # KAMUS LOKAL
    # database_hilang, database_temuan : list of dict
    # id_user : str
    # i : int
    # item : dict
    # ada_hilang, ada_temuan : bool
    print("\n============= STATUS BARANG ANDA =============")

    print("\n---- Laporan Barang Hilang ----")
    ada_hilang = False
    for i in range(len(database_hilang)):
        item = database_hilang[i]
        if item["id_pelapor"] == id_user and item["id_barang"] != "":
            ada_hilang = True
            print(f"[{item['id_barang']}] {item['nama_barang']} ({item['kategori']}, {item['warna']}) | "
                  f"Lokasi: {item['lokasi']} | Waktu: {item['waktu']} | "
                  f"Bounty: {item['bounty']} poin | Status: {item['status']}")

    if not ada_hilang:
        print("Belum ada laporan barang hilang")

    print("\n---- Laporan Barang Temuan ----")
    ada_temuan = False
    for i in range(len(database_temuan)):
        item = database_temuan[i]
        if item["id_pelapor"] == id_user and item["id_barang"] != "":
            ada_temuan = True
            print(f"[{item['id_barang']}] {item['nama_barang']} ({item['kategori']}, {item['warna']}) | "
                  f"Lokasi: {item['lokasi']} | Waktu: {item['waktu']} | Status: {item['status']}")

    if not ada_temuan:
        print("Belum ada laporan barang temuan")

def cetak_leaderboard(database_user):
    # Menampilkan peringkat user berdasarkan poin (selection sort, tertinggi ke terendah)
    # KAMUS LOKAL
    # database_user : list of dict
    # indeks_aktif : list of int
    # jumlah_user, i, j, indeks_max, poin_j, poin_max, temp : int
    # user : dict
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
        print(f"{i + 1} / {user['nama']} / {user['poin']}")

if __name__ == "__main__":
    main()