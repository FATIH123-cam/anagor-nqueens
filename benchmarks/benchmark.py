"""
Module benchmark.py
Mengukur waktu eksekusi, jumlah node yang dieksplorasi, dan membandingkan
berbagai pendekatan penyelesaian N-Queens Problem (Brute Force, Backtracking, Set-based, Bitmask).
Menghasilkan laporan tabel Markdown, JSON, dan grafik visualisasi.
"""

import os
import sys
import json
import time
import platform
from typing import Dict, Any, List

# Tambahkan root repo ke sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.brute_force import solve_n_queens_brute_force
from src.backtracking import solve_n_queens_backtracking
from src.optimized import solve_n_queens_sets, solve_n_queens_bitmask, count_n_queens_bitmask
from src.utils import KNOWN_SOLUTIONS

try:
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend untuk server/CI
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def measure_execution(func, *args, repeat: int = 3, **kwargs):
    """
    Menjalankan fungsi sebanyak `repeat` kali dan mengembalikan waktu rata-rata
    serta hasil eksekusi pertama.
    """
    times = []
    result = None
    for i in range(repeat):
        t0 = time.perf_counter()
        res = func(*args, **kwargs)
        t1 = time.perf_counter()
        times.append(t1 - t0)
        if i == 0:
            result = res
    avg_time = sum(times) / len(times)
    min_time = min(times)
    return result, avg_time, min_time


def run_comprehensive_benchmark():
    """
    Menjalankan benchmark menyeluruh untuk semua algoritma dengan rentang N yang sesuai.
    """
    results: Dict[str, Any] = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "os": f"{platform.system()} {platform.release()} ({platform.machine()})",
            "processor": platform.processor() or "Apple M3",
            "python_version": platform.python_version()
        },
        "data": []
    }

    print("================================================================================")
    print("               BENCHMARK EKSPERIMENTAL N-QUEENS PROBLEM                         ")
    print(f" OS: {results['metadata']['os']} | CPU: {results['metadata']['processor']}")
    print(f" Python: {results['metadata']['python_version']}")
    print("================================================================================")

    # Rentang N untuk tiap metode
    n_values = list(range(4, 13))

    for n in n_values:
        row: Dict[str, Any] = {"n": n, "known_solutions": KNOWN_SOLUTIONS.get(n, {}).get("total", -1)}
        print(f"\n[+] Menguji N = {n} (Target Solusi: {row['known_solutions']})...")

        # 1. Brute Force Grid (Hanya N <= 6 karena N=7 memakan 823.543 evaluasi)
        if n <= 6:
            repeat = 3 if n <= 5 else 1
            (sols, nodes), avg_t, _ = measure_execution(solve_n_queens_brute_force, n, mode="grid", repeat=repeat)
            row["bf_grid_time"] = avg_t
            row["bf_grid_nodes"] = nodes
            print(f"    - BF Grid        : {avg_t * 1000:10.3f} ms | Nodes: {nodes:10,d}")
        else:
            row["bf_grid_time"] = None
            row["bf_grid_nodes"] = None

        # 2. Brute Force Permutasi (Hanya N <= 8 karena 8! = 40.320, 9! = 362.880)
        if n <= 8:
            repeat = 3 if n <= 7 else 1
            (sols, nodes), avg_t, _ = measure_execution(solve_n_queens_brute_force, n, mode="permutation", repeat=repeat)
            row["bf_perm_time"] = avg_t
            row["bf_perm_nodes"] = nodes
            print(f"    - BF Permutasi   : {avg_t * 1000:10.3f} ms | Nodes: {nodes:10,d}")
        else:
            row["bf_perm_time"] = None
            row["bf_perm_nodes"] = None

        # 3. Classic Backtracking (N <= 12)
        if n <= 12:
            repeat = 5 if n <= 8 else (3 if n <= 10 else 1)
            (sols, nodes), avg_t, _ = measure_execution(solve_n_queens_backtracking, n, repeat=repeat)
            row["bt_classic_time"] = avg_t
            row["bt_classic_nodes"] = nodes
            print(f"    - BT Klasik      : {avg_t * 1000:10.3f} ms | Nodes: {nodes:10,d}")
        else:
            row["bt_classic_time"] = None
            row["bt_classic_nodes"] = None

        # 4. Optimized Set-based (N <= 12)
        if n <= 12:
            repeat = 5 if n <= 8 else (3 if n <= 10 else 1)
            (sols, nodes), avg_t, _ = measure_execution(solve_n_queens_sets, n, repeat=repeat)
            row["opt_sets_time"] = avg_t
            row["opt_sets_nodes"] = nodes
            print(f"    - Opt Set-based  : {avg_t * 1000:10.3f} ms | Nodes: {nodes:10,d}")
        else:
            row["opt_sets_time"] = None
            row["opt_sets_nodes"] = None

        # 5. Optimized Bitmask (Semua N, N=12 sangat cepat)
        repeat = 5 if n <= 9 else (3 if n <= 11 else 1)
        (sols, nodes), avg_t, _ = measure_execution(solve_n_queens_bitmask, n, repeat=repeat)
        row["opt_bitmask_time"] = avg_t
        row["opt_bitmask_nodes"] = nodes
        print(f"    - Opt Bitmask    : {avg_t * 1000:10.3f} ms | Nodes: {nodes:10,d}")

        results["data"].append(row)

    # Simpan hasil ke JSON
    results_dir = os.path.join(BASE_DIR, "results")
    os.makedirs(results_dir, exist_ok=True)
    json_path = os.path.join(results_dir, "benchmark_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[+] Data benchmark tersimpan di: {json_path}")

    # Simpan ke tabel Markdown
    md_path = os.path.join(results_dir, "benchmark_table.md")
    generate_markdown_table(results, md_path)
    print(f"[+] Tabel Markdown tersimpan di: {md_path}")

    # Buat grafik jika matplotlib tersedia
    if HAS_MATPLOTLIB:
        chart_path = os.path.join(results_dir, "benchmark_scaling.png")
        generate_plots(results, chart_path)
        print(f"[+] Grafik visualisasi tersimpan di: {chart_path}")

    return results


def generate_markdown_table(results: Dict[str, Any], output_path: str):
    """
    Membangkitkan tabel perbandingan Markdown dari data benchmark.
    """
    lines = [
        "### Tabel Hasil Pengukuran Empiris N-Queens",
        "",
        f"- **Mesin Uji**: {results['metadata']['processor']} ({results['metadata']['os']})",
        f"- **Runtime**: Python {results['metadata']['python_version']}",
        f"- **Waktu Pengujian**: {results['metadata']['timestamp']}",
        "",
        "| N | Solusi Total | BF Grid (ms) | BF Permutasi (ms) | BT Klasik (ms) | Opt Sets (ms) | Opt Bitmask (ms) | Node BT Klasik | Node Opt Bitmask | Speedup (BT / Bitmask) |",
        "|---|---|---|---|---|---|---|---|---|---|"
    ]

    for row in results["data"]:
        n = row["n"]
        sols = f"{row['known_solutions']:,}"
        bf_g = f"{row['bf_grid_time'] * 1000:.3f}" if row["bf_grid_time"] is not None else "-"
        bf_p = f"{row['bf_perm_time'] * 1000:.3f}" if row["bf_perm_time"] is not None else "-"
        bt_c = f"{row['bt_classic_time'] * 1000:.3f}" if row["bt_classic_time"] is not None else "-"
        opt_s = f"{row['opt_sets_time'] * 1000:.3f}" if row["opt_sets_time"] is not None else "-"
        opt_b = f"{row['opt_bitmask_time'] * 1000:.3f}" if row["opt_bitmask_time"] is not None else "-"

        nodes_bt = f"{row['bt_classic_nodes']:,}" if row["bt_classic_nodes"] is not None else "-"
        nodes_bm = f"{row['opt_bitmask_nodes']:,}" if row["opt_bitmask_nodes"] is not None else "-"

        if row["bt_classic_time"] and row["opt_bitmask_time"] and row["opt_bitmask_time"] > 0:
            speedup = f"{row['bt_classic_time'] / row['opt_bitmask_time']:.1f}x"
        else:
            speedup = "-"

        lines.append(f"| {n} | {sols} | {bf_g} | {bf_p} | {bt_c} | {opt_s} | {opt_b} | {nodes_bt} | {nodes_bm} | {speedup} |")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def generate_plots(results: Dict[str, Any], output_path: str):
    """
    Menghasilkan grafik visualisasi perbandingan waktu dan pertumbuhan node dieksplorasi.
    """
    data = results["data"]
    n_vals = [r["n"] for r in data]

    # Ekstrak metrik
    bt_times = [r["bt_classic_time"] * 1000 if r["bt_classic_time"] is not None else None for r in data]
    sets_times = [r["opt_sets_time"] * 1000 if r["opt_sets_time"] is not None else None for r in data]
    bm_times = [r["opt_bitmask_time"] * 1000 if r["opt_bitmask_time"] is not None else None for r in data]
    bf_perm_times = [r["bf_perm_time"] * 1000 if r["bf_perm_time"] is not None else None for r in data]

    bt_nodes = [r["bt_classic_nodes"] if r["bt_classic_nodes"] is not None else None for r in data]
    bm_nodes = [r["opt_bitmask_nodes"] if r["opt_bitmask_nodes"] is not None else None for r in data]

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Subplot 1: Skala Waktu Logaritmik
    if any(bf_perm_times):
        valid_bf = [(n, t) for n, t in zip(n_vals, bf_perm_times) if t is not None]
        ax1.plot([p[0] for p in valid_bf], [p[1] for p in valid_bf], "o--", color="#d9534f", label="Brute Force (Permutasi)", linewidth=1.5)

    valid_bt = [(n, t) for n, t in zip(n_vals, bt_times) if t is not None]
    ax1.plot([p[0] for p in valid_bt], [p[1] for p in valid_bt], "s-", color="#f0ad4e", label="Backtracking Klasik", linewidth=2)

    valid_sets = [(n, t) for n, t in zip(n_vals, sets_times) if t is not None]
    ax1.plot([p[0] for p in valid_sets], [p[1] for p in valid_sets], "^-", color="#0275d8", label="Optimasi Sets", linewidth=2)

    valid_bm = [(n, t) for n, t in zip(n_vals, bm_times) if t is not None]
    ax1.plot([p[0] for p in valid_bm], [p[1] for p in valid_bm], "D-", color="#5cb85c", label="Optimasi Bitmask", linewidth=2.2)

    ax1.set_yscale("log")
    ax1.set_xlabel("Ukuran Papan (N)", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Waktu Eksekusi (ms) [Skala Logaritmik]", fontsize=11, fontweight="bold")
    ax1.set_title("Pertumbuhan Waktu Eksekusi vs. N", fontsize=13, fontweight="bold")
    ax1.legend(loc="upper left", frameon=True)
    ax1.grid(True, which="both", ls=":", alpha=0.6)

    # Subplot 2: Perbandingan Node Pohon Ruang Status
    valid_nodes_bt = [(n, nd) for n, nd in zip(n_vals, bt_nodes) if nd is not None]
    ax2.plot([p[0] for p in valid_nodes_bt], [p[1] for p in valid_nodes_bt], "s-", color="#f0ad4e", label="Node Backtracking Klasik", linewidth=2)

    valid_nodes_bm = [(n, nd) for n, nd in zip(n_vals, bm_nodes) if nd is not None]
    ax2.plot([p[0] for p in valid_nodes_bm], [p[1] for p in valid_nodes_bm], "D-", color="#5cb85c", label="Node Optimasi Bitmask", linewidth=2)

    ax2.set_yscale("log")
    ax2.set_xlabel("Ukuran Papan (N)", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Node Pohon Status Dikunjungi [Skala Log]", fontsize=11, fontweight="bold")
    ax2.set_title("Perbandingan Eksplorasi Node (State-Space Tree)", fontsize=13, fontweight="bold")
    ax2.legend(loc="upper left", frameon=True)
    ax2.grid(True, which="both", ls=":", alpha=0.6)

    plt.suptitle("Analisis Kinerja Algoritma N-Queens Problem", fontsize=15, fontweight="bold", y=0.98)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


if __name__ == "__main__":
    run_comprehensive_benchmark()
