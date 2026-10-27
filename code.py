n = int(input())
arr = [int(x) for x in input().split()]

for i in range(n // 2 - 1, -1, -1):
    root = i
    while root * 2 + 1 < n:
        child = root * 2 + 1
        if child + 1 < n and arr[child] < arr[child + 1]:
            child += 1
        if arr[root] < arr[child]:
            arr[root], arr[child] = arr[child], arr[root]
            root = child
        else:
            break

for i in range(n - 1, 0, -1):
    arr[0], arr[i] = arr[i], arr[0]
    root = 0
    while root * 2 + 1 < i:
        child = root * 2 + 1
        if child + 1 < i and arr[child] < arr[child + 1]:
            child += 1
        if arr[root] < arr[child]:
            arr[root], arr[child] = arr[child], arr[root]
            root = child
        else:
            break

print(*(arr))
