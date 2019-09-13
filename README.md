# Live Package Manager

Live Package Manager is used to build, create and deploy packages for Live CV. 

 * **Version**: 1.4.0

## Usage

Run ```livepm/main.py help``` to see a list of available commands.

Commands that work on the source code require a package file to be available in the root of your source tree. The package
file should be named ```live*.json```, i.e. (```live.opencv.contrib.json```) and should describe the contents of the package and
also build and deployment requirements.

A minimal package file would contain the following fileds:

```
{
  "version" : "0.0.1"
  "name": "repository_name"
}
```

## Additional Info

Additional info on Live CV packages and package files is available [here](http://livekeys.dinusv.com/documentation/dev-deployment-scripts.html)



