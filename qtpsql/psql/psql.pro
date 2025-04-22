#QT  = core core-private sql-private
QT = core sql

TARGET = qsqlpsql

INCLUDEPATH += \
    /usr/include/postgresql/internal/ \
    /usr/include/postgresql/

INCLUDEPATH += \
    ../qt/QtSql/5.15.16 \
    ../qt/QtSql/5.15.16/QtSql \
    ../qt/QtCore/5.15.16 \
    ../qt/QtCore/5.15.16/QtCore \
    ../qt \
    ../qt/QtSql \
    ../qt/QtCore


QT.sqldrivers.enabled_features = 
QT.sqldrivers.disabled_features = 
QT.sqldrivers.QT_CONFIG = 
QT.sqldrivers.exports = 
QT.sqldrivers_private.enabled_features = sql-psql 
QT.sqldrivers_private.disabled_features = sql-db2 sql-ibase sql-mysql sql-oci sql-odbc sql-sqlite2 sql-tds system-sqlite sql-sqlite
QT.sqldrivers_private.libraries = psql
QMAKE_LIBS_PSQL = -lpq

HEADERS += $$PWD/qsql_psql_p.h
SOURCES += $$PWD/qsql_psql.cpp $$PWD/main.cpp

CONFIG += sqldrivers_standalone

QMAKE_USE += psql

OTHER_FILES += psql.json

PLUGIN_CLASS_NAME = QPSQLDriverPlugin

PLUGIN_TYPE = sqldrivers
load(qt_plugin)

DEFINES += QT_NO_CAST_TO_ASCII QT_NO_CAST_FROM_ASCII
