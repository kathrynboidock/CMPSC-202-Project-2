# Planning and Analysis

## Problem Formulation

## Baseline Solution

## Algorithmic Strategy

To efficiently determine the tallest possible stack of books, we propose using a dynamic programming approach based on the Longest Increasing Subsequence (LIS) problem. The main idea is to build solutions to smaller subproblems by determining the maximum number of books that can form a valid stack ending at each position in the original sequence.

We begin by creating an array, `dp`, where each position is initialized to 1, since every book can form a valid stack by itself. We then iterate through the sequence of books, comparing each book's Eldritch energy with the energies of all preceding books. If a previous book has strictly lower energy, the current book can be added to the stack ending at that previous book. We update the current position in `dp` if this produces a taller stack. After examining all books, the maximum value stored in `dp` represents the height of the tallest possible stable stack. To identify the actual sequence of books, we can also track the previous book in each optimal subsequence and reconstruct the stack.

```text
Algorithm eldritchBookStacking(E):
    input: Sequence of book energies E of length n
    output: Maximum stack height and selected books

    if n == 0:
        return 0, []

    dp = array of length n, initialized to 1
    previous = array of length n, initialized to -1

    for i = 0 to n - 1:
        for j = 0 to i - 1:
            if E[j] < E[i]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    previous[i] = j

    max_height = maximum value in dp
    max_index = index of max_height in dp

    stack = empty list

    while max_index != -1:
        Add E[max_index] to stack
        max_index = previous[max_index]

    Reverse stack

    return max_height, stack
```

## Complexity Analysis
