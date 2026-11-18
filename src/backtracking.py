"""
Module backtracking.py
Implementasi algoritma Backtracking klasik (Depth-First Search dengan pemangkasan)
untuk menyelesaikan N-Queens Problem.
"""

import time
from typing import List, Tuple
from src.utils import print_board


def is_safe(board: List[int], row: int, col: int) -> bool:
    """
    Memeriksa apakah aman menempatkan ratu pada koordinat (row, col)
    terhadap ratu-ratu yang sudah ditempatkan pada baris 0 s.d. row - 1.
    Kompleksitas: O(row) = O(N).
    
    Argumen:
        board: List panjang N berisi kolom ratu tiap baris.
        row: Baris kandidat penempatan.
        col: Kolom kandidat penempatan.
        
    Return:
        True jika tidak ada konflik, False jika saling serang.
    """
    for prev_row in range(row):
        prev_col = board[prev_row]
        # Konflik kolom
        if prev_col == col:
            return False
        # Konflik diagonal: |prev_row - row| == |prev_col - col|
        if abs(prev_row - row) == abs(prev_col - col):
            return False
    return True


def solve_n_queens_backtracking(n: int, first_only: bool = False) -> Tuple[List[List[int]], int]:
    """
    Mencari solusi N-Queens menggunakan algoritma Backtracking standar.
    
    Argumen:
        n: Ukuran papan catur (N x N) dan jumlah ratu.
        first_only: Jika True, berhenti setelah menemukan solusi pertama.
        
    Return:
        (solutions, nodes_explored):
            - solutions: List dari konfigurasi penempatan ratu yang valid.
            - nodes_explored: Jumlah node dalam pohon ruang status yang dikunjungi.
    """
    if n <= 0:
        return [], 0

    solutions: List[List[int]] = []
    board: List[int] = [-1] * n
    nodes_explored = 0

    def backtrack(row: int) -> bool:
        nonlocal nodes_explored
        nodes_explored += 1

        # Basis: jika semua baris sudah terisi ratu
        if row == n:
            solutions.append(list(board))
            return True if first_only else False

        # Langkah induktif: coba tempatkan ratu pada setiap kolom di baris saat ini
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                found = backtrack(row + 1)
                board[row] = -1  # Reset saat backtrack

                if found and first_only:
                    return True

        return False

    backtrack(0)
    return solutions, nodes_explored


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Penyelesai N-Queens (Klasik Backtracking)")
    parser.add_argument("-n", type=int, default=8, help="Ukuran papan N (default: 8)")
    parser.add_argument("--first-only", action="store_true", help="Berhenti setelah solusi pertama ditemukan")
    parser.add_argument("--print-first", action="store_true", help="Cetak solusi pertama ke terminal")
    parser.add_argument("--print-all", action="store_true", help="Cetak semua solusi ke terminal")
    args = parser.parse_args()

    print(f"=== N-Queens Classic Backtracking (N={args.n}) ===")
    start_time = time.perf_counter()
    sols, nodes = solve_n_queens_backtracking(args.n, first_only=args.first_only)
    elapsed = time.perf_counter() - start_time

    print(f"Jumlah solusi ditemukan : {len(sols)}")
    print(f"Node dieksplorasi       : {nodes:,}")
    print(f"Waktu eksekusi          : {elapsed:.6f} detik")

    if (args.print_first or args.print_all) and sols:
        limit = len(sols) if args.print_all else 1
        for idx in range(limit):
            print(f"\nSolusi #{idx + 1}:")
            print_board(sols[idx])
