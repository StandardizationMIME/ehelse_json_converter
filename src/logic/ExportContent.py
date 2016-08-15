from datetime import datetime

class ExportContent:

    def __init__(self):
        self.reset_list()

    def reset_list(self):
        """
        Set list top empty
        :return:
        """
        self.list = {
            'title': '',
            'timestamp': self.__get_timestamp(),
            'topics': []
        }

    def get_content(self):
        return self.list

    def set_title(self, title):
        """
        Set title on document. Currently not in template
        :param title:
        :return:
        """
        self.list['title'] = title

    def add_topic(self, topic, documents, input_handler, target_group_id):
        """
        Add topic with related documents.
        :param topic: a topic to add to word template.
        :param documents:   list of documents related to the topic.
        :param input_handler: instance of InputHandler that contains information needed for lookup.
        :return:
        """
        self.list['topics'].append(
            {
                'title': topic['title'],
                'documents': self.__get_document_list(input_handler, documents, target_group_id)
            }
        )

    def __get_document_list(self, input_handler, documents, target_group_id):
        """
        Generates a document list on the format the template understand.

        Hyperlinks are not supported in python-docx-template (docxtpl), and are therefore inserted as:
            "[[url||url_name||text]]", where url is the descriptive keyword to recognize what it is.
            url_name is the url you want the hyperlink to link to, and
            text is the text you want the link to have.
            Links will hat to be inserted using python-docx later.
        :param input_handler: input from JSON file
        :param documents: the documents to add to the list (e.g. for a topic)
        :return: {}: documents
        """
        documents_object = []
        for document in documents:
            include = False # Set to True, if target group filter is on, and selected target group exists in document

            document_id = document['id']
            document_object = {}

            # Doucment content
            document_object['title'] = document['title']
            document_object['description'] = document['description']
            document_object['status'] = input_handler.get_status_name_by_id(document['statusId'])
            document_object['contactAddress'] = input_handler.get_contact_address_name_by_document_id(document_id)

            # Fields
            document_object['fields'] = input_handler.get_field_list_by_document_id(document_id)

            # Target groups
            document_object['mandatoryList'] = []

            mandatory_dict = input_handler.get_mandatory_dict_on_document_id(document_id)
            for mandataory_id, mandataory in mandatory_dict.iteritems():  # Loop through all mandatories that appear on the document
                target_groups = []
                for target_group in input_handler. \
                        get_target_groups_by_mandatory_id_and_document_id(mandataory_id, document_id):
                    if target_group_id == target_group['targetGroupId'] or input_handler.is_child_of(target_group_id, target_group['targetGroupId']):
                        include = True
                    target_groups.append({
                        'name': input_handler.getTargetGroupById(target_group['targetGroupId'])['name'], # Name of target group
                        'action': input_handler.get_action_name_by_id(target_group['actionId'])          # Name of action
                    })
                # -- Add target group fields
                targetGroupLegalBases = ''
                if document['targetGroupLegalBases'] is not None:
                    targetGroupLegalBases = document['targetGroupLegalBases']
                decidedBy = ''
                if document['decidedBy'] is not None:
                    decidedBy = document['decidedBy']
                replacedBy = ''
                if document['replacedBy'] is not None:
                    replacedBy = document['replacedBy']
                notice = ''
                for mandatory_notice in document['mandatoryNotices']:
                    if mandatory_notice['mandatoryId'] == mandataory_id:
                        notice = mandatory_notice['notice']
                document_object['mandatoryList'].append({
                    'name': mandataory['name'],
                    'targetGroups': target_groups,
                    'targetGroupLegalBases': targetGroupLegalBases,
                    'decidedBy': decidedBy,
                    'replacedBy': replacedBy,
                    'notice': notice
                })

            # Headings with paragraph
            document_object['headings'] = []
            for heading in document['headingContent']:
                document_object['headings'].append({
                    'title': input_handler.get_heading_name_by_heading_id(heading['headingId']),
                    'text': heading['text']
                })

            # Link categories
            document_object['linksCategories'] = []
            link_category_dict = input_handler.get_link_category_dict_by_document_id(document_id)

            for link_category_id, link_category in link_category_dict.iteritems():  # Loop through all link categories of the document
                links = []
                for link in input_handler.get_links_by_link_category_id_and_document_id(link_category_id,
                                                                                        document_id):  # for each link in current category
                    links.append({
                        'value': "[[url||%s||%s]]" % (link['text'], link['url'])    # This format is read and replaced with a hyperlink using python-docx (docx)
                    })
                document_object['linksCategories'].append({
                    'name': link_category['name'],
                    'links': links
                })

            if target_group_id == 0:
                documents_object.append(document_object)
            elif target_group_id > 0 and include:
                documents_object.append(document_object)

        return documents_object

    def __get_timestamp(self):
        """
        Returns timestamp on the format YYYY-DD-MM hh:mm:ss as string
        :return:
        """
        timestamp = str(datetime.now())
        return timestamp[:19]