from __future__ import division, print_function, absolute_import

from hask.lang.syntax import H
from hask.lang.syntax import sig
from hask.lang.syntax import t

from hask.Data.Eq import Eq
from hask.Data.Ord import Ord
from hask.Data.Ord import Ordering
from hask.Data.Num import Num
from hask.Data.Num import Integral
from hask.Data.Maybe import Maybe


@sig(H/ ["a"] >> "a")
def head(xs):
    """``head :: [a] -> a``

    Extract the first element of a list, which must be non-empty.

    """
    return xs[0]


@sig(H/ ["a"] >> "a")
def last(xs):
    """``last :: [a] -> a``

    Extract the last element of a list, which must be finite and non-empty.

    """
    return xs[-1]


@sig(H/ ["a"] >> ["a"])
def tail(xs):
    """``tail :: [a] -> [a]``

    Extract the elements after the head of a list, which must be non-empty.

    """
    if not null(xs):
        return xs[1:]
    else:
        raise IndexError("empty list")


@sig(H/ ["a"] >> ["a"])
def init(xs):
    """``init :: [a] -> [a]``

    Return all the elements of a list except the last one.  The list must be
    non-empty.

    """
    if not null(xs):
        return xs[:-1]
    else:
        raise IndexError("empty list")


@sig(H/ ["a"] >> t(Maybe, ("a", ["a"])))
def uncons(xs):
    """``uncons :: [a] -> Maybe (a, [a])``

    Decompose a list into its head and tail.  If the list is empty, returns
    Nothing.  If the list is non-empty, returns Just((x, xs)), where x is the
    head of the list and xs its tail.

    """
    from hask.Data.Maybe import Just, Nothing
    return Just((head(xs), tail(xs))) if not null(xs) else Nothing


@sig(H/ ["a"] >> bool)
def null(xs):
    """``null :: [a] -> bool``

    Test whether the structure is empty.

    """
    from hask.lang.syntax import caseof, m
    return ~(caseof(xs)
                | m(m.y ^ m.ys) >> False
                | m(m.ys)       >> True)


@sig(H/ ["a"] >> int)
def length(xs):
    """``length :: [a] -> int``

    Returns the size/length of a finite structure as an Int.  The default
    implementation is optimized for structures that are similar to cons-lists,
    because there is no general way to do better.

    """
    return len(xs)


@sig(H/ (H/ "a" >> "b") >> ["a"] >> ["b"])
def map(f, xs):
    """``map :: (a -> b) -> [a] -> [b]``

    Returns the list obtained by applying f to each element of xs.

    """
    from xoutil.future.itertools import map as imap
    from hask.lang.lazylist import L
    return L[imap(f, xs)]


@sig(H/ ["a"] >> ["a"])
def reverse(xs):
    """``reverse :: [a] -> [a]``

    Returns the elements of `xs` in reverse order.  `xs` must be finite.

    """
    from hask.lang.lazylist import L
    return L[reversed(xs)]


@sig(H/ "a" >> ["a"] >> ["a"])
def intersperse(x, xs):
    """``intersperse :: a -> [a] -> [a]``

    Takes an element and a list and intersperses that element between the
    elements of the list.

    """
    from hask.lang.lazylist import L

    def __intersperse(x, xs):
        for y in init(xs):
            yield y
            yield x
        yield last(xs)

    if null(xs):
        return xs
    else:
        return L[__intersperse(x, xs)]


@sig(H/ ["a"] >> [["a"]] >> ["a"])
def intercalate(xs, xss):
    """``intercalate :: [a] -> [[a]] -> [a]``

    Equivalent to ``concat(intersperse(xs, xss))``.  It inserts the list
    `xs` in between the lists in `xss` and concatenates the result.

    """
    return concat(intersperse(xs, xss))


@sig(H/ [["a"]] >> [["a"]])
def transpose(xs):
    """``transpose :: [[a]] -> [[a]]``

    Transposes the rows and columns of its argument.

    """
    from xoutil.future.itertools import zip as izip
    from hask.lang.lazylist import L
    return L[(L[x] for x in izip(*xs))]


@sig(H/ ["a"] >> [["a"]])
def subsequences(xs):
    """``subsequences :: [a] -> [[a]]``

    Returns the list of all subsequences of the argument.

    """
    import itertools
    from hask.lang.lazylist import L
    res = L[[L[[]]]]
    for r, _ in enumerate(xs):
        res += L[(L[x] for x in itertools.combinations(xs, r + 1))]
    return res


@sig(H/ ["a"] >> [["a"]])
def permutations(xs):
    """``permutations :: [a] -> [[a]]``

    Returns the list of all permutations of the argument.

    """
    import itertools
    from hask.lang.lazylist import L
    if null(xs):
        return L[[]]
    else:
        return L[(L[x] for x in itertools.permutations(xs))]


@sig(H/ (H/ "b" >> "a" >> "b") >> "a" >> ["a"] >> "b")
def foldl(f, z, xs):
    """``foldl :: (b -> a -> b) -> b -> [a] -> b``

    Applied to a binary operator, a starting value (typically the
    left-identity of the operator), and a list, reduces the list using the
    binary operator, from left to right.  The list must be finite.

    """
    from functools import reduce
    return reduce(f, xs, z)


@sig(H/ (H/ "b" >> "a" >> "b") >> "a" >> ["a"] >> "b")
def foldl_(f, z, xs):
    """``foldl_ :: (b -> a -> b) -> b -> [a] -> b``

    A strict version of `foldl`:func`.

    """
    return foldl(f, z, xs)


@sig(H/ (H/ "a" >> "a" >> "a") >> ["a"] >> "a")
def foldl1(f, xs):
    """``foldl1 :: (a -> a -> a) -> [a] -> a``

    A variant of `foldl`:func: that has no starting value argument, and thus
    must be applied to non-empty lists.

    """
    return foldl(f, xs[0], xs[1:])


@sig(H/ (H/ "a" >> "a" >> "a") >> ["a"] >> "a")
def foldl1_(f, xs):
    """``foldl1_ :: (a -> a -> a) -> [a] -> a``

    A strict version of `foldl1`:func:.

    """
    return foldl1(f, xs[0], xs[1:])


@sig(H/ (H/ "a" >> "b" >> "b") >> "a" >> ["a"] >> "b")
def foldr(f, z, xs):
    """``foldr :: (a -> b -> b) -> b -> [a] -> b``

    Applied to a binary operator, a starting value (typically the
    right-identity of the operator), and a list, reduces the list using the
    binary operator, from right to left.

    """
    from hask.lang.lazylist import L
    from hask.lang.syntax import caseof, m, p
    return ~(caseof(xs)
                | m(L[[]])     >> z
                | m(m.a ^ m.b) >> f(p.a, foldr(f, z, p.b)))


@sig(H/ (H/ "a" >> "a" >> "a") >> ["a"] >> "a")
def foldr1(f, xs):
    """``foldr1 :: (a -> a -> a) -> [a] -> a``

    A variant of `foldr`:func: that has no starting value argument, and thus
    must be applied to non-empty lists.

    """
    return foldr(f, xs[0], xs[1:])


@sig(H/ [["a"]] >> ["a"])
def concat(xss):
    """``concat :: [[a]] -> [a]``

    Concatenate a list of lists.

    """
    from hask.lang.lazylist import L
    return L[(x for xs in xss for x in xs)]


@sig(H/ (H/ "a" >> ["b"]) >> ["a"] >> ["b"])
def concatMap(f, xs):
    """``concatMap :: (a -> [b]) -> [a] -> [b]``

    Map a function over a list and concatenate the results.

    """
    return concat(map(f, xs))


@sig(H/ [bool] >> bool)
def and_(xs):
    """``and_ :: [Bool] -> Bool``

    Returns the conjunction of a Boolean list.  For the result to be True, the
    list must be finite; False, however, results from a False value at a
    finite index of a finite or infinite list.

    """
    return False not in xs


@sig(H/ [bool] >> bool)
def or_(xs):
    """``or_ :: [Bool] -> Bool``

    Returns the disjunction of a Boolean list.  For the result to be False,
    the list must be finite; True, however, results from a True value at a
    finite index of a finite or infinite list.

    """
    return True in xs


@sig(H/ (H/ "a" >> bool) >> ["a"] >> bool)
def any(p, xs):
    """``any :: (a -> Bool) -> [a] -> Bool``

    Applied to a predicate and a list, any determines if any element of the
    list satisfies the predicate.  For the result to be False, the list must
    be finite; True, however, results from a True value for the predicate
    applied to an element at a finite index of a finite or infinite list.

    """
    return True in ((p(x) for x in xs))


@sig(H/ (H/ "a" >> bool) >> ["a"] >> bool)
def all(p, xs):
    """``all :: (a -> Bool) -> [a] -> Bool``

    Applied to a predicate and a list, all determines if all elements of the
    list satisfy the predicate.  For the result to be True, the list must be
    finite; False, however, results from a False value for the predicate
    applied to an element at a finite index of a finite or infinite list.

    """
    return False not in ((p(x) for x in xs))


@sig(H[(Num, "a")]/ ["a"] >> "a")
def sum(xs):
    """``sum :: Num a => [a] -> a``

    The sum function computes the sum of a finite list of numbers.

    """
    from functools import reduce
    import operator
    return reduce(operator.add, xs, 0)


@sig(H[(Num, "a")]/ ["a"] >> "a")
def product(xs):
    """``product :: Num a => [a] -> a``

    The product function computes the product of a finite list of numbers.

    """
    from functools import reduce
    import operator
    return reduce(operator.mul, xs, 1)


@sig(H[(Ord, "a")]/ ["a"] >> "a")
def minimum(xs):
    """``minimum :: Ord a => [a] -> a``

    Returns the minimum value from a list, which must be non-empty, finite,
    and of an ordered type.  It is a special case of minimumBy, which allows
    the programmer to supply their own comparison function.

    """
    return min(xs)


@sig(H[(Ord, "a")]/ ["a"] >> "a")
def maximum(xs):
    """``maximum :: Ord a => [a] -> a``

    Returns the maximum value from a list, which must be non-empty, finite,
    and of an ordered type.  It is a special case of maximumBy, which allows
    the programmer to supply their own comparison function.

    """
    return max(xs)


@sig(H/ (H/ "b" >> "a" >> "b") >> "b" >> ["a"] >> ["b"])
def scanl(f, z, xs):
    """``scanl :: (b -> a -> b) -> b -> [a] -> [b]``

    Similar to `foldl`:func:, but returns a list of successive reduced values
    from the left.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> "a" >> "a") >> ["a"] >> ["a"])
def scanl1(f, xs):
    """``scanl1 :: (a -> a -> a) -> [a] -> [a]``

    A variant of `scanl`:func: that has no starting value argument.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> "a" >> "b") >> "b" >> ["a"] >> ["b"])
def scanr(f, z, xs):
    """``scanr :: (a -> b -> b) -> b -> [a] -> [b]``

    The right-to-left dual of `scanl`:func:.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> "a" >> "a") >> ["a"] >> ["a"])
def scanr1(f, xs):
    """``scanr1 :: (a -> a -> a) -> [a] -> [a]``

    A variant of `scanr`:func: that has no starting value argument.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> "x" >> ("a", "y")) >> "a" >> ["x"] >> ("a", ["y"]))
def mapAccumL(xs):
    """``mapAccumL :: (a -> x -> (a, y)) -> a -> [x] -> (a, [y])``

    Behaves like a combination of `map`:func: and `foldl`:func:; it applies a
    function to each element of a list, passing an accumulating parameter from
    left to right, and returning a final value of this accumulator together
    with the new list.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> "x" >> ("a", "y")) >> "a" >> ["x"] >> ("a", ["y"]))
def mapAccumR(xs):
    """``mapAccumR :: (acc -> x -> (acc, y)) -> acc -> [x] -> (acc, [y])``

    Behaves like a combination of `map`:func: and `foldr`:func:; it applies a
    function to each element of a list, passing an accumulating parameter from
    right to left, and returning a final value of this accumulator together
    with the new list.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> "a") >> "a" >> ["a"])
def iterate(f, x):
    """``iterate :: (a -> a) -> a -> [a]``

    Returns an infinite list of repeated applications of `f` to `x`\ ::

      iterate(f, x) == [x, f(x), f(f(x)), ...]

    """
    from hask.lang.lazylist import L

    def __iterate(f, x):
        while True:
            yield x
            x = f(x)

    return L[__iterate(f, x)]


@sig(H/ "a" >> ["a"])
def repeat(x):
    """``repeat :: a -> [a]``

    Infinite list, with x the value of every element.

    """
    import itertools
    from hask.lang.lazylist import L
    return L[itertools.repeat(x)]


@sig(H/ int >> "a" >> ["a"])
def replicate(n, x):
    """``replicate :: Int -> a -> [a]``

    A list of length `n` with `x` the value of every element.

    """
    import itertools
    from hask.lang.lazylist import L
    return L[itertools.repeat(x, n)]


@sig(H/ ["a"] >> ["a"])
def cycle(x):
    """``cycle :: [a] -> [a]``

    Ties a finite list into a circular one, or equivalently, the infinite
    repetition of the original list.  It is the identity on infinite lists.

    """
    import itertools
    from hask.lang.lazylist import L
    return L[itertools.cycle(x)]


@sig(H/ (H/ "b" >> t(Maybe, ("a", "b"))) >> "b" >> ["a"])
def unfoldr(f, x):
    """``unfoldr :: (b -> Maybe (a, b)) -> b -> [a]``

    Dual to `foldr`:func:\ : while `foldr`:func: reduces a list to a summary
    value, this one builds a list from a seed value.  The function takes the
    element and returns `Nothing` if it is done producing the list or returns
    ``Just (a, b)``, in which case, `a` is prepended to the list and `b` is
    used as the next element in a recursive call.

    """
    from hask.lang.lazylist import L
    from hask.Data.Maybe import Nothing
    y = f(x)
    if y == Nothing:
        return L[[]]
    else:
        return y[0][0] ^ unfoldr(f, y[0][1])


@sig(H/ int >> ["a"] >> ["a"])
def take(n, xs):
    """``take :: Int -> [a] -> [a]``

    Applied to a list, returns the prefix of `xs` of length `n`, or `xs`
    itself if ``n > length xs``.

    """
    return xs[:n]


@sig(H/ int >> ["a"] >> ["a"])
def drop(n, xs):
    """``drop :: Int -> [a] -> [a]``

    Returns the suffix of list `xs` after the first `n` elements, or `[]` if
    ``n > length xs``.

    """
    return xs[n:]


@sig(H/ int >> ["a"] >> (["a"], ["a"]))
def splitAt(n, xs):
    """``splitAt :: Int -> [a] -> ([a], [a])``

    Returns a tuple where first element is `xs` prefix of length `n` and
    second element is the remainder of the list.

    """
    return xs[:n], xs[n:]


@sig(H/ (H/ "a" >> bool) >> ["a"] >> ["a"])
def takeWhile(p, xs):
    """``takeWhile :: (a -> Bool) -> [a] -> [a]``

    Returns the longest prefix (possibly empty) of the list `xs` of elements
    that satisfy predicate `p`.

    """
    import itertools
    from hask.lang.lazylist import L
    return L[itertools.takewhile(p, xs)]


@sig(H/ (H/ "a" >> bool) >> ["a"] >> ["a"])
def dropWhile(p, xs):
    """``dropWhile :: (a -> Bool) -> [a] -> [a]``

    Returns the suffix remaining after ``takeWhile(p, xs)``.

    """
    import itertools
    from hask.lang.lazylist import L
    return L[itertools.dropwhile(p, xs)]


@sig(H/ (H/ "a" >> bool) >> ["a"] >> ["a"])
def dropWhileEnd(p, xs):
    """``dropWhileEnd :: (a -> Bool) -> [a] -> [a]``

    Drops the largest suffix of a list in which the given predicate holds for
    all elements.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> bool)  >> ["a"] >> (["a"], ["a"]))
def span(p, xs):
    """``span :: (a -> Bool) -> [a] -> ([a], [a])``

    Returns a tuple where first element is longest prefix (possibly empty) of
    list `xs` of elements that satisfy predicate `p` and second element is the
    remainder of the list.

    """
    front = takeWhile(p, xs)
    rest = xs[len(front):]
    return front, rest


@sig(H/ (H/ "a" >> bool)  >> ["a"] >> (["a"], ["a"]))
def break_(p, xs):
    """``break :: (a -> Bool) -> [a] -> ([a], [a])``

    Returns a tuple where first element is longest prefix (possibly empty) of
    list `xs` of elements that do not satisfy predicate `p` and second element
    is the remainder of the list.

    """
    from hask.lang.syntax import H
    inv = (lambda x: not p(x)) ** (H/ "a" >> bool)
    return span(inv, xs)


@sig(H[(Eq, "a")]/ ["a"] >> ["a"] >> t(Maybe, ["a"]))
def stripPrefix(xs, ys):
    """``stripPrefix :: Eq a => [a] -> [a] -> Maybe [a]``

    Drops the given prefix from a list.  It returns `Nothing` if the list
    did not start with the prefix given, or `Just` the list after the
    prefix, if it does.

    """
    from hask.Data.Maybe import Just, Nothing
    return Just(ys[len(xs)]) if isPrefixOf(xs, ys) else Nothing


@sig(H[(Eq, "a")]/ ["a"] >> [["a"]])
def group(xs):
    """``group :: Eq a => [a] -> [[a]]``

    Takes a list and returns a list of lists such that the concatenation of
    the result is equal to the argument.  Moreover, each sublist in the result
    contains only equal elements.  It is a special case of `groupBy`:func:,
    which allows the programmer to supply their own equality test.

    """
    from hask.lang.syntax import __
    return groupBy(xs, (__==__))


@sig(H/ ["a"] >> [["a"]])
def inits(xs):
    """``inits :: [a] -> [[a]]``

    Returns all initial segments of the argument, shortest first.

    """
    from hask.lang.lazylist import L
    if null(xs):
        return L[[xs]]
    else:
        return L[[L[[]]]] + L[(xs[:n + 1] for n, _ in enumerate(xs))]


@sig(H/ ["a"] >> [["a"]])
def tails(xs):
    """``tails :: [a] -> [[a]]``

    Returns all final segments of the argument, longest first.

    """
    from hask.lang.lazylist import L
    if null(xs):
        return L[[L[[]]]]
    else:
        return L[(xs[n:] for n, _ in enumerate(xs))] + L[[L[[]]]]


@sig(H[(Eq, "a")]/ ["a"] >> ["a"] >> bool)
def isPrefixOf(xs, ys):
    """``isPrefixOf :: Eq a => [a] -> [a] -> Bool``

    Returns True if the first list is a prefix of the second.

    """
    return xs == ys[:len(xs)]


@sig(H[(Eq, "a")]/ ["a"] >> ["a"] >> bool)
def isSuffixOf(xs, ys):
    """``isSuffixOf :: Eq a => [a] -> [a] -> Bool``

    Returns True if the first list is a suffix of the second.  The second list
    must be finite.

    """
    return xs == ys[-len(xs):]


@sig(H[(Eq, "a")]/ ["a"] >> ["a"] >> bool)
def isInfixOf(xs, ys):
    """``isInfixOf :: Eq a => [a] -> [a] -> Bool``

    Returns True if the first list is contained, wholly and intact, anywhere
    within the second.

    """
    return any(isPrefixOf(xs), tails(ys))


@sig(H[(Eq, "a")]/ ["a"] >> ["a"] >> bool)
def isSubsequenceOf(x, y):
    """``isSubsequenceOf :: Eq a => [a] -> [a] -> Bool``

    Returns True if the first list is a subsequence of the second list.

    isSubsequenceOf(x, y) is equivalent to elem(x, subsequences(y))

    """
    return elem(x, subsequences(y))


@sig(H[(Eq, "a")]/ "a" >> ["a"] >> bool)
def elem(x, xs):
    """``elem :: Eq a => a -> [a] -> Bool``

    List membership predicate, ``elem(x, xs)``.  For the result to be False,
    the list must be finite; True, however, results from an element equal to
    `x` found at a finite index of a finite or infinite list.

    """
    return x in xs


@sig(H[(Eq, "a")]/ "a" >> ["a"] >> bool)
def notElem(x, xs):
    """``notElem :: Eq a => a -> [a] -> Bool``

    The negation of `elem`:func:.

    """
    return not elem(x, xs)


@sig(H[(Eq, "a")]/ "a" >> [("a", "b")] >> t(Maybe, "b"))
def lookup(key, assocs):
    """``lookup :: Eq a => a -> [(a, b)] -> Maybe b``

    Looks up a key in an association list.

    """
    from hask.Data.Maybe import Just, Nothing
    return next((Just(value) for k, value in assocs if k == key), Nothing)


@sig(H/ (H/ "a" >> bool) >> ["a"] >> t(Maybe, "a"))
def find(p, xs):
    """``find :: (a -> Bool) -> [a] -> Maybe a``

    Returns the left-most element of the list matching the predicate, or
    `Nothing` if there is no such element.

    """
    from hask.Data.Maybe import Just, Nothing
    return next((Just(x) for x in xs if p(x)), Nothing)


@sig(H/ (H/ "a" >> bool) >> ["a"] >> ["a"])
def filter(p, xs):
    """``filter :: (a -> Bool) -> [a] -> [a]``

    Returns the list of those elements that satisfy the predicate `p`.

    """
    from hask.lang.lazylist import L
    return L[(x for x in xs if p(x))]


@sig(H/ (H/ "a" >> bool) >> ["a"] >> (["a"], ["a"]))
def partition(p, xs):
    """``partition :: (a -> Bool) -> [a] -> ([a], [a])``

    Returns the pair of lists of elements which do and do not satisfy the
    predicate `p`.

    """
    import itertools
    from hask.lang.lazylist import L
    yes, no = itertools.tee(xs)
    return L[(x for x in yes if p(x))], L[(x for x in no if not p(x))]


@sig(H[(Eq, "a")]/ "a" >> ["a"] >> t(Maybe, int))
def elemIndex(x, xs):
    """``elemIndex :: Eq a => a -> [a] -> Maybe Int``

    Returns the index of the first element in the given list which is equal
    (by ``==``) to the query element, or `Nothing` if there is no such
    element.

    """
    from hask.Data.Maybe import Just, Nothing
    return next((Just(i) for i, a in enumerate(xs) if a == x), Nothing)


@sig(H[(Eq, "a")]/ "a" >> ["a"] >> [int])
def elemIndices(x, xs):
    """``elemIndices :: Eq a => a -> [a] -> [Int]``

    Extends `elemIndex`:func:, by returning the indices of all elements equal
    to the query element, in ascending order.

    """
    from hask.lang.lazylist import L
    return L[(i for i, a in enumerate(xs) if a == x)]


@sig(H/ (H/ "a" >> bool) >> ["a"] >> t(Maybe, int))
def findIndex(p, xs):
    """``findIndex :: (a -> Bool) -> [a] -> Maybe Int``

    Returns the index of the first element in the list `xs` satisfying the
    predicate `p`, or `Nothing` if there is no such element.

    """
    from hask.Data.Maybe import Just, Nothing
    return next((Just(i) for i, a in enumerate(xs) if p(a)), Nothing)


@sig(H/ (H/ "a" >> bool) >> ["a"] >> [int])
def findIndicies(p, xs):
    """``findIndices :: (a -> Bool) -> [a] -> [Int]``

    Extends `findIndex`:func:, by returning the indices of all elements
    satisfying the predicate `p`, in ascending order.

    """
    from hask.lang.lazylist import L
    return L[(i for i, x in enumerate(xs) if p(x))]


@sig(H/ ["a"] >> ["b"] >> [("a", "b")])
def zip(xs, ys):
    """``zip :: [a] -> [b] -> [(a, b)]``

    Takes two lists and returns a list of corresponding pairs.  If one input
    list is short, excess elements of the longer list are discarded.

    """
    from xoutil.future.itertools import zip as izip
    from hask.lang.lazylist import L
    return L[izip(xs, ys)]


@sig(H/ ["a"] >> ["b"] >> ["c"] >> [("a", "b", "c")])
def zip3(a, b, c):
    """``zip3 :: [a] -> [b] -> [c] -> [(a, b, c)]``

    Takes three lists and returns a list of triples, analogous to `zip`:func:.

    """
    from xoutil.future.itertools import zip as izip
    from hask.lang.lazylist import L
    return L[izip(a, b, c)]


@sig(H/ ["a"] >> ["b"] >> ["c"] >> ["d"] >> [("a", "b", "c", "d")])
def zip4(a, b, c, d):
    """``zip4 :: [a] -> [b] -> [c] -> [d] -> [(a, b, c, d)]``

    Takes four lists and returns a list of quadruples, analogous to `zip`:func:.

    """
    from xoutil.future.itertools import zip as izip
    from hask.lang.lazylist import L
    return L[izip(a, b, c, d)]


@sig(H/ ["a"] >> ["b"] >> ["c"] >> ["d"] >> ["e"] >>
        [("a", "b", "c", "d", "e")])
def zip5(a, b, c, d, e):
    """``zip5 :: [a] -> [b] -> [c] -> [d] -> [e] -> [(a, b, c, d, e)]``

    Takes five lists and returns a list of five-tuples, analogous to
    `zip`:func:.

    """
    from xoutil.future.itertools import zip as izip
    from hask.lang.lazylist import L
    return L[izip(a, b, c, d, e)]


@sig(H/ ["a"] >> ["b"] >> ["c"] >> ["d"] >> ["e"] >> ["f"] >>
        [("a", "b", "c", "d", "e", "f")])
def zip6(a, b, c, d, e, f):
    """``zip6 :: [a] -> [b] -> [c] -> [d] -> [e] -> [f] -> [(a, b, c, d, e, f)]``

    Takes six lists and returns a list of six-tuples, analogous to `zip`:func:.

    """
    from xoutil.future.itertools import zip as izip
    from hask.lang.lazylist import L
    return L[izip(a, b, c, d, e, f)]


@sig(H/ ["a"] >> ["b"] >> ["c"] >> ["d"] >> ["e"] >> ["f"] >> ["g"] >>
        [("a", "b", "c", "d", "e", "f", "g")])
def zip7(a, b, c, d, e, f, g):
    """``zip7 :: [a] -> [b] -> [c] -> [d] -> [e] -> [f] -> [g] -> [(a, b, c, d, e, f, g)]``

    Takes seven lists and returns a list of seven-tuples, analogous to
    `zip`:func:.

    """
    from xoutil.future.itertools import zip as izip
    from hask.lang.lazylist import L
    return L[izip(a, b, c, d, e, f, g)]


@sig(H/ (H/ "a" >> "b" >> "c") >> ["a"] >> ["b"] >> ["c"])
def zipWith(fn, xs, ys):
    """``zipWith :: (a -> b -> c) -> [a] -> [b] -> [c]``

    Generalises `zip`:func: by zipping with the function given as the first
    argument, instead of a tupling function.  For example, ``zipWith (+)`` is
    applied to two lists to produce the list of corresponding sums.

    """
    from hask.lang.lazylist import L
    return L[(fn(*s) for s in zip(xs, ys))]


@sig(H/ (H/ "a" >> "b" >> "c" >> "d") >> ["a"] >> ["b"] >> ["c"] >> ["d"])
def zipWith3(fn, a, b, c):
    """``zipWith3 :: (a -> b -> c -> d) -> [a] -> [b] -> [c] -> [d]``

    Takes a function which combines three elements, as well as three lists and
    returns a list of their point-wise combination, analogous to
    `zipWith`:func:.

    """
    from hask.lang.lazylist import L
    return L[(fn(*s) for s in zip3(a, b, c))]


@sig(H/ (H/ "a" >> "b" >> "c" >> "d" >> "e") >>
        ["a"] >> ["b"] >> ["c"] >> ["d"] >> ["e"])
def zipWith4(fn, a, b, c, d):
    """``zipWith4 :: (a -> b -> c -> d -> e) -> [a] -> [b] -> [c] -> [d] -> [e]``

    Takes a function which combines four elements, as well as four lists and
    returns a list of their point-wise combination, analogous to
    `zipWith`:func:.

    """
    from hask.lang.lazylist import L
    return L[(fn(*s) for s in zip4(a, b, c, d))]


@sig(H/ (H/ "a" >> "b" >> "c" >> "d" >> "e" >> "f") >>
        ["a"] >> ["b"] >> ["c"] >> ["d"] >> ["e"] >> ["f"])
def zipWith5(fn, a, b, c, d, e):
    """``zipWith5 :: (a -> b -> c -> d -> e -> f) -> [a] -> [b] -> [c] -> [d] -> [e] -> [f]``

    Takes a function which combines five elements, as well as five lists and
    returns a list of their point-wise combination, analogous to
    `zipWith`:func:.

    """
    from hask.lang.lazylist import L
    return L[(fn(*s) for s in zip5(a, b, c, d, e))]


@sig(H/ (H/ "a" >> "b" >> "c" >> "d" >> "e" >> "f" >> "g") >>
        ["a"] >> ["b"] >> ["c"] >> ["d"] >> ["e"] >> ["f"] >> ["g"])
def zipWith6(fn, a, b, c, d, e, f):
    """``zipWith6 :: (a -> b -> c -> d -> e -> f -> g) -> [a] -> [b] -> [c] -> [d] -> [e] -> [f] -> [g]``

    Takes a function which combines six elements, as well as six lists and
    returns a list of their point-wise combination, analogous to
    `zipWith`:func:.

    """
    from hask.lang.lazylist import L
    return L[(fn(*s) for s in zip6(a, b, c, d, e, f))]


@sig(H/ (H/ "a" >> "b" >> "c" >> "d" >> "e" >> "f" >> "g" >> "h") >>
        ["a"] >> ["b"] >> ["c"] >> ["d"] >> ["e"] >> ["f"] >> ["g"] >> ["h"])
def zipWith7(fn, a, b, c, d, e, f):
    """``zipWith7 :: (a -> b -> c -> d -> e -> f -> g -> h) -> [a] -> [b] -> [c] -> [d] -> [e] -> [f] -> [g] -> [h]``

    Takes a function which combines seven elements, as well as seven lists and
    returns a list of their point-wise combination, analogous to
    `zipWith`:func:.

    """
    from hask.lang.lazylist import L
    return L[(fn(*s) for s in zip7(a, b, c, d, e, f))]


@sig(H/ [("a", "b")] >> (["a"], ["b"]))
def unzip(xs):
    """``unzip :: [(a, b)] -> ([a], [b])``

    Transforms a list of pairs into a list of first components and a list of
    second components.

    """
    from hask.lang.lazylist import L
    a = L[(i[0] for i in xs)]
    b = L[(i[1] for i in xs)]
    return a, b


@sig(H/ [("a", "b", "c")] >> (["a"], ["b"], ["c"]))
def unzip3(xs):
    """``unzip3 :: [(a, b, c)] -> ([a], [b], [c])``

    Takes a list of triples and returns three lists, analogous to
    `unzip`:func:.

    """
    from hask.lang.lazylist import L
    a = L[(i[0] for i in xs)]
    b = L[(i[1] for i in xs)]
    c = L[(i[2] for i in xs)]
    return a, b, c


@sig(H/ [("a", "b", "c", "d")] >> (["a"], ["b"], ["c"], ["d"]))
def unzip4(xs):
    """``unzip4 :: [(a, b, c, d)] -> ([a], [b], [c], [d])``

    Takes a list of quadruples and returns four lists, analogous to
    `unzip`:func:.

    """
    from hask.lang.lazylist import L
    a = L[(i[0] for i in xs)]
    b = L[(i[1] for i in xs)]
    c = L[(i[2] for i in xs)]
    d = L[(i[3] for i in xs)]
    return a, b, c, d


@sig(H/ [("a", "b", "c", "d", "e")] >> (["a"], ["b"], ["c"], ["d"], ["e"]))
def unzip5(xs):
    """``unzip5 :: [(a, b, c, d, e)] -> ([a], [b], [c], [d], [e])``

    Takes a list of five-tuples and returns five lists, analogous to
    `unzip`:func:.

    """
    from hask.lang.lazylist import L
    a = L[(i[0] for i in xs)]
    b = L[(i[1] for i in xs)]
    c = L[(i[2] for i in xs)]
    d = L[(i[3] for i in xs)]
    e = L[(i[4] for i in xs)]
    return a, b, c, d, e


@sig(H/ [("a", "b", "c", "d", "e", "f")]
        >> (["a"], ["b"], ["c"], ["d"], ["e"], ["f"]))
def unzip6(xs):
    """``unzip6 :: [(a, b, c, d, e, f)] -> ([a], [b], [c], [d], [e], [f])``

    Takes a list of six-tuples and returns six lists, analogous to
    `unzip`:func:.

    """
    from hask.lang.lazylist import L
    a = L[(i[0] for i in xs)]
    b = L[(i[1] for i in xs)]
    c = L[(i[2] for i in xs)]
    d = L[(i[3] for i in xs)]
    e = L[(i[4] for i in xs)]
    f = L[(i[5] for i in xs)]
    return a, b, c, d, e, f


@sig(H/ [("a", "b", "c", "d", "e", "f", "g")]
        >> (["a"], ["b"], ["c"], ["d"], ["e"], ["f"], ["g"]))
def unzip7(xs):
    """``unzip7 :: [(a, b, c, d, e, f, g)] -> ([a], [b], [c], [d], [e], [f], [g])``

    Takes a list of seven-tuples and returns seven lists, analogous to
    `unzip`:func:.

    """
    from hask.lang.lazylist import L
    a = L[(i[0] for i in xs)]
    b = L[(i[1] for i in xs)]
    c = L[(i[2] for i in xs)]
    d = L[(i[3] for i in xs)]
    e = L[(i[4] for i in xs)]
    f = L[(i[5] for i in xs)]
    g = L[(i[6] for i in xs)]
    return a, b, c, d, e, f, g


from hask.Data.String import lines  # noqa
from hask.Data.String import words  # noqa
from hask.Data.String import unlines  # noqa
from hask.Data.String import unwords  # noqa


@sig(H[(Eq, "a")]/ ["a"] >> ["a"])
def nub(xs):
    """``nub :: Eq a => [a] -> [a]``

    Removes duplicate elements from a list `xs`.  In particular, it keeps only
    the first occurrence of each element.  (The name nub means essence.)  It
    is a special case of `nubBy`:func:, which allows the programmer to supply
    their own equality test.

    """
    from hask.lang.lazylist import L
    return L[(i for i in set(xs))]


@sig(H[(Eq, "a")]/ "a" >> ["a"] >> ["a"])
def delete(x, xs):
    """``delete :: Eq a => a -> [a] -> [a]``

    Removes the first occurrence of `x` from its list argument.

    It is a special case of `deleteBy`:func:, which allows the programmer to
    supply their own equality test.

    """
    raise NotImplementedError()


@sig(H[(Eq, "a")]/ ["a"] >> ["a"] >> ["a"])
def diff(xs, ys):
    """``diff :: :: Eq a => [a] -> [a] -> [a]``

    List difference.

    """
    raise NotImplementedError()


@sig(H[(Eq, "a")]/ ["a"] >> ["a"] >> ["a"])
def union(xs, ys):
    """``union :: Eq a => [a] -> [a] -> [a]``

    Returns the list union of the two lists.

    Duplicates, and elements of the first list, are removed from the the
    second list, but if the first list contains duplicates, so will the
    result.  It is a special case of `unionBy`:func:, which allows the
    programmer to supply their own equality test.

    """
    raise NotImplementedError()


@sig(H[(Eq, "a")]/ ["a"] >> ["a"] >> ["a"])
def intersect(xs, ys):
    """``intersect :: Eq a => [a] -> [a] -> [a]``

    Takes the list intersection of two lists.  It is a special case of
    `intersectBy`:func:, which allows the programmer to supply their own
    equality test.  If the element is found in both the first and the second
    list, the element from the first list will be used.

    """
    raise NotImplementedError()


@sig(H[(Ord, "a")]/ ["a"] >> ["a"])
def sort(xs):
    """``sort :: Ord a => [a] -> [a]``

    Implements a stable sorting algorithm.  It is a special case of
    `sortBy`:func:, which allows the programmer to supply their own comparison
    function.

    .. note:: Current implementation is not lazy

    """
    from hask.lang.lazylist import L
    return L[sorted(xs)]


@sig(H[(Ord, "b")]/ (H/ "a" >> "b") >> ["a"] >> ["a"])
def sortOn(f, xs):
    """``sortOn :: Ord b => (a -> b) -> [a] -> [a]``

    Sort a list by comparing the results of a key function applied to each
    element.

    .. note:: Current implementation is not lazy

    """
    raise NotImplementedError()


@sig(H[(Ord, "a")]/ "a" >> ["a"] >> ["a"])
def insert(x, xs):
    """``insert :: Ord a => a -> [a] -> [a]``

    Takes an element and a list and inserts the element into the list at the
    first position where it is less than or equal to the next element.  In
    particular, if the list is sorted before the call, the result will also be
    sorted.

    """
    from hask.lang.lazylist import L

    def __insert(x, xs):
        for i in xs:
            if i > x:
                yield x
            yield i

    return L[__insert(x, xs)]


@sig(H/ (H/ "a" >> "a" >> bool) >> ["a"] >> ["a"])
def nubBy(f, xs):
    """``nubBy :: (a -> a -> Bool) -> [a] -> [a]``

    Behaves just like `nub`:func:, except it uses a user-supplied equality
    predicate instead of the overloaded ``==`` function.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> "a" >> bool) >> "a" >> ["a"] >> ["a"])
def deleteBy(f, xs):
    """``deleteBy :: (a -> a -> Bool) -> a -> [a] -> [a]``

    Behaves like `delete`:func:, but takes a user-supplied equality predicate.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> "a" >> bool) >> ["a"] >> ["a"] >> ["a"])
def deleteFirstBy(f, xs, ys):
    """``deleteFirstsBy :: (a -> a -> Bool) -> [a] -> [a] -> [a]``

    Takes a predicate and two lists and returns the first list with the first
    occurrence of each element of the second list removed.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> "a" >> bool) >> ["a"] >> ["a"] >> ["a"])
def unionBy(f, xs, ys):
    """``unionBy :: (a -> a -> Bool) -> [a] -> [a] -> [a]``

    The non-overloaded version of `union`:func:.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> "a" >> bool) >> ["a"] >> ["a"] >> ["a"])
def intersectBy(f, xs, ys):
    """``intersectBy :: (a -> a -> Bool) -> [a] -> [a] -> [a]``

    The non-overloaded version of `intersect`:func:.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> "a" >> bool) >> ["a"] >> [["a"]])
def groupBy(f, xs):
    """``groupBy :: (a -> a -> Bool) -> [a] -> [[a]]``

    The non-overloaded version of `group`:func:.

    """
    import itertools
    from hask.lang.lazylist import L
    return L[(L[i[1]] for i in itertools.groupby(xs, keyfunc=f))]


@sig(H/ (H/ "a" >> "a" >> Ordering) >> ["a"] >> ["a"])
def sortBy(f, xs):
    """``sortBy :: (a -> a -> Ordering) -> [a] -> [a]``

    The non-overloaded version of `sort`:func:.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> "a" >> Ordering) >> "a" >> ["a"] >> ["a"])
def insertBy(f, xs):
    """``insertBy :: (a -> a -> Ordering) -> a -> [a] -> [a]``

    The non-overloaded version of `insert`:func:.

    """
    raise NotImplementedError()


@sig(H/ (H/ "a" >> "a" >> Ordering) >> ["a"] >> "a")
def maximumBy(f, xs):
    """``maximumBy :: (a -> a -> Ordering) -> [a] -> a``

    Returns the greatest element of the list by the comparison function.  The
    list must be finite and non-empty.

    """
    return max(xs, key=f)


@sig(H/ (H/ "a" >> "a" >> Ordering) >> ["a"] >> "a")
def minimumBy(f, xs):
    """``minimumBy :: (a -> a -> Ordering) -> [a] -> a``

    Returns the least element of the list by the comparison function.  The
    list must be finite and non-empty.

    """
    return min(xs, key=f)


@sig(H[(Num, "i")]/ ["a"] >> "i")
def genericLength(xs):
    """``genericLength :: Num i => [a] -> i``

    An overloaded version of `length`:func:.  In particular, instead of
    returning an `Int`, it returns any type which is an instance of `Num`.  It
    is, however, less efficient than length.

    """
    raise NotImplementedError()


@sig(H[Integral, "i"]/ "i" >> ["a"] >> ["a"])
def genericTake(n, xs):
    """``genericTake :: Integral i => i -> [a] -> [a]``

    An overloaded version of `take`:func:, which accepts any `Integral` value
    as the number of elements to take.

    """
    raise NotImplementedError()


@sig(H[Integral, "i"]/ "i" >> ["a"] >> ["a"])
def genericDrop(n, xs):
    """``genericDrop :: Integral i => i -> [a] -> [a]``

    An overloaded version of `drop`:func:, which accepts any `Integral` value
    as the number of elements to drop.

    """
    raise NotImplementedError()


@sig(H[Integral, "i"]/ "i" >> ["a"] >> (["a"], ["a"]))
def genericSplitAt(n, xs):
    """``genericSplitAt :: Integral i => i -> [a] -> ([a], [a])``

    An overloaded version of `splitAt`:func:, which accepts any `Integral`
    value as the position at which to split.

    """
    raise NotImplementedError()


@sig(H[Integral, "i"]/ ["a"] >> "i" >> ["a"])
def genericIndex(xs, i):
    """``genericIndex :: Integral i => [a] -> i -> a``

    An overloaded version of ``!!``, which accepts any `Integral` value as the
    index.

    """
    raise NotImplementedError()


@sig(H[Integral, "i"]/ "i" >> ["a"] >> ["a"])
def genericReplicate(i, a):
    """``genericReplicate :: Integral i => i -> a -> [a]``

    An overloaded version of `replicate`:func:, which accepts any `Integral`
    value as the number of repetitions to make.

    """
    raise NotImplementedError()


del Maybe, Integral, Num, Ordering, Ord, Eq
del t, sig, H
