from docx import Document

class WordHandler:
    HEADING_2 = 2
    HEADING_3 = 3
    
    word_document = None

    def __init__(self):
        self.word_document = Document()

    def add_topic(self, topic):
        self.word_document.add_heading(topic['title'], level=self.HEADING_2)

    def add_document(self, document, document_fields):
        # Title
        self.word_document.add_heading(document['title'], level= self.HEADING_3)
        # Description
        self.word_document.add_paragraph(document['description'])
        # Fields
        table = self.word_document.add_table(1,2)
        for document_field in document_fields:
            cells = table.add_row().cells
            cells[0].text = document_field['name']
            cells[1].text = document_field['value']

    def save_word_document(self, file_path, file_name):
        self.word_document.save("%s/%s.docx" % (file_path, file_name))

