"""Implements baseline and proposed solutions for the Eldritch Book Stacking problem."""


def generateAllsequences(E):
    """
    Generates all possible subsequences of book energies
    while preserving their original order.
    """
    if len(E) == 0:
        return [[]]

    first_element = E[0]
    remaining_elements = E[1:]

    # Generate subsequences from the remaining books
    sub_problem_solutions = generateAllsequences(remaining_elements)

    all_combined = []

    for sub_solution in sub_problem_solutions:
        # Exclude the first element
        all_combined.append(sub_solution)

        # Include the first element
        all_combined.append([first_element] + sub_solution)

    return all_combined


def baselineEldritchBookStacking(E):
    """
    Baseline Algorithm: O(n * 2^n) time complexity.
    Generates all possible subsequences and finds the
    longest one with strictly increasing energy.
    """
    max_height = 0
    best_stack = []

    # Generate all possible subsequences
    all_subsets = generateAllsequences(E)

    for subset in all_subsets:
        is_valid = True

        # Check if the subsequence is strictly increasing
        for i in range(len(subset) - 1):
            if subset[i] >= subset[i + 1]:
                is_valid = False
                break

        # Track the longest valid stack
        if is_valid:
            if len(subset) > max_height:
                max_height = len(subset)
                best_stack = subset

    return max_height, best_stack


def eldritchBookStacking(E):
    """
    Proposed Algorithm: O(n^2) time complexity.
    Uses dynamic programming to find the longest
    strictly increasing subsequence of book energies.
    """
    n = len(E)

    if n == 0:
        return 0, []

    # Each book can form a stack of height 1
    dp = [1] * n
    previous = [-1] * n

    # Find the longest valid stack ending at each position
    for i in range(n):
        for j in range(i):
            if E[j] < E[i]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    previous[i] = j

    # Find the height and ending position of the tallest stack
    max_height = max(dp)
    max_index = dp.index(max_height)

    # Reconstruct the selected books
    stack = []

    while max_index != -1:
        stack.append(E[max_index])
        max_index = previous[max_index]

    stack.reverse()

    return max_height, stack