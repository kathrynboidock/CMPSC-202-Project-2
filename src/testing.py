def eldritchBookStacking(E):
    n = len(E)

    if n == 0:
        return 0, []

    dp = [1] * n
    previous = [-1] * n

    for i in range(n):
        for j in range(i):
            if E[j] < E[i]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    previous[i] = j

    max_height = max(dp)
    max_index = dp.index(max_height)

    stack = []
    while max_index != -1:
        stack.append(E[max_index])
        max_index = previous[max_index]

    stack.reverse()
    return max_height, stack

print(eldritchBookStacking([2, 5, 3, 8, 6]))
print(eldritchBookStacking([]))
print(eldritchBookStacking([9, 7, 5, 3, 1]))
print(eldritchBookStacking([4, 4, 4, 4]))
print(eldritchBookStacking([-5, -2, -8, 0, -1]))
