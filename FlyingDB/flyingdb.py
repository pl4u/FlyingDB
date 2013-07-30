'''
Copyright (C) 2013 Paul Lee

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and 
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

# ---------------------------------------------------------------------
# FlyingDB
# 
# Paul Lee
# 7/29/2013
#
# ---------------------------------------------------------------------

import sqlite3 as lite
import sys
import os
import shutil


GENERATED_DIR = 'generated/'
ANDROID_DIR = GENERATED_DIR + 'android/'
IOS_DIR = GENERATED_DIR + 'ios/'

# ---------------------------------------------------------------------
#
#  Extract database meta-data
#
#
# ---------------------------------------------------------------------

# Static Column Indexes for table data returned
COL_ORDER_INDEX = 0
COL_NAME_INDEX = 1
COL_TYPE_INDEX = 2

def getTableData(dbName, tableName):
    con = lite.connect(dbName)
    with con:
        cur = con.cursor()
        cur.execute('PRAGMA table_info(' + tableName + ')')
        data = cur.fetchall()
        return data

def getTableNames(dbName):
    tableList = []
    con = lite.connect(dbName)
    with con:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        rows = cur.fetchall()
        for row in rows:
            tableList.append(row[0])
    return tableList


# ---------------------------------------------------------------------
#
#  Create JAVA POJOs
#
#
# ---------------------------------------------------------------------
def createJavaClass(prefix, tableName, tableData):
    outFile = open(ANDROID_DIR + prefix + tableName + '.java', 'w')    
    outFile.write('//**********************************************************\n')
    outFile.write('//************** AUTOGENERATED with FLYINGDB ***************\n')
    outFile.write('//**********************************************************\n\n')
    outFile.write('package com.flyingboba.flyingdb;\n\n\n')
    outFile.write('public class ' + prefix + tableName + ' {\n')
    
    memberDeclarations = ''
    constructorParams = ''
    constructorInitStatements = ''
    javaGets = ''
    javaSets = ''
    for d in tableData:
        memberDeclarations += '\tprivate String ' + objCFormat(tableName, d[COL_NAME_INDEX]) + ';\n'
        javaGets += createJavaGet(objCFormat(tableName, d[COL_NAME_INDEX]))
        javaSets += createJavaSet(objCFormat(tableName, d[COL_NAME_INDEX]))
        constructorInitStatements += '\t\tset' + capitalize(objCFormat(tableName, d[COL_NAME_INDEX])) + '(' + objCFormat(tableName, d[COL_NAME_INDEX]) + ');\n'

    for i in range(0, len(tableData)-1):
        constructorParams += 'String ' +  objCFormat(tableName, tableData[i][COL_NAME_INDEX]) + ', '
    constructorParams += 'String ' +  objCFormat(tableName, tableData[len(tableData)-1][COL_NAME_INDEX])

    outFile.write('\n')

    outFile.write(memberDeclarations)

    outFile.write('\n')

    outFile.write('\tpublic ' + prefix + tableName + '(' + constructorParams + ') {\n')
    outFile.write(constructorInitStatements)
    outFile.write('\t}\n')

    outFile.write('\n')

    outFile.write(javaSets)
    outFile.write(javaGets)

    outFile.write('}')
    outFile.close()

def createJavaGet(memberName):
    getString = ''
    getString += '\tpublic String get' + capitalize(memberName) + '() {\n'
    getString += '\t\treturn ' + memberName + ';\n'
    getString += '\t}\n\n'
    return getString

def createJavaSet(memberName):
    setString = ''
    setString += '\tpublic void set' + capitalize(memberName) + '(String ' + memberName + ') {\n'
    setString += '\t\tthis.' + memberName + ' = ' + memberName + ';\n'
    setString += '\t}\n\n'
    return setString

# ---------------------------------------------------------------------
#
#  Create ObjC POJOs
#
#
# ---------------------------------------------------------------------
def createObjCClass(prefix, tableName, tableData):
    outFile = open(IOS_DIR + prefix + tableName+'.h', 'w')
    outFile.write('//**********************************************************\n')
    outFile.write('//************** AUTOGENERATED with FLYINGDB ***************\n')
    outFile.write('//**********************************************************\n\n')
    outFile.write('#import <Foundation/Foundation.h>\n\n')
    outFile.write('@interface ' + prefix + tableName + ' : NSObject\n\n')
    for d in tableData:
        outFile.write('@property (strong) NSString* ' + objCFormat(tableName, d[COL_NAME_INDEX]) + ';\n')
    outFile.write('\n')
    outFile.write(' - (id) init;\n')
    initWithString = ' - (id) initWith' + capitalize(objCFormat(tableName,tableData[0][COL_NAME_INDEX])) + ': (NSString*) param' + capitalize(objCFormat(tableName,tableData[0][COL_NAME_INDEX]))
    for i in range(1, len(tableData)):
        initWithString += ' with' + capitalize(objCFormat(tableName,tableData[i][COL_NAME_INDEX])) + ': (NSString*) param' + capitalize(objCFormat(tableName,tableData[i][COL_NAME_INDEX]))
    initWithString += ';\n'
    outFile.write(initWithString)
    outFile.write('\n@end')
    outFile.close()

    # Create the .m file
    outFile = open(IOS_DIR + prefix + tableName+'.m', 'w')
    outFile.write('//**********************************************************\n')
    outFile.write('//************** AUTOGENERATED with FLYINGDB ***************\n')
    outFile.write('//**********************************************************\n\n')
    outFile.write('#import ' + prefix + tableName + '.h\n\n')
    outFile.write('@implementation ' + prefix + tableName + '\n\n')
    for d in tableData:
        outFile.write('@synthesize ' + objCFormat(tableName,d[COL_NAME_INDEX]) + ';\n')
    outFile.write('\n')
    outFile.write('- (id) init\n')
    outFile.write('{\n')
    initWithStringNil = 'initWith' + capitalize(objCFormat(tableName, tableData[0][COL_NAME_INDEX])) + ': nil'
    for i in range(1, len(tableData)):
        initWithStringNil += ' with' + capitalize(objCFormat(tableName, tableData[i][COL_NAME_INDEX])) + ': nil'
    outFile.write('\treturn [self ' + initWithStringNil + '];\n')
    outFile.write('}\n')

    outFile.write(initWithString)
    outFile.write('{\n')
    outFile.write('\tself = [super init];\n')
    outFile.write('\tif(self)\n')
    outFile.write('\t{\n')
    for d in tableData:
        outFile.write('\t\t' + objCFormat(tableName, d[COL_NAME_INDEX]) + ' = ' + 'param' + capitalize(objCFormat(tableName, d[COL_NAME_INDEX])) + ';\n')
    outFile.write('\t}\n')
    outFile.write('\treturn self;\n')
    outFile.write('}\n')
    outFile.close()

# ---------------------------------------------------------------------
#
#  Utility functions
#
#
# ---------------------------------------------------------------------

# id is reserved in objective c
# if a column is named id, then rename so that it becomes prefix + 'Id'
def objCFormat(prefix, string) :
    if string=='id' :
        return decapitalize(prefix) + 'Id'
    return string

# Return the string with the first letter lower cased
def decapitalize(string):
    return string[0].lower() + string[1:]

# Return the string with the first letter upper cased
def capitalize(string):
    return string[0].upper() + string[1:]

# This may not be needed
def createColumnLookup(prefix, tableName, tableData):
    print 'createColumnLookup stub'  
    count=0
    stringLookup = 'public final static string[] ' + prefix + tableName + 'DataLookup = {' 
    enumData = 'public enum ' + prefix + tableName + 'DataEnum ' + ' {\n\t'
    for d in tableData:
        enumData += d[COL_NAME_INDEX] + '(' + str(count) + '), '
        stringLookup += '"' + d[COL_NAME_INDEX] + '", '
        count += 1
    enumData = enumData.rstrip(', ')
    enumData += '\n}'
    stringLookup = stringLookup.rstrip(', ')
    stringLookup += '};'
    print enumData
    print stringLookup



# ---------------------------------------------------------------------
#
#  Create Android Query Methods
#
#
# ---------------------------------------------------------------------


def createJavaQueryMethods(prefix, tableName, tableData):
    queryMethods = '\n\n\t// -----------------------------------------------------------------------------'
    queryMethods += '\n\t// ' + tableName + ' Query Methods'
    queryMethods += '\n\t// -----------------------------------------------------------------------------'
    queryMethods += '\n' + createJavaSelectMethods(prefix, tableName, tableData)
    queryMethods += '\n' + createJavaInsertMethods(prefix, tableName, tableData)
    queryMethods += '\n' + createJavaUpdateMethods(prefix, tableName, tableData) 
    queryMethods += '\n' + createJavaDeleteMethods(tableName)
    return queryMethods

def createJavaSelectMethods(prefix, tableName, tableData):
    queryString = 'SELECT '
    for d in tableData:
        queryString += d[COL_NAME_INDEX] +', '
    queryString = queryString.rstrip(', ')
    templateFile = open('Templates/Java/Select.txt', 'r')
    templateString = templateFile.read()
    templateFile.close()

    templateString = templateString.replace('[POJO]', prefix + tableName)
    templateString = templateString.replace('[TABLE_NAME_CAPITAL]', capitalize(tableName))
    templateString = templateString.replace('[SELECT_QUERY]', queryString)
    templateString = templateString.replace('[TABLE_NAME]', tableName)

    newPojoString = 'new ' + prefix + tableName + '('
    for i in range(0, len(tableData)):
        newPojoString += 'result.getString(' + str(i) + '), '
    newPojoString = newPojoString.rstrip(', ') + ')'
    templateString = templateString.replace('[NEW_POJO]', newPojoString)

    return templateString

def createJavaInsertMethods(prefix, tableName, tableData):
    fields = ''
    values = ''
    pojoMembers = ''
    for d in tableData:
        # Do not set key on insert
        if d[5] != 1:
            fields += 'String a' + capitalize(d[COL_NAME_INDEX]) + ', '
            values += 'values.put("' + d[COL_NAME_INDEX] + '", a' + capitalize(d[COL_NAME_INDEX]) + ');\n\t\t'
            pojoMembers += 'pojo.get' + capitalize(objCFormat(tableName, d[COL_NAME_INDEX])) + '(), '
    fields = fields.rstrip(', ')
    pojoMembers = pojoMembers.rstrip(', ')
    templateFile = open('Templates/Java/Insert.txt', 'r')
    templateString = templateFile.read()
    templateFile.close()
    templateString = templateString.replace('[TABLE_NAME_CAPITAL]', capitalize(tableName))
    templateString = templateString.replace('[TABLE_NAME]', tableName)
    templateString = templateString.replace('[TABLE_FIELDS]', fields)
    templateString = templateString.replace('[VALUES]', values) 
    
    pojoInsertString = '\n\n\tpublic long add' + capitalize(tableName) + '(' + prefix + tableName + ' pojo) {'
    pojoInsertString += '\n\t\treturn add' + capitalize(tableName) + '(' + pojoMembers + ');' 
    pojoInsertString += '\n\t}'
    
    templateString += pojoInsertString
    return templateString

def createJavaUpdateMethods(prefix, tableName, tableData):
    fields = ''
    values = ''
    pojoMembers = ''
    for d in tableData:
        # Do not set key on update
        if d[5] != 1:
            fields += 'String a' + capitalize(d[COL_NAME_INDEX]) + ', '
            values += 'values.put("' + d[COL_NAME_INDEX] + '", a' + capitalize(d[COL_NAME_INDEX]) + ');\n\t\t'
            pojoMembers += 'pojo.get' + capitalize(objCFormat(tableName, d[COL_NAME_INDEX])) + '(), '
    fields = fields.rstrip(', ')
    pojoMembers = pojoMembers.rstrip(', ') 
    templateFile = open('Templates/Java/Update.txt', 'r')
    templateString = templateFile.read()
    templateFile.close()
    templateString = templateString.replace('[TABLE_NAME_CAPITAL]', capitalize(tableName))
    templateString = templateString.replace('[TABLE_NAME]', tableName)
    templateString = templateString.replace('[TABLE_FIELDS]', fields)
    templateString = templateString.replace('[VALUES]', values) 
    
    pojoUpdateString = '\n\n\tpublic long update' + capitalize(tableName) + '(' + prefix + tableName + ' pojo, String fieldName, String fieldValue) {'
    pojoUpdateString += '\n\t\treturn update' + capitalize(tableName) + '(' + pojoMembers + ', fieldName, fieldValue);' 
    pojoUpdateString += '\n\t}'
    
    templateString += pojoUpdateString
    return templateString

def createJavaDeleteMethods(tableName):
    templateFile = open('Templates/Java/Delete.txt', 'r')
    templateString = templateFile.read()
    templateFile.close()
    templateString = templateString.replace('[TABLE_NAME]', tableName)
    templateString = templateString.replace('[TABLE_NAME_CAPITAL]', capitalize(tableName))

    return templateString

def setupJavaDatabaseAdapter(queryMethods):
    templateFile = open('Templates/Java/DatabaseAdapter.txt', 'r')
    dbAdapterFile = open(ANDROID_DIR + '/DatabaseAdapter.java', 'w')
    templateString = templateFile.read()
    templateString = templateString.replace('[QUERY_METHODS]', queryMethods)
    dbAdapterFile.write(templateString)
    templateFile.close()
    dbAdapterFile.close()

def setupJavaDatabaseHelper(dbName, dbVersion, dbPath):
    templateFile = open('Templates/Java/DatabaseHelper.txt', 'r')
    dbHelperFile = open(ANDROID_DIR + '/DatabaseHelper.java', 'w')
    templateString = templateFile.read()
    templateString = templateString.replace('[DATABASE_NAME]', dbName)
    templateString = templateString.replace('[DATABASE_VERSION]', dbVersion)
    templateString = templateString.replace('[DATABASE_PATH]', dbPath)
    dbHelperFile.write(templateString)
    templateFile.close()
    dbHelperFile.close()

# ---------------------------------------------------------------------
#
#  Create iOS Query Methods
#
#
# ---------------------------------------------------------------------

def createObjCQueryMethods(Prefix, TableName, TableData):
    print 'CreateObjCQueryMethods Stub'


def setupObjCDatabaseAdapterH(queryMethods):
    templateFile = open('Templates/ObjC/DatabaseAdapterH.txt', 'r')
    dbAdapterFile = open(IOS_DIR + '/DatabaseAdapter.h', 'w')
    templateString = templateFile.read()
    dbAdapterFile.write(templateString)
    templateFile.close()
    dbAdapterFile.close()



# ---------------------------------------------------------------------
#
#  Main function that calls all of the other functions
#
#
# ---------------------------------------------------------------------
def fly(dbName, prefix):       

    if not os.path.exists(GENERATED_DIR):
        os.makedirs(GENERATED_DIR)
    else:
        shutil.rmtree(GENERATED_DIR)       
    if not os.path.exists(ANDROID_DIR):
        os.makedirs(ANDROID_DIR)
    if not os.path.exists(IOS_DIR):
        os.makedirs(IOS_DIR)
    
    tables =  getTableNames(dbName)
    tableNames = ''
    javaQueryMethods = ''
    for tableName in tables:
        tableData = getTableData(dbName, tableName)
        createJavaClass(prefix, tableName, tableData)
        createObjCClass(prefix, tableName, tableData)
        tableNames += '"' + tableName + '",'
        javaQueryMethods += createJavaQueryMethods(prefix, tableName, tableData)
    
    tableNames = tableNames.rstrip(',')
    
    setupJavaDatabaseAdapter(javaQueryMethods)
    setupJavaDatabaseHelper('test.sqlite', '1', '/data/data/COM.YOUR.PACKAGE.NAME/databases/')


if len(sys.argv)<2:
    print 'Usage --  flyingdb.py sqliteFileName optionalClassPrefix\n\n'
    print 'Or\n\n'
    print 'flyingdb.py sqliteFileName'
elif len(sys.argv)==3:
    fly(sys.argv[1], sys.argv[2])
elif len(sys.argv)==2:
    fly(sys.argv[1],'')
