import json
from copy import deepcopy

class InputHandler:
    json = None

    #Dicationaries
    documents_dict = {}
    document_fields_dict = {}

    # InputHandler Constructor
    def __init__(self, file_path):
        with open(file_path, 'r') as content_file:
            content = content_file.read()
            # print content
            j = json.loads(content)
            self.json = j

        # Set dictionaries with id as key, for faster lookup
        self.documents_dict = self.__generate_dict(self.getDocuments())
        self.document_fields_dict = self.__generate_dict(self.getDocumentFields())


    def getActions(self):
        return self.json['actions']

    def getActionById(self, id):
        return self.__getElementById('actions', id)

    def getDocumentFields(self):
        return deepcopy(self.json['documentFields'])

    def getADocumentFieldById(self, id):
        return deepcopy(self.document_fields_dict[id])

    def getDocumentTypes(self):
        return self.json['documentTypes']

    def getADocumentTypeById(self, id):
        return self.__getElementById('documentTypes', id)

    def getLinkCategories(self):
        return self.json['linkCategories']

    def getLinkCategoryById(self, id):
        return self.__getElementById('linkCategories', id)

    def getMandatory(self):
        return self.json['mandatory']

    def getMandatoryById(self, id):
        return self.__getElementById('mandatory', id)

    def getTargetGroups(self):
        return self.json['targetGroups']

    def getTargetGroupById(self, id):
        return self.__getElementById('targetGroups', id)

    def getStatuses(self):
        return self.json['status']

    def getStatusById(self, id):
        return self.__getElementById('status', id)

    # Returns entire json list
    def getJSON(self, file_path):
        return self.json

    def getTopics(self):
        if (self.json):
            return self.json['topics']

    def getTopicById(self, id):
        return self.__getElementById('topics', id)

    def getDocuments(self):
        if (self.json):
            return deepcopy(self.json['documents'])

    def getDocumentById(self, id):
        return self.documents_dict[id]

    # Returns a list document fields with the data needed to generate Word file
    def get_field_list_by_document_id(self, document_id):
        field_list = []
        for document_field in self.getDocumentById(document_id)['fields']:
            field_id = document_field['fieldId']
            field =  {
                'name' : self.getADocumentFieldById(field_id)['name'],
                'value': document_field['value']
            }
            field_list.append(field)
        return field_list

    # Returns element, if found, else None
    def __getElementById(self, elements, id):
        if not isinstance(id, basestring):  # TODO: Throw exception instead?
            id = '' + id
        for element in self.json[elements]:
            if element['id'] == id:
                return element
        return None

    # Returns a dictionary from json_list, with id as key
    # @param json_element_list: list of elements form the JSON file, such as self.json['documents']
    # @returns {dictionary}: dictionary with element id as key
    def __generate_dict(self, json_element_list):
        dict = {}
        for element in json_element_list:
            dict[element['id']] = element
        return dict