#!/usr/bin/env python
# -*- coding: utf-8 -*-
from docx import *  #TODO: check if we can import less
from docx.shared import Inches
from docx.oxml.shared import *
from docxtpl import DocxTemplate

class WordTemplateExporter:

    def __init__(self, template_path):
        self.tpl = DocxTemplate('C:/Users/AK/Documents/GitHub/ehelse_json_converter/templates/template.docx')
        print 'word template ex initiated'
        print self.tpl


    def save_file(self, content, path):
        self.tpl.render(content)
        self.tpl.save('c:/users/AK/Desktop/this2.docx')