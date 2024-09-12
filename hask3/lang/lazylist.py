from collections.abc import Sequence
from hask3.hack import objectify
from hask3.lang.type_system import Typeclass
from hask3.lang.type_system import Hask
from hask3.lang.typeclasses import Show
from hask3.lang.typeclasses import Eq
from hask3.lang.typeclasses import Ord
from hask3.lang.syntax import Syntax
from hask3.lang.syntax import instance
from hask3.lang.syntax import sig
from hask3.lang.syntax import H

# LT, EQ, GT = -1, 0, 1

try:
    from __builtin__ import cmp
except ImportError:
    def cmp(a, b):
        if a == b:
            return 0
        elif a < b:
            return -1
        else:
            return 1


class Enum(Typeclass):
    """
    Class Enum defines operations on sequentially ordered types.

    The enumFrom... methods are used in translation of arithmetic sequences.

    Instances of Enum may be derived for any enumeration type (types whose
    constructors have no fields). The nullary constructors are assumed to be
    numbered left-to-right by fromEnum from 0 through n-1.

    Attributes:

    - ``toEnum``
    - ``fromEnum``
    - ``succ``
    - ``pred``
    - ``enumFrom``
    - ``enumFromThen``
    - ``enumFrom``
    - ``enumFromThenTo``
    - ``EnumFromTo``

    Minimal complete definition:

    - ``toEnum``
    - ``fromEnum``

    """
    @classmethod
    def make_instance(typeclass, cls, toEnum, fromEnum):
        from hask3.lang.type_system import build_instance

        def succ(a):
            return toEnum(fromEnum(a) + 1)

        def pred(a):
            return toEnum(fromEnum(a) - 1)

        def enumFromThen(start, second):
            pointer = fromEnum(start)
            step = fromEnum(second) - pointer
            while True:
                yield toEnum(pointer)
                pointer += step

        def enumFrom(start):
            return enumFromThen(start, succ(start))

        def enumFromThenTo(start, second, end):
            if start == end:
                yield start
                return

            elif (second >= start > end) or (second <= start < end):
                return

            pointer, stop = fromEnum(start), fromEnum(end)
            step = fromEnum(second) - pointer
            while (start < end and pointer <= stop) or \
                  (start > end and pointer >= stop):
                yield toEnum(pointer)
                pointer += step

        def enumFromTo(start, end):
            second = succ(start) if start < end else pred(start)
            return enumFromThenTo(start, second, end)

        attrs = {"toEnum": toEnum, "fromEnum": fromEnum, "succ": succ, "pred":
                 pred, "enumFromThen": enumFromThen, "enumFrom": enumFrom,
                 "enumFromThenTo": enumFromThenTo, "enumFromTo": enumFromTo}
        build_instance(Enum, cls, attrs)


@sig(H/ "a" >> int)
def fromEnum(a):
    """``fromEnum :: a -> int``

    Convert to an int.

    """
    return Enum[a].toEnum(a)


@sig(H/ "a" >> "a")
def succ(a):
    """``succ :: a -> a``

    the successor of a value. For numeric types, succ adds 1.

    """
    return Enum[a].succ(a)


@sig(H/ "a" >> "a")
def pred(a):
    """
    pred :: a -> a

    the predecessor of a value. For numeric types, pred subtracts 1.
    """
    return Enum[a].pred(a)


@sig(H/ "a" >> "a" >> ["a"])
def enumFromThen(start, second):
    """``enumFromThen :: a -> a -> [a]``

    Used in translation of ``[n, n_, ...]``.

    """
    return L[Enum[start].enumFromThen(start, second)]


@sig(H/ "a" >> ["a"])
def enumFrom(start):
    """``enumFrom :: a -> [a]``

    Used in translation of L[n, ...]

    """
    return L[Enum[start].enumFrom(start)]


@sig(H/ "a" >> "a" >> "a" >> ["a"])
def enumFromThenTo(start, second, end):
    """``enumFromThenTo :: a -> a -> a -> [a]``

    Used in translation of ``L[n, n_, ..., m]``.

    """
    return L[Enum[start].enumFromThenTo(start, second, end)]


@sig(H/ "a" >> "a" >> ["a"])
def enumFromTo(start, end):
    """``enumFromTo :: a -> a -> [a]``

    Used in translation of L[n, ..., m]

    """
    return L[Enum[start].enumFromTo(start, end)]


instance(Enum, int).where(fromEnum=int, toEnum=int)
instance(Enum, bool).where(fromEnum=int, toEnum=bool)
instance(Enum, str).where(fromEnum=ord, toEnum=chr)


class List(Sequence, Hask):
    """Statically typed lazy sequence datatype.

    See `L`:obj: for more information.

    """
    def __init__(self, head=None, tail=None):
        from itertools import chain
        from hask3.lang.type_system import typeof
        from hask3.lang.hindley_milner import unify
        if head is not None:
            count = len(head)
            if count > 0:
                fst = head[0]
                i = 1
                while i < count:
                    unify(typeof(fst), typeof(head[i]))
                    i += 1
            self.__head = list(head)
        else:
            self.__head = []
        self.__is_evaluated = tail is None
        self.__tail = chain([] if self.__is_evaluated else tail)

    def __type__(self):
        from hask3.lang.type_system import typeof
        from hask3.lang.hindley_milner import TypeVariable, ListType
        if len(self.__head) == 0:
            if self.__is_evaluated:
                return ListType(TypeVariable())
            else:
                self.__next()
                return self.__type__()
        else:
            return ListType(typeof(self[0]))

    def __next(self):
        """Evaluate the next element of the tail, and add it to the head."""
        from hask3.lang.type_system import typeof
        from hask3.lang.hindley_milner import unify
        if self.__is_evaluated:
            raise StopIteration
        else:
            try:
                next_iter = next(self.__tail)
                if len(self.__head) > 0:
                    unify(typeof(self[0]), typeof(next_iter))
                self.__head.append(next_iter)
            except StopIteration:
                self.__is_evaluated = True

    def __evaluate(self):
        """Evaluate the entire List."""
        while not self.__is_evaluated:
            self.__next()

    def __rxor__(self, item):
        """``^`` is the ``cons`` operator (equivalent to ``:`` in Haskell)."""
        from hask3.lang.type_system import typeof
        from hask3.lang.hindley_milner import ListType, unify
        unify(self.__type__(), ListType(typeof(item)))
        if self.__is_evaluated:
            return List(head=[item] + self.__head)
        return List(head=[item] + self.__head, tail=self.__tail)

    def __add__(self, other):
        """``(+) :: [a] -> [a] -> [a]``

        ``+`` is the list concatenation operator, equivalent to ``++`` in
        Haskell and + for Python lists

        """
        from itertools import chain
        from hask3.lang.type_system import typeof
        from hask3.lang.hindley_milner import unify
        unify(self.__type__(), typeof(other))
        if self.__is_evaluated and other.__is_evaluated:
            return List(head=self.__head + other.__head)
        elif self.__is_evaluated and not other.__is_evaluated:
            return List(head=self.__head + other.__head, tail=other.__tail)
        else:
            return List(head=self.__head, tail=chain(self.__tail, other))

    def __str__(self):
        from hask3.lang.typeclasses import show
        body = ", ".join(map(show, self.__head))
        if self.__is_evaluated:
            if len(self.__head) <= 1:
                body = f'[{body}]'
            suffix = ''
        else:
            suffix = ' ...'
        return f"L[{body}{suffix}]"

    def __cmp__(self, other):
        if self.__is_evaluated and other.__is_evaluated:
            return cmp(self.__head, other.__head)

        elif len(self.__head) >= len(other.__head):
            # check the evaluated heads
            heads = zip(self.__head[:len(other.__head)], other.__head)
            heads_comp = ((cmp(h1, h2) for h1, h2 in heads))
            for comp in heads_comp:
                if comp != 0:
                    return comp

            # evaluate the shorter-headed list until it is the same size
            while len(self.__head) > len(other.__head):
                if other.__is_evaluated:
                    return 1
                other.__next()
                comp = cmp(self.__head[len(other.__head)-1], other.__head[-1])
                if comp != 0:
                    return comp

            # evaluate the tails, checking each time
            while not self.__is_evaluated or not other.__is_evaluated:
                if not self.__is_evaluated:
                    self.__next()
                if not other.__is_evaluated:
                    other.__next()

                len_comp = cmp(len(self.__head), len(other.__head))
                if len_comp != 0:
                    return len_comp

                if len(self.__head) > 0:
                    value_comp = cmp(self.__head[-1], other.__head[-1])
                    if value_comp != 0:
                        return value_comp

        elif len(other.__head) > len(self.__head):
            return -other.__cmp__(self)

        return 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __lt__(self, other):
        return self.__cmp__(other) == -1

    def __gt__(self, other):
        return self.__cmp__(other) == 1

    def __le__(self, other):
        comp = self.__cmp__(other)
        return comp in (-1, 0)

    def __ge__(self, other):
        comp = self.__cmp__(other)
        return comp in (1, 0)

    def __len__(self):
        self.__evaluate()
        return len(self.__head)

    def __iter__(self):
        for item in self.__head:
            yield item

        for item in self.__tail:
            self.__head.append(item)
            yield item

    def count(self, x):
        from hask3.lang.type_system import typeof
        from hask3.lang.hindley_milner import ListType, unify
        unify(self.__type__(), ListType(typeof(x)))
        self.__evaluate()
        return self.__head.count(x)

    def index(self, x):
        from hask3.lang.type_system import typeof
        from hask3.lang.hindley_milner import ListType, unify
        unify(self.__type__(), ListType(typeof(x)))
        self.__evaluate()
        return self.__head.index(x)

    def __contains__(self, x):
        from hask3.hack import isin
        from hask3.lang.type_system import typeof
        from hask3.lang.hindley_milner import ListType, unify
        unify(self.__type__(), ListType(typeof(x)))
        return isin(x, iter(self))

    def __getitem__(self, ix):
        is_slice = isinstance(ix, slice)
        if is_slice:
            i = ix.start if ix.stop is None else ix.stop
        else:
            i = ix
        # make sure that the list is evaluated enough to do the indexing, but
        # not any more than necessary
        # if index is negative, evaluate the entire list
        if i is None:
            # In Python 3, `None >= 0` is a TypeError, but in Python 2 returns
            # False.  So let's go negative in any case...
            i = -1
        if i >= 0:
            while (i+1) > len(self.__head):
                try:
                    self.__next()
                except StopIteration:
                    break
        else:
            self.__evaluate()
        if is_slice:
            if ix.stop is None and not self.__is_evaluated:
                return List(head=self.__head[ix], tail=self.__tail)
            else:
                return List(head=self.__head[ix])
        else:
            return self.__head[i]


# Basic typeclass instances for list
instance(Show, List).where(
    show = List.__str__
)

instance(Eq, List).where(
    eq = List.__eq__
)

instance(Ord, List).where(
    lt = List.__lt__,
    gt = List.__gt__,
    le = List.__le__,
    ge = List.__ge__
)


@objectify
class L(Syntax):
    """``L`` is for comprehensions and lazy creation of Haskell-style lists.

    To create a new List, just wrap an interable in ``L[ ]``.

    List comprehensions can be used with any instance of Enum, including the
    built-in types int, float, and char.
    There are four basic list comprehension patterns::

        >>> L[1, ...]
        # list from 1 to infinity, counting by ones

        >>> L[1, 3, ...]
        # list from 1 to infinity, counting by twos

        >>> L[1, ..., 20]
        # list from 1 to 20 (inclusive), counting by ones

        >>> L[1, 5, ..., 20]
        # list from 1 to 20 (inclusive), counting by fours

    There is a semantic problem because differences between Python sequences
    and Haskell List.  Because of that ``L[1, 2]`` will pass a tuple to
    `__getitem__` magic, but ``L[1]`` will not.  To avoid, as much as
    possible, this issue related with two phrases with equivalent denotations,
    singular elements will be converted to lists.  The logic to test if a
    given value is singular is whether is not an instance of
    `~collections.Sequence`:class: or a string.  For example:

        >>> from hask3 import L
        >>> L[1] == L[[1]]
        True

    """

    invalid_syntax_message = "Invalid input to list constructor"

    def __getitem__(self, lst):
        from collections.abc import Sequence
        from hask3.hack import isin, is_iterator
        if isinstance(lst, tuple) and len(lst) < 5 and isin(Ellipsis, lst):
            # L[x, ...]
            if len(lst) == 2 and lst[1] is Ellipsis:
                return enumFrom(lst[0])
            # L[x, y, ...]
            elif len(lst) == 3 and lst[2] is Ellipsis:
                return enumFromThen(lst[0], lst[1])
            # L[x, ..., y]
            elif len(lst) == 3 and lst[1] is Ellipsis:
                return enumFromTo(lst[0], lst[2])
            # L[x, y, ..., z]
            elif len(lst) == 4 and lst[2] is Ellipsis:
                return enumFromThenTo(lst[0], lst[1], lst[3])
            else:
                raise SyntaxError("Invalid list comprehension: %s" % str(lst))
        elif is_iterator(lst) or isinstance(lst, List):
            return List(tail=lst)
        elif isinstance(lst, Sequence) and not isinstance(lst, str):
            return List(head=list(lst))
        else:
            return List(head=[lst])


del Sequence, objectify
del Typeclass, Hask, Show, Eq, Ord
del Syntax, instance, sig, H
