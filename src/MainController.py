from InputHandler import *
from MainView import *
from WordHandler import *
import tkFileDialog


class MainController:

    def __init__(self, root):
        # View config
        self.main_view = MainView(root)

        self.main_view.upload_button.config(command=self.uplpoad)
        self.main_view.download_button.config(command=self.download)

        # Paths
        self.input_path = ''
        self.output_path = ''

    def download(self):
        self.__clear_error_message()
        if self.input_path:
            self.output_path = tkFileDialog.asksaveasfilename(defaultextension=".docx")
            if self.output_path is None:  # asksaveasfile return `None` if dialog closed with "cancel".
                print 'error, idk'
                return

            self.__generate_word_document(self.input_path, self.output_path)
        else:
            # Error feedback
            self.main_view.set_error_message('Error!')
            print 'No file selected'

    def uplpoad(self):
        self.input_path = tkFileDialog.askopenfilename(parent=self.main_view, initialdir="/", title='Last opp JSON-fil')
        self.main_view.set_input_path('')
        if self.input_path:
            self.main_view.set_input_path(self.input_path)

    def __clear_error_message(self):
        self.main_view.set_error_message('')


    def __generate_word_document(self, input_path, output_path):
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
        file_path = self.__get_file_path(output_path)
        file_name = self.__get_file_name(output_path)
        word_handler.save_word_document(file_path, file_name)

        print 'download complete'

    def __get_file_path(self, full_path):
        end_of_path_index = full_path.rfind('/')  # Last occurrence of '/'
        return full_path[:end_of_path_index]

    def __get_file_name(self, full_path):
        file_name_with_extension = full_path[len(self.__get_file_path(full_path)) + 1:]
        file_extension_index = file_name_with_extension.rfind('.docx')
        return file_name_with_extension[:file_extension_index]
