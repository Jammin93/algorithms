from typing import Optional


def linear_search(arr: list, key, lo: int = 0, hi: Optional[int] = None) -> int:
    size = len(arr)
    hi = size if hi is None else hi
    for i in range(lo, hi):
        if arr[i] == key:
            return i

    return None


def binsearch(
        arr: list,
        key,
        lo: int = 0,
        hi: Optional[int] = None,
        sort: bool = False,
        ) -> int | None:
    size = len(arr)
    lo = 0
    hi = size if hi is None else hi
    if sort:
        arr = sorted([(i, v) for i, v in enumerate(arr)], key=lambda x: x[1])
        while lo < hi:
            # We don't need to worry about overflow in Python, but this is the
            # correct formula for finding `mid` for languages where we do need
            # to worry about overflow.
            mid = lo + (hi - lo) // 2
            if arr[mid][1] < key:
                lo = mid + 1
            else:
                hi = mid

        if lo <= size and arr[lo][1] != key:
            return None

        res = arr[lo][0]
    else:
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if arr[mid] < key:
                lo = mid + 1
            else:
                hi = mid

        if lo <= size and arr[lo] != key:
            return None

        res = lo

    return res
