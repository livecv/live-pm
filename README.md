# Live CV Scripts

Scripts used to manage Live CV build and deployment processes.

## Usage

Copy these scripts to live cv build directory and run.

## Description

### livecv_license_set.py

Sets livecv license on all source files to the latest version. To run, simply
use it from livecv/build dir. To run it from somewhere else, specify the source
dir as its first argument:

```
livecv_license_set.py /path/to/livecv-src
```

### livecv_version.py

Get or set the livecv version.

To print the version:

```
livecv_version.py get [<source_dir>]
```

To set the version

```
livecv_version.py set <major>.<minor>.<patch> [<source_dir>]
```

Where source dir is not required if the script is used from livecv/build directory.


### livecv_build.py

Build Live CV.



### livecv_deploy.py

Deploy live cv after the build process
