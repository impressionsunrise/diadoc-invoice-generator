# -*- coding: utf-8 -*-
"""
Created on Sat May  9 15:14:41 2020

@author: IVAALEX
"""


from lxml import etree
from io import StringIO
import os
from XMLio import XMLio

class ValidationResult(object):
    def __init__(self, XMLvalid, errorText):
        self.XMLvalid = XMLvalid
        self.errorText = errorText
    def __str__(self):
        if self.XMLvalid:
            return "Check XML against XSD was successful"    
        else:
            return "XML is not valid. Error below: \n " + self.errorText



class XMLValidator(object):
    
    
    def __init__(self):
        pass
    
    @classmethod
    def fromFilePath(cls,xsdSchemePath, xmlDocumentPath):
        """ os.path, os.path -> XMLValidator
            Creates XMLValidator object, which reads XSD and XML documents from 
            path, provided in parameters
        """
        validator = cls()
        validator._readXMLandXSD(xsdSchemePath,xmlDocumentPath)
        return validator
    @classmethod
    def fromData(cls,xsdScheme, xmlDocument):
        """ StringIO, StringIO -> XMLValidator
            Creates XMLValidator object with assigned xsdScheme and xmlDocument
        """
        validator = cls()
        validator.setxsdScheme(xsdScheme)
        validator.setxmlDocument(xmlDocument)
        return validator

    def _readXMLandXSD(self, xsdSchemePath, xmlDocumentPath):   
        """ os.path, os.path -> None
            Reads XML and XSD files to object variables self.xsdScheme and self.xmlDocument
        """
        try:
            
            xmlReader = XMLio()
            self.xsdScheme = xmlReader.readXML(xsdSchemePath)
            self.xmlDocument = xmlReader.readXML(xmlDocumentPath)
            
            # xsdScheme = open(xsdSchemePath,'r')
            # xmlDocument = open(xmlDocumentPath,'r')
            
            # self.xsdScheme = StringIO(xsdScheme.read())
            # self.xmlDocument = StringIO(xmlDocument.read())
            
            # xsdScheme.close()
            # xmlDocument.close()
        except Exception as e:
            print(e)
            
    def setxsdScheme(self, xsdScheme):
        self.xsdScheme = xsdScheme
        
    def setxmlDocument(self, xmlDocument):
        self.xmlDocument = xmlDocument
        
    def validateXML(self):
        """ None -> ValidationResult
            Check XML against XSD structure, and return ValidationResult object.
            It consists of two fields - XMLvalid and errorText
            If XML is valid, XMLvalid = true and errorText is empty
            Otherwise, XMLvalid = false, a errorText filled with error from exception
        """
        errorText = ""
        result = ValidationResult(False, errorText)
        try:
            xmlschema_doc = etree.parse(self.xsdScheme)
            xmlschema = etree.XMLSchema(xmlschema_doc)
            doc = etree.parse(self.xmlDocument)
            #XMLvalid = xmlschema.validate(doc)
            xmlschema.assertValid(doc)
            result = ValidationResult(True, errorText)
        except Exception as e:
            result = ValidationResult(False, str(e))
        finally:
            return result            




if __name__ == '__main__':

    # f = StringIO('''<?xml version="1.0" encoding="UTF-8"?>
    # <xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    #  	<xsd:element name="Файл" type="AType"/>
    #  	<xsd:complexType name="AType">
    # 		<xsd:sequence>
    #  			<xsd:element name="b" type="xsd:string" />
    # 		</xsd:sequence>
    #  	</xsd:complexType>
    # </xsd:schema>
    # ''')
    
    # xmlschema_doc = etree.parse(f)
    # xmlschema = etree.XMLSchema(xmlschema_doc)
    
    # valid = StringIO('''
    # <Файл>
    #  	<b/>
    # </Файл>                 
    # ''')
    # doc = etree.parse(valid)
    # print(xmlschema.validate(doc))
    # try:
    #     print(xmlschema.assertValid(doc))
    # except Exception as e:
    #     print(e)
    # validator = XMLValidator.fromData(f,valid)
    # print(validator.validateXML())
    
    script_dir = os.path.dirname(__file__)
    
    xsd_path = "Docs/scheme1.xsd"
    abs_xsd_path = os.path.join(script_dir, xsd_path)
    
    xml_path = "Docs/УПД_GMPT.xml"
    abs_xml_path = os.path.join(script_dir, xml_path )
    
    validator2 = XMLValidator.fromFilePath(xsd_path, xml_path)
    result = validator2.validateXML()
    print(result)










    
    
