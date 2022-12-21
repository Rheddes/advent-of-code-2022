from typing import Iterator


class Vector:
    def __init__(self, items: Iterator):
        self.items = [item for item in items]

    def shape(self):
        return len(self.items)

    def __iter__(self):
        for item in self.items:
            yield item

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.items[item]
        return Vector(self.items[item])

    def __add__(self, other):
        if isinstance(other, int):
            return Vector([i + other for i in self])
        if not isinstance(other, Vector):
            raise ValueError('Cannot add together types of Vector and ', type(other))
        if other.shape() != self.shape():
            raise ValueError(f'Cannot add together vectors of shapes {self.shape()} and {other.shape()}')
        return Vector([i + j for i, j in zip(self, other)])

    def __eq__(self, other):
        return isinstance(other, Vector) and self.items == other.items

    def __str__(self):
        return f'vector({self.items})'

    def __repr__(self):
        return self.__str__()
