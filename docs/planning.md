# Planning and Analysis

## Problem Formulation

The objective of the Eldritch Book Stacking problem is to efficienly stack a series of tomes on a lectern. We are told that the tomes must be stacked in order of low to high Eldritch Energy that is radiating off each tome, while also keeping the tomes in their original left to right order. Our goal is to design an algorithm that identifies the tallest possible stack of tomes while following the constraints of radiating Eldritch Energy and relitive order of the tomes.

## Baseline Solution
To establish a functional baseline, we can implement a naive brute-force strategy. This approach recursively generates all possible subsequences from the sequence of book energies E and checks each one to verify if its energy values strictly increase from left to right. The algorithm then tracks and returns the longest valid stack it finds.

```
def generateAllsequences(E):
    # brute force strategy to return all sequences
    input: Sequence E
    output: List of all possible sequences

    if length of E == 0:
        return [ [] ]

    first_element = E[0]
    remaining_elements = E[1 to end]
    
    # Recursive call to get subsets of the rest of the array
    sub_problem_solutions = generateAllsequences(remaining_elements)
    
    all_combined = empty list
    
    for each sub_solution in sub_problem_solutions:
        # Exclude the first element
        Add sub_solution to all_combined
        # Include the first element
        Add [first_element] + sub_solution to all_combined
        
    return all_combined

def baselineEldritchBookStacking(E):
    input: Sequence of book energies E of length n
    output: Maximum stack height and selected books

    max_height = 0
    best_stack = empty list

    # Generate all possible sequences
    
    all_subsets = generateAllsequences(E)

    for each subset in all_subsets:
        is_valid = true
        
        # Verify if the subset increases from left to right
        for i from 0 to length(subset) - 2:
            if subset[i] >= subset[i + 1]:
                is_valid = false
                break

        # Track the longest valid stack found
        if is_valid == true:
            if length of subset > max_height:
                max_height = length of subset
                best_stack = subset

    return max_height, best_stack

```

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

Let $n$ be the number of books.

For the brute-force baseline, the algorithm generates and checks all $2^n$ subsets. Checking each subset takes at most $O(n)$ time, so the running time is $\Theta(n2^n)$. Storing all subsets requires $\Theta(n2^n)$ space; generating and checking them one at a time requires $O(n)$ auxiliary space, not counting the result.

For the dynamic-programming approach, the nested loops make $\sum_{i=0}^{n-1} i = n(n-1)/2$ comparisons, so the running time is $\Theta(n^2)$. Initialization, finding the maximum, and reconstructing the stack each take $O(n)$ time and do not change this bound. The `dp` and `previous` arrays, along with the reconstructed stack, require $\Theta(n)$ space.