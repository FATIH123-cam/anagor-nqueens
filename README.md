# anagor-nqueens
# N-Queens Problem (`anagor-nqueens`)

Repositori ini berisi implementasi dan analisis algoritma untuk menyelesaikan **N-Queens Problem**, salah satu permasalahan klasik dalam ilmu komputer, kombinatorika, dan kecerdasan buatan.

---

## Latar Belakang Masalah

**N-Queens Problem** merupakan pengembangan dari teka-teki catur klasik *Eight Queens Puzzle* yang pertama kali diperkenalkan oleh pemain catur asal Jerman, Max Bezzel, pada tahun 1848. 

Permasalahan ini menanyakan: **Bagaimana cara menempatkan $N$ buah bidak Ratu (*Queen*) pada papan catur berukuran $N \times N$ sedemikian rupa sehingga tidak ada dua Ratu yang saling menyerang?**

Dalam permainan catur, Ratu dapat bergerak secara **horizontal** (baris), **vertikal** (kolom), maupun **diagonal** sejauh mungkin. Oleh karena itu, syarat mutlak konfigurasi yang valid adalah:
1. Tidak boleh ada dua Ratu pada **baris** yang sama.
2. Tidak boleh ada dua Ratu pada **kolom** yang sama.
3. Tidak boleh ada dua Ratu pada **jalur diagonal** yang sama.

> **Catatan:** Solusi valid untuk permasalahan ini ada untuk semua bilangan bulat positif $N$, kecuali untuk $N = 2$ dan $N = 3$.

---

## Cara Menyelesaikan

Karena ruang pencarian (*search space*) tumbuh secara eksponensial seiring bertambahnya nilai $N$ (terdapat $\binom{N^2}{N}$ kemungkinan penempatan), pendekatan *brute-force* murni menjadi sangat tidak efisien. Beberapa metode umum yang digunakan antara lain:

### 1. Backtracking (Runut Balik)
Pendekatan paling populer yang membangun solusi secara bertahap kolom demi kolom (atau baris demi baris):
- Tempatkan satu Ratu di kolom pertama pada baris yang aman.
- Lanjutkan ke kolom berikutnya dan cari baris yang tidak berkonflik dengan Ratu yang sudah ditempatkan sebelumnya.
- Jika tidak ditemukan posisi aman pada kolom saat ini, lakukan **backtrack** (mundur ke kolom sebelumnya) dan pindahkan posisi Ratu sebelumnya ke baris valid berikutnya.
- Ulangi hingga seluruh $N$ Ratu berhasil ditempatkan atau semua kemungkinan telah dieksplorasi.

### 2. Optimasi Pengecekan Konflik (*Hashing / Bitmasking*)
Untuk mempercepat proses pengecekan posisi aman dari $O(N)$ menjadi $O(1)$:
- **Array Penanda:** Gunakan tiga array boolean untuk melacak baris yang terisi, diagonal utama (`baris - kolom`), dan diagonal sekunder (`baris + kolom`).
- **Bitmasking:** Menggunakan operasi bitwise untuk merepresentasikan status kolom dan diagonal sehingga jauh lebih hemat memori dan cepat dieksekusi.

### 3. Pendekatan Heuristik & Metaheuristik (Untuk $N$ Sangat Besar)
Untuk nilai $N$ yang sangat besar (misalnya $N > 1000$), algoritma *backtracking* membutuhkan waktu komputasi yang terlalu lama. Alternatifnya meliputi:
- **Min-Conflicts Algorithm (Local Search):** Menempatkan seluruh Ratu secara acak lalu memindahkannya secara iteratif ke posisi dengan jumlah konflik paling sedikit.
- **Genetic Algorithm / Simulated Annealing:** Menggunakan teknik optimasi stokastik untuk mendekati konfigurasi bebas konflik.

---

## Analisis Kompleksitas

Untuk pendekatan standar menggunakan algoritma **Backtracking**:

| Aspek | Kompleksitas | Keterangan |
| :--- | :---: | :--- |
| **Kompleksitas Waktu** | $O(N!)$ | Pada kolom pertama ada $N$ pilihan, kolom kedua maksimal $N-1$, dan seterusnya (dipangkas secara signifikan oleh *pruning*). |
| **Kompleksitas Ruang** | $O(N^2)$ atau $O(N)$ | $O(N^2)$ jika menyimpan seluruh papan matriks, atau $O(N)$ jika hanya menyimpan posisi indeks baris tiap kolom. |

---

## Contoh Visualisasi Solusi ($N = 4$)

Salah satu konfigurasi valid untuk papan berukuran $4 \times 4$ (di mana `Q` adalah Ratu dan `.` adalah petak kosong):

```text
. Q . .
. . . Q
Q . . .
. . Q .
