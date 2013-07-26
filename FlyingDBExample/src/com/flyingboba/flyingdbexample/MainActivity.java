/*
 * Copyright (C) 2013 Paul Lee
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
 * documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
 * the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and 
 * to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
 * the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
 * THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * 
 * 
 * FlyingDB Example
 * 7/23/2013
 * Paul Lee
 * 
 * This code demonstrates use of the package com.flyingboba.flyingdb generated with FlyingDB.
 * The code below connects to the test.sqlite database, inserts a record to the Events table, updates the same record,
 * and then deletes the record.
 * 
 * Status updates are output to the EditText view.
 * 
 * The sqlite database file used to generate the com.flyingboba.flyingdb package can be found in assets.
 * 
 */

package com.flyingboba.flyingdbexample;

import java.util.List;

import android.os.Bundle;
import android.app.Activity;
import android.widget.EditText;

import com.flyingboba.flyingdb.*;

public class MainActivity extends Activity {

	private EditText textbox;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		textbox = (EditText) findViewById(R.id.editText);
		demonstrateFlyingDB();
	}

	public void demonstrateFlyingDB() {
		textbox.append("Demonstrating FlyingDB on table Event\n\n");
		DatabaseAdapter dbAdapter = new DatabaseAdapter(this);
		dbAdapter.open();

		List<PrefixEvent> rowList = null;
		PrefixEvent row = null;

		// Perform Insert
		textbox.append("Adding a record with following fields:\n");
		textbox.append("\tTime: 1983-01-23 15:23:00, Location ID: 0, Title: TestTitle\n\n");
		String rowId = Long.toString(dbAdapter.addEvent("1983-01-23 15:23:00", "0",
				"TestTitle"));
		textbox.append("Inserted event record has id " + rowId + ".\n\n");
		
		rowList = dbAdapter.getEventList("id", rowId, null);
		if (rowList.size() > 0) {
			row = rowList.get(0);
			textbox.append("Select event on id " + rowId + " returns:\n");
			textbox.append("\tTime: " + row.getDate() + ", Location ID: " + row.getLocationId() + ", Title: " + row.getTitle() + "\n\n");
		} else {
			textbox.append("Record with id " + rowId + " not found!\n\n");
		}

		// Perform Update
		textbox.append("Demonstrating record update......\n");
		dbAdapter.updateEvent("2013-07-23 12:00:00", "14", "UpdatedTestTitle", "id",
				rowId);
		rowList = dbAdapter.getEventList("id", rowId, null);
		if (rowList.size() > 0) {
			row = rowList.get(0);
			textbox.append("Updated Event with id " + rowId + " now contains following:\n");
			textbox.append("\tTime: " + row.getDate() + ", Location ID: " + row.getLocationId() + ", Title: " + row.getTitle() + "\n\n");
		} else {
			textbox.append("Record with id " + rowId + " not found!\n\n");
		}

		// Perform Delete
		textbox.append("Demonstrating row deletion......\n");
		textbox.append("\tDeleting record with id " + rowId + "\n");
		dbAdapter.removeEvent("id", rowId);
		// Select verifies changes to the DB
		rowList = dbAdapter.getEventList("id", rowId, null);
		if (rowList.size() == 0) {
			textbox.append("Success!\n");
		} else {
			textbox.append("Fail!\n");
		}

		dbAdapter.close();

	}

}
