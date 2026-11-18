"""
Module utils.py
Fungsi bantu untuk validasi papan, format tampilan ASCII, dan konstanta jumlah solusi N-Queens.
"""

from typing import List, Tuple, Dict

# Referensi OEIS A000170 (Total Solusi) dan A002562 (Solusi Unik / Fundamental)
KNOWN_SOLUTIONS: Dict[int, Dict[str, int]] = {
    1: {"total": 1, "unique": 1},
    2: {"total": 0, "unique": 0},
    3: {"total": 0, "unique": 0},
    4: {"total": 2, "unique": 1},
    5: {"total": 10, "unique": 2},
    6: {"total": 4, "unique": 1},
    7: {"total": 40, "unique": 6},
    8: {"total": 92, "unique": 12},
    9: {"total": 352, "unique": 46},
    10: {"total": 724, "unique": 92},
    11: {"total": 2680, "unique": 341},
    12: {"total": 14200, "unique": 1787},
    13: {"total": 73712, "unique": 9233},
    14: {"total": 365596, "unique": 45752},
}


def is_valid_board(solution: List[int]) -> bool:
    """
    Melakukan validasi independen apakah konfigurasi ratu valid:
    - Tidak ada ratu di kolom yang sama.
    - Tidak ada ratu di diagonal yang sama (utama maupun sekunder).
    
    Argumen:
        solution: List indeks kolom untuk setiap baris, berukuran N.
        
    Return:
        True jika posisi valid (tidak saling serang), False jika konflik.
    """
    n = len(solution)
    if n == 0:
        return False

    # Validasi rentang kolom dan keunikan kolom
    if any(c < 0 or c >= n for c in solution):
        return False
    if len(set(solution)) != n:
        return False

    # Validasi diagonal
    for r1 in range(n):
        c1 = solution[r1]
        for r2 in range(r1 + 1, n):
            c2 = solution[r2]
            # |r1 - r2| == |c1 - c2| menandakan berada pada diagonal yang sama
            if abs(r1 - r2) == abs(c1 - c2):
                return False

    return True


def format_board_ascii(solution: List[int]) -> str:
    """
    Mengonversi representasi solusi ratu ke bentuk visual papan catur ASCII.
    
    Argumen:
        solution: List indeks kolom untuk setiap baris.
        
    Return:
        String representasi papan catur dengan border dan koordinat.
    """
    n = len(solution)
    col_headers = "   " + " ".join([f"{c}" for c in range(n)])
    border = "  +" + "-" * (2 * n + 1) + "+"
    lines = [col_headers, border]

    for r in range(n):
        row_str = []
        for c in range(n):
            if solution[r] == c:
                row_str.append("Q")
            else:
                row_str.append(".")
        lines.append(f"{r:2d}| {' '.join(row_str)} |")

    lines.append(border)
    return "\n".join(lines)


def print_board(solution: List[int]) -> None:
    """
    Mencetak papan catur ke standard output.
    """
    print(format_board_ascii(solution))
