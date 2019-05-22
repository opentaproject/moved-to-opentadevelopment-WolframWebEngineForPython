# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import os

from wolframclient.utils.tests import TestCase as BaseTestCase
from wolframwebengine.server.explorer import get_wl_handler_path_from_folder


class TestCase(BaseTestCase):
    def test_sample_explorer(self):

        folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "sampleapp")

        for path, resolved in (
            ("/", "index.m"),
            ("/random.m", "random.m"),
            ("/foo/bar/", "foo/bar/index.m"),
            ("/foo/", "foo/index.m"),
            ("/foo/bar/index.m", "foo/bar/index.m"),
            ("/foo/bar/something.m", "foo/bar/something.m"),
        ):

            for root in ("/cached", None, ""):

                self.assertEqual(
                    get_wl_handler_path_from_folder(folder, ((root or "") + path), root=root),
                    os.path.join(folder, resolved),
                )
