# Dokumentasi Visual & Diagram Alur N-Queens Problem

Dokumen ini memuat ilustrasi visual, diagram alur algoritma, pohon ruang status (state-space tree), dan formulasi matematis pemetaan papan pada N-Queens Problem.

---

## 1. Pohon Ruang Status (State-Space Tree) untuk N = 4

Pada masalah 4-Queens, setiap level pada pohon merepresentasikan baris papan ($r = 0, 1, 2, 3$), dan setiap cabang merepresentasikan pilihan kolom ($c = 0, 1, 2, 3$).

Pruning (pemangkasan) terjadi seketika saat ratu baru menyerang ratu yang sudah terpasang di baris sebelumnya.

```
                           Root (Level 0: Baris 0)
          /                 |                 \                 \
      c=0                 c=1                 c=2                 c=3
     [0]                 [1]                 [2]                 [3]
   (Baris 1)           (Baris 1)           (Baris 1)           (Baris 1)
  /  |  \  \          /  |  \  \          /  |  \  \          /  |  \  \
 0   1   2  3        0   1   2  3        0   1   2  3        0   1   2  3
 x   x  [0,2] x      x   x   x [1,3]    [2,0] x  x   x       x  [3,1] x  x
        / | \ \                / | \ \   / | \ \                / | \ \
     Semua konflik          [1,3,0]...  ...[2,0,3]           Semua konflik
      (Pruning!)               |             |                (Pruning!)
                            (Baris 3)     (Baris 3)
                               |             |
                           [1,3,0,2]     [2,0,3,1]
                           (SOLUSI 1)    (SOLUSI 2)
```

### Penjelasan Pemangkasan (Pruning) pada N=4:
1. Jika $Q_0$ ditempatkan di $(0, 0)$:
   - Baris 1: Kolom 0 (konflik kolom), Kolom 1 (konflik diagonal). Pilihan kolom 2 aman: $[0, 2]$.
   - Baris 2: Dari $[0, 2]$, kolom 0, 1, 2, 3 semuanya diserang oleh $(0,0)$ atau $(1,2)$. **Cabang mati (pruned)**.
   - Pilihan kolom 3 di baris 1: $[0, 3]$. Di baris 2 hanya kolom 1 yang aman $[0, 3, 1]$. Di baris 3, semua kolom diserang. **Cabang mati (pruned)**.
2. Jika $Q_0$ ditempatkan di $(0, 1)$:
   - Baris 1: Kolom 3 aman: $[1, 3]$.
   - Baris 2: Kolom 0 aman: $[1, 3, 0]$.
   - Baris 3: Kolom 2 aman: $[1, 3, 0, 2]$ $\to$ **SOLUSI 1 VALID!**
3. Jika $Q_0$ ditempatkan di $(0, 2)$:
   - Baris 1: Kolom 0 aman: $[2, 0]$.
   - Baris 2: Kolom 3 aman: $[2, 0, 3]$.
   - Baris 3: Kolom 1 aman: $[2, 0, 3, 1]$ $\to$ **SOLUSI 2 VALID!**

---

## 2. Diagram Alur Algoritma Backtracking (Flowchart)

```mermaid
flowchart TD
    Start([Mulai: solve_backtrack row=0]) --> CheckRow{row == N ?}
    CheckRow -- Ya --> SaveSol[Simpan Solusi Papan]
    SaveSol --> BacktrackUp[Kembali / Backtrack ke Baris Sebelumnya]
    CheckRow -- Tidak --> InitCol[Mulai col = 0]
    
    InitCol --> CheckColBound{col < N ?}
    CheckColBound -- Tidak --> BacktrackUp
    CheckColBound -- Ya --> IsSafe{is_safe row, col ?}
    
    IsSafe -- Tidak (Pruning!) --> NextCol[col = col + 1]
    NextCol --> CheckColBound
    
    IsSafe -- Ya --> PlaceQueen[board[row] = col]
    PlaceQueen --> Recurse[Panggil solve_backtrack row + 1]
    Recurse --> UnplaceQueen[board[row] = -1 / Reset]
    UnplaceQueen --> NextCol
```

---

## 3. Sistem Koordinat dan Formula Diagonal

Sebuah papan catur berukuran $N \times N$ memiliki:
- $N$ baris berindeks $r \in [0, N-1]$
- $N$ kolom berindeks $c \in [0, N-1]$
- $2N - 1$ diagonal utama ($\searrow$)
- $2N - 1$ diagonal sekunder ($\nearrow$)

### Matriks Rumus Diagonal:
1. **Diagonal Utama ($\searrow$)**:
   $$\text{diag}_1 = r - c$$
   Rentang nilai: $-(N-1) \le r - c \le N-1$.
   Agar menjadi indeks array non-negatif:
   $$\text{index}_{\text{diag}1} = r - c + (N - 1) \in [0, 2N-2]$$

2. **Diagonal Sekunder ($\nearrow$)**:
   $$\text{diag}_2 = r + c$$
   Rentang nilai: $0 \le r + c \le 2N - 2$.
   Langsung dapat digunakan sebagai indeks array:
   $$\text{index}_{\text{diag}2} = r + c \in [0, 2N-2]$$

---

## 4. Representasi dan Operasi Bitmasking

Dalam varian Bitmasking:
- Variabel integer merepresentasikan vektor boolean berukuran $N$ bit.
- Bit ke-$k$ bernilai `1` menandakan kolom/diagonal tersebut sedang terancam/terisi.

| Komponen | Makna Bitwise | Pembaruan saat Rekursi (`row` $\to$ `row + 1`) |
|---|---|---|
| `cols` | Kolom terisi | `cols | bit` |
| `diag1` | Diagonal utama terancam | `((diag1 | bit) << 1) & mask` |
| `diag2` | Diagonal sekunder terancam | `(diag2 | bit) >> 1` |
| `avail` | Posisi aman untuk ditempati | `~(cols | diag1 | diag2) & mask` |
| `bit` | Ratu ditaruh di kolom aman | `avail & -avail` (ambil lowest set bit) |
