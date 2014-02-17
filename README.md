<h1>FlyingDB</h1>
This is a side project for me that I hope could be useful to other people.

<h2>Description</h2>
An Android/iOS SQLite code generator utility written in Python



<h2>Introduction</h2>

FlyingDB generates simple object files and simple query methods based on any SQLite database file. The files generated provide a preliminary set of classes and methods for interacting with a database. Although the data query methods are simple CRUD operations, hopefully, this will provide a code base to build upon and save time in the long run.
 
Currently, this tool handles all data in the database as String values. This tool retrieves data from the database and converts to a String type and also updates the database using a String type. Multiple data types may not be a huge issue due to SQLite's data type affinity feature if data is stored in the correct format (for example, only integers being stored in integer columns even though it's sent as a string to the database).  

FlyingDB is released under the MIT License. See the license file for details.




<h2>Generating Code</h2>

FlyingDB is written as a Python script. flyingdb.py must be run in its home directory. To run and generate code, execute: 

	python flyingdb.py sqliteDBFile 


To run and generate code with a prefix in front of class names for POJOs, execute:

	python flyingdb.py sqliteDBFile prefix
	
	
The python script generates Android Java code in the generated\android directory and IOS code in the generated\ios directory. The Android database helper class files are DatabaseAdapter.java and DatabaseHelper.java. The IOS database adapter class files are DatabaseAdapter.h and DatabaseAdapter.m.





<h2>Using the Generated Code for Android</h2>

An example of using the generated code can be found in the accompanying FlyingDBExample Eclipse project. To add to an existing project, create a new package called com.flyingboba.flyingdb and copy your files into it. The Android generated code will require some modifications depending on how you want to create your database (creating from code or embedding your DB file in the App and copying over to accessible phone storage).

<h5>If you do not want to copy an existing database over and want to generate the database in code, you can make the following modifications:</h5>

To generate your database by code, do it in the onCreate method of DatabaseHelper. Remove the methods related to copying the database over which include copyDatabase, checkDatabase, and createDatabase. 

<h5>If you want to copy an existing database over, you can do so in the DatabaseAdapter.open() method by uncommenting and using the DatabaseHelper copyDatabase, checkDatabase, and createDatabase methods as shown in the FlyingDBExample code.</h5>


<b>DatabaseAdapter.java - </b> This file contains all the query methods for interacting with the database and utilizes the DatabaseHelper class.


<b>DatabaseHelper.java - </b> This file establishes a connection to the database and contains methods for copying an existing database over to phone storage.







<h2>Using the Generated Code for iOS</h2>

See and try out the example IOS project (FlyingDBExampleIOS) for how you might use the generated code. The main code that calls the generated code can be found in ViewController.m. In ViewController.m, the code creates the database by calling on the DatabaseAdapter.copyOverDatabase() method which copies the database (assuming that you included the database in your project) to the App's document path. If you want to create the database in code, you can do so, but the database needs to be created in the App's document path for the other DatabaseAdapter query methods to work. 


<h2>Thanks for checking this out and would appreciate any feedback!</h2>
