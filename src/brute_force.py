"""
Module brute_force.py
Implementasi algoritma Brute Force untuk N-Queens Problem sebagai pembanding (baseline).
Mendukung mode Grid (O(N^N)) dan Permutasi (O(N!)).
"""

import itertools
import time
from typing import List, Tuple
from src.utils import is_valid_board, print_board


def solve_n_queens_brute_force(n: int, mode: str = "grid") -> Tuple[List[List[int]], int]:
    """
    Menyelesaikan N-Queens dengan pendekatan Brute Force tanpa pemangkasan (pruning).
    
    Argumen:
        n: Ukuran papan catur (N x N) dan jumlah ratu.
        mode: 
            - "grid": Membangkitkan seluruh N^N penempatan (1 ratu per baris pada kolom 0..N-1).
            - "permutation": Membangkitkan seluruh N! permutasi kolom tanpa konflik baris & kolom.
            
    Return:
        (solutions, nodes_explored):
            - solutions: List dari seluruh solusi valid.
            - nodes_explored: Total konfigurasi/node yang dievaluasi.
    """
    if n <= 0:
        return [], 0

    solutions: List[List[int]] = []
    nodes_explored = 0

    if mode == "grid":
        # Membangkitkan kombinasi Cartesian product: N^N kemungkinan
        # Setiap elemen adalah tuple panjang N, di mana indeks adalah baris dan nilai adalah kolom
        for candidate in itertools.product(range(n), repeat=n):
            nodes_explored += 1
            board = list(candidate)
            if is_valid_board(board):
                solutions.append(board)

    elif mode == "permutation":
        # Membangkitkan seluruh permutasi: N! kemungkinan
        # Sudah menjamin tidak ada konflik baris maupun kolom, hanya perlu uji diagonal
        for candidate in itertools.permutations(range(n)):
            nodes_explored += 1
            board = list(candidate)
            # Evaluasi diagonal saja
            is_diag_valid = True
            for r1 in range(n):
                for r2 in range(r1 + 1, n):
                    if abs(r1 - r2) == abs(board[r1] - board[r2]):
                        is_diag_valid = False
                        break
                if not is_diag_valid:
                    break
            if is_diag_valid:
                solutions.append(board)
    else:
        raise ValueError(f"Mode '{mode}' tidak dikenal. Pilih 'grid' atau 'permutation'.")

    return solutions, nodes_explored


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Penyelesai N-Queens (Brute Force)")
    parser.add_argument("-n", type=int, default=4, help="Ukuran papan N (default: 4)")
    parser.add_argument("--mode", choices=["grid", "permutation"], default="grid",
                        help="Mode brute force: 'grid' (N^N) atau 'permutation' (N!)")
    parser.add_argument("--print-first", action="store_true", help="Cetak solusi pertama")
    args = parser.parse_args()

    print(f"=== N-Queens Brute Force (Mode: {args.mode}, N={args.n}) ===")
    start_time = time.perf_counter()
    sols, nodes = solve_n_queens_brute_force(args.n, mode=args.mode)
    elapsed = time.perf_counter() - start_time

    print(f"Jumlah solusi ditemukan : {len(sols)}")
    print(f"Node dieksplorasi       : {nodes:,}")
    print(f"Waktu eksekusi          : {elapsed:.6f} detik")

    if args.print_first and sols:
        print("\nSolusi pertama:")
        print_board(sols[0])
