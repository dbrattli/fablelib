from __future__ import annotations

from abc import abstractstaticmethod
from typing import Any, Iterable, List

from .util import IComparable


class Union(IComparable["Union"]):
    def __init__(self):
        self.tag: int
        self.fields: List[int] = []

    @abstractstaticmethod
    def cases() -> List[str]:
        ...

    @property
    def name(self) -> str:
        return self.cases()[self.tag]

    def to_JSON(self) -> str:
        raise NotImplementedError
        # return str([self.name] + self.fields) if len(self.fields) else self.name

    def __str__(self) -> str:
        if not len(self.fields):
            return self.name

        fields = ""
        with_parens = True
        if len(self.fields) == 1:
            field = str(self.fields[0])
            with_parens = field.find(" ") >= 0
            fields = field
        else:
            fields = ", ".join(map(str, self.fields))

        return self.name + (" (" if with_parens else " ") + fields + (")" if with_parens else "")

    def __hash__(self) -> int:
        hashes = map(hash, self.fields)
        return hash([hash(self.tag), *hashes])

    def __eq__(self, other: Any) -> bool:
        if self is other:
            return True
        if not isinstance(other, Union):
            return False

        if self.tag == other.tag:
            return self.fields == other.fields

        return False

    def __lt__(self, other: Any) -> bool:
        if self.tag == other.tag:
            return self.fields < other.fields

        return self.tag < other.tag


def recordEquals(self, other):
    if self is other:
        return True

    else:
        for name in self.keys():
            if self[name] != other.get(name):
                return False

        return True


def recordCompareTo(self, other):
    if self is other:
        return 0

    else:
        for name in self.keys():
            if self[name] < other.get(name):
                return -1
            elif self[name] > other.get(name):
                return 1

        return 0


def recordGetHashCode(self):
    return hash(*self.values())


class Record(IComparable["Record"]):
    def toJSON(self) -> str:
        return recordToJSON(this)

    def toString(self) -> str:
        return recordToString(self)

    def GetHashCode(self) -> int:
        return recordGetHashCode(self)

    def Equals(self, other: Record) -> bool:
        return recordEquals(self, other)

    def CompareTo(self, other: Record) -> int:
        return recordCompareTo(self, other)

    def __lt__(self, other: Any) -> bool:
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        return recordEquals(self, other)

    def __hash__(self) -> int:
        return recordGetHashCode(self)


class Attribute:
    pass


def seqToString(self):
    str = "["

    for count, x in enumerate(self):
        if count == 0:
            str += toString(x)

        elif count == 100:
            str += "; ..."
            break

        else:
            str += "; " + toString(x)

    return str + "]"


def toString(x, callStack=0):
    if x is not None:
        # if (typeof x.toString === "function") {
        #    return x.toString();

        if isinstance(x, str):
            return str(x)

        if isinstance(x, Iterable):
            return seqToString(x)

        # else: // TODO: Date?
        #     const cons = Object.getPrototypeOf(x).constructor;
        #     return cons === Object && callStack < 10
        #         // Same format as recordToString
        #         ? "{ " + Object.entries(x).map(([k, v]) => k + " = " + toString(v, callStack + 1)).join("\n  ") + " }"
        #         : cons.name;

    return str(x)


__all__ = ["Attribute", "Union"]
