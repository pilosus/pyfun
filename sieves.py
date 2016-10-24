#!/usr/bin/env python3

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

def take(pred, gen):
    """
    Return a generator with elements not satisfying predicate filtered out

    :param pred: a predicate function
    :param iter: a generator
    :return: a generator with predicate applied to the given generator

    >>> list(take(lambda x: x < 10, (i for i in range(100))))[-1]
    9
    """
    for i in gen:
        if pred(i):
            yield i
        else:
            break

def remove_multiples(m, ints):
    """
    Return a generator based on the given one without multiples of the given number
    :param m: an int whose multiples should be removed
    :param ints: a generator of ints
    :return: a generator of ints

    >>> list(remove_multiples(2, range(10)))
    [1, 3, 5, 7, 9]
    """
    for i in ints:
        if (i % m):
            yield i

def sieve(ints):
    """
    Return a generator of prime numbers sieved out of the given generator f ints

    Ints are sieved out with Eratosthenes sieve algorithm.
    :param ints: a generator of ints
    :return: a generator of prime numbers

    >>> list(sieve((i for i in range(2, 100))))[-1]
    97

    >>> list(take(lambda x: x < 10, sieve(count(start=2, step=1))))
    [2, 3, 5, 7]

    >>> 7 in take(lambda x: x < 10, sieve(count(start=2, step=1)))
    True
    """
    while True:
        prime = next(ints)
        yield prime
        ints = remove_multiples(prime, ints)


def fib():
    """
    Return a generator of Fibonacci sequence
    :return: a generator of Fibinacci numbers

    >>> list(take(lambda x: x < 100, fib()))
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, (a + b)
