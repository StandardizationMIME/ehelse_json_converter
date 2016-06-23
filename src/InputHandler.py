import json

class InputHandler:
    json = None

    # InputHandler Constructor
    def __init__(self, file_path):
        with open(file_path, 'r') as content_file:
            content = content_file.read()
            # print content
            j = json.loads(content)
            self.json = j

    # Returns entire json list
    def getJSON(self, file_path):
        return self.json

    def getTopics(self):
        if (self.json):
            return self.json['topicss']

    def getTopicById(self, id):
        return self.__getElementById('topics', id)

    def getDocuments(self):
        if (self.json):
            return self.json['documents']

    def getDocumentById(self, id):
        return self.__getElementById('documents', id)

    def getActions(self):
        return self.json['actions']

    def getActionById(self, id):
        return self.__getElementById('actions', id)

    def getDocumentFields(self):
        return self.json['documentFields']

    def getADocumentFieldById(self, id):
        return self.__getElementById('documentFields', id)

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

    # Returns element, if found, or None
    def __getElementById(self, elements, id):
        if not isinstance(id, basestring):  # TODO: Throw exception instead?
            id = '' + id
        for element in self.json[elements]:
            if element['id'] == id:
                return element
        return None