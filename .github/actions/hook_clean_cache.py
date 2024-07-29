#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan.api.conan_api import ConanAPI
from conan.api.model import ListPattern
from subprocess import check_output, check_call

def post_package(conanfile):
    conan_api = ConanAPI()
    ref_pattern = ListPattern('*', rrev="*", package_id="*", prev="*")
    package_list = conan_api.list.select(ref_pattern)
    conan_api.cache.clean(package_list, source=True, build=True, download=True, temp=False)
    conanfile.output.info("running cleanup hook")
