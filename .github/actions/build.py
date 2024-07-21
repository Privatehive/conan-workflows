#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import check_output, check_call
import os
import random
import string
import json


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

helper_dir = os.path.dirname(__file__)

if __name__ == "__main__":

    host_profile_path = None
    check_call("conan profile detect", shell=True)
    check_call("conan config install %s" % os.path.join(helper_dir, "global.conf"), shell=True)
    #check_call("conan config install -tf extensions/hooks %s" % os.path.join(helper_dir, "hook_clean_cache.py"), shell=True)

    if 'CONAN_HOST_PROFILE_PATH' in os.environ:
        host_profile_path = os.environ['CONAN_HOST_PROFILE_PATH']

    recipe_path = "./"
      
    if 'CONAN_RECIPE_PATH' in os.environ:
        recipe_path = os.environ['CONAN_RECIPE_PATH']

    if 'CONAN_REMOTES' in os.environ:
        for remote in os.environ['CONAN_REMOTES'].split(','):
            rep_name = randomString()
            print("Adding remote: " + rep_name + " url: " + remote)
            check_call("conan remote add --index 0 --force %s %s" % (rep_name, remote), shell=True)

    options = ""
    if 'CONAN_OPTIONS' in os.environ:
        for option in os.environ['CONAN_OPTIONS'].split(','):
            options += " -o " + option

    name = json.loads(check_output("conan inspect %s -f json" % recipe_path, shell=True).decode("ascii"))["name"]
    version = json.loads(check_output("conan inspect %s -f json" % recipe_path, shell=True).decode("ascii"))["version"]
    user = json.loads(check_output("conan inspect %s -f json" % recipe_path, shell=True).decode("ascii"))["user"]
    cannel = json.loads(check_output("conan inspect %s -f json" % recipe_path, shell=True).decode("ascii"))["channel"]

    package_ref = "%s/%s@%s/%s" % (name, version, user, cannel)

    if host_profile_path is not None:
        print("Cross building recipe: " + package_ref)
        check_call("conan create %s -pr:h \"%s\" -tf \"\" %s -u -b missing" % (recipe_path, host_profile_path, options), shell=True)
    else:
        print("Building recipe: " + package_ref)
        check_call("conan create %s -tf \"\" %s -u -b missing" % (recipe_path, options), shell=True)
    print("-----Finished-----")
