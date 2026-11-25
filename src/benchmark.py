"""Empirically measure the baseline and dynamic-programming book-stack algorithms."""

import os
import random
from time import perf_counter

import matplotlib.pyplot as plt
import pandas as pd
from methods import baselineEldritchBookStacking, eldritchBookStacking


def generate_test_data(size, max_L):
    """Generate a list of *size* random Eldritch energy values from 1 to max_L."""
    # Validate inputs
    if size < 0:
        raise ValueError("size must be non-negative")
    if max_L < 1:
        raise ValueError("max_L must be at least 1")
    # Generate random integers in the range [1, max_L]
    return [random.randint(1, max_L) for _ in range(size)]


def benchmark_algo_multi(algo, test_cases, repeat=1):
    """Time an algorithm repeatedly for each test case."""
    # Validate inputs
    if repeat < 1:
        raise ValueError("repeat must be at least 1")

    times = []
    # Loop through each test case and repeat the timing
    for energies in test_cases:
        for _ in range(repeat):
            start = perf_counter()
            algo(energies)
            elapsed = perf_counter() - start
            times.append((len(energies), elapsed))
    # Return the list of timing results
    return times


def run_benchmarks():
    """Run benchmarks for both the baseline and dynamic programming algorithms."""
    # Define the input sizes and maximum energy value for the test cases
    input_sizes = [5, 7, 8, 9, 10, 50, 100, 500, 1000, 5000, 10000, 20000, 30000, 40000, 50000]
    max_energy = 100

    # Seed the random number generator for reproducibility and generate test cases
    random.seed(42)
    test_cases = [generate_test_data(size, max_energy) for size in input_sizes]

    # The brute-force baseline is Theta(n * 2^n), so benchmark it only at practical sizes.
    baseline_test_cases = [case for case in test_cases if len(case) <= 10]

    # Benchmark the baseline algorithm
    print("Running Baseline algorithm...")
    baseline_times = benchmark_algo_multi(
        baselineEldritchBookStacking, baseline_test_cases, repeat=5
    )

    # Benchmark the dynamic programming algorithm
    print("Running Dynamic Programming algorithm...")
    dynamic_times = benchmark_algo_multi(
        eldritchBookStacking, test_cases, repeat=5
    )

    # Create DataFrames for the results
    df_baseline = pd.DataFrame(baseline_times, columns=["Books", "Time(seconds)"])
    df_baseline["Algorithm"] = "Baseline"

    df_dynamic = pd.DataFrame(dynamic_times, columns=["Books", "Time(seconds)"])
    df_dynamic["Algorithm"] = "Dynamic Programming"

    df_all = pd.concat([df_baseline, df_dynamic], ignore_index=True)

    # Save the results to a CSV file in the assets directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(project_root, "assets", "empirical_results.csv")
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    df_all.to_csv(target_path, index=False)

    # Print the results to the console
    print("\nAll Recorded Times:")
    print(df_all)

    # Return the DataFrame for further analysis if needed
    return df_all


def create_visualization(benchmark_results, output_file="results.png"):
    """Plot average runtimes from the DataFrame returned by run_benchmarks."""
    required_columns = {"Books", "Time(seconds)", "Algorithm"}
    if not required_columns.issubset(benchmark_results.columns):
        raise ValueError(
            "benchmark_results must contain Books, Time(seconds), and Algorithm columns."
        )
    if benchmark_results.empty:
        raise ValueError("benchmark_results must not be empty.")

    averages = benchmark_results.groupby(
        ["Algorithm", "Books"], as_index=False
    )["Time(seconds)"].mean()

    figure, axes = plt.subplots(1, 2, figsize=(13, 5))
    for algorithm, results in averages.groupby("Algorithm"):
        results = results.sort_values("Books")
        for axis in axes:
            axis.plot(
                results["Books"],
                results["Time(seconds)"],
                marker="o",
                label=algorithm,
            )

    axes[0].set_title("Runtime Comparison: Linear Scale")
    axes[0].set_xlabel("Number of Books (N)")
    axes[0].set_ylabel("Average Runtime (seconds)")
    axes[0].grid(True, linestyle="--", alpha=0.6)
    axes[0].legend()

    axes[1].set_yscale("log")
    axes[1].set_title("Runtime Comparison: Logarithmic Scale")
    axes[1].set_xlabel("Number of Books (N)")
    axes[1].set_ylabel("Average Runtime (seconds)")
    axes[1].grid(True, linestyle="--", alpha=0.6)
    axes[1].legend()

    figure.suptitle("Baseline vs. Dynamic Programming Book-Stack Algorithms")
    figure.tight_layout()
    figure.savefig(output_file, dpi=300)
    plt.close(figure)


if __name__ == "__main__":
    """Run the benchmarks when this script is executed directly."""
    results = run_benchmarks()
    create_visualization(results, output_file="benchmark_results.png")