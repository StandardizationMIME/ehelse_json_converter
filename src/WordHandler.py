from docx import Document

class WordHanlder:
    HEADING_2 = 2
    HEADING_3 = 3
    
    word_document = None

    def __init__(self):
        self.word_document = Document()

    def add_topic(self, topic):
        self.word_document.add_heading(topic['title'], level=self.HEADING_2)

    def add_document(self, document):
        self.word_document.add_heading(document['title'], level= self.HEADING_3)
        self.word_document.add_paragraph(document['description'])

    def save_word_document(self, file_path, file_name):
        self.word_document.save("%s/%s.docx" % (file_path, file_name))
