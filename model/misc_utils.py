from datetime import datetime
from datetime import date

'''

This provide all miscllenous functions which is used by all model controllers

Currently is has functionslity to return datetime object

'''

def getTodaysDate() ->date:
    return date.today()

def getCurDateTime() ->datetime:
    return datetime.now()