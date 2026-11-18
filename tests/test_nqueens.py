"""
Unit testing untuk solusi N-Queens Problem.
Menjalankan pengujian kebenaran, konsistensi antar algoritma, dan validasi papan.
"""

import unittest
from src.utils import is_valid_board, KNOWN_SOLUTIONS
from src.backtracking import solve_n_queens_backtracking
from src.optimized import solve_n_queens_sets, solve_n_queens_bitmask, count_n_queens_bitmask
from src.brute_force import solve_n_queens_brute_force


class TestNQueens(unittest.TestCase):

    def test_known_solution_counts_backtracking(self):
        """Memverifikasi jumlah solusi backtracking untuk N=1..10 terhadap OEIS A000170."""
        for n in range(1, 11):
            expected = KNOWN_SOLUTIONS[n]["total"]
            sols, _ = solve_n_queens_backtracking(n)
            self.assertEqual(len(sols), expected, f"Gagal pada N={n} untuk backtracking klasik")

    def test_known_solution_counts_bitmask(self):
        """Memverifikasi jumlah solusi bitmasking untuk N=1..10 terhadap OEIS A000170."""
        for n in range(1, 11):
            expected = KNOWN_SOLUTIONS[n]["total"]
            sols, _ = solve_n_queens_bitmask(n)
            self.assertEqual(len(sols), expected, f"Gagal pada N={n} untuk bitmasking")

    def test_known_solution_counts_sets(self):
        """Memverifikasi jumlah solusi set-based untuk N=1..10 terhadap OEIS A000170."""
        for n in range(1, 11):
            expected = KNOWN_SOLUTIONS[n]["total"]
            sols, _ = solve_n_queens_sets(n)
            self.assertEqual(len(sols), expected, f"Gagal pada N={n} untuk set-based")

    def test_count_only_bitmask(self):
        """Memverifikasi count_n_queens_bitmask cepat hingga N=11."""
        for n in range(1, 12):
            expected = KNOWN_SOLUTIONS[n]["total"]
            count, _ = count_n_queens_bitmask(n)
            self.assertEqual(count, expected, f"Gagal pada count_only N={n}")

    def test_solution_validity(self):
        """Memastikan semua solusi yang dihasilkan oleh algoritma benar-benar valid."""
        for n in [4, 5, 6, 7, 8]:
            sols, _ = solve_n_queens_bitmask(n)
            for sol in sols:
                self.assertTrue(is_valid_board(sol), f"Solusi tidak valid terdeteksi pada N={n}: {sol}")

    def test_algorithm_equivalence(self):
        """Memastikan backtracking klasik, set-based, dan bitmask menghasilkan himpunan solusi identik."""
        for n in [4, 5, 6, 7]:
            sols_bt, _ = solve_n_queens_backtracking(n)
            sols_set, _ = solve_n_queens_sets(n)
            sols_bm, _ = solve_n_queens_bitmask(n)

            set_bt = {tuple(s) for s in sols_bt}
            set_set = {tuple(s) for s in sols_set}
            set_bm = {tuple(s) for s in sols_bm}

            self.assertEqual(set_bt, set_set, f"Perbedaan hasil antara BT dan Set pada N={n}")
            self.assertEqual(set_bt, set_bm, f"Perbedaan hasil antara BT dan Bitmask pada N={n}")

    def test_brute_force_equivalence(self):
        """Memastikan Brute Force (Grid & Permutasi) menghasilkan solusi identik untuk N=1..5."""
        for n in [1, 2, 3, 4, 5]:
            sols_grid, _ = solve_n_queens_brute_force(n, mode="grid")
            sols_perm, _ = solve_n_queens_brute_force(n, mode="permutation")
            sols_bt, _ = solve_n_queens_backtracking(n)

            self.assertEqual({tuple(s) for s in sols_grid}, {tuple(s) for s in sols_bt})
            self.assertEqual({tuple(s) for s in sols_perm}, {tuple(s) for s in sols_bt})

    def test_validator_detects_conflicts(self):
        """Menguji fungsi validator is_valid_board mendeteksi konflik dengan benar."""
        # Konflik baris/kolom sama
        self.assertFalse(is_valid_board([0, 0, 1, 2]))
        # Konflik diagonal utama
        self.assertFalse(is_valid_board([0, 1, 2, 3]))
        # Konflik diagonal sekunder
        self.assertFalse(is_valid_board([3, 2, 1, 0]))
        # Solusi 4-Queens yang valid: [1, 3, 0, 2]
        self.assertTrue(is_valid_board([1, 3, 0, 2]))
        # Solusi 8-Queens yang valid: [0, 4, 7, 5, 2, 6, 1, 3]
        self.assertTrue(is_valid_board([0, 4, 7, 5, 2, 6, 1, 3]))

    def test_first_only_mode(self):
        """Memastikan mode first_only mengembalikan tepat satu solusi jika ada."""
        sols, _ = solve_n_queens_backtracking(8, first_only=True)
        self.assertEqual(len(sols), 1)
        self.assertTrue(is_valid_board(sols[0]))

    def test_edge_cases(self):
        """Memastikan penanganan input batas (edge case) seperti N=0, N negatif, dan N=1..3."""
        sols, nodes = solve_n_queens_backtracking(0)
        self.assertEqual(sols, [])
        self.assertEqual(nodes, 0)

        sols, nodes = solve_n_queens_backtracking(-1)
        self.assertEqual(sols, [])
        self.assertEqual(nodes, 0)

        sols1, _ = solve_n_queens_backtracking(1)
        self.assertEqual(sols1, [[0]])

        sols2, _ = solve_n_queens_backtracking(2)
        self.assertEqual(sols2, [])

        sols3, _ = solve_n_queens_backtracking(3)
        self.assertEqual(sols3, [])


if __name__ == "__main__":
    unittest.main()
