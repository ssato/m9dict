#
# Copyright (C) 2017 Satoru SATOH <ssato @ redhat.com>
#
# pylint: disable=missing-docstring,invalid-name,protected-access
from __future__ import absolute_import
import unittest
import m9dicts.relations as TT


class Test_10_functions(unittest.TestCase):

    def test_10_dict_to_rels_itr__simple(self):
        dic = dict(id=0, a=1, b="b")
        ref = [('ab', [('id', 0), ('a', 1), ('b', 'b')])]
        self.assertEqual(list(TT._dict_to_rels_itr(dic, "ab")), ref)

    def test_12_dict_to_rels_itr__lists(self):
        dic = dict(id=0, a=1, b=[2, 3], c="c")
        id_0 = TT._gen_id('b', 2)
        id_1 = TT._gen_id('b', 3)
        ref = [('ac', [('id', 0), ('a', 1), ('c', 'c')]),
               ('rel_ac_b', [('id', id_0), ('ac', 0), ('b', 2)]),
               ('rel_ac_b', [('id', id_1), ('ac', 0), ('b', 3)])]
        self.assertEqual(list(TT._dict_to_rels_itr(dic, "ac")), ref)

    def test_14_dict_to_rels_itr__lists(self):
        dic = dict(id='01', a=1, b=[2, 3], c=["c"])
        id_0 = TT._gen_id('b', 2)
        id_1 = TT._gen_id('b', 3)
        id_2 = TT._gen_id('c', 'c')
        ref = [('A', [('id', '01'), ('a', 1)]),
               ('rel_A_b', [('id', id_0), ('A', '01'), ('b', 2)]),
               ('rel_A_b', [('id', id_1), ('A', '01'), ('b', 3)]),
               ('rel_A_c', [('id', id_2), ('A', '01'), ('c', 'c')])]
        self.assertEqual(list(TT._dict_to_rels_itr(dic, "A")), ref)

# vim:sw=4:ts=4:et:
