import json
from copy import deepcopy


class InputHandler:
    json = None

    # Dicationaries
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

    def get_contact_address_name_by_document_id(self, id):
        '''
        Returns name of contact address
        :param id:
        :return: string - name of contact adress
        '''
        contact_address_id = self.getDocumentById(id)['contactAddressId']
        contact_address = self.__get_contact_address_by_id(contact_address_id)
        contact_address_name = ''
        try:
            contact_address_name = contact_address['name']
        except:
            pass
        return contact_address_name

    def __get_contact_address_by_id(self, id):
        return self.__getElementById('contactAddresses', id)

    def getDocumentFields(self):
        return deepcopy(self.json['documentFields'])

    def get_documents_by_topic_id(self, id):
        documents = []

        for document in self.getDocuments():
            if id == document['topicId']:
                documents.append(document)

        return documents

    def getADocumentFieldById(self, id):
        return deepcopy(self.document_fields_dict[id])

    def getDocumentTypes(self):
        return self.json['documentTypes']

    def getADocumentTypeById(self, id):
        return self.__getElementById('documentTypes', id)

    def get_section_dict_by_document_id(self, document_id):
        # headingContent
        document = self.getDocumentById(id)
        link_categories_dict = {}

        for link in document['links']:
            link_category_id = link['linkCategoryId']
            if link_category_id not in link_categories_dict:
                link_categories_dict[link_category_id] = self.getLinkCategoryById(link_category_id)

        return link_categories_dict

    def get_heading_dict_by_document_id(self, id):
        return self.get_element_dict_by_document_id('headings', 'headingContent', 'headingId', id)

    def get_heading_content_by_heading_id_and_document_id(self, heading_id, document_id):
        document = self.getDocumentById(document_id)
        for heading in document['headingContent']:
            if heading['headingId'] == heading_id:
                return heading
        return None

    def get_element_dict_by_document_id(self, element_name, element_document_name, element_id_name, document_id):
        '''
        Returns a dictionary with element_id as key, and element as value.
        :param element_name: name of the list from JSON file, such as "headings"
        :param element_document_name: name of the list in document, such as "headingContent"
        :param element_id_name: name if the ids, such as "headingId"
        :param document_id:
        :return:
        '''
        document = self.getDocumentById(document_id)
        dict = {}
        for element in document[element_document_name]:
            element_id = element[element_id_name]
            if element_id not in dict:
                dict[element_id] = self.__getElementById(element_name, element_id)
        return dict

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
            return self.get_sorted_topics(self.json['topics'])

    def get_sorted_topics(self, topics):
        """
        Returns a list of sorted topics, e.g. [1, 1.1, 1.1.1, 1.1.2, 1.2, 2, 2.1 , 3, 3.1]
        :param topics: array of topics
        :return: array of sorted topics
        """
        top_level_topics = []
        for topic in topics:
            if not topic['parentId']:
                top_level_topics.append(topic)
        top_level_topics = self.__get_list_sorted_by_property(top_level_topics, 'sequence')

        sorted_topics = []
        for top_level_topic in top_level_topics:
            children = self.__get_list_of_topic_children(topics, top_level_topic)
            sorted_topics.extend(children)

        for t in sorted_topics:
            print t['title']

        return sorted_topics


    def __get_list_of_topic_children(self, topics, topic):
        sorted_topics = []
        children = self.__get_topic_children(topics, topic['id'])
        children = self.__get_list_sorted_by_property(children, 'sequence')
        sorted_topics.append(topic)
        for c in children:
            sorted_topics.extend(self.__get_list_of_topic_children(topics, c))
        return sorted_topics

    def __get_topic_children(self, topics, id):
        children = []
        for topic in topics:
            if topic['parentId'] == id:
                children.append(topic)
        return self.__get_list_sorted_by_property(children, 'sequence')

    def __get_list_sorted_by_id(self, list):
        return sorted(list, key=lambda element: element['id'])

    def __get_list_sorted_by_property(self, list, property):
        return sorted(list, key=lambda element: element[property])

    def getTopicById(self, id):
        return self.__getElementById('topics', id)

    def getDocuments(self):
        if (self.json):
            return deepcopy(self.json['documents'])

    def getDocumentById(self, id):
        return self.documents_dict[id]

    def get_field_list_by_document_id(self, document_id):
        '''
        Returns a list document fields with the data needed to generate Word file
        :param document_id:
        :return: list of document fields with "name" and "value"
        '''
        field_list = []
        for document_field in self.getDocumentById(document_id)['fields']:
            field_id = document_field['fieldId']
            field = {
                'name': self.getADocumentFieldById(field_id)['name'],
                'value': document_field['value']
            }
            field_list.append(field)
        return field_list

    def get_action_name_by_id(self, id):
        action = self.getActionById(id)
        action_name = ''
        try:
            action_name = action['name']
        except:
            pass
        return action_name

    def get_hjemmel_by_document_id(self, id):
        return self.getDocumentById(id)['hjemmel']

    def get_decided_by_by_document_id(self, id):
        return self.getDocumentById(id)['decidedBy']

    def get_mandatory_notice_by_mandatory_id_and_document_id(self, mandatory_id, document_id):
        document = self.getDocumentById(document_id)
        mandatory_notices_dict = self.__generate_dict(document['mandatoryNotices'], 'mandatoryId')
        return mandatory_notices_dict[mandatory_id]['notice']


    def __getElementById(self, elements, id):  # TODO: store all as dictionaries for faster access?
        """
        Returns element, if found, else None
        :param elements:
        :param id:
        :return: element | None
        """
        if not isinstance(id, basestring):  # TODO: Throw exception instead?
            id = str(id)
        for element in self.json[elements]:
            if element['id'] == id:
                return element
        return None

    def __generate_dict(self, json_element_list, id='id'):
        """
        Returns a dictionary from json_list, with id as key
        :param json_element_list: json_element_list: list of elements form the JSON file, such as self.json['documents']
        :return: dictionary with element id as key
        """
        dict = {}
        for element in json_element_list:
            dict[element[id]] = element
        return dict
