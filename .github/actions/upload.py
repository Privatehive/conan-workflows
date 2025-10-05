#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import check_output, check_call
import os
import random
import string
import json
import time


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


if __name__ == "__main__":
     
    recipe_path = "./"

    if 'CONAN_RECIPE_PATH' in os.environ:
        recipe_path = os.environ['CONAN_RECIPE_PATH']
    
    upload_all = False
    if 'UPLOAD_ALL' in os.environ and os.environ['UPLOAD_ALL'] == 'true':
        upload_all = True
    
    if not 'CONAN_UPLOAD' in os.environ:
        print('Missing "CONAN_UPLOAD" env. variable')
        quit(1)

    rep_name = randomString()

    print("Adding remote for upload: " + os.environ['CONAN_UPLOAD'])
    check_call("conan remote add --index 0 --force %s %s" % (rep_name, os.environ['CONAN_UPLOAD']), shell=True)
    try:
        check_call("conan remote login -p %s %s %s" % (os.environ['CONAN_PASSWORD'], rep_name, os.environ['CONAN_LOGIN_USERNAME']), shell=True)
    except:
        print("Warning: Couldn't set user credentials for remote")

    name = json.loads(check_output("conan inspect %s -f json" % recipe_path, shell=True).decode("ascii"))["name"]
    version = json.loads(check_output("conan inspect %s -f json" % recipe_path, shell=True).decode("ascii"))["version"]
    user = json.loads(check_output("conan inspect %s -f json" % recipe_path, shell=True).decode("ascii"))["user"]
    cannel = json.loads(check_output("conan inspect %s -f json" % recipe_path, shell=True).decode("ascii"))["channel"]

    package_ref = "%s/%s@%s/%s" % (name, version, user, cannel)

    f = open("conan_package_ref", "w")
    f.write(package_ref)
    f.close()

    print("Exporting recipe: " + package_ref)
    check_call("conan export %s" % recipe_path, shell=True)
    if upload_all:
        print("Uploading recipe and package: " + package_ref)
        check_call("conan upload %s -r %s" % (package_ref, rep_name), shell=True)
    else:
        print("Uploading recipe: " + package_ref)
        check_call("conan upload %s -r %s --only-recipe" % (package_ref, rep_name), shell=True)
