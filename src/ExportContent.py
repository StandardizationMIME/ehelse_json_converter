#!/usr/bin/env python
# -*- coding: utf-8 -*-
from docx import *  # TODO: check if we can import less
from docx.shared import Inches
from docx.oxml.shared import *
from docxtpl import DocxTemplate


class ExportContent:
    def __init__(self):
        self.list = {
            'title': '',
            'topics': []
        }
    def get_content(self):
        return self.list

    def set_title(self, title):
        self.list['title'] = title

    def add_topic(self, topic, documents, input_handler):
        self.list['topics'].append(
            {
                'title': topic['title'],
                'documents' : self.__get_document_list(input_handler, documents)
            }
        )

    def __get_document_list(self, input_handler, documents):
        documents_object = []
        for document in documents:
            document_id = document['id']
            document_object = {}

            document_object['title'] = document['title']
            document_object['description'] = document['description']
            document_object['status'] = input_handler.get_status_name_by_id(document['statusId'])

            # Fields
            document_object['fields'] = input_handler.get_field_list_by_document_id(document_id)

            # Target groups
            document_object['mandatoryList'] = []

            mandatory_dict = input_handler.get_mandatory_dict_on_document_id(document_id)
            for mandataory_id, mandataory in mandatory_dict.iteritems():
                target_groups = []
                for target_group in input_handler.get_target_groups_by_mandatory_id_and_document_id(mandataory_id,
                                                                                                document_id):
                    target_groups.append({
                        'name': input_handler.getTargetGroupById(target_group['targetGroupId'])['name'], # Name of target group
                        'action': input_handler.get_action_name_by_id(target_group['actionId'])
                    })

                print 'mandatroyId ' + mandataory_id + ' ' + mandataory['name']
                document_object['mandatoryList'].append({
                    'name' : mandataory['name'],
                    'targetGroups': target_groups,
                    'hjemmel': document['hjemmel'] if (mandataory_id == 1 and document['hjemmel'] is not None) else '',
                    'decidedBy':
                        document['decidedBy'] if (mandataory_id == 1 and document['decidedBy'] is not None) else ''

                })

            '''
            print input_handler.get_target_group_values_by_target_group_id_and_document_id()
            for mandatory in input_handler.getMandatory():
                document_object['mandatoryList'].append({
                    'name': mandatory['name'],
                    'targetGroups':
                })
            '''
            documents_object.append(document_object)
        return documents_object






