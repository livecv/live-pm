PLUGIN_NAME = __plugin_name
PLUGIN_PATH = __plugin_path

## PLUGIN_NAME and PLUGIN_PATH must be set up prior to including this config file
include($$LIVECV_DEV_PATH/project/plugin.pri)

TARGET = live__{_plugin_name}
uri = __plugin_uri

DEFINES += Q_LCV

## Dependencies (linkPlugin(...))


## Deploying qml is handled by the plugin.pri configuration

## Source

include($$PWD/src/__plugin_name.pri)

OTHER_FILES *= \
    qml/*.qml \
    qml/qmldir
