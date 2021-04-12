# -*- coding: utf-8 -*-
"""
Created on Sun May 10 13:30:48 2020

@author: IVAALEX
"""
from abc import ABC, abstractmethod
from XMLio import XMLio
from lxml import etree
import datetime
from copy import deepcopy

class XMLGeneratorBase(ABC):
    @abstractmethod
    def _readTemplate(self, templatePath):
        """
        Read template XML file under the path provided in templatePath.
        Store this in self.template
+        """
        raise NotImplementedError
    @abstractmethod
    def constructXMLFiles(self):
        """
        Create XML from provided template and data
        Store this in self.generatedXML
        """
        raise NotImplementedError
    @abstractmethod
    def _isValideXML(self, xsdPath):
        """
        Check XML against XSD
        Return true if XML is valid
        """
        raise NotImplementedError
        
class XMLGenerator820Invoice(XMLGeneratorBase):
    def __init__(self, templatePath, XMLparamDict, config):
        """
        
        
        Parameters
        ----------
        templatePath : os.path
            Path to XML template.
        XMLparamDict : Dictionary
            Dict of parameters, that should be transferred to XML.

        Returns
        -------
        None.
        """
        self.XMLio = XMLio()
        self.XMLparamDict = XMLparamDict
        self.XMLtemplate = self._readTemplate(templatePath)
        self.totalDocumentPrice = 0.0
        self.config = config
        
        
    def _readTemplate(self, templatePath):
        template = etree.parse(self.XMLio.readXML(templatePath))
        return template 
    def constructXMLFiles(self):
        """
        None -> List of XML files
        
        Generate XML files based on template and data provided in XMLparamDict
        Number of files depends on number of customers
        """
        customers = self._getCustomers()
        positions = self._createPositions()
        
        outputFileList = []
        iteration = 1
        for customer in customers:
            filteredPositions = self._getPositionsByCustomer(customer, positions)
            outputFile = self._constructSingleXML(filteredPositions, iteration)
            if self._isValideXML(outputFile, "TODO"): #TODO Add xsd path parameter
                outputFileList.append(outputFile)
                self._writeXML(etree.tounicode(outputFile), "Invoices\\"  + "УПД_"+customer+" "+str(iteration)+".xml")
                print(etree.tounicode(outputFile))
            iteration+=1    
        return outputFileList
        
    def _isValideXML(self, outputFile, xsdPath):
        return True            #TODO implement
    
    
    def _getNumberOfInvoice(self, iteration):
        """
        Get invoice number in format "01-05-2020" where,
        01 - iteration
        05 - Previous month
        2020 - Year of the previous month
        Parameters
        ----------
        iteration : Number
            .

        Returns
        -------
        numberOfInvoice : String.

        """
        #
        lastMonth = self._getLastDayOfPreviousMonth()
        formattedDate = lastMonth.strftime("-%m-%Y")
        numberOfInvoice = str(iteration).zfill(2) + formattedDate
        return numberOfInvoice
    
    def _getLastDayOfPreviousMonth(self):
        today = datetime.date.today()
        first = today.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1)
        lastMonth = first
        return lastMonth
    def _getFormattedLastDayOfPreviousMonth(self):
        lastMonth = self._getLastDayOfPreviousMonth()
        '''TODO Добавить параметр'''
        return lastMonth.strftime("%d.%m.%Y")
        
    def _getServicesDateRange(self):
        """
        Get string like "Услуги оказывались в период с 01.02.2020 по 29.02.2020"
        where dates are first and last date of previous month

        Returns
        -------
        servicesDateRange : String.

        """
        lastDayOfPreviousMonth = self._getLastDayOfPreviousMonth()
        firstDayOfPreviousMonth = lastDayOfPreviousMonth.replace(day=1)
        servicesDateRange = ("Услуги оказывались в период с %s по %s" % (firstDayOfPreviousMonth.strftime("%d.%m.%Y"), lastDayOfPreviousMonth.strftime("%d.%m.%Y")))
        '''TODO Добавить параметр'''
        return servicesDateRange
        
        
        
    def _constructSingleXML(self, positions, iteration):
        """
        Construct XML file from positions, XMLparamDict and template.
        
        Parameters
        ----------
        customer : String
            Customer name, which is filter for positions.
        positions : TYPE
            Full list of positions.

        Returns
        -------
        None.

        """
        
        resultXML = self.XMLtemplate
        resultXMLroot = resultXML.getroot()
        #tree = resultXMLroot.getroottree()
        #document = etree.SubElement(resultXMLroot, "Документ")
        #positionTable = etree.SubElement(document, "ТаблСчФакт")
        
        
        #Add positions to XML
        positionTotalPrice = 0.0
        for element in resultXMLroot.iter("ТаблСчФакт"):
            if element.tag == "ТаблСчФакт":
                del element[:]
                for position in positions:
                    positionTotalPrice += float(position[1].get("СтТовБезНДС"))
                    element.append(position[1])
                self._appendTotalLine(element)
                      
                
        for element in resultXMLroot.iter():  
            if element.tag == "СвСчФакт":
                element.set("НомерСчФ", self._getNumberOfInvoice(iteration))
                element.set("ДатаСчФ", self._getFormattedLastDayOfPreviousMonth())
            
            if element.tag == "ОснПер":
                element.set("ДопСвОсн", self._getServicesDateRange())
            
            if element.tag == "ВсегоОпл":
                element.set("СтТовБезНДСВсего", format(positionTotalPrice,".2f"))
                element.set("СтТовУчНалВсего", format(positionTotalPrice,".2f"))
            
        #print(etree.tounicode(document))
        #print(etree.tounicode(tree))
        return resultXMLroot.getroottree()
    
    def _appendTotalLine(self, element):
        """<ВсегоОпл СтТовБезНДСВсего="50040.00" СтТовУчНалВсего="50040.00">
				<СумНалВсего>
					<БезНДС>без НДС</БезНДС>
				</СумНалВсего>
			</ВсегоОпл>"""
            
        totalPaymentTag = etree.Element("ВсегоОпл")
        sumTag = etree.Element("СумНалВсего")
        noVatTag = etree.Element("БезНДС")
        noVatTag.text = "без НДС"
        sumTag.append(noVatTag)    
        
        totalPaymentTag.append(sumTag)
        
        element.append(totalPaymentTag)
                
        
        
    def _getPositionsByCustomer(self, customer, positions):
        """ Filter inbound positions by customer provided
        Parameters
        ----------
        customer : String
            Customer name, which is filter for positions.
        positions : List
            Full list of positions.
        Returns
        -------
        filteredPositionsList : List
        """
        filteredPositionsList = []
        
        for key in positions:
            if positions[key][0] == customer:
                filteredPositionsList.append(positions[key])
        
        return filteredPositionsList
                    
        
    def _getCustomers(self):
        customers = []
        for position in self.XMLparamDict["Positions"]:
            if not position.customer in customers:
                customers.append(position.customer)
        return customers
    
    def _createPositions(self):
        """ 
          <СведТов НомСтр="1" НаимТов="Разработка и планирование для первой фазы GMPT" ОКЕИ_Тов="539" КолТов="3.5" ЦенаТов="1200.00" СтТовБезНДС="4200.00" НалСт="без НДС" СтТовУчНал="4200.00">
        <Акциз>
          <БезАкциз>без акциза</БезАкциз>
        </Акциз>
        <СумНал>
          <БезНДС>без НДС</БезНДС>
        </СумНал>
        <ДопСведТов ПрТовРаб="3" КодТов="gmpt-imp-ph1-in" НаимЕдИзм="чел. ч" />
   </СведТов>
   """
        exciseTag = etree.Element("Акциз")
        noExciseTag = etree.Element("БезАкциз")
        noExciseTag.text = "без акциза"
        exciseTag.append(noExciseTag)
                
        sumTag = etree.Element("СумНал")
        noVatTag = etree.Element("БезНДС")
        noVatTag.text = "без НДС"
        sumTag.append(noVatTag)
        
        
        rate = self.XMLparamDict["Rate"]
        
        positionTexts = self._getPositionTexts()
        
        XMLpositions = {}
        positionNumbers = {}
        totalDocumentPrice = 0.0
        for position  in self.XMLparamDict["Positions"]:
            
            if position.customer not in positionNumbers.keys():
                positionNumbers[position.customer] = 1
            else:
                positionNumbers[position.customer] += 1
            
            positionText = ""
            try:
                positionText = positionTexts[position.service]
            except:
                positionText = "Текст позиции"
                
            
            XMLposition = etree.Element("СведТов")
            XMLposition.set("НомСтр", str(positionNumbers[position.customer]))
            XMLposition.set("НаимТов", positionText) 
            XMLposition.set("ОКЕИ_Тов", "539")
            XMLposition.set("КолТов", str(position.time))
            XMLposition.set("ЦенаТов", format(rate,".2f"))
            
            price = position.time * rate
            priceStr = format(price,".2f") 
            XMLposition.set("СтТовБезНДС", priceStr)
            XMLposition.set("НалСт", "без НДС")
            XMLposition.set("СтТовУчНал", priceStr)
            
            
            
            goodsTag = etree.Element("ДопСведТов")
            goodsTag.set("ПрТовРаб", "3")
            goodsTag.set("КодТов", position.service)
            goodsTag.set("НаимЕдИзм", "чел. ч")
            
            XMLposition.append(deepcopy(exciseTag))
            XMLposition.append(deepcopy(sumTag))
            XMLposition.append(goodsTag)
            
            XMLpositions[position.service] = [position.customer, XMLposition]
            #XMLpositions.append(XMLposition)
            #print(etree.tounicode(XMLposition))
            totalDocumentPrice+=price
            
        self.totalDocumentPrice = format(totalDocumentPrice, ".2f")
        return XMLpositions
            
    def _getPositionTexts(self):
        #TODO Сделать считывание из настроечного файла
        # positionTexts = {   "mon_ipwr":"Мониторинг системы iPower",
        #                     "SAP3rdERP":"Поддержка ERP и работа над запросами на изменение",
        #                     "Mercedes_CRM":"Работа над запросами MBR",
        #                     "gmpt-imp-ph2-pr":"Внедрение второй фаза GMPT",
        #                     "gmpt-sup-int":"Поддержка GMPT",
        #                     "SAP3rdCRM":"Поддержка CRM и работа над запросами на изменение",
        #                     "k2-internal-prj":"Внутренние проекты К2",
        #                     "RUSM-IMPL":"Создание интеграционных потоков RM",
        #                     "alianta-imp-с4с":"Создание интеграционных потоков Alianta",
        #                     "IMP_22":"Работа над запросами на изменение Inchcape",
        #                     "pers-tasks":"Персональные задачи К2"
        #                     }
        positionTexts = self.config["positionTexts"]
        return positionTexts

        
    def _writeXML(self, xmlFile, name):
        self.XMLio.writeXML(xmlFile, name)
    
    
    
    
if __name__ == '__main__':
    from Efforts import EffortsBuilder
    import os
    path = (r'efforts2.xls')
    eb = EffortsBuilder(path)
    efforts = eb.composeEfforts()
    XMLparamDict = {
        "Positions" : efforts,
        "Rate" : 1200.00
        }
    
    script_dir = os.path.dirname(__file__)
    xsd_path = "Docs/Template.xml"
    abs_xsd_path = os.path.join(script_dir, xsd_path )
    generator = XMLGenerator820Invoice(abs_xsd_path, XMLparamDict)
    outputFileList = generator.constructXMLFiles()
    
    
    
    
    
    
    
    
    
    
    