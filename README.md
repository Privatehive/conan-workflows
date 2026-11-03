# conan-workflows

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Privatehive/conan-workflows/main.yml?branch=master&style=flat&logo=github&label=Docker+build)](https://github.com/Privatehive/conan-workflows/actions?query=branch%3Amaster)

**This shared GitHub workflows help you to build/upload conan packages**

### Conan profiles

Contains predefined Conan host/build profiles which can be used by projects targeting different operating systems and architectures.
If a build profile exists you should also use it. Only using a host profile w/o the matching build profile will probably fail.

**Android**
```
androidArmv7.host.profile
androidArmv8.host.profile
androidx86.host.profile
androidx86_64.host.profile
android.build.profile
```

**Windows (MinGW)**

```
windowsMinGW.host.profile
windowsMinGW.build.profile
```

**Raspberry Pi OS**
```
raspberrypiosArmv6.host.profile
raspberrypiosArmv8.host.profile
```

### docker/ubuntu

Contains a Dockerfile that provides a conan environment to build binaries for Linux.

### docker/wine

Contains a Dockerfile that provides a conan environment to build binaries for Windows (by using wine).

### .github/workflows/createPackage.yml

Use this shared GitHub workflow to create a Conan package on a regular GitHub-hosted runner (e.g. `ubuntu-22.04`, `windows-2022`, `macos-15`). If you need a self-hosted [gcp-hosted-github-runner](https://github.com/Privatehive/gcp-hosted-github-runner) instead (e.g. for a custom machine type), use [createPackageGcpRunner.yml](#githubworkflowscreatepackagegcprunneryml).

``` yml
jobs:
  build_linux:
    name: "Build Linux"
    uses: Privatehive/conan-workflows/.github/workflows/createPackage.yml@master
    with:
      image: "ubuntu-22.04"
      conan_host_profile: "androidArmv8.host.profile"
      conan_build_profile: "android.build.profile"
      conan_remotes: https://conan.privatehive.de/artifactory/api/conan/public-conan
      conan_options: "qt/*:shared=True,qt/*:qtbase=True"
```

| input parameter          | default                                               | description                                                                                                                                                                                                                                                                               |
| ------------------------ | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name                     | `Create package`                                      | A name for the build step                                                                                                                                                                                                                                                                 |
| image                    | `ubuntu-latest`                                       | The GitHub-hosted runner image to build the conan package on, e.g. `ubuntu-22.04`, `windows-2022`, `macos-15`.                                                                                                                                                                            |
| export_conan_cache       | false                                                 | If `true`, the conan cache is saved as a GitHub Actions cache entry (keyed by `${{ runner.os }}-${{ github.sha }}`) after the build, so a later job/workflow run can restore it via `import_conan_cache`.                                                                                 |
| import_conan_cache       | false                                                 | If `true`, restores a conan cache previously saved with `export_conan_cache` before building. Fails the job if no matching cache entry exists.                                                                                                                                            |
| export_conan_cache_key   | `""`                                                  | Optional suffix appended to the cache key used by `export_conan_cache` (`${{ runner.os }}-${{ github.sha }}-<suffix>`). Needed when several jobs of the same workflow run export a cache on the same OS, as a cache key can only be saved once.                                           |
| import_conan_cache_key   | `""`                                                  | Optional suffix of the cache key restored by `import_conan_cache` (see `export_conan_cache_key`). A job can import one cache and export an extended one under a different suffix, e.g. to collect the binaries of several builds for [uploadRecipe.yml](#githubworkflowsuploadrecipeyml). |
| conan_host_profile       | if omitted the conan default profile will be used     | One of the [*.host.profiles](#conan-profiles).                                                                                                                                                                                                                                            |
| conan_build_profile      | if omitted the conan default profile will be used     | One of the [*.build.profiles](#conan-profiles).                                                                                                                                                                                                                                           |
| conan_host_profile_path  | `""`                                                  | Path to a custom conan host profile file, used instead of `conan_host_profile` when you don't want one of the predefined [*.host.profiles](#conan-profiles).                                                                                                                              |
| conan_build_profile_path | `""`                                                  | Path to a custom conan build profile file, used instead of `conan_build_profile` when you don't want one of the predefined [*.build.profiles](#conan-profiles).                                                                                                                           |
| conan_build_require      | false                                                 | Will run a "--build-require" build. Only has an effect if a host profile is provided.                                                                                                                                                                                                     |
| conan_recipe_path        | `./`                                                  | The relative path pointing to the directory where `conanfile.py` is located.                                                                                                                                                                                                              |
| conan_version            | if omitted the version declared in the recipe is used | The version to build, passed as `--version` to conan. Use this when the recipe doesn't hardcode a version (e.g. `conandata.yml` declares sources for several versions).                                                                                                                   |
| conan_remotes            | `""`                                                  | Comma separated list of conan remotes.                                                                                                                                                                                                                                                    |
| conan_options            | `""`                                                  | Comma separated list of conan options e.g.: `qt/*:shared=True,qt/*:GUI=True`.                                                                                                                                                                                                             |
| conan_deploy_artifacts   | false                                                 | If equals true, conan deploy() will be invoked and the output is saved as an artifact.                                                                                                                                                                                                    |
| conan_artifact_name      | if omitted a random name will be generated            | If conan_deploy_artifacts equals true you can give the workflow artifact a specific name. If kept empty a random name is generated                                                                                                                                                        |

### .github/workflows/createPackageGcpRunner.yml

Same purpose as [createPackage.yml](#githubworkflowscreatepackageyml), but runs the build in a Docker container on a self-hosted [gcp-hosted-github-runner](https://github.com/Privatehive/gcp-hosted-github-runner) instead of a regular GitHub-hosted runner. Use this when you need a specific machine type or a custom Docker build image.

``` yml
jobs:
  build_linux:
    name: "Build Linux"
    uses: Privatehive/conan-workflows/.github/workflows/createPackageGcpRunner.yml@master
    with:
      docker_image: "ghcr.io/privatehive/conan-ubuntu:latest"
      conan_host_profile: "androidArmv8.host.profile"
      conan_build_profile: "android.build.profile"
      conan_remotes: https://conan.privatehive.de/artifactory/api/conan/public-conan
      conan_options: "qt/*:shared=True,qt/*:qtbase=True"
```

| input parameter          | default                                           | description                                                                                                                                                     |
| ------------------------ | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| docker_image             | `ghcr.io/privatehive/conan-ubuntu:latest`         | The Docker Image to use to build the conan package. Use one of [conan-ubuntu](#docker/ubuntu), [conan-wine](#docker/wine).                                      |
| machine_type             | `""`                                              | Provide a GCE machine type e.g. c2d-standard-8                                                                                                                  |
| conan_host_profile       | if omitted the conan default profile will be used | One of the [*.host.profiles](#conan-profiles).                                                                                                                  |
| conan_build_profile      | if omitted the conan default profile will be used | One of the [*.build.profiles](#conan-profiles).                                                                                                                 |
| conan_host_profile_path  | `""`                                              | Path to a custom conan host profile file, used instead of `conan_host_profile` when you don't want one of the predefined [*.host.profiles](#conan-profiles).    |
| conan_build_profile_path | `""`                                              | Path to a custom conan build profile file, used instead of `conan_build_profile` when you don't want one of the predefined [*.build.profiles](#conan-profiles). |
| conan_recipe_path        | `./`                                              | The relative path pointing to the directory where `conanfile.py` is located.                                                                                    |
| conan_remotes            | `""`                                              | Comma separated list of conan remotes.                                                                                                                          |
| conan_options            | `""`                                              | Comma separated list of conan options e.g.: `qt/*:shared=True,qt/*:GUI=True`.                                                                                   |
| conan_build_require      | false                                             | Will run a "--build-require" build. Only has an effect if a host profile is provided.                                                                           |
| conan_deploy_artifacts   | false                                             | If equals true, conan deploy() will be invoked and the output is saved as an artifact named `conan-package-artifacts`.                                          |

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

| input parameter        | default                                               | description                                                                                                                                                                         |
| ---------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| import_conan_cache     | false                                                 | If `true`, restores a conan cache previously saved by [createPackage.yml](#githubworkflowscreatepackageyml)'s `export_conan_cache` before uploading.                                |
| import_conan_cache_key | `""`                                                  | Optional suffix of the cache key to restore, matching the `export_conan_cache_key` of the [createPackage.yml](#githubworkflowscreatepackageyml) job whose cache should be uploaded. |
| conan_recipe_path      | `./`                                                  | The relative path pointing to the directory where `conanfile.py` is located.                                                                                                        |
| conan_versions         | if omitted the version declared in the recipe is used | Comma separated list of versions to export/upload (for recipes whose `conandata.yml` declares sources for several versions instead of hardcoding one).                              |
| conan_primary_version  | last entry of `conan_versions`                        | Which of `conan_versions` is reported as the `conan-package` repo property (e.g. the one shown in a README badge).                                                                  |
| conan_upload_remote    | `""`                                                  | The remote where the recipe will be uploaded to.                                                                                                                                    |
| upload_include_package | false                                                 | If `true`, uploads the built binary packages in addition to the recipe. If `false` (default), only the recipe is uploaded (`--only-recipe`).                                        |
| publish_property       | `true`                                                | If `true` a custom property `conan-package` will be set containing the recipe ref. Make sure the custom property is enabled in the GitHub organization.                             |

| secret parameter      | default | description                                                                                             |
| --------------------- | ------- | ------------------------------------------------------------------------------------------------------- |
| conan_upload_login    | `""`    | The account to log into the remote.                                                                     |
| conan_upload_password | `""`    | The password of the account to log into the remote.                                                     |
| install_token_app_id  | `""`    | The app id of a GitHub app that has write access to organization/repository custom properties.          |
| install_token_secret  | `""`    | The app private key of a GitHub app that has write access to organization/repository custom properties. |
