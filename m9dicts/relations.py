#
# Copyright (C) 2017 Red Hat, Inc.
# License: MIT
#
"""Flatten nested dicts, etc.
"""
from __future__ import absolute_import

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

import m9dicts.utils


def object_to_id(obj):
    """Object -> id.

    :param obj: Any object has __str__ method to get its ID value

    >>> object_to_id("test")
    '098f6bcd4621d373cade4e832627b4f6'
    >>> object_to_id({'a': "test"})
    'c5b846ec3b2f1a5b7c44c91678a61f47'
    >>> object_to_id(['a', 'b', 'c'])
    'eea457285a61f212e4bbaaf890263ab4'
    """
    return md5(str(obj)).hexdigest()


def _gen_id(*args):
    """
    :return: ID generated from `args`
    """
    return object_to_id(args)


def _rel_name(*relations):
    """
    :return: Generated composite relation name from relations
    """
    return "rel_" + '_'.join(relations)


def _dict_to_rels_itr(dic, rel_name):
    """
    Convert nested dict[s] to tuples of relation name and relations of items in
    the dict, and yields each pairs.

    :param dic: A dict or dict-like object
    :param rel_name: Name for relations of items in `dic`
    :return: A list of (<relation_name>, [tuple of key and value])

    >>> list(_dict_to_rels_itr(dict(id=0, a=1, b="b"), "ab"))
    [('ab', [('id', 0), ('a', 1), ('b', 'b')])]
    """
    lkeys = [k for k, v in dic.items() if m9dicts.utils.is_list_like(v)]
    dkeys = [k for k, v in dic.items() if m9dicts.utils.is_dict_like(v)]
    items = sorted((k, v) for k, v in dic.items()
                   if k != "id" and k not in lkeys and k not in dkeys)
    oid = dic.get("id", _gen_id(*items))
    yield (rel_name, [("id", oid)] + items)

    if lkeys:
        for key in sorted(lkeys):
            name = _rel_name(rel_name, key)
            for val in sorted(dic[key]):
                if m9dicts.utils.is_dict_like(val):
                    for tpl in _dict_to_rels_itr(val, key):
                        yield tpl
                else:
                    lid = _gen_id(key, val)
                    yield (name, [("id", lid), (rel_name, oid), (key, val)])

    if dkeys:
        for key in sorted(dkeys):
            name = _rel_name(rel_name, key)
            for tpl in _dict_to_rels_itr(dic[key], key):
                yield tpl

# vim:sw=4:ts=4:et:
