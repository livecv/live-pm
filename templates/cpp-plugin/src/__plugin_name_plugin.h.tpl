#ifndef __{plugin_name_upper}_PLUGIN_H
#define __{plugin_name_upper}_PLUGIN_H

#include <QQmlExtensionPlugin>

class __{plugin_name_capital}Plugin : public QQmlExtensionPlugin{

    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QQmlExtensionInterface")

public:
    void registerTypes(const char *uri);
};

#endif // __{plugin_name_upper}_PLUGIN_H
