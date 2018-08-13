from hask3.lang.type_system import Typeclass
from hask3.lang.syntax import instance, sig, H


class Show(Typeclass):
    """Conversion of values to readable strings.

    Attributes:

    - ``__str__``
    - ``show``

    Minimal complete definition:

    - ``show``

    """
    @classmethod
    def make_instance(typeclass, cls, show):
        from hask3.hack import is_builtin
        from hask3.lang.type_system import build_instance
        __show__ = show ** (H/ "a" >> str)
        show = lambda self: __show__(self)

        build_instance(Show, cls, {"show": show})
        if not is_builtin(cls):
            cls.__repr__ = show
            cls.__str__ = show

    @classmethod
    def derive_instance(typeclass, cls):
        def show(self):
            from hask3.hack import nt_to_tuple
            klass = type(self)
            if len(klass._fields) == 0:
                return klass.__name__
            else:
                nt_tup = nt_to_tuple(self)
                if len(nt_tup) == 1:
                    tuple_str = f"({Show[nt_tup[0]].show(nt_tup[0])})"
                else:
                    tuple_str = Show[nt_tup].show(nt_tup)
                return f"{type(self).__name__}{tuple_str}"
        Show.make_instance(cls, show=show)


@sig(H/ "a" >> str)
def show(obj):
    """``show :: a -> str``

    Convert a value to a readable string.

    """
    return Show[obj].show(obj)


class Eq(Typeclass):
    """The Eq class defines equality (==) and inequality (!=).

    Attributes:

    - ``__eq__``
    - ``__ne__``

    Minimal complete definition:

    - ``eq``

    """
    @classmethod
    def make_instance(typeclass, cls, eq, ne=None):
        from hask3.hack import is_builtin
        from hask3.lang.type_system import build_instance

        def default_ne(self, other):
            return not eq(self, other)

        __eq__ = eq ** (H/ "a" >> "a" >> bool)
        __ne__ = (default_ne if ne is None else ne) ** (H/ "a" >> "a" >> bool)
        eq = lambda self, other: __eq__(self, other)
        ne = lambda self, other: __ne__(self, other)

        build_instance(Eq, cls, {"eq": eq, "ne": ne})
        if not is_builtin(cls):
            cls.__eq__ = eq
            cls.__ne__ = ne

    @classmethod
    def derive_instance(typeclass, cls):
        from hask3.hack import nt_to_tuple

        def __eq__(self, other):
            return (type(self) == type(other) and
                    nt_to_tuple(self) == nt_to_tuple(other))

        def __ne__(self, other):
            return not __eq__(self, other)

        Eq.make_instance(cls, eq=__eq__, ne=__ne__)


class Ord(Eq):
    """The `Ord` class is used for totally ordered datatypes.

    Instances of `Ord` can be derived for any user-defined datatype whose
    constituent types are in `Ord`.  The declared order of the constructors in
    the data declaration determines the ordering in derived `Ord` instances.
    The Ordering datatype allows a single comparison to determine the precise
    ordering of two objects.

    Dependencies:

    - `Eq`:class:

    Attributes: ``< <= > >=``

    Minimal complete definition: ``<``

    """
    @classmethod
    def make_instance(typeclass, cls, lt, le=None, gt=None, ge=None):
        from hask3.hack import is_builtin
        from hask3.lang.type_system import build_instance
        if le is None:
            le = lambda s, o: s.__lt__(o) or s.__eq__(o)
        if gt is None:
            gt = lambda s, o: not s.__lt__(o) and not s.__eq__(o)
        if ge is None:
            ge = lambda s, o: not s.__lt__(o) or s.__eq__(o)

        __lt__ = lt ** (H/ "a" >> "a" >> bool)
        __le__ = le ** (H/ "a" >> "a" >> bool)
        __gt__ = gt ** (H/ "a" >> "a" >> bool)
        __ge__ = ge ** (H/ "a" >> "a" >> bool)

        lt = lambda self, other: __lt__(self, other)
        le = lambda self, other: __le__(self, other)
        gt = lambda self, other: __gt__(self, other)
        ge = lambda self, other: __ge__(self, other)

        attrs = {"lt": lt, "le": le, "gt": gt, "ge": ge}
        build_instance(Ord, cls, attrs)
        if not is_builtin(cls):
            cls.__lt__ = lt
            cls.__le__ = le
            cls.__gt__ = gt
            cls.__ge__ = ge

    @classmethod
    def derive_instance(typeclass, cls):
        import operator

        def zip_cmp(self, other, fn):
            """Compare data constructor and all fields of two ADTs."""
            from hask3.hack import nt_to_tuple
            if self.__ADT_slot__ == other.__ADT_slot__:
                one = nt_to_tuple(self)
                if len(one) == 0:
                    return fn((), ())
                else:
                    return fn(one, nt_to_tuple(other))
            else:
                return fn(self.__ADT_slot__, other.__ADT_slot__)

        lt = lambda s, o: zip_cmp(s, o, operator.lt)
        le = lambda s, o: zip_cmp(s, o, operator.le)
        gt = lambda s, o: zip_cmp(s, o, operator.gt)
        ge = lambda s, o: zip_cmp(s, o, operator.ge)

        Ord.make_instance(cls, lt=lt, le=le, gt=gt, ge=ge)


class Bounded(Typeclass):
    """Used to name the upper and lower limits of a type.

    `Ord` is not a super-class of `Bounded` since types that are not totally
    ordered may also have upper and lower bounds.

    The Bounded class may be derived for any enumeration type; `minBound` is
    the first constructor listed in the data declaration and `maxBound` is the
    last.  `Bounded` may also be derived for single-constructor datatypes
    whose constituent types are in Bounded.

    Attributes:

    - ``minBound``
    - ``maxBound``

    Minimal complete definition:

    - ``minBound``
    - ``maxBound``

    """
    @classmethod
    def make_instance(typeclass, cls, minBound, maxBound):
        from hask3.lang.type_system import build_instance
        attrs = {"minBound": minBound, "maxBound": maxBound}
        build_instance(Bounded, cls, attrs)

    @classmethod
    def derive_instance(typeclass, cls):
        constructors = cls.__constructors__
        bad = next((c for c in constructors if not isinstance(c, cls)), None)
        if bad is None:
            maxBound = lambda s: constructors[0]
            minBound = lambda s: constructors[-1]
            Bounded.make_instance(cls, minBound=minBound, maxBound=maxBound)
        else:
            msg = f"Cannot derive Bounded; {bad.__name__} is not an enum"
            raise TypeError(msg)


class Read(Typeclass):
    """Parsing of Strings, producing values.

    Attributes:

    - ``read``

    Minimal complete definition:

    - ``read``

    """
    @classmethod
    def make_instance(typeclass, cls, read):
        from hask3.lang.type_system import build_instance
        build_instance(Read, cls, {"read": read})

    @classmethod
    def derive_instance(typeclass, cls):
        Read.make_instance(cls, read=eval)


instance(Show, str).where(show=str.__repr__)
instance(Show, int).where(show=int.__str__)
instance(Show, float).where(show=tuple.__str__)
instance(Show, complex).where(show=complex.__str__)
instance(Show, bool).where(show=bool.__str__)
instance(Show, list).where(show=list.__str__)
instance(Show, tuple).where(show=tuple.__str__)
instance(Show, set).where(show=set.__str__)
instance(Show, dict).where(show=dict.__str__)
instance(Show, frozenset).where(show=frozenset.__str__)
instance(Show, slice).where(show=slice.__str__)

instance(Eq, str).where(eq=str.__eq__, ne=str.__ne__)
instance(Eq, int).where(eq=int.__eq__, ne=int.__ne__)
instance(Eq, float).where(eq=float.__eq__, ne=float.__ne__)
instance(Eq, complex).where(eq=complex.__eq__, ne=complex.__ne__)
instance(Eq, bool).where(eq=bool.__eq__, ne=bool.__ne__)
instance(Eq, list).where(eq=list.__eq__, ne=list.__ne__)
instance(Eq, tuple).where(eq=tuple.__eq__, ne=tuple.__ne__)
instance(Eq, set).where(eq=set.__eq__, ne=set.__ne__)
instance(Eq, dict).where(eq=dict.__eq__, ne=dict.__ne__)
instance(Eq, frozenset).where(eq=frozenset.__eq__, ne=frozenset.__ne__)
instance(Eq, slice).where(eq=slice.__eq__, ne=slice.__ne__)
instance(Eq, type).where(eq=type.__eq__, ne=type.__ne__)

instance(Ord, str).where(lt=str.__lt__, le=str.__le__,
                         gt=str.__gt__, ge=str.__ge__)
instance(Ord, int).where(lt=int.__lt__, le=int.__le__,
                         gt=int.__gt__, ge=int.__ge__)
instance(Ord, float).where(lt=float.__lt__, le=float.__le__,
                           gt=float.__gt__, ge=float.__ge__)
instance(Ord, complex).where(lt=complex.__lt__, le=complex.__le__,
                             gt=complex.__gt__, ge=complex.__ge__)
instance(Ord, bool).where(lt=bool.__lt__, le=bool.__le__,
                          gt=bool.__gt__, ge=bool.__ge__)
instance(Ord, list).where(lt=list.__lt__, le=list.__le__,
                          gt=list.__gt__, ge=list.__ge__)
instance(Ord, tuple).where(lt=tuple.__lt__, le=tuple.__le__,
                           gt=tuple.__gt__, ge=tuple.__ge__)
instance(Ord, set).where(lt=set.__lt__, le=set.__le__,
                          gt=set.__gt__, ge=set.__ge__)
instance(Ord, dict).where(lt=dict.__lt__, le=dict.__le__,
                          gt=dict.__gt__, ge=dict.__ge__)
instance(Ord, frozenset).where(lt=frozenset.__lt__, le=frozenset.__le__,
                               gt=frozenset.__gt__, ge=frozenset.__ge__)
