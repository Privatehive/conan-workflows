# conan-workflows

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Privatehive/conan-workflows/main.yml?branch=master&style=flat&logo=github&label=Docker+build)](https://github.com/Privatehive/conan-workflows/actions?query=branch%3Amaster)

**This shared GitHub workflows help you to build/upload conan packages**

### hostProfiles

Contains predefined Conan host profiles which are use by all Qt based projects targeting different operating systems and architectures.
```
androidArmv7.profile
androidArmv8.profile
androidArmvx86.profile
androidArmvx86_64.profile
raspberrypios-bullseye.profile
raspberrypios-buster.profile
windowsMinGW.profile
```

### docker/ubuntu

Contains a Dockerfile that provides a conan environment to build binaries for Linux.

### docker/wine

Contains a Dockerfile that provides a conan environment to build binaries for Windows (by using wine).

### .github/workflows/createPackage.yml

Use this shared GitHub workflow to create a Conan package

``` yml
jobs:
  build_linux:
    name: "Build Linux"
    uses: Privatehive/conan-workflows/.github/workflows/createPackage.yml@master
    with:
      image: "ghcr.io/tereius/conan-ubuntu:latest"
      runs-on: self-hosted
      conan_host_profile: "androidArmv8"
      conan_remotes: https://conan.privatehive.de/artifactory/api/conan/public-conan
      conan_options: "qt/*:shared=True,qt/*:qtbase=True"
```

| input parameter    | default                                           | description                                                                                                                                                                                                                          |
| ------------------ | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| image              | `ghcr.io/Privatehive/conan-ubuntu:latest`         | The Docker Image to use to build the conan package. Use one of [conan-ubuntu](#docker/ubuntu), [conan-wine](#docker/wine).                                                                                                           |
| runs-on            | `ubuntu-latest`                                   | You probably have to use 'self-hosted' here and use the [Google Cloud hosted runner](https://github.com/Privatehive/g-spot-runner-github-actions). This runner runs the CI jobs with the same user uid like in the Docker Container. |
| conan_host_profile | if ommited the conan default profile will be used | One of the [hostProfiles](#hostProfiles) (omit the `.profile` suffix - e.g. `androidArmv8`).                                                                                                                                         |
| conan_recipe_path  | `./`                                              | The relative path pointing to the directory where `conanfile.py` is located.                                                                                                                                                         |
| conan_remotes      | `""`                                              | Comma separated list of conan remotes.                                                                                                                                                                                               |
| conan_options      | `""`                                              | Comma separated list of conan options e.g.: `qt/*:shared=True,qt/*:GUI=True`.                                                                                                                                                        |

### .github/workflows/uploadPackage.yml

Use this shared GitHub workflow to upload a Conan recipe to a remote

``` yml
jobs:
  build_linux: ...

  upload_recipe:
    name: "Finalize"
    uses: Privatehive/conan-workflows/.github/workflows/uploadRecipe.yml@master
    needs: [build_linux]
    if: ${{ success() && github.ref == 'refs/heads/master' }}
    secrets: inherit
    with:
      conan_upload_remote: https://conan.privatehive.de/artifactory/api/conan/public-conan
```

| input parameter     | default                                   | description                                                                                                                                                                                                                          |
| ------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| image               | `ghcr.io/Privatehive/conan-ubuntu:latest` | The Docker Image to use to build the conan package. Use one of [conan-ubuntu](#docker/ubuntu), [conan-wine](#docker/wine).                                                                                                           |
| runs-on             | `ubuntu-latest`                           | You probably have to use 'self-hosted' here and use the [Google Cloud hosted runner](https://github.com/Privatehive/g-spot-runner-github-actions). This runner runs the CI jobs with the same user uid like in the Docker Container. |
| conan_recipe_path   | `./`                                      | The relative path pointing to the directory where `conanfile.py` is located.                                                                                                                                                         |
| conan_upload_remote | `""`                                      | The remote where the recipe will be uploaded to.                                                                                                                                                                                     |
| publish_property    | `true`                                    | If `true` a custom property `conan-package` will be set containing the recipe ref. Make sure the custom property is enabled in the GitHub organization.                                                                                      |

| secret parameter      | default | description                                                                                             |
| --------------------- | ------- | ------------------------------------------------------------------------------------------------------- |
| conan_upload_login    | `""`    | The account to log into the remote.                                                                     |
| conan_upload_password | `""`    | The password of the account to log into the remote.                                                     |
| install_token_app_id  | `""`    | The app id of a GitHub app that has write access to organization/repository custom properties.          |
| install_token_secret  | `""`    | The app private key of a GitHub app that has write access to organization/repository custom properties. |

