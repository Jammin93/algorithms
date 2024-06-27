from abc import ABCMeta, abstractmethod
from typing import Optional

# todo: merge code for both MinHeap and MaxHeap into Heap.


class _Heap(metaclass=ABCMeta):

    def __init__(self, values: Optional[list] = None):
        if values is None:
            values = []

        self._items = values
        self.heapify()

    @abstractmethod
    def heapify(self):
        ...

    @abstractmethod
    def push(self, value) -> None:
        ...

    @abstractmethod
    def pop(self):
        ...

    @abstractmethod
    def _sift_up(self, index: int) -> None:
        ...

    @abstractmethod
    def _sift_down(self, index: int, upper: Optional[int] = None) -> None:
        ...

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return self._items.__str__()

    def __iter__(self):
        return self._items.__iter__()

    def __getitem__(self, item):
        return self._items.__getitem__(item)


class MaxHeap(_Heap):

    def __init__(self, values: Optional[list] = None):
        super().__init__(values)

    @property
    def largest(self):
        return self._items[0]

    def nth_largest(self, n: int, allow_dupes: bool = False):
        if n > len(self._items):
            return None

        if n == 1:
            return self._items[0]

        if allow_dupes:
            if n <= 50_000:
                keep = []
                value = self.pop()
                keep.append(value)
                for _ in range(1, n):
                    value = self.pop()
                    keep.append(value)

                for v in keep:
                    self.push(v)
            else:
                lst = sorted(self._items, reverse=True)
                value = lst[n - 1]
        else:
            if n <= 50_000:
                k = 1
                i = 0
                value = self._items[0]
                keep = []
                while k < n:
                    if i > len(self._items) - 1:
                        return None

                    v = self.pop()
                    if v < value:
                        value = v
                        k += 1

                    keep.append(v)
                    i += 1

                for v in keep:
                    self.push(v)

                return value
            else:
                lst = list(set(self._items))
                if n > len(lst):
                    return None

                lst.sort(reverse=True)
                value = lst[n - 1]

        return value

    def heapify(self) -> None:
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
            value = self._items.pop(0)
        else:
            value = self._items.pop()

        return value

    def _sift_up(self, index: int) -> None:
        parent = (index - 1) // 2
        items = self._items
        while index > 0 and items[index] > items[parent]:
            items[index], items[parent] = items[parent], items[index]
            index = parent
            parent = (index - 1) // 2

    def _sift_down(self, index: int, upper: Optional[int] = None) -> None:
        items = self._items
        if upper is None:
            upper = len(items) - 1

        while True:
            left = index * 2 + 1
            right = index * 2 + 2
            # Determine whether our upper value has two children.
            if right <= upper:
                if items[left] >= items[right]:
                    mx = left
                else:
                    mx = right

                # Don't swap unless the value at `index` is strictly smaller
                # than the rightmost child.
                if items[index] >= items[mx]:
                    break

                items[index], items[mx] = items[mx], items[index]
                index = mx
            # If we don't have two children, check to see if we have one.
            elif left <= upper:
                if items[index] >= items[left]:
                    break

                items[index], items[left] = items[left], items[index]
                index = left
            # If we don't have any children then we can't perform a swap.
            else:
                break


class MinHeap(MaxHeap):

    def __init__(self, values: Optional[list] = None):
        super().__init__(values)

    @property
    def smallest(self):
        return self._items[0]

    def nth_smallest(self, n: int, allow_dupes: bool = False):
        if n > len(self._items):
            return None

        if n == 1:
            return self._items[0]

        if allow_dupes:
            if n <= 50_000:
                keep = []
                value = self.pop()
                keep.append(value)
                for _ in range(1, n):
                    value = self.pop()
                    keep.append(value)

                for v in keep:
                    self.push(v)
            else:
                lst = sorted(self._items)
                value = lst[n - 1]
        else:
            if n <= 50_000:
                k = 1
                i = 0
                value = self._items[0]
                keep = []
                while k < n:
                    if i > len(self._items) - 1:
                        return None

                    v = self.pop()
                    if v < value:
                        value = v
                        k += 1

                    keep.append(v)
                    i += 1

                for v in keep:
                    self.push(v)

                return value
            else:
                lst = list(set(self._items))
                if n > len(lst):
                    return None

                lst.sort()
                value = lst[n - 1]

        return value

    def _sift_up(self, index: int) -> None:
        parent = (index - 1) // 2
        items = self._items
        while index > 0 and items[index] < items[parent]:
            items[index], items[parent] = items[parent], items[index]
            index = parent
            parent = (index - 1) // 2

    def _sift_down(self, index: int, upper: Optional[int] = None) -> None:
        items = self._items
        if upper is None:
            upper = len(items) - 1

        while True:
            left = index * 2 + 1
            right = index * 2 + 2
            # Determine whether our upper value has two children.
            if right <= upper:
                if items[left] <= items[right]:
                    mn = left
                else:
                    mn = right

                if items[index] <= items[mn]:
                    break

                # Don't swap unless the value at `index` is strictly smaller
                # than the rightmost child.
                items[index], items[mn] = items[mn], items[index]
                index = mn
            # If we don't have two children, check to see if we have one.
            elif left <= upper:
                if items[index] <= items[left]:
                    break

                items[index], items[left] = items[left], items[index]
                index = left
            # If we don't have any children then we can't perform a swap.
            else:
                break
