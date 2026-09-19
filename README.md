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

Use this shared GitHub workflow to create a Conan package on a regular GitHub-hosted runner (e.g. `ubuntu-22.04`, `windows-2022`, `macos-13`). If you need a self-hosted [gcp-hosted-github-runner](https://github.com/Privatehive/gcp-hosted-github-runner) instead (e.g. for a custom machine type), use [createPackageGcpRunner.yml](#githubworkflowscreatepackagegcprunneryml).

``` yml
jobs:
  build_linux:
    name: "Build Linux"
    uses: Privatehive/conan-workflows/.github/workflows/createPackage.yml@master
    with:
      image: "ubuntu-22.04"
      conan_host_profile: "androidArmv8"
      conan_remotes: https://conan.privatehive.de/artifactory/api/conan/public-conan
      conan_options: "qt/*:shared=True,qt/*:qtbase=True"
```

| input parameter          | default                                           | description                                                                                                                        |
| ------------------------ | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| name                     | `Create package`                                  | A name for the build step                                                                                                          |
| image                    | `ubuntu-latest`                                   | The GitHub-hosted runner image to build the conan package on, e.g. `ubuntu-22.04`, `windows-2022`, `macos-13`.                     |
| export_conan_cache       | false                                              | If `true`, the conan cache is saved as a GitHub Actions cache entry (keyed by `${{ runner.os }}-${{ github.sha }}`) after the build, so a later job/workflow run can restore it via `import_conan_cache`. |
| import_conan_cache       | false                                              | If `true`, restores a conan cache previously saved with `export_conan_cache` before building. Fails the job if no matching cache entry exists. |
| conan_host_profile       | if ommited the conan default profile will be used | One of the [hostProfiles](#hostProfiles) (omit the `.profile` suffix - e.g. `androidArmv8`).                                       |
| conan_build_profile      | if ommited the conan default profile will be used | Like `conan_host_profile`, but for the build profile (`-pr:b`).                                                                    |
| conan_host_profile_path  | `""`                                               | Path to a custom conan host profile file, used instead of `conan_host_profile` when you don't want one of the predefined [hostProfiles](#hostProfiles). |
| conan_build_profile_path | `""`                                               | Like `conan_host_profile_path`, but for the build profile (`-pr:b`).                                                               |
| conan_build_require      | false                                              | Will run a "--build-require" build. Only has an effect if `conan_host_profile` is provided.                                        |
| conan_recipe_path        | `./`                                               | The relative path pointing to the directory where `conanfile.py` is located.                                                       |
| conan_version            | if ommited the version declared in the recipe is used | The version to build, passed as `--version` to conan. Use this when the recipe doesn't hardcode a version (e.g. `conandata.yml` declares sources for several versions). |
| conan_remotes            | `""`                                               | Comma separated list of conan remotes.                                                                                             |
| conan_options            | `""`                                               | Comma separated list of conan options e.g.: `qt/*:shared=True,qt/*:GUI=True`.                                                      |
| conan_deploy_artifacts   | false                                              | If equals true, conan deploy() will be invoked and the output is saved as an artifact.                                             |
| conan_artifact_name      | if ommited a random name will be generated         | If conan_deploy_artifacts equals true you can give the workflow artifact a specific name. If kept empty a random name is generated |

### .github/workflows/createPackageGcpRunner.yml

Same purpose as [createPackage.yml](#githubworkflowscreatepackageyml), but runs the build in a Docker container on a self-hosted [gcp-hosted-github-runner](https://github.com/Privatehive/gcp-hosted-github-runner) instead of a regular GitHub-hosted runner. Use this when you need a specific machine type or a custom Docker build image.

``` yml
jobs:
  build_linux:
    name: "Build Linux"
    uses: Privatehive/conan-workflows/.github/workflows/createPackageGcpRunner.yml@master
    with:
      docker_image: "ghcr.io/privatehive/conan-ubuntu:latest"
      conan_host_profile: "androidArmv8"
      conan_remotes: https://conan.privatehive.de/artifactory/api/conan/public-conan
      conan_options: "qt/*:shared=True,qt/*:qtbase=True"
```

| input parameter          | default                                           | description                                                                                                                        |
| ------------------------ | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| docker_image             | `ghcr.io/privatehive/conan-ubuntu:latest`         | The Docker Image to use to build the conan package. Use one of [conan-ubuntu](#docker/ubuntu), [conan-wine](#docker/wine).         |
| machine_type             | `""`                                               | Provide a GCE machine type e.g. c2d-standard-8                                                                                     |
| conan_host_profile       | if ommited the conan default profile will be used | One of the [hostProfiles](#hostProfiles) (omit the `.profile` suffix - e.g. `androidArmv8`).                                       |
| conan_build_profile      | if ommited the conan default profile will be used | Like `conan_host_profile`, but for the build profile (`-pr:b`).                                                                    |
| conan_host_profile_path  | `""`                                               | Path to a custom conan host profile file, used instead of `conan_host_profile` when you don't want one of the predefined [hostProfiles](#hostProfiles). |
| conan_build_profile_path | `""`                                               | Like `conan_host_profile_path`, but for the build profile (`-pr:b`).                                                               |
| conan_recipe_path        | `./`                                               | The relative path pointing to the directory where `conanfile.py` is located.                                                       |
| conan_remotes            | `""`                                               | Comma separated list of conan remotes.                                                                                             |
| conan_options            | `""`                                               | Comma separated list of conan options e.g.: `qt/*:shared=True,qt/*:GUI=True`.                                                      |
| conan_build_require      | false                                              | Will run a "--build-require" build. Only has an effect if `conan_host_profile` is provided.                                        |
| conan_deploy_artifacts   | false                                              | If equals true, conan deploy() will be invoked and the output is saved as an artifact named `conan-package-artifacts`.             |

### .github/workflows/uploadRecipe.yml

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

| input parameter        | default                                | description                                                                                                                                             |
| ----------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| import_conan_cache     | false                                  | If `true`, restores a conan cache previously saved by [createPackage.yml](#githubworkflowscreatepackageyml)'s `export_conan_cache` before uploading.   |
| conan_recipe_path      | `./`                                   | The relative path pointing to the directory where `conanfile.py` is located.                                                                            |
| conan_versions         | if ommited the version declared in the recipe is used | Comma separated list of versions to export/upload (for recipes whose `conandata.yml` declares sources for several versions instead of hardcoding one). |
| conan_primary_version  | last entry of `conan_versions`         | Which of `conan_versions` is reported as the `conan-package` repo property (e.g. the one shown in a README badge).                                      |
| conan_upload_remote    | `""`                                   | The remote where the recipe will be uploaded to.                                                                                                        |
| upload_include_package | false                                  | If `true`, uploads the built binary packages in addition to the recipe. If `false` (default), only the recipe is uploaded (`--only-recipe`).            |
| publish_property       | `true`                                 | If `true` a custom property `conan-package` will be set containing the recipe ref. Make sure the custom property is enabled in the GitHub organization. |

| secret parameter      | default | description                                                                                             |
| --------------------- | ------- | ------------------------------------------------------------------------------------------------------- |
| conan_upload_login    | `""`    | The account to log into the remote.                                                                     |
| conan_upload_password | `""`    | The password of the account to log into the remote.                                                     |
| install_token_app_id  | `""`    | The app id of a GitHub app that has write access to organization/repository custom properties.          |
| install_token_secret  | `""`    | The app private key of a GitHub app that has write access to organization/repository custom properties. |

