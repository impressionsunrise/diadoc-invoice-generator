# -*- coding: utf-8 -*-
"""
Created on Wed May 13 23:53:01 2020

@author: IVAALEX
"""
from Efforts import EffortsBuilder
import os
import yaml
from XMLGenerator import *
if __name__ == '__main__':
    
    script_dir = os.path.dirname(__file__)
    conf_path = "conf/configuration.yml"
    abs_conf_path = os.path.join(script_dir, conf_path )
    with open(abs_conf_path, 'rt', encoding='utf8') as yml:
        config = yaml.safe_load(yml)
    #config = yaml.safe_load(open("conf/configuration.yml"))
    #path = (r'efforts2.xls')
    path = (config["effortsFilePath"])
    
    #eb = EffortsBuilder(path, config)
    eb = EffortsBuilder(os.path.join(script_dir, path ), config)
    efforts = eb.composeEfforts()
    XMLparamDict = {
        "Positions" : efforts,
        "Rate" : config["rate"]
        }
    
    script_dir = os.path.dirname(__file__)
    xsd_path = "Docs/Template.xml"
    abs_xsd_path = os.path.join(script_dir, xsd_path )
    generator = XMLGenerator820Invoice(abs_xsd_path, XMLparamDict, config)
    outputFileList = generator.constructXMLFiles()
