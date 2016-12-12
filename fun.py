#!/usr/bin/env python3

import sys
from math import ceil, floor

### Misc functions you should find in a standard library of any decent functional PL

def enumerate(iterable, start=0):
    """
    Return an enumerate object.
    :param iterable: a sequence, an iterator, or some other object
                     which supports iteration.
    :return: tuple containing a count (from start which defaults to 0)
              and the values obtained from iterating over iterable.

    >>> [i for i in enumerate(['a', 'b', 'c'], 10)]
    [(10, 'a'), (11, 'b'), (12, 'c')]
    """
    for i in iterable:
        yield (start, i)
        start += 1


def sorted(iterable, key=None, reverse=False):
    """
    Return a new sorted list from the items in iterable.
    :param iterable: any iterable obejct
    :param key: key specifies a function of one argument that is used
                to extract a comparison key from each list element
                (for example, key=str.lower).
    :param reverse: reverse is a boolean value. If set to True,
                    then the list elements are sorted as if each comparison
                    were reversed.
    :return:

    >>> sorted(range(10), reverse=True)
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    """
    result = list(iterable)
    # .sort() mutates the list
    result.sort(key=key, reverse=reverse)
    return result


def is_true(v):
    """
    Return True if given value can be considered as True, return False otherwise.
    :param v: integer, boolean or str that can be use to denote a boolean value
    :return: boolean
    """
    return v in [1, True, 'True', 'true', 'T', 't', 'Yes', 'yes', 'y']


def any(iterable):
    """
    Return True if at least one element of iterable is True, otherwise return False
    :param iterable: any iterable object
    :return: boolean

    >>> any([0,1,0])
    True
    >>> any([0,0,0])
    False
    """
    return True in filter(is_true, iterable)


def foldl(function, base, iterable):
    """Recombine the results of recursively processing its constituent parts, building up a return value.

    :param function: function taking base and an element of iterable as arguments
    :param base: base value taken by the function
    :param iterable: any iterable object
    :return: result of applying function to elements of iterable

    >>> foldl(lambda a, b: a + b, 0, range(11))
    55
    """
    result = None
    for i in iterable:
        result = function(base, i)
        base = result
    return result


def all(iterable):
    """
    Return True if all elements of iterable are True, return False if at least on element is False.
    :param iterable: any iterable object
    :return: boolean

    >>> all([0,1,0])
    False
    >>> all([1,1,1])
    True
    """

    return is_true(foldl(lambda a, b: a and b, True, iterable))


def zip(iterable1, iterable2):
    """
    Return a generator of tuples of two corresponding elements of the given iterables.
    :param iterable1:
    :param iterable2:
    :return: a generator of tuples of two

    >>> list(zip(['a', 'b', 'c'], (1, 2, 3)))
    [('a', 1), ('b', 2), ('c', 3)]
    """
    i1 = iter(iterable1)
    i2 = iter(iterable2)

    while True:
        e1 = next(i1)
        e2 = next(i2)
        yield (e1, e2)


### Creating new iterators


def count(start=2, step=1):
    """
    Return an infinite generator of ints starting from the given value changing with a given step

    :param start: an int the generator starts with
    :param step: an int succeeding elements increased by
    :return: an infinite generator

    >>> N = count()
    >>> next(N)
    2
    >>> next(N)
    3
    >>> N.send(100)
    100
    >>> next(N)
    101
    """
    while True:
        val = (yield start)
        # if .send() method invoked
        if val is not None:
            start = val
        # if .__next__() method invoked
        else:
            start += step


def cycle(iterable):
    """
    Return an iterator of elements from the given iterable repeating from first to last infinitely.
    :param iterable:
    :return: an iterator

    >>> list(firstn(cycle([1,2,3]), 9))
    [1, 2, 3, 1, 2, 3, 1, 2, 3]

    >>> list(firstn(cycle(range(3)), 9))
    [0, 1, 2, 0, 1, 2, 0, 1, 2]

    """
    result = list(iterable)
    while True:
        for i in result:
            yield i


def firstn(iterable, n):
    """
    Return an iterable with first n elements of the proviced iterable.
    :param iterable:  any iterable
    :param n: number of elements to take from the beginning of the provided iterable
    :return: an iterable

    >>> list(firstn(range(10), 5))
    [0, 1, 2, 3, 4]
    """
    it = iter(iterable)
    for i in range(n):
        e = next(it)
        yield e


def repeat(elem, times=None):
    """
    Return the provided element repeated given number of times.
    :param elem: an element ot be repeated
    :param times: number of times element to be repeated;
                  if omitted an infinite iterable returned
    :return: an iterable

    >>> list(repeat('abc', 5))
    ['abc', 'abc', 'abc', 'abc', 'abc']

    >>> list(firstn(repeat('cba'), 3))
    ['cba', 'cba', 'cba']
    """

    while True:
        yield elem
        if times is not None:
            times -= 1
        if times is not None and times <= 0:
            break


def chain(*iterables):
    """
    Return an iterable consisting of all iterables passed as arguments/
    :param iterables: any iterable objects
    :return: an iterable

    >>> list(chain(['a', 'b', 'c'], (1, 2, 3)))
    ['a', 'b', 'c', 1, 2, 3]
    """
    for iterable in iterables:
        for i in iterable:
            yield i


def islice(iterable=None, *args):
    """
    Return a stream that's a slice of the iterator.
    :param iterable: any kind of iterable object
    :param *args: is a slice object slice(start, stop[, step])
    :param start: a start index of resulting iterable
    :param stop: a stop index of resulting iterable
    :param step: step to skip elements
    :return: an iterable

    >>> list(islice(range(10), 5))
    [0, 1, 2, 3, 4]

    >>> list(islice(range(10), 2, 8, 2))
    [2, 4, 6]

    >>> list(islice('ABCDEFG', 0, None, 2))
    ['A', 'C', 'E', 'G']
    """
    sl = slice(*args)
    it = iter(range(sl.start or 0, sl.stop or sys.maxsize, sl.step or 1))

    j = next(it)

    for i, elem in enumerate(iterable):
        if i == j:
            yield elem
            j = next(it)


def tee(iterable, n=2):
    """
    Return n independent iterators that will all return the contents of the source iterator.
    :param iterable: any iterable obejct
    :param n: number of iterators returned
    :return: an iterator of iterators

    >>> iterA, iterB, iterC = tee(range(1, 4), 3)
    >>> iterA == iterB == iterC
    True
    >>> iterC == range(1, 4)
    True
    """
    for i in range(n):
        yield iterable


### Selecting elements


def map(function, iterable):
    """
    Return an iterator that applies function to every item of iterable, yielding the results.
    See https://docs.python.org/3/library/functions.html#map

    >>>
    :param function: any function
    :param iterable: an iterable object
    :return: a generator
    >>> list(map(lambda x: x.upper(), ['hello', 'there']))
    ['HELLO', 'THERE']
    """
    for i in iterable:
        yield function(i)


def filter(predicate, iterable):
    """
    Construct an iterator from those elements of iterable for which function returns true.
    See https://docs.python.org/3/library/functions.html#filter
    :param predicate: a function with one argument returning bool
    :param iterable: any iterable object
    :return: an iterable

    >>> list(filter(lambda x: (x % 2) == 0, range(10)))
    [0, 2, 4, 6, 8]
    """
    for i in iterable:
        if predicate(i):
            yield i

def takewhile(predicate, iterable):
    """
    Make an iterator that returns elements from the iterable as long as the predicate is true.
    :param predicate: a function returning bool
    :param iterable: any iterable
    :return: an iterable with elements satisfying predicate

    >>> list(takewhile(lambda x: x < 5, range(100)))
    [0, 1, 2, 3, 4]
    """
    for i in iterable:
        if predicate(i):
            yield i
        else:
            break

def dropwhile(predicate, iterable):
    """
    Make an iterator that drops elements from the iterable as long as the predicate is true;
    afterwards, returns every element.

    :param predicate: a function returning bool
    :param iterable: any iterable
    :return: an iterable

    >>> list(dropwhile(lambda x: x < 5, [1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 10]))
    [5, 6, 7, 8, 0, 1, 2, 10]
    """
    it = iter(iterable)
    while True:
        e = next(it)
        if not predicate(e):
            yield e
            break

    for i in it:
        yield i


def filterfalse(predicate, iterable):
    """
    Construct an iterator from those elements of iterable for which function returns false.
    :param predicate: a function with one argument returning bool
    :param iterable: any iterable object
    :return: an iterable

    >>> list(filterfalse(lambda x: (x % 2) == 0, range(10)))
    [1, 3, 5, 7, 9]
    """
    for i in iterable:
        if not predicate(i):
            yield i


def compress(data, selectors):
    """
    returns only those elements of data for which the corresponding element of selectors is true
    :param data: iterable of elements to select from
    :param selectors: boolean selectors used to select elements of data iterable
    :return: an iterable of selected elements

    >>> list(compress([1,2,3,4,5], [True, True, False, False, True]))
    [1, 2, 5]

    >>> list(compress([1,2,3,4,5], [lambda x: x > 0, lambda x: x == 1, False, True, lambda x: x % 2 != 0]))
    [1, 2, 4, 5]
    """
    datai = iter(data)
    selectorsi = iter(selectors)

    while True:
        elem = next(datai)
        pred = next(selectorsi)
        if pred:
            yield elem


### Combinatoric functions

def combinations(iterable, r):
    """
    Return an iterator giving all possible r-tuple combinations of the elements contained in iterable.
    :param iterable: any iterable object
    :param r: size
    :return: iterable of r-tuples

    >>> len(list(combinations("abcdefgh",3)))
    56

    >>> list(combinations("abc", 2))
    [('a', 'b'), ('a', 'c'), ('b', 'c')]
    """
    elements = list(iterable)

    for i in range(len(elements)):
        if r == 1:
            yield (elements[i],)
        else:
            for n in combinations(elements[i + 1:len(elements)], r - 1):
                yield (elements[i],) + n

def combinations_with_replacement(iterable, r):
    """
    Return an iterator giving all possible r-tuple combinations of the elements contained in iterable.
    :param iterable: any iterable object
    :param r: size
    :return: iterable of r-tuples

    >>> list(combinations_with_replacement("abc", 2))
    [('a', 'a'), ('a', 'b'), ('a', 'c'), ('b', 'b'), ('b', 'c'), ('c', 'c')]
    """
    elements = list(iterable)

    for i in range(len(elements)):
        if r == 1:
            yield (elements[i],)
        else:
            for n in combinations(elements[i:len(elements)], r - 1):
                yield (elements[i],) + n


def permutations(iterable, r=None):
    """
    Return successive r length permutations of elements in the iterable.

    :param iterable: any iterable object
    :param r: size of the tuple
    :return: iterable of tuples

    >>> list(permutations(range(3), 2))
    [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
    """
    elements = list(iterable)
    n = len(elements)
    r = n if r is None else r
    if r > n:
        return
    idx = list(range(n))
    cycles = list(range(n, n - r, -1))
    yield tuple(elements[i] for i in idx[:r])

    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                idx[i:] = idx[i+1:] + idx[i:i+1]
                cycles[i] = n - 1
            else:
                j = cycles[i]
                idx[i], idx[-j] = idx[-j], idx[i]
                yield tuple(elements[i] for i in idx[:r])
                break
        else:
            return


### Grouping elements


def groupby(iterable, keyfun=None):
    """
    Return a stream of 2-tuples containing a key value and an iterator for the elements with that key.

    :param iterable: any iterable object
    :param keyfun: a function that can compute a key value for each element returned by the iterable.
    :return: an iterable of 2-tuples, each tuple's made up of a key and an iterable with that key

    >>> city_list = [('Decatur', 'AL'), ('Huntsville', 'AL'), ('Selma', 'AL'),\
             ('Anchorage', 'AK'), ('Nome', 'AK'),\
             ('Flagstaff', 'AZ'), ('Phoenix', 'AZ'), ('Tucson', 'AZ'),]
    >>>
    >>> for i in groupby(city_list, lambda x: x[1]):
    ...     if i[0] == 'AL':
    ...         print(list(i[1]))
    ...
    [('Decatur', 'AL'), ('Huntsville', 'AL'), ('Selma', 'AL')]

    >>> [k for k, g in groupby('AAAABBBCCDAABBB')]
    ['A', 'B', 'C', 'D', 'A', 'B']

    >>> [list(g) for k, g in groupby('AAAABBBCCD')]
    [['A', 'A', 'A', 'A'], ['B', 'B', 'B'], ['C', 'C'], ['D']]

    """
    # if key function is not provided, use identity function
    if keyfun is None:
        keyfun = lambda x: x

    # last_key used to track when repeated key changes
    last_key = keyfun(list(iterable)[0])
    vals = ()
    for i in iterable:
        key = keyfun(i)
        # if key hasn't changed since the previous iteration, save element
        if key == last_key:
            vals += (i,)
        # if key has changed, yield a two-tuple (key, iterable of elements using this key)
        else:
            yield (last_key, iter(vals))
            vals = ()
            # don't forget to save element into an empty tuple
            vals += (i,)
        # at the end of iteration last_key becomes the key of the current element
        last_key = key

    # the very last iteration doesn't save two-tuple, so do it here
    yield (last_key, iter(vals))


### functools module

def reduce(function, base, iterable):
    # See foldl function in this file
    return foldl(function, base, iterable)

def accumulate(function, base, iterable):
    """
    Return an iterable of partial results of recursively applying a function to the given iterable.

    :param function: function taking base and an element of iterable as arguments
    :param base: base value taken by the function
    :param iterable: any iterable object
    :return: an iterable of partial results

    >>> list(accumulate(lambda a, b: a + b, 0, range(10)))
    [0, 1, 3, 6, 10, 15, 21, 28, 36, 45]

    >>> list(accumulate(lambda a, b: a + b, 0, range(10)))[-1] == reduce(lambda a, b: a + b, 0, range(10))
    True

    # factorial function
    >>> list(accumulate(lambda a, b: a * b, 1, range(1, 6)))[-1]
    120
    """

    for i in iterable:
        base = function(base, i)
        yield base

### operator module

# maths
add = lambda a, b: a + b
sub = lambda a, b: a - b
mul = lambda a, b: a * b
floordiv = lambda a, b: floor(a / b)
ceildiv = lambda a, b: ceil(a / b)
abs = lambda a: abs(a)

"""
>>> reduce(add, 0, range(10))
45

>>> reduce(mul, 1, range(1, 6))
120
"""
