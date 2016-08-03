import json
from copy import deepcopy

class InputHandler:
    json = None

    #Dicationaries
    documents_dict = {}
    document_fields_dict = {}
    status_dict = {}

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
        self.status_dict = self.__generate_dict(self.getStatuses())


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

    # Returns link category dictionary with the link categories on the specified document
    # TODO: should be array instead?
    def get_link_category_dict_by_document_id(self, id):
        document = self.getDocumentById(id)
        link_categories_dict = {}

        for link in document['links']:
            link_category_id = link['linkCategoryId']
            if link_category_id not in link_categories_dict:
                link_categories_dict[link_category_id] = self.getLinkCategoryById(link_category_id)

        return link_categories_dict

    def get_links_by_link_category_id_and_document_id(self, link_category_id, document_id):
        document = self.getDocumentById(document_id)
        links = []

        for link in document['links']:
            if link['linkCategoryId'] == link_category_id:
                links.append(link)

        return links

    def getMandatory(self):
        return self.json['mandatory']

    def getMandatoryById(self, id):
        return self.__getElementById('mandatory', id)

    def get_mandatory_dict_on_document_id(self, document_id):
        document = self.getDocumentById(document_id)
        mandatory_dict = {}

        for target_group in document['targetGroups']:
            mandatory_id = target_group['mandatoryId']
            if mandatory_id not in mandatory_dict:
                mandatory_dict[mandatory_id] = self.getMandatoryById(mandatory_id)

        return mandatory_dict

    def get_target_groups_by_mandatory_id_and_document_id(self, mandatory_id, document_id):
        document = self.getDocumentById(document_id)
        target_groups = []

        for target_group in document['targetGroups']:
            if target_group['mandatoryId'] == mandatory_id:
                target_groups.append(target_group)

        return target_groups

    def getTargetGroups(self):
        return self.json['targetGroups']

    def getTargetGroupById(self, id):
        return self.__getElementById('targetGroups', id)

    def get_target_groups_by_document_id(self, id):

        document = self.getDocumentById(id)
        target_groups_dict = {}

        for target_group in document['targetGroup']:
            target_group_id = target_group['targetGroupId']
            if target_group_id not in target_groups_dict:
                target_groups_dict[target_group_id] = self.getTargetGroupById(target_group_id)

        return target_groups_dict

    def get_target_group_values_by_target_group_id_and_document_id(self, target_group_id, document_id):
        document = self.getDocumentById(document_id)
        target_groups_values = []

        for target_group in document['targetGroups']:
            if target_group['targetGroupId'] == target_group_id:
                target_groups_values.append(target_group)

        return target_groups_values

    def getStatuses(self):
        return self.json['status']

    def getStatusById(self, id):
        return self.status_dict[id];

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
            print 'something went wrong'
            id = str(id)
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