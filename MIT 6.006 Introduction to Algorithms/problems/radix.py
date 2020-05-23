"""
Radix sort
"""

arr = [0, 4, 1, 3, 2, 3]

def counting_sort(arr):
    """
    1. create array on length max(n)
    2. caclulate number of items in array
    3. to preserve order (stable) calculate number of items less
    """
    n = max(arr) + 1
    pos = [0 for _ in range(n)]
    for item in arr:
        pos[item] += 1

    # Make it stable
    # count how many elements less then add[i] - this will be postion in final array
    for i in range(1, n):
        pos[i] = pos[i] + pos[i-1]

    # moving backwards from arr assing arr[i] to its position, then pos - 1
    result = [-1 for _ in range(len(arr))]
    for i in range(len(arr)-1, -1, -1):
        pos[arr[i]] -= 1
        position = pos[arr[i]]
        result[position] = arr[i]

    for i in range(len(arr)):
        arr[i]=result[i]
    return result

def base_counting_sort(arr, exp):
    """
    counting sort by digit
    """
    pos = [0 for _ in range(10)]
    for item in arr:
        index = item//(exp)
        pos[index%10] += 1
    # Make it stable
    # count how many elements less then add[i] - this will be postion in final array
    for i in range(1, 10):
        pos[i] = pos[i] + pos[i-1]

    # moving backwards from arr assing arr[i] to its position, then pos - 1
    result = [-1 for _ in range(len(arr))]
    for i in range(len(arr)-1, -1, -1):
        index = (arr[i]//exp)%10
        pos[index] -= 1
        result[pos[index]] = arr[i]

    for i in range(len(arr)):
        arr[i]=result[i]
    return result

def radix_sort(arr):
    max_num = max(arr)
    exp = 1
    while max_num/exp > 0:
        base_counting_sort(arr, exp)
        exp *= 10
    return arr
# Driver code to test above
arr = [ 170, 45, 75, 90, 802, 24, 2, 66]
# arr = [ 22, 23, 51, 24, 25, 39]

print(radix_sort(arr))
