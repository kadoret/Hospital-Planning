'''
Created on Nov 22, 2014

@author: knguyen
'''
import datetime

""" Calendar class  """
class calendar:
    def __init__(self, day, description, mytype, passed, irange =  None, work = None):
        self.day = day
        self.desc = description
        self.type = mytype
        self.passed = passed
        self.range = irange
        self.work = work

      
        
def getFirstDayOfMonth(aDay):
    myMonth = aDay.month
    myYear = aDay.year
    return datetime.date(myYear, myMonth, 1)

def isNewMonth(aDay, aNewDay):
    myMonth = aDay.month
    myNewMonth = aNewDay.month
    if myMonth !=  myNewMonth:
        return True
    else:
        return False