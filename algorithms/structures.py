from math import log2
from typing import Optional

from algorithms.sort import _quick_sort


class MaxHeap:

    def __init__(self, values: Optional[list] = None):
        if values is None:
            values = []

        self._items = values
        self.heapify()

    @property
    def largest(self):
        return self._items[0]

    def nth_largest(self, n: int):
        raise NotImplementedError

    def heapify(self):
        # See https://tinyurl.com/34m7tun3 for why this is optimal.
        start = (len(self._items) - 2) // 2 # The last parent
        for i in range(start, -1, -1):
            self._sift_down(i)

    def push(self, value) -> None:
        self._items.append(value)
        self._sift_up(len(self._items) - 1)

    def pop(self):
        if len(self._items) > 2:
            to_swap = len(self._items) - 1
            self._items[0], self._items[to_swap] = (
                self._items[to_swap],
                self._items[0],
            )
            value = self._items.pop()
            self._sift_down(0)
        elif len(self._items) == 2:
            # self._items[0], self._items[1] = self._items[1], self._items[0]
            value = self._items.pop(0)
        else:
            value = self._items.pop()

        return value

    def sort(self, reverse: bool = False):
        if not reverse:
            for upper in range(len(self._items) - 1, 0, -1):
                self._items[0], self._items[upper] = (
                    self._items[upper],
                    self._items[0]
                )
                self._sift_down(0, upper - 1)
        else:
            levels = int(log2(len(self._items)))
            for lvl in range(levels + 1):
                n = 2 ** lvl
                idx = n - 1
                end = idx + n
                if end > (e := len(self._items) - 1):
                    end = e

                _quick_sort(self._items, idx, end, reverse=True)

    def _sift_up(self, index: int) -> None:
        parent = (index - 1) // 2
        items = self._items
        while index > 0 and items[index] > items[parent]:
            items[index], items[parent] = items[parent], items[index]
            index = parent
            parent = (index - 1) // 2

    def _sift_down(self, index: int, upper: Optional[int] = None) -> None:
        if upper is None:
            upper = len(self._items) - 1

        items = self._items
        while True:
            left = index * 2 + 1
            right = index * 2 + 2
            # Determine whether we have two children.
            if right <= upper:
                if items[left] >= items[right]:
                    mx = left
                else:
                    mx = right

                if items[index] >= items[mx]:
                    break

                items[index], items[mx] = items[mx], items[index]
                index = mx
            # If we don't have two children, check to see if we have one child.
            elif left <= upper:
                if items[index] >= items[left]:
                    break

                items[index], items[left] = items[left], items[index]
                index = left
            # If we don't have any children then we can't perform a swap.
            else:
                break
