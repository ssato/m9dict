#
# Copyright (C) 2017 Satoru SATOH <ssato @ redhat.com>
#
# pylint: disable=missing-docstring,invalid-name,protected-access
from __future__ import absolute_import
import unittest
import m9dicts.relations as TT


def _ndict_to_rels(*args, **kwargs):
    return sorted(TT._ndict_to_rels_itr(*args, **kwargs))


class Test_20__ndict_to_rels_itr(unittest.TestCase):
    """
    >>> f = _ndict_to_rels
    >>> s = set(); f(dict(A=dict(id=0, a=1), id=1),
    ...   s, "data")  # doctest: +NORMALIZE_WHITESPACE
    [('A', (('a', 1), ('id', 0))),
     ('data', (('A', Ref(relvar='A', id=0)), ('id', 1)))]

    >>> s = set(); f(dict(A=dict(a=1, id=1)),
    ...              s)  # doctest: +NORMALIZE_WHITESPACE
    [('A', (('A', Ref(relvar='A.A', id=1)), ('id', 285990133928))),
     ('A.A', (('a', 1), ('id', 1)))]

    >>> s = set(); f(dict(A=dict(a=1)),
    ...              s)  # doctest: +NORMALIZE_WHITESPACE
    [('A', (('A', Ref(relvar='A.A', id=224491522528)), ('id', 227711280590))),
     ('A.A', (('a', 1), ('id', 224491522528)))]

    >>> f(dict(A=[dict(a=1, id=0)]),
    ...   s, "A")  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    [('A', (('A', Ref(relvar='A.A', id=0)), ('id', 235603264683))),
     ('A.A', (('a', 1), ('id', 0)))]
    """

    def test_10_with_id_and_relvar(self):
        dic = dict(a=1, id=0)
        ref = [('A', (('a', 1), ('id', 0)))]
        self.assertEqual(_ndict_to_rels(dic, "A"), ref)

# vim:sw=4:ts=4:et:
