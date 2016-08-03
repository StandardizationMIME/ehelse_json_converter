from InputHandler import *
from WordHandler import *
from MainView import *

class MainViewController:

    main_view = None

    def __init__(self):
        self.main_view = MainView(self)

    def run(self):
        input_handler = InputHandler(input_path)
        word_handler = WordHandler()

        # Heading
        word_handler.add_heading('Eksport fra MIME')

        # Content
        for topic in input_handler.getTopics():
            # Topic
            word_handler.add_topic(topic)

            # Document
            for document in input_handler.get_documents_by_topic_id(topic['id']):
                word_handler.add_document(document, input_handler)

        # Save tile to disk
        word_handler.save_word_document(file_path, file_name)

        print 'complete'

if __name__ == '__main__':
    program = MainViewController()
    program.run()