=================
Functional Python
=================

-----
About
-----

There's nothing really important here. Just a bunch of exercises in Python 3 that I did for recreational purposes
while learning functional features Python inherited from Haskell. In fact what I did is the following:

#. Followed `Functional Programming HOWTO`_
#. Tried to implement (sometimes naïvely, sometimes not) functions one would expect to find in a standard library of
   any decent functional programming language like Haskell or Scheme

Although most of the functions already exist in Python's _itertools_ and _functool_ modules, I think reinventing
the wheel may be fun!

-----
Tests
-----

One of the reasons why I set out for these exercises was an intention to find out if life beyond GNU/Emacs
actually possible. For a moment I switch over to IntelliJ's PyCharm CE. The short answer to my questions is
yes, it's possible, and actually is pretty convenient.

PyCharm allows to run **unit-test** with _doctest_ module's features without any additional line of code -
you just need the tests themselves written directly in functions' docstrings + IDE's configuration for running
tests.

.. _Functional Programming HOWTO: https://docs.python.org/3/howto/functional.html
