"""
Split text into “good” lines
"""


text = ["blah", "blah", "blah", "blah", "reallylongword"]

def greed_split(text, width):
    line = text[0]
    for word in text[1:]:
        if len(line) + len(word) + 1 <= width:
            line = line + " " + word
        else:
            print(line)
            line = "" + word
    print(line)




def dp_split(text, width):
    """
    - badness(line) = (width - len(line))^3
    - minimize badness of all lines accross text

    Subproblems:
    - guess where lines begin (recursive)
    memoize[i] = min ( DP(j) + badness(i,j) for j in range(i+1, n))

    to reconstruct path store parents pointers
    """

    def badness(i, j):
        """
        metric to minimize
        """
        line_width = len(' '.join(text[i:j]))
        if line_width > width:
            return float('inf')
        return (width - line_width)**3

    n = len(text)
    memoize = [float('inf') for _ in range(n)]
    parents = {}
    #base case 0
    memoize[n][n] = 0

    for start in range(n-1, 0, -1):
        for end in range(n-1, 0, -1):
            line_weight = memoize[start+1][end+1] + badness(start, end)
            if memoize[start][end] > line_weight:
                memoize[start][end] = line_weight
                parents[start] = end


def dp_split_rec(text, width):
    """
    recursive
    - memoize
    - parents

    """
    n = len(text)
    parents = {}
    memoize = {}

    def dp(i):
        # base case
        if i == n:
            return 0
        elif i in memoize:
            return memoize[i]

        # dp state
        seq = {j: dp(j) + badness(i,j) for j in range(i+1, n+1)}
        min_key, min_value = min(seq.items(), key=lambda x: x[1])

        #store sub-solutions
        memoize[min_key] = min_value
        parents[i] = min_key

        return min_value


    def badness(i, j):
        line_width = len(' '.join(text[i:j]))
        if line_width > width:
            return float('inf')
        return (width - line_width)**3

    print("recursive cost:", dp(0))
    start = 0
    end = 0
    while end < n:
        start = end
        end = parents[start]
        print(text[start:end])

# greed_split(text, 16)

# dp_split_rec(text, 16)

# dp_split(text, 16)


text1 = "aaa bb cc ddddd".split()
width = 6

greed_split(text1, width)
dp_split_rec(text1, width)

