# -*- coding: utf-8 -*-
"""
Created on Sun May 10 11:28:14 2020

@author: IVAALEX
"""
from EffortsReader import EffortsReaderFactory

class Effort:
    def __init__(self, customer, service, time):
        self.customer = customer
        self.service = service
        self.time = time
    def __str__(self):
        return "|" + self.customer + "|" + self.service + "|" + str(self.time) + "|" 

class EffortsBuilder(object):
    def __init__(self, pathToFile, config):
        typ = "ExcelEffortsReader"
        #TODO add parameter for file path
        #path = (r'efforts2.xls')
        path = pathToFile
        effortsReaderFact = EffortsReaderFactory()
        self.config = config
        self.effortsReader = effortsReaderFact.createEffortsReader(typ, path)
        self._effortsDict = {}
        self._readEfforts()
        self._services = self._readServiceClientMapping()
        self.effortsList = []
        
        
    def _readEfforts(self):
        self._effortsDict = self.effortsReader.generateEffortDict()
    def _readServiceClientMapping(self):
        #TODO Add parameters file read instead of hardcode
        # servicesClientsDict = {    "mon_ipwr":"Inchcape",
        #                 "SAP3rdERP":"Inchcape",
        #                 "Mercedes_CRM":"Mercedes",
        #                 "gmpt-imp-ph2-pr":"GMPT",
        #                 "gmpt-sup-int":"GMPT",
        #                 "SAP3rdCRM":"Inchcape",
        #                 "k2-internal-prj":"K2",
        #                 "RUSM-IMPL":"RM",
        #                 "alianta-imp-с4с":"Alianta",
        #                 "IMP_22":"Inchcape",
        #                 "pers-tasks":"K2"
        #                 }
        servicesClientsDict = self.config["servicesClientsDict"]
        
        return servicesClientsDict
    
    def composeEfforts(self):
        servicesClientsDict = self._readServiceClientMapping()
        for serviceKey in self._effortsDict:
            client = servicesClientsDict[serviceKey]
            effort = Effort(client,serviceKey,self._effortsDict[serviceKey])
            self.effortsList.append(effort)
        return self.effortsList
        

if __name__ == '__main__':
    eb = EffortsBuilder()
    efforts = eb.composeEfforts()
    for effort in efforts:
        print(effort)
        
        
        
        
        
        
        
        
        
        
        