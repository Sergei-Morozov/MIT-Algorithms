"""
Input: 8 3 5
Output: longest increasing subsequence

dp:
dp[i] - show calculated optimal longest subsequence
iterate from end to start
"""

input = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]

# 0, 2, 6, 9, 13, 15.
# 0, 4, 6, 9, 11, 15.


def sequence(array):

    n = len(array)

    dp = [None for _ in range(n)]
    for i in range(n-1, -1, -1):
        #base case (moving nowhere)
        choice = [1]
        for j in range(i+1, n):
            if array[j] > array[i]:
                choice.append(1+dp[j])
        dp[i] = max(choice)

    print(dp)

sequence(input)

