# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:00:36 2020

@author: IVAALEX
"""
from io import StringIO
import os
from loguru import logger

class XMLio(object):
    def readXML(self, path):
        logger.debug("Reading XML file " + path)
        xmlFile = open(path,'r')
        resultXML = StringIO(xmlFile.read())
        xmlFile.close()
        return resultXML
    def writeXML(self, XMLdata, path):
        try:
            xmlFile = open(path, "w")
        except:
            script_dir = os.path.dirname(__file__)
            abs_xml_path = os.path.join(script_dir, path )
            xmlFile = open(abs_xml_path, "w")
        xmlFile.write("<?xml version=\"1.0\" encoding=\"windows-1251\"?>\n" + XMLdata)
        xmlFile.close()