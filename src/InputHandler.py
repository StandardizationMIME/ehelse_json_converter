from copy import deepcopy
import json


class InputHandler:
    json = None

    # Dictionaries
    documents_dict = {}
    document_fields_dict = {}
    status_dict = {}

    # InputHandler Constructor
    def __init__(self, file_path):
        with open(file_path, 'r') as content_file:
            content = content_file.read()
            j = json.loads(content)
            self.json = j

        # Set dictionaries with id as key, for faster lookup
        self.documents_dict = self.__generate_dict(self.get_documents())
        self.document_fields_dict = self.__generate_dict(self.getDocumentFields())
        self.status_dict = self.__generate_dict(self.get_statuses())


    def get_ation_by_id(self, id):
        return self.__getElementById('actions', id)

    def get_contact_address_name_by_document_id(self, id):
        '''
        Returns name of contact address
        :param id:
        :return: string - name of contact adress
        '''
        contact_address_id = self.get_document_by_id(id)['contactAddressId']
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

        for document in self.get_documents():
            if id == document['topicId']:
                documents.append(document)

        return documents

    def get_document_field_by_id(self, id):
        return deepcopy(self.document_fields_dict[id])

    def get_heading_dict_by_document_id(self, id):
        return self.get_element_dict_by_document_id('headings', 'headingContent', 'headingId', id)

    def get_heading_name_by_heading_id(self, id):
        return self.__getElementById('headings', id)['name']

    def get_heading_content_by_heading_id_and_document_id(self, heading_id, document_id):
        document = self.get_document_by_id(document_id)
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
        document = self.get_document_by_id(document_id)
        dict = {}
        for element in document[element_document_name]:
            element_id = element[element_id_name]
            if element_id not in dict:
                dict[element_id] = self.__getElementById(element_name, element_id)
        return dict

    def get_link_category_by_id(self, id):
        return self.__getElementById('linkCategories', id)

    def get_link_category_dict_by_document_id(self, id):
        """
        Returns link category dictionary with the link categories on the specified document.
        :param id:
        :return:
        """
        document = self.get_document_by_id(id)
        link_categories_dict = {}

        for link in document['links']:
            link_category_id = link['linkCategoryId']
            if link_category_id not in link_categories_dict:
                link_categories_dict[link_category_id] = self.get_link_category_by_id(link_category_id)
        # NO sort of dictionaries?
        return self.__get_list_sorted_by_property(link_categories_dict, 'sequence')

    def get_link_categories_by_document_id(self, id):
        document = self.get_document_by_id(id)
        link_categories = []

        for link in document['links']:
            link_category_id = link['linkCategoryId']
            if not self.__id_is_in_list(link_category_id , link_categories):
                link_categories.append(self.get_link_category_by_id(link_category_id))

        return self.__get_list_sorted_by_property(link_categories, 'sequence')

    def __id_is_in_list(self, id, list):
        """
        Returns true if an element with the given id exists in list.
        :param id:
        :param list:
        :return:
        """
        for element in list:
            if element['id'] == id:
                return True
        return False

    def get_links_by_link_category_id_and_document_id(self, link_category_id, document_id):
        document = self.get_document_by_id(document_id)
        links = []

        for link in document['links']:
            if link['linkCategoryId'] == link_category_id:
                links.append(link)

        return self.__get_list_sorted_by_property(links, 'sequence')


    def get_mandatory_by_id(self, id):
        return self.__getElementById('mandatory', id)

    def get_mandatory_dict_on_document_id(self, document_id):
        document = self.get_document_by_id(document_id)
        mandatory_dict = {}

        for target_group in document['targetGroups']:
            mandatory_id = target_group['mandatoryId']
            if mandatory_id not in mandatory_dict:
                mandatory_dict[mandatory_id] = self.get_mandatory_by_id(mandatory_id)

        return mandatory_dict

    def get_target_groups_by_mandatory_id_and_document_id(self, mandatory_id, document_id):
        document = self.get_document_by_id(document_id)
        target_groups = []

        for target_group in document['targetGroups']:
            if target_group['mandatoryId'] == mandatory_id:
                target_groups.append(target_group)

        return target_groups

    def get_target_groups(self):
        return self.json['targetGroups']

    def get_target_group_by_id(self, id):
        return self.__getElementById('targetGroups', id)

    def get_statuses(self):
        return self.json['status']

    def get_status_by_id(self, id):
        if id in self.status_dict:
            return self.status_dict[id]
        return None

    def get_status_name_by_id(self, id):
        status = self.get_status_by_id(id)
        if status:
            return status['name']
        return ''

    def get_json(self, file_path):
        """
        Returns entire json list.
        :param file_path:
        :return:
        """
        return self.json

    def getTopics(self):
        return self.json['topics'] # TODO: Check sort!
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

        return sorted_topics


    def __get_list_of_topic_children(self, topics, topic):
        """
        Returns a sorted list of children for the specified topic.
        :param topics: all topics
        :param topic: the topic for which the child list is generated
        :return:
        """
        sorted_topics = []
        children = self.__get_topic_children(topics, topic['id'])
        children = self.__get_list_sorted_by_property(children, 'sequence')
        sorted_topics.append(topic)
        for c in children:
            sorted_topics.extend(self.__get_list_of_topic_children(topics, c))
        return sorted_topics

    def __get_topic_children(self, topics, id):
        """
        Returns a list of children for the specified topic.
        :param topics: all topics
        :param id:
        :return:
        """
        children = []
        for topic in topics:
            if topic['parentId'] == id:
                children.append(topic)
        return self.__get_list_sorted_by_property(children, 'sequence')

    def __get_list_sorted_by_id(self, list):
        return sorted(list, key=lambda element: element['id'])

    def __get_list_sorted_by_sequence(self, list):
        return self.__get_list_sorted_by_property(list,'sequence')

    def __get_list_sorted_by_property(self, list, property_name):
        """
        Returns list sorted on a specified property.
        :param list: e.g. [{'id':1, 'sequence':2}, {'id':2, 'sequence':1}]
        :param property_name: e.g. 'sequence'
        :return: sorted list, from example above: [{'id':2, 'sequence':1}, {'id':1, 'sequence':2}]
        """
        return sorted(list, key=lambda element: element[property_name])

    def get_topic_by_id(self, id):
        return self.__getElementById('topics', id)

    def get_documents(self):
        if (self.json):
            return deepcopy(self.json['documents'])

    def get_document_by_id(self, id):
        return self.documents_dict[id]

    def get_field_list_by_document_id(self, document_id):
        '''
        Returns a list document fields with the data needed to generate Word file
        :param document_id:
        :return: list of document fields with "name" and "value"
        '''
        field_list = []
        for document_field in self.get_document_by_id(document_id)['fields']:
            field_id = document_field['fieldId']
            field = {
                'name': self.get_document_field_by_id(field_id)['name'],
                'value': document_field['value']
            }
            field_list.append(field)
        return field_list

    def get_action_name_by_id(self, id):
        action = self.get_ation_by_id(id)
        action_name = ''
        try:
            action_name = action['name']
        except:
            pass
        return action_name

    def get_target_group_legal_bases_by_document_id(self, id):
        return self.get_document_by_id(id)['targetGroupLegalBases']

    def get_decided_by_by_document_id(self, id):
        return self.get_document_by_id(id)['decidedBy']

    def get_mandatory_notice_by_mandatory_id_and_document_id(self, mandatory_id, document_id):
        document = self.get_document_by_id(document_id)
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

    def is_child_of(self, parent_id, child_id):
        """
        Returns True if children is parent's child, return false otherwise.
        :param parent_id:
        :param child_id:
        :return:
        """
        child = self.get_target_group_by_id(child_id)
        if child:
            if child and child['parentId'] is None:
                return False
            if child['parentId'] == parent_id:
                return True
            else:
                return self.is_child_of(parent_id, child['parentId'])
        return False