def insertion_sort(
        arr: list,
        inplace: bool = False,
        reverse: bool = False,
        ) -> list | None:
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
    if len(arr) <= 16:
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
    # Merge the left and right halve of the array into a single, sorted array.
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
