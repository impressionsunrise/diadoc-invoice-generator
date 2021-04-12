# -*- coding: utf-8 -*-
"""
Created on Sat May  9 00:30:21 2020

@author: IVAALEX
"""


import pandas as pd
from TimeUtility import TimeUtility 
from loguru import logger



class EffortsReader(object):
    def __init__(self):
        self.effortsDict = {}
        self.totalEfforts = TimeUtility.NULL_TIME
        self._timeUtil = TimeUtility()
    def generateEffortDict():
        pass
    def getEffortsDict(self):
        return self.effortsDict
    def getTotalEfforts(self):
        """ None -> datetime.time
            Calculate total efforts from effortDict and return it
        """
        sumEfforts = TimeUtility.NULL_TIME
        
        for key in self.effortsDict:
            self.timeUtil.addTimes(sumEfforts, self.effortsDict[key])
        
        return sumEfforts

class ExcelEffortsReader(EffortsReader):
    def __init__(self, path):
        super().__init__()
        self._readExcelFile(path)
       
    def generateEffortDict(self):
        """ None -> Dictionary
            Calculate dictionary with sum of efforts by service and return it.
            Also assign self.effortsDict to it
        """
        column = { "Executor":0,
                   "Date":1,
                   "Comment":2,
                   "Service":3,
                   "TicketNumber":4,
                   "TicketName":5,
                   "Applicant":6,
                   "Hours":7
                   }
        
        effortsDict = {}
        for i, line in self.excelData.iterrows():
            if line[column["TicketNumber"]] != 0:
                if line[column["Service"]] in effortsDict.keys():
                    effortsDict[line[column["Service"]]] = self._timeUtil.addTimes(effortsDict[line[column["Service"]]], line[column["Hours"]])
                else:
                    effortsDict[line[column["Service"]]] = self._timeUtil.addTimes(TimeUtility.NULL_TIME, line[column["Hours"]])
        
        for effort in effortsDict:
            effortsDict[effort] = self._timeUtil.convertToDecimal(effortsDict[effort])
       
        self.effortsDict = effortsDict
         
        return self.effortsDict
    
    
            
    def _readExcelFile(self,path):
        """ os.path -> None
            Read data from file under the path provided
            If read is not successful, then ....
        """
        try:
            logger.debug(path)
            self.excelData = pd.read_excel(path)
        except Exception as e:
            print(e)


class APIEffortsReader(EffortsReader):
    def __init__(self, path):
        super().__init__()
    def generateEffortDict():
        pass

class EffortsReaderFactory(object):
    def createEffortsReader(self, typ, param1):
         targetclass = typ
         return globals()[targetclass](param1)

      


if __name__ == '__main__':

    # effortsList = {}
    # df = pd.read_excel (r'efforts2.xls')
    # sumEfforts = "%d:%02d:%02d" % (0, 0, 0)
    # timeUtil = TimeUtility()
    # for i, j in df.iterrows():
    
    #     if j[4] != 0:
    #         if j[3] in effortsList.keys():
    #             effortsList[j[3]] = timeUtil.addTimes(effortsList[j[3]], j[7])
    #         else:
    #             effortsList[j[3]] = timeUtil.addTimes("00:00:00", j[7])
    #         sumEfforts = timeUtil.addTimes(sumEfforts, j[7])
          
          
    # print(sumEfforts)
    path = (r'efforts2.xls')
    effort = ExcelEffortsReader(path)
    effortsDict = effort.generateEffortDict()
    
    
          
    #TODO Read data for projects     
    #TODO Create class for entry
    #TODO Generate xml with neccessary data