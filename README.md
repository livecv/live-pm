# Live CV Deployment Scripts

These are scripts used by Live CV modules to manage source code and create deployment packages.

 * **Version**: 1.4.0

## Usage

There are currently 4 available scripts:

 * livecv_build.py
 * livecv_deploy.py
 * livecv_license_sync.py
 * livecv_version_sync.py

All scripts require that live*.json configuration file is available in your repository.
The file basically describes the available packages within that particular repository and also the requirements to build and deploy those packages.

## Configuring livecv.json

A minimal livecv.json file would contain the following fileds:

```
{
  "version" : "0.0.1"
  "name": "repository_name"
}
```
## Building a livecv plugin

## Deploying a livecv plugin

## Syncing livecv plugin licenses

## Syncing livecv plugin versions

To sync a livecv version with the package file, run the following script:

```
livecv_version_sync.py [-s <source_dir>] <packagefile>
```





## Description

### livecv_version_sync.py


### livecv_license_set.py

Sets livecv license on all source files to the latest version. To run, simply
use it from livecv/build dir. To run it from somewhere else, specify the source
dir as its first argument:

```
livecv_license_set.py /path/to/livecv-src
```
