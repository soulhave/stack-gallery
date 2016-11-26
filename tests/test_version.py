#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of sandbox.
# https://github.com/marcuslacerda/tech-gallery-analytics

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Marcus Lacerda <marcus.lacerda@gmail.com>

from preggy import expect

from techanalytics import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        expect(__version__).to_equal('0.1.0')
