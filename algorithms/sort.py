import random


def insertion_sort(
        arr: list,
        inplace: bool = False,
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
    if not isinstance(arr, list):
        arr = list(arr)

    if inplace and not reverse:
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
    elif inplace and reverse:
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
    elif not inplace and not reverse:
        new_arr = arr.copy()
        for i in range(1, len(new_arr)):
            current = new_arr[i]
            swap_idx = i - 1
            for k in range(i - 1, -2, -1):
                swap_idx = k
                if new_arr[k] > current:
                    new_arr[k + 1] = new_arr[k]
                else:
                    break

            new_arr[swap_idx + 1] = current

        return new_arr
    else:
        new_arr = arr.copy()
        for i in range(1, len(new_arr)):
            current = new_arr[i]
            swap_idx = i - 1
            for k in range(i - 1, -2, -1):
                swap_idx = k
                if new_arr[k] < current:
                    new_arr[k + 1] = new_arr[k]
                else:
                    break

            new_arr[swap_idx + 1] = current

        return new_arr


def select_sort(
        arr: list,
        inplace: bool = False,
        reverse: bool = False,
        ) -> list | None:
    """Basic selection sort implementation which operates in O(n^2) time."""
    arrsize = len(arr)
    if inplace and not reverse:
        for i in range(arrsize):
            min_index = i
            for k in range(i + 1, arrsize):
                if arr[k] < arr[min_index]:
                    min_index = k

            arr[i], arr[min_index] = arr[min_index], arr[i]
    elif inplace and reverse:
        for i in range(arrsize):
            max_index = i
            for k in range(i + 1, arrsize):
                if arr[k] > arr[max_index]:
                    max_index = k

            arr[i], arr[max_index] = arr[max_index], arr[i]
    elif not inplace and not reverse:
        new_arr = arr.copy()
        for i in range(arrsize):
            min_index = i
            for k in range(i + 1, arrsize):
                if new_arr[k] < new_arr[min_index]:
                    min_index = k

            new_arr[i], new_arr[min_index] = new_arr[min_index], new_arr[i]

        return new_arr
    else:
        new_arr = arr.copy()
        for i in range(arrsize):
            max_index = i
            for k in range(i + 1, arrsize):
                if new_arr[k] > new_arr[max_index]:
                    max_index = k

            new_arr[i], new_arr[max_index] = new_arr[max_index], new_arr[i]

        return new_arr


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
    _quick_sort(arr, 0, len(arr) - 1)


def _quick_sort(arr: list, low: int, high: int):
    if low < high:
        if high - low <= 10:
            # Modified insertion sort which maximizes cache hits and operates
            # closer to O(n) for smaller lists.
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
            i = low
            k = high
            while i <= k:
                while arr[i] < pivot_value:
                    i += 1
                while arr[k] > pivot_value:
                    k -= 1

                if i <= k:
                    arr[i], arr[k] = arr[k], arr[i]
                    i += 1
                    k -= 1

            _quick_sort(arr, low, k)
            _quick_sort(arr, i, high)
