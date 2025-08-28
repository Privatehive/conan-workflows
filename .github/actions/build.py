#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import check_output, check_call
import tempfile
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
    build_profile_path = None
    check_call("conan profile detect -f", shell=True)
    check_call("conan config install %s" % os.path.join(helper_dir, "global.conf"), shell=True)
    check_call("conan config install -tf extensions/hooks %s" % os.path.join(helper_dir, "hook_clean_cache.py"), shell=True)

    options = ""

    if 'CONAN_HOST_PROFILE_PATH' in os.environ and os.environ['CONAN_HOST_PROFILE_PATH']:
        host_profile_path = os.environ['CONAN_HOST_PROFILE_PATH']
        options += " -pr:h %s " % host_profile_path

    if 'CONAN_BUILD_PROFILE_PATH' in os.environ and os.environ['CONAN_BUILD_PROFILE_PATH']:
        build_profile_path = os.environ['CONAN_BUILD_PROFILE_PATH']
        options += " -pr:b %s " % build_profile_path

    recipe_path = "./"
      
    if 'CONAN_RECIPE_PATH' in os.environ:
        recipe_path = os.environ['CONAN_RECIPE_PATH']

    if 'CONAN_REMOTES' in os.environ and os.environ['CONAN_REMOTES']:
        for remote in os.environ['CONAN_REMOTES'].split(','):
            if remote:
                rep_name = randomString()
                print("Adding remote: " + rep_name + " url: " + remote)
                check_call("conan remote add --index 0 --force %s %s" % (rep_name, remote), shell=True)

    remotes = []
    for remote in json.loads(check_output("conan remote list -f json", shell=True).decode("ascii")):
        if remote["enabled"] == True:
            remotes.append(remote["name"])

    print("Active remotes: " + ', '.join(remotes))

    if 'CONAN_OPTIONS' in os.environ and os.environ['CONAN_OPTIONS']:
        for option in os.environ['CONAN_OPTIONS'].split(','):
            options += " -o " + option

    if 'CONAN_BUILD_REQUIRE' in os.environ and os.environ['CONAN_BUILD_REQUIRE'] == "true":
        print("build-require option is used")
        options += " --build-require "

    deploy_path = None
    if 'CONAN_DEPLOY_PATH' in os.environ and os.environ['CONAN_DEPLOY_PATH']:
        deploy_path = os.environ['CONAN_DEPLOY_PATH']

    name = json.loads(check_output("conan inspect %s -f json" % recipe_path, shell=True).decode("ascii"))["name"]
    version = json.loads(check_output("conan inspect %s -f json" % recipe_path, shell=True).decode("ascii"))["version"]
    user = json.loads(check_output("conan inspect %s -f json" % recipe_path, shell=True).decode("ascii"))["user"]
    cannel = json.loads(check_output("conan inspect %s -f json" % recipe_path, shell=True).decode("ascii"))["channel"]

    for key, val in json.loads(check_output("conan graph info %s -vquiet -f json" % recipe_path, shell=True).decode("ascii"))["graph"]["resolved_ranges"].items():
        if val.startswith("qt/"):
            print("found qt dependency - downloading recipe to search for conan profiles")
            for remote in remotes:
                # download recipe containing conan profiles
                with tempfile.TemporaryDirectory() as tmpdir:
                    try:
                        check_output("conan download %s -vquiet -f json --only-recipe -cc core.cache:storage_path=%s -r %s" % (val, tmpdir, remote), shell=True)
                    except Exception:
                        continue
                    tmp_recipe_path = json.loads(check_output("conan cache path %s -vquiet -cc core.cache:storage_path=%s -f json" % (val, tmpdir), shell=True).decode("ascii"))["cache_path"]
                    tmp_profile_path = os.path.join(tmp_recipe_path, 'profiles')
                    print("found conan profiles in qt recipe - installing")
                    if os.path.isdir(tmp_profile_path):
                        check_output("conan config install -tf profiles %s" % tmp_profile_path, shell=True)

    package_ref = "%s/%s@%s/%s" % (name, version, user, cannel)

    print("Building recipe: " + package_ref)
    check_call("conan create %s -tf \"\" %s -u -b missing" % (recipe_path, options), shell=True)
    if deploy_path is not None:
        check_call("conan install --requires=\"%s\" %s --deployer-package=\"%s/*\" --deployer-folder=\"%s\"" % (package_ref, options, name, deploy_path), shell=True)

    print("-----Finished-----")
