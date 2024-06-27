import random

import algorithms.structures as structs

from functools import lru_cache
from typing import Optional

CIURA_SEQUENCE = (4, 10, 23, 57, 132, 301, 701, 1750)


def bubble_sort(arr: list, reverse: bool = False) -> None:
    upper = len(arr) - 1
    if reverse:
        for i in range(0, upper):
            for k in range(0, upper - i):
                right_idx = k + 1
                if (left := arr[k]) < (right := arr[right_idx]):
                    arr[k], arr[right_idx] = right, left
    else:
        for i in range(0, upper):
            for k in range(0, upper - i):
                right_idx = k + 1
                if (left := arr[k]) > (right := arr[right_idx]):
                    arr[k], arr[right_idx] = right, left


def comb_sort(arr: list, reverse: bool = False) -> None:
    n = gap = len(arr)
    swapped = True
    if not reverse:
        while gap != 1 or swapped is not False:
            gap = max(1, int(gap // 1.3))
            swapped = False
            for i in range(n - gap):
                right_idx = i + gap
                if (left := arr[i]) > (right := arr[right_idx]):
                    arr[i], arr[right_idx] = right, left
                    swapped = True
    else:
        while gap != 1 or swapped is not False:
            gap = max(1, int(gap // 1.3))
            swapped = False
            for i in range(n - gap):
                right_idx = i + gap
                if (left := arr[i]) < (right := arr[right_idx]):
                    arr[i], arr[right_idx] = right, left
                    swapped = True


def insertion_sort(
        arr: list,
        reverse: bool = False,
        ) -> None:
    if reverse:
        for i in range(1, len(arr)):
            temp = arr[i]
            k = i
            while k >= 1 and (v := arr[k - 1]) < temp:
                arr[k] = v
                k -= 1

            arr[k] = temp
    else:
        for i in range(1, len(arr)):
            temp = arr[i]
            k = i
            while k >= 1 and (v := arr[k - 1]) > temp:
                arr[k] = v
                k -= 1

            arr[k] = temp


def shell_sort(arr: list, reverse: bool = False) -> None:
    _shell_sort(arr, reverse=reverse)


def _shell_sort(
        arr: list,
        reverse: bool = False,
        ) -> None:
    n = len(arr)
    gaps = [k for k in _generate_shell_gap_sequence(n)][::-1]
    if reverse:
        for gap in gaps:
            for i in range(gap, n):
                temp = arr[i]
                k = i
                while k >= gap and (v := arr[k - gap]) < temp:
                    arr[k] = v
                    k -= gap

                arr[k] = temp
    else:
        for gap in gaps:
            for i in range(gap, n):
                temp = arr[i]
                k = i
                while k >= gap and (v := arr[k - gap]) > temp:
                    arr[k] = v
                    k -= gap

                arr[k] = temp


def _generate_shell_gap_sequence(n: int) -> list[int]:
    """Generate shell sort gaps using Ciura255Odd."""
    seq = CIURA_SEQUENCE
    gap = 1
    yield gap
    for gap in seq:
        if gap >= n:
            break

        yield gap
    else:
        while True:
            gap = int(gap * 2.25) | 1
            if gap >= n:
                break

            yield gap


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
    insertion sort for smaller lists in order to minimize the number of times
    pages are swapped in and out of memory.
    """
    if len(arr) <= 1:
        return arr
    elif len(arr) <= 16:
        # Use insertion sort for small lists, to maximize cache hits.
        insertion_sort(arr, reverse=reverse)
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
            if reverse:
                for i in range(low + 1, high + 1):
                    temp = arr[i]
                    k = i
                    while k >= 1 and (v := arr[k - 1]) < temp:
                        arr[k] = v
                        k -= 1

                    arr[k] = temp
            else:
                for i in range(low + 1, high + 1):
                    temp = arr[i]
                    k = i
                    while k >= 1 and (v := arr[k - 1]) > temp:
                        arr[k] = v
                        k -= 1

                    arr[k] = temp
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
