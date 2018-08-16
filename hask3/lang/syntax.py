import sys
from hask3.hack import objectify, settle_magic_methods
from hask3.lang.type_system import PatternMatchBind
from hask3.lang.type_system import PatternMatchListBind
from hask3.lang.type_system import Undefined

from hask3.lang.type_system import PyFunc as func    # noqa


# Main

# TODO: Try to use a metaclass in `Syntax`
@settle_magic_methods(lambda self, *args: self.__syntaxerr__())
class Syntax:
    """Base class for new syntactic constructs.

    All of the new "syntax" elements of Hask inherit from this class.

    By default, a piece of syntax will raise a syntax error with a standard
    error message if the syntax object is used with a Python builtin operator.

    Subclasses may override these methods to define what syntax is valid for
    those objects.

    """
    def __syntaxerr__(self):
        raise SyntaxError(self.invalid_syntax_message)


class instance(Syntax):
    """Special syntax for defining typeclass instances.

    Example usage::

        instance(Functor, Maybe).where(
            fmap = ...
        )

    """
    def __init__(self, typecls, cls):
        from hask3.hack import safe_issubclass
        from hask3.lang.type_system import Typeclass
        if safe_issubclass(typecls, Typeclass):
            self.typeclass = typecls
            self.cls = cls
        else:
            raise TypeError(f"{typecls} is not a type-class")

    def where(self, **kwargs):
        self.typeclass.make_instance(self.cls, **kwargs)


@objectify
class H(Syntax):
    """``H/`` creates a new function type signature.

    Examples::

        (H/ int >> int >> int)
        (H/ (H/ "a" >> "b" >> "c") >> "b" >> "a" >> "c")
        (H/ func >> set >> set)
        (H/ (H/ "a" >> "b") >> ["a"] >> ["b"])
        (H[(Eq, "a")]/ "a" >> ["a"] >> bool)
        (H/ int >> int >> t(Maybe, int))
        (H/ int >> None)

    See `sig`:class: for more information on type signature decorators.

    """

    invalid_syntax_message = "Syntax error in type signature"

    def __init__(self, constraints=None):
        from collections import defaultdict
        self.constraints = defaultdict(lambda: [])
        if constraints:
            if isinstance(constraints[0], tuple):    # multiple constraints
                for con in constraints:
                    self.__add_constraint(con)
            else:    # only one constraint
                self.__add_constraint(constraints)
        super().__init__()

    def __add_constraint(self, con):
        from hask3.hack import safe_issubclass
        from hask3.lang.type_system import Typeclass
        if len(con) != 2 or not isinstance(con, tuple):
            raise SyntaxError("Invalid typeclass constraint: %s" % str(con))
        elif not isinstance(con[1], str):
            raise SyntaxError("%s is not a type variable" % con[1])
        elif not safe_issubclass(con[0], Typeclass):
            raise SyntaxError("%s is not a typeclass" % con[0])
        else:
            self.constraints[con[1]].append(con[0])

    def __getitem__(self, constraints):
        return type(self)(constraints)

    def __truediv__(self, arg):
        return __signature__((), self.constraints) >> arg

    __div__ = __truediv__


class __signature__(Syntax):
    """A (complete or incomplete) type signature."""

    invalid_syntax_message = "Syntax error in type signature"

    def __init__(self, args, constraints):
        from hask3.lang.type_system import TypeSignature
        self.sig = TypeSignature(args, constraints)
        super().__init__()

    def __rshift__(self, arg):
        arg = __signature__._inner(arg)
        return __signature__(self.sig.args + (arg,), self.sig.constraints)

    def __rpow__(self, fn):
        return sig(self)(fn)

    @staticmethod
    def _inner(arg):
        return arg.sig if isinstance(arg, __signature__) else arg


# TODO: Improve function signatures logic.
#
# For example, when a predicate is applied to a lazy-list, first element of
# the list is gotten to test the compatibility of the types
class sig(Syntax):
    """Convert a Python function into a Statically Typed Function.

    Statically typed functions are represented by the class
    `~hask3.lang.type_system.TypedFunc`:class:.

    `TypedFunc` instances are automagically curried, and polymorphic type
    arguments will be inferred by the type system.

    Usage::

        @sig(H/ int >> int >> int)
        def add(x, y):
            return x + y

        @sig(H[(Show, "a")]/ >> "a" >> str)
        def to_str(x):
            return str(x)

    See `H`:obj: special object, and `t`:func: function for more information.

    """

    invalid_syntax_message = "Syntax error in type signature"

    def __init__(self, signature):
        from hask3.lang.type_system import build_sig, make_fn_type
        if isinstance(signature, __signature__):
            if len(signature.sig.args) >= 2:
                super().__init__()
                self.sig = signature.sig
                self.fn_args = fn_args = build_sig(self.sig)
                self.fn_type = make_fn_type(fn_args)
            else:
                raise SyntaxError("Not enough type arguments in signature")
        else:
            msg = f"Signature expected in sig(); found {signature}"
            raise SyntaxError(msg)

    def __str__(self):
        # TODO: f'sig({self.sig})'
        return str(self.sig)

    __repr__ = __str__

    def __call__(self, fn):
        from hask3.lang.type_system import TypedFunc
        res = TypedFunc(fn, self.fn_args, self.fn_type)
        res.haskell_sig = self
        return res


def t(tcon, *params):
    '''Helper to instantiate a higher-kinded type.

    :param tcon: type constructor.

    :param params: type parameter names.

    See `~hask3.lang.type_system.TypeSignatureHKT`:class: class.

    '''
    from hask3.hack import safe_issubclass
    from hask3.lang.type_system import ADT, TypeSignatureHKT
    if not safe_issubclass(tcon, ADT) or len(tcon.__params__) == len(params):
        return TypeSignatureHKT(tcon, list(map(__signature__._inner, params)))
    else:
        _msg = f"Incorrect number of type parameters to {tcon.__name__}"
        raise TypeError(_msg)


def typify(fn, hkt=None):
    """Convert an untyped Python function to a `TypedFunc`.

    :param fn: The function to wrap

    :param hkt: A higher-kinded type wrapped in a closure (e.g.,
               ``lambda x: t(Maybe, x)``)

    :returns: A `~hask3.lang.type_system.TypedFunc`:class: object with a
        polymorphic type (e.g. ``a -> b -> c``, etc) with the same number of
        arguments as `fn`.  If `hkt` is supplied, the return type will be the
        supplied HKT parameterized by a type variable.

    Example usage::

        @typify(hkt=lambda x: t(Maybe, x))
        def add(x, y):
            return x + y

    """
    A = ord('a')
    args = [chr(i) for i in range(A, A + fn.__code__.co_argcount + 1)]
    if hkt is not None:
        args[-1] = hkt(args[-1])
    return sig(__signature__(args, []))


@objectify
@settle_magic_methods(lambda self, *args: undefined)
class undefined(Undefined):
    """Undefined value with special syntactic powers.

    Whenever you try to use one if its magic methods, it returns
    undefined.  Used to prevent overzealous evaluation in pattern matching.

    Its type unifies with any other type.

    """
    pass


# Constructs for pattern matching.
# Note that the approach implemented here uses lots of global state and is
# pretty much the opposite of "functional" or "thread-safe."

class IncompletePatternError(Exception):
    pass


class MatchStackFrame:
    """One stack frame for pattern matching bound variable stack."""
    def __init__(self, value):
        self.value = value
        self.cache = {}
        self.matched = False


class MatchStack:
    """Stack for storing locally bound variables from matches."""
    from collections import deque
    __stack__ = deque()
    del deque

    @classmethod
    def push(cls, value):
        """Push a new frame onto the stack, representing a new case expr."""
        cls.__stack__.append(MatchStackFrame(value))

    @classmethod
    def pop(cls):
        """Pop the current frame off the stack."""
        cls.__stack__.pop()

    @classmethod
    def get_frame(cls):
        """Access the current frame."""
        return cls.__stack__[-1]

    @classmethod
    def get_name(cls, name):
        """Lookup a variable name in the current frame."""
        frm = cls.get_frame()
        return undefined if frm.matched else frm.cache.get(name, undefined)


@objectify
class m(Syntax):
    """``m.*`` binds a local variable while pattern matching.

    For example usage, see `caseof`:class:.

    """

    invalid_syntax_message = "Syntax error in pattern match"

    def __getattr__(self, name):
        return __pattern_bind__(name)

    def __call__(self, pattern):
        from hask3.lang.type_system import pattern_match
        is_match, env = pattern_match(MatchStack.get_frame().value, pattern)
        if is_match and not MatchStack.get_frame().matched:
            MatchStack.get_frame().cache = env
        return __match_test__(is_match)


@objectify
class p(Syntax):
    """``p.*`` accesses a local variable bound during pattern matching.

    For example usage, see `caseof`:class:.

    """

    invalid_syntax_message = "Syntax error in pattern match"

    def __getattr__(self, name):
        return MatchStack.get_name(name)


class __pattern_bind_list__(Syntax, PatternMatchListBind):
    """Represents a pattern designed to match a bind list.

    A bind list is any iterable, consisting of a head (one element) and a tail
    (zero to many elements).

    """

    invalid_syntax_message = "Syntax error in match"

    def __init__(self, head, tail):
        super().__init__([head], tail)

    def __rxor__(self, head):
        self.head.insert(0, head)
        return self


class __pattern_bind__(Syntax, PatternMatchBind):
    """A pattern designed to match any value and bind it to a name."""

    invalid_syntax_message = "Syntax error in match"

    def __rxor__(self, cell):
        return __pattern_bind_list__(cell, self)

    def __xor__(self, other):
        if isinstance(other, __pattern_bind_list__):
            return other.__rxor__(self)
        elif isinstance(other, __pattern_bind__):
            return __pattern_bind_list__(self, other)
        else:
            raise SyntaxError(self.invalid_syntax_message)


class __match_line__(Syntax):
    """One line of a caseof expression.

    i.e.: ``m( ... ) >> return_value``.

    """
    def __init__(self, is_match, return_value):
        self.is_match = is_match
        self.return_value = return_value


class __match_test__(Syntax):
    """The pattern part of one caseof line.

    i.e.: ``m( ... )``.

    """
    def __init__(self, is_match):
        self.is_match = is_match

    def __rshift__(self, value):
        MatchStack.get_frame().cache = {}
        return __match_line__(self.is_match, value)


class __unmatched_case__(Syntax):
    """An unmatched caseof expression in mid-evaluation.

    That is, when zero or more lines have been tested, but before a match has
    been found.

    """
    def __or__(self, line):
        if line.is_match:
            MatchStack.get_frame().matched = True
            return __matched_case__(line.return_value)
        return self

    def __invert__(self):
        value = MatchStack.get_frame().value
        MatchStack.pop()
        raise IncompletePatternError(value)


class __matched_case__(Syntax):
    """A matched caseof expression in mid-evaluation.

    When one or more lines have been tested and after a match has been found.

    """
    def __init__(self, return_value):
        self.value = return_value

    def __or__(self, line):
        return self

    def __invert__(self):
        MatchStack.pop()
        return self.value


class caseof(__unmatched_case__):
    """Pattern matching.

    Can be used to deconstruct lists and ADTs, and it is a very useful control
    flow tool.

    Usage::

        ~(caseof(value_to_match)
            | m(pattern_1) >> return_value_1
            | m(pattern_2) >> return_value_2
            | m(pattern_3) >> return_value_3)

    Example usage::

        @sig(H/ int >> int)
        def fib(x):
            return ~(caseof(x)
                        | m(0)   >> 1
                        | m(1)   >> 1
                        | m(m.n) >> fib(p.n - 1) + fib(p.n - 2))

    See `m`:obj: and `p`:obj: special pattern matching constructions.

    """
    def __init__(self, value):
        if isinstance(value, Undefined):
            return
        MatchStack.push(value)


# ADT creation syntax ("data" expressions)
# "data"/type constructor half of the expression


@objectify
class data(Syntax):
    """Syntax for defining Algebraic Data Types.

    Example usage::

        >>> from hask3 import data, d, deriving, Read, Show, Eq, Ord

        >>> Maybe, Nothing, Just = (
        ...     data.Maybe("a") == d.Nothing | d.Just("a") &
        ...     deriving(Read, Show, Eq, Ord)
        ...     )

    """

    invalid_syntax_message = "Syntax error in `data`"

    def __getattr__(self, value):
        if value[0].isupper():
            return __new_tcon_enum__(value)
        else:
            raise SyntaxError("Type constructor name must be capitalized")


class __new_tcon__(Syntax):
    """Base for Syntax classes related to creating new type constructors."""

    invalid_syntax_message = "Syntax error in `data`"

    def __init__(self, name, args=()):
        self.name = name
        self.args = args
        super().__init__()

    def __eq__(self, d):
        from hask3.lang.type_system import build_ADT
        # one data constructor, zero or more derived typeclasses
        if isinstance(d, __new_dcon__):
            return build_ADT(self.name, self.args, [(d.name, d.args)], d.classes)
        # one or more data constructors, zero or more derived typeclasses
        elif isinstance(d, __new_dcons_deriving__):
            return build_ADT(self.name, self.args, d.dcons, d.classes)
        else:
            raise SyntaxError(self.invalid_syntax_message)


class __new_tcon_enum__(__new_tcon__):
    """A `data` statement in mid evaluation.

    It represents the part of the expression that builds the type constructor,
    before type parameters have been added.

    Examples::

       data.Either
       data.Ordering

    """
    def __call__(self, *typeargs):
        count = len(typeargs)
        if count == 0:
            msg = f"Missing type arguments in statement: `data.{self.name}()`"
            raise SyntaxError(msg)
        elif count != len(set(typeargs)):
            raise SyntaxError("Type parameters are not unique")
        elif not all(type(arg) == str and arg.islower() for arg in typeargs):
            raise SyntaxError("Type parameters must be lowercase strings")
        else:
            return __new_tcon_hkt__(self.name, typeargs)


class __new_tcon_hkt__(__new_tcon__):
    """A `data` statement in mid evaluation.

    It represents the part of the expression that builds the type constructor,
    after type parameters have been added.

    Examples::

        data.Maybe("a")
        data.Either("a", "b")

    """
    pass


# "d"/data constructor half of the expression
@objectify
class d(Syntax):
    """Part of hask's special syntax for defining Algebraic Data Types.

    See `data`:obj: for more information.

    """

    invalid_syntax_message = "Syntax error in `d`"

    def __getattr__(self, value):
        if value[0].isupper():
            return __new_dcon_enum__(value)
        else:
            raise SyntaxError("Data constructor name must be capitalized")


class __new_dcon__(Syntax):
    """Base for Syntax objects that handle data constructor creation.

    That is within a `data` statment (`d.*`).

    """

    invalid_syntax_message = "Syntax error in `d`"

    def __init__(self, dcon_name, args=(), classes=()):
        self.name = dcon_name
        self.args = args
        self.classes = classes
        super().__init__()


class __new_dcon_params__(__new_dcon__):
    """Represents a `data` statement in mid evaluation.

    It represents the part of the expression that builds a data constructor,
    after type parameters have been added.

    Examples::

        d.Just("a")
        d.Foo(int, "a", "b", str)

    """
    def __and__(self, derive_exp):
        if isinstance(derive_exp, deriving):
            cls = __new_dcon_deriving__
            return cls(self.name, self.args, derive_exp.classes)
        else:
            raise SyntaxError(self.invalid_syntax_message)

    def __or__(self, dcon):
        if isinstance(dcon, __new_dcon__):
            constructors = ((self.name, self.args), (dcon.name, dcon.args))
            if isinstance(dcon, __new_dcon_deriving__):
                return __new_dcons_deriving__(constructors, dcon.classes)
            else:
                return __new_dcons__(constructors)
        else:
            raise SyntaxError(self.invalid_syntax_message)


class __new_dcon_deriving__(__new_dcon__):
    """Represents a `data` statement in mid evaluation.

    The part of the expression that builds a data constructor (with or without
    type parameters) and adds derived `~hask3.lang.typeclasses`:mod:.

    Examples::

        d.Just("a") & deriving(Show, Eq, Ord)
        d.Bar & deriving(Eq)

    """
    pass


class __new_dcon_enum__(__new_dcon_params__):
    """Represents a `data` statement in mid evaluation.

    The part of the expression that builds a data constructor, after type
    parameters have been added.

    Examples::

        d.Just
        d.Foo

    """
    def __call__(self, *typeargs):
        return __new_dcon_params__(self.name, typeargs)


class __new_dcons_deriving__(Syntax):
    """A `data` statement in mid evaluation.

    The part of the expression that builds data constructors (with or without
    type parameters) and adds derived `~hask3.lang.typeclasses`:mod:.

    Examples::

        d.Nothing | d.Just("a") & deriving(Show, Eq, Ord)
        d.Foo(int, "a", "b", str) | d.Bar & deriving(Eq)

    """

    invalid_syntax_message = "Syntax error in `d`"

    def __init__(self, data_consts, classes=()):
        self.dcons = data_consts
        self.classes = classes
        super().__init__()


class __new_dcons__(__new_dcons_deriving__):
    """A `data` statement in mid evaluation.

    The part of the expression that builds data constructors (with or without
    type parameters), with no derived `~hask3.lang.typeclasses`:mod:.

    Examples::

       d.Foo(int, "a", "b", str) | d.Bar

    """
    def __init__(self, data_consts):
        super().__init__(data_consts)

    def __or__(self, new_dcon):
        if isinstance(new_dcon, __new_dcon__):
            constructor = self.dcons + ((new_dcon.name, new_dcon.args), )
            if isinstance(new_dcon, __new_dcon_deriving__):
                return __new_dcons_deriving__(constructor, new_dcon.classes)
            else:
                return __new_dcons__(constructor)
        else:
            raise SyntaxError(self.invalid_syntax_message)


class deriving(Syntax):
    """Part of hask's special syntax for defining Algebraic Data Types.

    See `data`:obj: for more information.

    """

    invalid_syntax_message = "Syntax error in `deriving`"

    def __init__(self, *tclasses):
        from hask3.lang.type_system import Typeclass
        ok = lambda c: not issubclass(c, Typeclass)
        wrong = next((c for c in tclasses if ok(c)), None)
        if wrong is None:
            self.classes = tclasses
            super().__init__()
        else:
            raise TypeError(f"Cannot derive non-typeclass {wrong}")


@objectify
class __(Syntax):
    """This is Hask's special syntax for operator sections.

    It is a placeholder for arguments (operands).

    Example usage::

        >>> (__+1)(5)
        6

        >>> (6//__) * (__-1) % 4
        2

        >>> (__**__)(2, 10)
        1024

    Operators supported::

        + - * / // ** >> << | & ^ == != > >= < <=

    """

    invalid_syntax_message = "Error in section"

    @staticmethod
    def __make_section(fn):
        """Create an operator section from a binary operator."""
        def section_wrapper(self, y):
            if isinstance(y, type(__)):
                # double section, e.g. (__+__)
                @sig(H/ "a" >> "b" >> "c")
                def double_section(a, b):
                    return fn(a, b)
                return double_section
            else:
                # single section, e.g. (__+1) or (1+__)
                @sig(H/ "a" >> "b")
                def section(a):
                    return fn(a, y)
                return section
        return section_wrapper

    # TODO: Migrate next section methods definition into a class decorator

    # left section, e.g. (__+1)
    __wrap = __make_section.__func__

    # right section, e.g. (1+__)
    __flip = lambda f: lambda x, y: f(y, x)

    import operator

    __add__ = __wrap(operator.add)
    __sub__ = __wrap(operator.sub)
    __mul__ = __wrap(operator.mul)
    __truediv__ = __wrap(operator.truediv)
    __floordiv__ = __wrap(operator.floordiv)
    __mod__ = __wrap(operator.mod)
    __divmod__ = __wrap(divmod)
    __pow__ = __wrap(operator.pow)
    __lshift__ = __wrap(operator.lshift)
    __rshift__ = __wrap(operator.rshift)
    __or__ = __wrap(operator.or_)
    __and__ = __wrap(operator.and_)
    __xor__ = __wrap(operator.xor)

    __eq__ = __wrap(operator.eq)
    __ne__ = __wrap(operator.ne)
    __gt__ = __wrap(operator.gt)
    __lt__ = __wrap(operator.lt)
    __ge__ = __wrap(operator.ge)
    __le__ = __wrap(operator.le)

    __radd__ = __wrap(__flip(operator.add))
    __rsub__ = __wrap(__flip(operator.sub))
    __rmul__ = __wrap(__flip(operator.mul))
    __rtruediv__ = __wrap(__flip(operator.truediv))
    __rfloordiv__ = __wrap(__flip(operator.floordiv))
    __rmod__ = __wrap(__flip(operator.mod))
    __rdivmod__ = __wrap(__flip(divmod))
    __rpow__ = __wrap(__flip(operator.pow))
    __rlshift__ = __wrap(__flip(operator.lshift))
    __rrshift__ = __wrap(__flip(operator.rshift))
    __ror__ = __wrap(__flip(operator.or_))
    __rand__ = __wrap(__flip(operator.and_))
    __rxor__ = __wrap(__flip(operator.xor))

    del operator


# Guards! Guards!

# Unlike pattern matching, this approach is completely stateless and
# thread-safe. However, it has the pretty undesireable property that it cannot
# be used with recursive functions.


class NoGuardMatchException(Exception):
    pass


class c(Syntax):
    """A case in a guard.

    Creates a new condition that can be used in a guard expression.

    `otherwise`:obj: is a `guard`:class: condition that always evaluates to
    True.

    Usage::

        ~(guard(<expr to test>)
            | c(<test_fn_1>) >> <return_value_1>
            | c(<test_fn_2>) >> <return_value_2>
            | otherwise      >> <return_value_3>
        )

    """

    invalid_syntax_message = "Syntax error in guard condition"

    def __init__(self, fn):
        if callable(fn):
            self.__test = fn
            super().__init__()
        else:
            raise ValueError("Guard condition must be callable")

    def __rshift__(self, value):
        wrong_types = (type(self), __guard_conditional__, __guard_base__)
        if not isinstance(value, wrong_types):
            return __guard_conditional__(self.__test, value)
        else:
            raise SyntaxError(self.invalid_syntax_message)


class __guard_conditional__(Syntax):
    """One line of a guard expression.

    Consists of:

    1) a condition (a test function wrapped in c and a value to be returned
       if that condition is satisfied).

    2) a return value, which will be returned if the condition evaluates
       to True

    See `guard`:class: for more details.

    """

    invalid_syntax_message = "Syntax error in guard condition"

    def __init__(self, fn, return_value):
        self.check = fn
        self.return_value = return_value
        super().__init__()


class __guard_base__(Syntax):
    """Base for __unmatched_guard__ and __matched_guard__.

    Represent the internal state of a guard expression as it is being
    evaluated.

    See `guard`:class: for more details.

    """

    invalid_syntax_message = "Syntax error in guard"

    def __init__(self, value):
        self.value = value
        super().__init__()


class __unmatched_guard__(__guard_base__):
    """The state of a guard expression in mid-evaluation.

    Before one of the conditions in the expression has been satisfied.

    See `guard`:class: for more details.

    """
    def __or__(self, cond):
        # Consume the next line of the guard expression
        if isinstance(cond, type(c)):
            raise SyntaxError("Guard expression is missing return value")
        elif not isinstance(cond, __guard_conditional__):
            raise SyntaxError("Guard condition expected, got %s" % cond)
        # If the condition is satisfied, change the evaluation state to
        # __matched_guard__, setting the return value to the value provided on
        # the current line
        elif cond.check(self.value):
            return __matched_guard__(cond.return_value)
        # If the condition is not satisfied, continue on with the next line,
        # still in __unmatched_guard__ state with the return value not set
        else:
            return __unmatched_guard__(self.value)

    def __invert__(self):
        msg = f"No match found in guard({self.value})"
        raise NoGuardMatchException(msg)


class __matched_guard__(__guard_base__):
    """State of a guard expression in mid-evaluation.

    After one of the conditions in the expression has been satisfied.

    See `guard`:class: for more details.

    """
    def __or__(self, cond):
        # Consume the next line of the guard expression
        # Since a condition has already been satisfied, we can ignore the rest
        # of the lines in the guard expression
        if isinstance(cond, __guard_conditional__):
            return self
        else:
            raise SyntaxError(self.invalid_syntax_message)

    def __invert__(self):
        return self.value


class guard(__unmatched_guard__):
    """Special syntax for guard expression.

    Usage::

        ~(guard(<expr to test>)
            | c(<test_fn_1>) >> <return_value_1>
            | c(<test_fn_2>) >> <return_value_2>
            | otherwise      >> <return_value_3>
        )

    Examples::

        ~(guard(8)
             | c(lambda x: x < 5) >> "less than 5"
             | c(lambda x: x < 9) >> "less than 9"
             | otherwise          >> "unsure"
        )

        # Using guards with sections.
        # See help(__) for information on sections.
        ~(guard(20)
            | c(__ > 10)  >> 20
            | c(__ == 10) >> 10
            | c(__ > 5)   >> 5
            | otherwise   >> 0)

    :param value: the value being tested in the guard expression.

    :returns: the return value corresponding to the first matching condition.

    :raises: NoGuardMatchException (if no match is found).

    See `otherwise`:obj:, and `c`:class: special guards.

    """
    def __invert__(self):
        raise SyntaxError(self.invalid_syntax_message)


#: A special `c`:class: instance, used in a `guard`:class:, that evaluates to
#: True.
otherwise = c(lambda _: True)    # noqa


# REPL tools (:q, :t, :i)

def _q(status=None):
    """Shorthand for sys.exit() or exit() with no arguments.

    Equivalent to :q in Haskell.  Should only be used in the REPL.

    Usage:

        >>> _q()

    """
    from sys import exit
    try:
        exit(*([] if status is None else [status]))
    except BaseException as error:
        ipython = sys.modules.get('IPython.core.interactiveshell', None)
        if ipython is not None:
            print('System exit failed, trying IPython quit.')
            shell = ipython.InteractiveShell.instance()
            shell.ns_table['user_global']['exit']()
        else:
            raise


def _t(obj):
    """Returns a string representing the type of an object.

    Includes higher-kinded types and ADTs.  Equivalent to ``:t`` in Haskell.
    Meant to be used in the REPL, but might also be useful for debugging.

    :param obj: the object to inspect.

    :returns: A string representation of the type.

    Usage::

        >>> from hask3 import _t

        >>> _t(1)
        'int'

        >>> _t(Just("hello world"))
        '(Maybe str)'

    """
    from hask3.lang.type_system import typeof
    return str(typeof(obj))


def _i(obj):
    """Show information about an object.

    Equivalent to ``:i`` in Haskell or ``help(obj)`` in Python.  Should only
    be used in the REPL.

    :param obj: the object to inspect.

    Usage::

        >>> _i(Just("hello world"))
        ...

        >>> _i(Either)
        ...

    """
    help(obj)

    del sys, settle_magic_methods, objectify
