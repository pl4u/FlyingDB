FlyingDB
========

Description
An Android/iOS SQLite code generator utility written in Python



Introduction

FlyingDB generates Plain Old Java Objects (POJOs) and simple query methods based on any SQLite database file. The files 
generated provide a preliminary set of classes and methods for interacting with a database. 
Although the data query methods are simple CRUD operations, hopefully, this will provide a code base
to build upon and save time in the long run.
 
This software utility is still being developed and the goal will be to eventually also generate iOS code as well.
Currently, this tool handles all data in the database as String values. This tool retrieves data from the database and converts 
to a String type and also updates the database using a String type. Supporting non-String data types will be added in a future 
release. Multiple data types may not be a huge issue due to SQLite's data type affinity feature if data is stored in the correct format 
(for example, only integers being stored in integer columns even though it's sent as a string to the database).  

FlyingDB is released under the MIT License. See the license file for details.




Generating Code

FlyingDB is written as a Python script. flyingdb.py must be run in its home directory. To run and generate code, execute: 

	python flyingdb.py sqliteDBFile 


To run and generate code with a prefix in front of class names for POJOs, execute:

	python flyingdb.py sqliteDBFile prefix
	
	
The python script generates Android Java code in the generated\android directory. The database helper classes are DatabaseAdapter.java and 
DatabaseHelper.java.





Using the Generated Code for Android

An example of using the generated code can be found in the accompanying FlyingDBExample Eclipse project.
To add to an existing project, create a new package called com.flyingboba.flyingdb and copy your files into it.


DatabaseAdapter.java

This file contains all the query methods for interacting with the database and utilizes the DatabaseHelper class.


DatabaseHelper.java

This file establishes a connection to the database and contains methods for copying an existing database over to phone storage.


If you do not want to copy an existing database over and want to generate the database in code, you can make the following modifications:
To generate your database by code, do it in the onCreate method of DatabaseHelper. Remove the methods related to copying the database over 
which include copyDatabase, checkDatabase, and createDatabase. Also, remove the call to createDatabase in the DatabaseAdapter open method.




Using the Generated Code for iOS

Currently, the iOS dev branch only produces simple objective-c objects and the database helper classes are not created.

