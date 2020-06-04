#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import os
import sys

from reclut.utils import get_extension, sanitize_title

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_get_extension():
    assert get_extension("https://www.foo.bar/get.this/file.ext") == "ext"


def test_sanitize_title():
    assert sanitize_title("I took a few shots at Lake Louise today and Google offered me this panorama:") \
           == "I_took_a_few_shots_at_Lake_Louise_today_and_Google_offered_me_this_panorama:"

    assert sanitize_title(" - -.,/!?()[] ") == "___"
