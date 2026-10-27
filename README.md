# DSA — Heap Sort (Python)

An in-place, comparison-based sorting algorithm that turns the list into a **max-heap** and then repeatedly moves the largest element to the end. This implementation is **iterative** (no recursion) and reads its input from standard input.

---

## Problem Statement

Given a list of `n` integers, sort it in **ascending order** using Heap Sort.

**Example**

```
Input:
5
4 10 3 5 1

Output:
1 3 4 5 10
```

---

## Solution

```python
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
```

---

## The Critical Idea

A list can be read as a **complete binary tree** without any extra memory. For the element at index `i`:

| Relation     | Index     |
|--------------|-----------|
| Left child   | `2i + 1`  |
| Right child  | `2i + 2`  |
| Parent       | `(i-1)//2` |

A **max-heap** guarantees every parent is greater than or equal to its children, so the largest element always sits at index `0`. Heap Sort works in two phases:

1. **Build the heap** — rearrange the list into a max-heap.
2. **Extract the maximum** — swap the root with the last unsorted element, shrink the heap by one, and restore the heap property. Repeat.

Each extraction places one element in its final position, so the sorted region grows from the right.

---

## How the Loop Works

### Phase 1 — Build the Max-Heap

```python
for i in range(n // 2 - 1, -1, -1):
```

- Indices `n // 2` to `n - 1` are leaves, so they are already valid heaps. The loop starts at the **last non-leaf node** and moves up to the root.
- For each `i`, the inner `while` loop does a **sift-down**: pick the larger child, and if it is bigger than `root`, swap and continue downward. Otherwise `break`.

### Phase 2 — Sort

```python
for i in range(n - 1, 0, -1):
    arr[0], arr[i] = arr[i], arr[0]   # move current max to its final position
    # sift-down arr[0] within the heap of size i
```

- After the swap, the heap occupies indices `0 .. i-1` (size `i`), which is why the sift-down condition uses `< i` instead of `< n`.
- The loop stops at `i = 1`; the last remaining element is automatically in place.

---

## Pseudocode

```
HEAP-SORT(arr, n):
    for i = n/2 - 1 down to 0:
        SIFT-DOWN(arr, i, n)

    for i = n-1 down to 1:
        swap(arr[0], arr[i])
        SIFT-DOWN(arr, 0, i)

SIFT-DOWN(arr, root, size):
    while 2*root + 1 < size:
        child = 2*root + 1
        if child + 1 < size and arr[child] < arr[child + 1]:
            child = child + 1
        if arr[root] < arr[child]:
            swap(arr[root], arr[child])
            root = child
        else:
            break
```

---

## Dry Run

Input: `arr = [4, 10, 3, 5, 1]`, `n = 5`

**Phase 1 — Build the heap** (start at `i = n // 2 - 1 = 1`)

| Step | Action | List |
|------|--------|------|
| i = 1 | `10` vs larger child `5` — already in place | `[4, 10, 3, 5, 1]` |
| i = 0 | `4` < `10` → swap | `[10, 4, 3, 5, 1]` |
| continue | `4` (index 1) < `5` (index 3) → swap | `[10, 5, 3, 4, 1]` |

Max-heap: `[10, 5, 3, 4, 1]`

**Phase 2 — Extract the maximum**

| i | Swap `arr[0]` ↔ `arr[i]` | Sift-down (heap size = i) | List |
|---|--------------------------|---------------------------|------|
| 4 | `10` ↔ `1` | `1` sinks below `5`, then `4` | `[5, 4, 3, 1, 10]` |
| 3 | `5` ↔ `1` | `1` sinks below `4` | `[4, 1, 3, 5, 10]` |
| 2 | `4` ↔ `3` | `3` vs child `1` — stays | `[3, 1, 4, 5, 10]` |
| 1 | `3` ↔ `1` | heap of size 1 | `[1, 3, 4, 5, 10]` |

**Output:** `1 3 4 5 10`

---

## Complexity Analysis

| Case    | Time          | Space  |
|---------|---------------|--------|
| Best    | O(n log n)    | O(1)   |
| Average | O(n log n)    | O(1)   |
| Worst   | O(n log n)    | O(1)   |

- **Build heap:** O(n) — most nodes are near the bottom and sink only a few levels.
- **n extractions:** each sift-down costs O(log n), giving O(n log n) overall.
- **Space:** sorting is done in place; only a few index variables are used beyond the input list.
- **Stability:** Heap Sort is **not stable** — equal elements may change their relative order.

---

## Edge Cases

| Input | Behaviour |
|-------|-----------|
| `n = 1` | Neither loop does any work; the single element is printed |
| `n = 0` | Both loops are skipped and an empty line is printed (provided the second input line is empty) |
| Already sorted | Still O(n log n) — the heap is built and fully unwound |
| Reverse sorted | Same O(n log n) bound |
| All equal elements | Comparisons use strict `<`, so no needless swaps occur |
| Negative numbers | Handled naturally, since only comparisons are used |
| Duplicates | Sorted correctly, but their original relative order is not preserved |

---

## Code-Quality Notes

- The sift-down logic is written twice (build phase and sort phase). Extracting it into a helper such as `sift_down(arr, root, size)` removes the duplication.
- `n` is read separately but the list length comes from the second line; using `n = len(arr)` avoids a mismatch if the input is inconsistent.
- `print(*(arr))` can be written `print(*arr)`.
- In real projects, prefer Python's built-in `heapq` module or `sorted()`; this script is meant for learning how the algorithm works.

---

## Natural Extension

- Extract `sift_down` into a reusable function.
- Sort in **descending** order by using a min-heap (flip the comparisons).
- Compare with `heapq.heapify` and `heapq.heappop` from the standard library.
- Use the heap-building step to solve **Top-K** problems.

---

## Repository Structure

```
DSA/
└── Sorting/
    └── Heap-Sort/
        ├── heap_sort.py
        └── README.md
```

---

## How to Run

```bash
python heap_sort.py
```

**Sample session**

```
5
4 10 3 5 1
1 3 4 5 10
```

---

## Key Concepts

- **Complete binary tree in a list** — parent and child positions come from index arithmetic
- **Max-heap property** — every parent ≥ its children
- **Sift-down (heapify)** — restores the heap after a change at the root
- **In-place sorting** — O(1) auxiliary space
- **Tuple swapping** — `a, b = b, a` swaps without a temporary variable

---

## Why This Problem Matters

Heap Sort is the classic example of getting a **guaranteed O(n log n)** sort with **O(1) extra space**, and the heap it builds is the engine behind priority queues.

| Problem | Concept Used |
|---------|--------------|
| Kth Largest Element in an Array | Heap |
| Top K Frequent Elements | Heap + hashing |
| Merge K Sorted Lists | Min-heap |
| Find Median from Data Stream | Two heaps |
| Sort an Array | Sorting algorithms |

---

## Contributing

Contributions are welcome! Fork the repository, create a feature branch, and open a pull request with a short description of the change.

---

## License

This project is licensed under the MIT License.