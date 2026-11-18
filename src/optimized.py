"""
Module optimized.py
Implementasi N-Queens dengan optimasi:
1. Set-based tracking: O(1) pengecekan konflik kolom dan diagonal.
2. Bitmasking: representasi biner dan manipulasi bitwise untuk performa maksimum.
"""

import time
from typing import List, Tuple
from src.utils import print_board


def solve_n_queens_sets(n: int, first_only: bool = False) -> Tuple[List[List[int]], int]:
    """
    Menyelesaikan N-Queens menggunakan tracking Himpunan (Set / Lookup Array)
    untuk kolom, diagonal utama (row - col), dan diagonal sekunder (row + col).
    Pengecekan konflik menjadi O(1) rata-rata.
    
    Argumen:
        n: Ukuran papan catur (N x N) dan jumlah ratu.
        first_only: Berhenti saat solusi pertama ditemukan.
        
    Return:
        (solutions, nodes_explored)
    """
    if n <= 0:
        return [], 0

    solutions: List[List[int]] = []
    board: List[int] = [-1] * n
    nodes_explored = 0

    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    def backtrack(row: int) -> bool:
        nonlocal nodes_explored
        nodes_explored += 1

        if row == n:
            solutions.append(list(board))
            return True if first_only else False

        for col in range(n):
            d1 = row - col
            d2 = row + col

            # O(1) konflik check
            if col not in cols and d1 not in diag1 and d2 not in diag2:
                # Place queen
                board[row] = col
                cols.add(col)
                diag1.add(d1)
                diag2.add(d2)

                found = backtrack(row + 1)

                # Backtrack / Unplace
                board[row] = -1
                cols.remove(col)
                diag1.remove(d1)
                diag2.remove(d2)

                if found and first_only:
                    return True

        return False

    backtrack(0)
    return solutions, nodes_explored


def solve_n_queens_bitmask(n: int, first_only: bool = False) -> Tuple[List[List[int]], int]:
    """
    Menyelesaikan N-Queens menggunakan manipulasi Bitwise (Bitmasking).
    Setiap status kolom dan diagonal direpresentasikan dalam integer N-bit.
    
    Argumen:
        n: Ukuran papan catur (N x N) dan jumlah ratu.
        first_only: Berhenti saat solusi pertama ditemukan.
        
    Return:
        (solutions, nodes_explored)
    """
    if n <= 0:
        return [], 0

    solutions: List[List[int]] = []
    board: List[int] = [-1] * n
    nodes_explored = 0
    all_ones = (1 << n) - 1  # Mask dengan N bit bernilai 1

    def backtrack(row: int, cols_mask: int, diag1_mask: int, diag2_mask: int) -> bool:
        nonlocal nodes_explored
        nodes_explored += 1

        if row == n:
            solutions.append(list(board))
            return True if first_only else False

        # Bit 1 merepresentasikan kolom yang aman ditempati
        avail = ~(cols_mask | diag1_mask | diag2_mask) & all_ones

        while avail:
            # Ambil bit 1 paling kanan (Lowest Set Bit)
            bit = avail & -avail
            # Hapus bit tersebut dari kandidat
            avail &= avail - 1

            # Hitung indeks kolom dari nilai bit (misal: 0b0001 -> 0, 0b0010 -> 1)
            col = (bit).bit_length() - 1
            board[row] = col

            # Geser diagonal utama ke kiri dan diagonal sekunder ke kanan untuk baris berikutnya
            found = backtrack(
                row + 1,
                cols_mask | bit,
                ((diag1_mask | bit) << 1) & all_ones,
                (diag2_mask | bit) >> 1
            )

            board[row] = -1

            if found and first_only:
                return True

        return False

    backtrack(0, 0, 0, 0)
    return solutions, nodes_explored


def count_n_queens_bitmask(n: int) -> Tuple[int, int]:
    """
    Varian penghitungan cepat (Count Only) berbasis Bitmasking.
    Dioptimasi tanpa overhead instansiasi objek papan untuk benchmark N besar.
    
    Return:
        (total_solutions, nodes_explored)
    """
    if n <= 0:
        return 0, 0

    total_solutions = 0
    nodes_explored = 0
    all_ones = (1 << n) - 1

    def backtrack(row: int, cols_mask: int, diag1_mask: int, diag2_mask: int):
        nonlocal total_solutions, nodes_explored
        nodes_explored += 1

        if row == n:
            total_solutions += 1
            return

        avail = ~(cols_mask | diag1_mask | diag2_mask) & all_ones
        while avail:
            bit = avail & -avail
            avail &= avail - 1
            backtrack(
                row + 1,
                cols_mask | bit,
                ((diag1_mask | bit) << 1) & all_ones,
                (diag2_mask | bit) >> 1
            )

    backtrack(0, 0, 0, 0)
    return total_solutions, nodes_explored


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Penyelesai N-Queens (Optimasi Set & Bitmask)")
    parser.add_argument("-n", type=int, default=8, help="Ukuran papan N (default: 8)")
    parser.add_argument("--method", choices=["bitmask", "set"], default="bitmask",
                        help="Metode optimasi yang digunakan")
    parser.add_argument("--first-only", action="store_true", help="Berhenti setelah solusi pertama ditemukan")
    parser.add_argument("--print-first", action="store_true", help="Cetak solusi pertama ke terminal")
    parser.add_argument("--count-only", action="store_true", help="Hanya hitung total solusi (khusus bitmask cepat)")
    args = parser.parse_args()

    print(f"=== N-Queens Optimized (Metode: {args.method}, N={args.n}) ===")
    start_time = time.perf_counter()

    if args.count_only and args.method == "bitmask":
        count, nodes = count_n_queens_bitmask(args.n)
        sols = []
    elif args.method == "bitmask":
        sols, nodes = solve_n_queens_bitmask(args.n, first_only=args.first_only)
        count = len(sols)
    else:
        sols, nodes = solve_n_queens_sets(args.n, first_only=args.first_only)
        count = len(sols)

    elapsed = time.perf_counter() - start_time

    print(f"Jumlah solusi ditemukan : {count}")
    print(f"Node dieksplorasi       : {nodes:,}")
    print(f"Waktu eksekusi          : {elapsed:.6f} detik")

    if args.print_first and sols:
        print("\nSolusi pertama:")
        print_board(sols[0])
