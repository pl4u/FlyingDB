//
//  ViewController.m
//  FlyingDB
//
//  Created by Paul Lee on 8/11/13.
//  Copyright (c) 2013 Paul Lee. All rights reserved.
//

#import "ViewController.h"
#import "DatabaseAdapter.h"
#import "Event.h"

@interface ViewController ()

@end

@implementation ViewController
@synthesize textView;

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
    [self demonstrateFlyingDB];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void) demonstrateFlyingDB
{
    
    [DatabaseAdapter copyOverDatabase];
    
    NSMutableString* output = [NSMutableString stringWithString: @"Demonstrating FlyingDB on table Event\n\n"];
    
    textView.text = output;
    
    // Perform Insert
    [output appendString:@"Adding a record with following fields:\n\tDate: 1983-01-23 15:23:00, Location ID: 0, Title: TestTitle\n"];
    textView.text = output;
    
    NSString* rowId = [DatabaseAdapter addEventWithDate:@"1983-01-23 15:23:00" withLocationId:@"0" withTitle:@"TestTitle"];
    [output appendFormat:@"Inserted event record has id %@\n\n", rowId];
    textView.text = output;
    
    
    // Perform Update
    [output appendString:@"Demonstrating record update......\n"];
    textView.text = output;
    [DatabaseAdapter updateEventWithDate:@"2013-07-23 12:00:00" withLocationId:@"14" withTitle:@"UpdatedTestTitle" withFieldName:@"id" withFieldValue:rowId];
    
    Event* event = nil;
    NSMutableArray* eventList = [DatabaseAdapter getEventListWithFieldName:@"id" withFieldValue:rowId withOrderBy:nil];
    if(eventList.count>0){
        event = [eventList objectAtIndex:0];
    }
    if(event==nil)
    {
        [output appendFormat:@"Event not found with rowId %@", rowId];
        return;
    }
    [output appendFormat:@"Record with id %@ now contains the following:\n\tDate: %@, LocationID: %@, Title: %@\n\n", rowId, event.date, event.locationId, event.title];
    textView.text = output;
    
    
    
    // Perform Delete
    [output appendFormat:@"Demonstrating record deletion......\nDeleting record with rowId %@\n", rowId];
    textView.text = output;
    [DatabaseAdapter removeEventWithFieldName:@"id" withFieldValue:rowId];
    
    // Select to verify changes to the DB
    event=nil;
    eventList = [DatabaseAdapter getEventListWithFieldName:@"id" withFieldValue:rowId withOrderBy:nil];
    if(eventList.count>0)
    {
        event = [[DatabaseAdapter getEventListWithFieldName:@"id" withFieldValue:rowId withOrderBy:nil] objectAtIndex:0];
    }
    if(event==nil)
    {
        [output appendFormat:@"Success! Could not find Event record with id %@\n\n", rowId];
    }
    else
    {
        [output appendFormat:@"Fail! Found Event record with id %@\n\n", rowId];
    }
    [output appendString: @"End of FlyingDB Demo"];
    textView.text = output;

}






@end
