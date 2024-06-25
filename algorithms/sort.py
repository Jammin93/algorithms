import random

import algorithms.structures as structs

# todo: add thin wrappers to allow non-inplace sorting.
# todo: add shell sort and possible replace insertion sort logic in quick
#  sort and merge sort with shell sort. This needs to be tested but should
#  may be more efficient. It's unclear whether it will be more efficient for
#  small lists like those encountered in merge and quick sort.


def insertion_sort(
        arr: list,
        reverse: bool = False,
        ) -> list | None:
    """
    Optimized insertion sort which operates in O(n^2) time. Only one swap is
    performed per iteration of the outer loop. Until the inner loop exits,
    values are merely pushed up or down the list, overwriting the values of
    immediate neighbors. The target value from the outer loop is then
    inserted once the inner loop exits, constituting a swap. Consider the
    array [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]. Let `i` start at 5
    and set `k` equal `i` - 1 at the start of the inner loop. The array
    will be manipulated as follows.

    [10, 9, 8, 7, 6, 6, 4, 3, 2, 1]  --->  `k` = 4
    [10, 9, 8, 7, 7, 6, 4, 3, 2, 1]  --->  `k` = 3
    [10, 9, 8, 8, 7, 6, 4, 3, 2, 1]  --->  `k` = 2
    [10, 9, 9, 8, 7, 6, 4, 3, 2, 1]  --->  `k` = 1
    [10, 10, 9, 8, 7, 6, 4, 3, 2, 1] --->  `k` = 0
    [5, 10, 9, 8, 7, 6, 4, 3, 2, 1]  --->  `k` = -1
    """
    if not reverse:
        for i in range(1, len(arr)):
            current = arr[i]
            swap_idx = i - 1
            for k in range(i - 1, -2, -1):
                swap_idx = k
                if arr[k] > current:
                    arr[k + 1] = arr[k]
                else:
                    break

            arr[swap_idx + 1] = current
    else:
        for i in range(1, len(arr)):
            current = arr[i]
            swap_idx = i - 1
            for k in range(i - 1, -2, -1):
                swap_idx = k
                if arr[k] < current:
                    arr[k + 1] = arr[k]
                else:
                    break

            arr[swap_idx + 1] = current


def select_sort(
        arr: list,
        reverse: bool = False,
        ) -> list | None:
    """Basic selection sort implementation which operates in O(n^2) time."""
    arrsize = len(arr)
    if not reverse:
        for i in range(arrsize):
            min_index = i
            for k in range(i + 1, arrsize):
                if arr[k] < arr[min_index]:
                    min_index = k

            arr[i], arr[min_index] = arr[min_index], arr[i]
    else:
        for i in range(arrsize):
            max_index = i
            for k in range(i + 1, arrsize):
                if arr[k] > arr[max_index]:
                    max_index = k

            arr[i], arr[max_index] = arr[max_index], arr[i]


def merge_sort(arr: list, reverse: bool = False):
    """
    Optimized top-down merge sort which operates in O(nlogn) time. Uses
    optimized insertion sort for smaller lists in order to minimize pages
    being swapped in and out of the memory cache.
    """
    if len(arr) <= 1:
        return arr
    elif len(arr) <= 16:
        # Use insertion sort for small lists, to maximize cache hits.
        if not reverse:
            for i in range(1, len(arr)):
                current = arr[i]
                swap_idx = i - 1
                for k in range(swap_idx, -2, -1):
                    swap_idx = k
                    if arr[k] > current:
                        arr[k + 1] = arr[k]
                    else:
                        break

                arr[swap_idx + 1] = current
        else:
            for i in range(1, len(arr)):
                current = arr[i]
                swap_idx = i - 1
                for k in range(swap_idx, -2, -1):
                    swap_idx = k
                    if arr[k] < current:
                        arr[k + 1] = arr[k]
                    else:
                        break

                arr[swap_idx + 1] = current

        return arr
    else:
        mid = len(arr) // 2
        # Split the array into left and right halves.
        left = arr[:mid]
        right = arr[mid:]
        # Recursively split each half until the returned halves are small
        # enough to be efficiently sorted via insertion sort, then work our
        # way back up the stack.
        left = merge_sort(left, reverse)
        right = merge_sort(right, reverse)
        return _merge(left, right, reverse)


def _merge(left: list, right: list, reverse: bool):
    # Merge the left and right halves of the array into a single, sorted array.
    merged = []
    left_index = 0
    right_index = 0
    if not reverse:
        while left_index < len(left) and right_index < len(right):
            lval = left[left_index]
            rval = right[right_index]
            if lval == rval:
                merged.append(lval)
                merged.append(rval)
                left_index += 1
                right_index += 1
            elif lval < rval:
                merged.append(lval)
                left_index += 1
            else:
                merged.append(rval)
                right_index += 1
    else:
        while left_index < len(left) and right_index < len(right):
            lval = left[left_index]
            rval = right[right_index]
            if lval == rval:
                merged.append(lval)
                merged.append(rval)
                left_index += 1
                right_index += 1
            elif lval > rval:
                merged.append(lval)
                left_index += 1
            else:
                merged.append(rval)
                right_index += 1

    # We should always end up with one empty and one non-empty array.
    merged.extend(right[right_index:] or left[left_index:])
    return merged


def quick_sort(arr: list, reverse: bool = False):
    _quick_sort(arr, 0, len(arr) - 1, reverse=reverse)


def _quick_sort(arr: list, low: int, high: int, reverse: bool = False):
    if low < high:
        if high - low <= 10:
            if not reverse:
                # Modified insertion sort which maximizes cache hits and
                # operates closer to O(n) for smaller lists.
                for i in range(low + 1, high + 1):
                    current = arr[i]
                    swap_idx = i - 1
                    for k in range(swap_idx, -2, -1):
                        swap_idx = k
                        if arr[k] > current:
                            arr[k + 1] = arr[k]
                        else:
                            break

                    arr[swap_idx + 1] = current
            else:
                for i in range(low + 1, high + 1):
                    current = arr[i]
                    swap_idx = i - 1
                    for k in range(swap_idx, -2, -1):
                        swap_idx = k
                        if arr[k] < current:
                            arr[k + 1] = arr[k]
                        else:
                            break

                    arr[swap_idx + 1] = current
        else:
            # After testing, this appears to be the best way to select the
            # pivot.
            if high - low <= 54:
                pivot = random.randint(low, high)
            else:
                pivot = (high + low) // 2
                if arr[low] < arr[high]:
                    if arr[high] < arr[pivot]:
                        pivot = high
                elif arr[low] < arr[pivot]:
                    pivot = low

            pivot_value = arr[pivot]
            arr[pivot], arr[low] = arr[low], arr[pivot]
            border = low
            if not reverse:
                for i in range(low, high + 1):
                    if arr[i] < pivot_value:
                        border += 1
                        arr[i], arr[border] = arr[border], arr[i]
            else:
                for i in range(low, high + 1):
                    if arr[i] > pivot_value:
                        border += 1
                        arr[i], arr[border] = arr[border], arr[i]

            arr[low], arr[border] = arr[border], arr[low]
            _quick_sort(arr, low, border - 1, reverse=reverse)
            _quick_sort(arr, border + 1, high, reverse=reverse)


def heap_sort(arr: list, reverse: bool = False):
    if not reverse:
        heap = structs.MaxHeap(arr)
    else:
        heap = structs.MinHeap(arr)

    values = heap._items
    for upper in range(len(heap) - 1, 0, -1):
        values[0], values[upper] = values[upper], values[0]
        heap._sift_down(0, upper - 1)


def comb_sort(arr: list, reverse: bool = False):
    n = gap = len(arr)
    swapped = True
    if not reverse:
        while gap != 1 or swapped is not False:
            gap = max(1, int(gap // 1.3))
            swapped = False
            for i in range(n - gap):
                ridx = i + gap
                if (left := arr[i]) > (right := arr[ridx]):
                    arr[i], arr[ridx] = right, left
                    swapped = True
    else:
        while gap != 1 or swapped is not False:
            gap = max(1, int(gap // 1.3))
            swapped = False
            for i in range(n - gap):
                ridx = i + gap
                if (left := arr[i]) < (right := arr[ridx]):
                    arr[i], arr[ridx] = right, left
                    swapped = True


def bubble_sort(arr: list, reverse: bool = False):
    upper = len(arr) - 1
    for i in range(0, upper):
        for k in range(0, upper - i):
            ridx = k + 1
            if (left := arr[k]) > (right := arr[ridx]):
                arr[k], arr[ridx] = right, left
