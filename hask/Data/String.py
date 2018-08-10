from __future__ import division, print_function, absolute_import

from hask.lang.syntax import H
from hask.lang.syntax import sig


@sig(H/ str >> [str])
def lines(string):
    """``lines :: String -> [String]``

    Breaks a string up into a list of strings at newline characters.  The
    resulting strings do not contain newlines.

    """
    from hask.lang.lazylist import L
    return L[[]] if not string else L[string.split("\n")]


@sig(H/ str >> [str])
def words(string):
    """``words :: String -> [String]``

    Breaks a string up into a list of words, which were delimited by white
    space.

    """
    from hask.lang.lazylist import L
    return L[[]] if string == "" else L[string.split(" ")]


@sig(H/ [str] >> str)
def unlines(strings):
    """``lines :: [String] -> String``

    An inverse operation to lines.  It joins lines, after appending a
    terminating newline to each.

    """
    return "\n".join(strings)


@sig(H/ [str] >> str)
def unwords(strings):
    """``unwords :: [String] -> String``

    An inverse operation to words.  It joins words with separating spaces.

    """
    return " ".join(strings)


del H, sig
