from InputHandler import *
from MainView import *
from Messages import *
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

        # Word handler
        self.word_handler = WordHandler()


    def download(self):
        self.__clear_error_message()
        if self.input_path:
            self.output_path = tkFileDialog.asksaveasfilename(defaultextension=".docx")
            if self.output_path:
                self.__download_generated_word_document(self.output_path)
                self.__set_success_message(Messages.SUCCESS_DOWNLOAD)
        else:
            self.__set_error_message(Messages.ERROR_NO_INPUT_PATH_SELECTED)

    def uplpoad(self):
        self.__clear_error_message()
        self.main_view.disable_download_button(True)
        path = tkFileDialog.askopenfilename(parent=self.main_view, initialdir="/", title='Last opp JSON-fil')
        self.main_view.set_input_path('')
        if not path:
            pass
        elif self.__get_file_extension(path).lower() != 'json':
            self.__set_error_message(Messages.ERROR_INVALID_FILE_FORMAT)
        else:   # Valid path
            self.input_path = path
            self.main_view.set_input_path(self.input_path)
            try:
                self.__generate_word_document(self.input_path)
                self.main_view.disable_download_button(False)
            except ValueError as e:
                print e
                self.__set_error_message(Messages.ERROR_INVALID_JSON)
            except Exception as e:
                print e
                self.__set_error_message(Messages.ERROR_INVALID_INPUT_CONTENT)

    def __clear_error_message(self):
        self.main_view.set_error_message('')

    def __set_error_message(self, error_message):
        self.main_view.set_success_message('')
        self.main_view.set_error_message(error_message)

    def __set_success_message(self, success_message):
        self.main_view.set_error_message('')
        self.main_view.set_success_message(success_message)


    def __generate_word_document(self, input_path):
        input_handler = InputHandler(input_path)

        # Heading
        self.word_handler.add_heading('Eksport fra MIME')

        # Content
        for topic in input_handler.getTopics():
            # Topic
            self.word_handler.add_topic(topic)

            # Document
            for document in input_handler.get_documents_by_topic_id(topic['id']):
                self.word_handler.add_document(document, input_handler)

    def __download_generated_word_document(self, output_path):
        file_path = self.__get_file_path(output_path)
        file_name = self.__get_file_name(output_path)
        self.word_handler.save_word_document(file_path, file_name)

        print 'download complete'

    def __get_file_path(self, full_path):
        end_of_path_index = full_path.rfind('/')  # Last occurrence of '/'
        return full_path[:end_of_path_index]

    def __get_file_name(self, full_path):
        file_name_with_extension = full_path[len(self.__get_file_path(full_path)) + 1:]
        file_extension_index = file_name_with_extension.rfind('.docx')
        return file_name_with_extension[:file_extension_index]

    def __get_file_extension(self, full_path):
        file_name_with_extension = full_path[len(self.__get_file_path(full_path)) + 1:]
        file_extension_index = file_name_with_extension.rfind('.')
        return file_name_with_extension[file_extension_index+1 :]
