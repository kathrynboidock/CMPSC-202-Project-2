"""Empirically measure the baseline and dynamic-programming book-stack algorithms."""

import os
import random
from time import perf_counter

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


if __name__ == "__main__":
    """Run the benchmarks when this script is executed directly."""
    run_benchmarks()