import tkFileDialog
from src.logic.InputHandler import *
from src.helpers.Messages import *
from src.logic.ExportContent import *
from src.logic.WordHandler import *
from src.views.MainView import *


class MainController:

    def __init__(self, root):
        # View config
        self.main_view = MainView(root)
        self.main_view.upload_button.config(command=self.upload)
        self.main_view.upload_button_template.config(command=self.upload_template)
        self.main_view.download_button.config(command=self.download)

        # Paths
        self.input_path = ''
        self.input_path_template = ''
        self.output_path = ''

        # Export content
        self.export_content = ExportContent()

    def download(self):
        """
        Downloads word document

        Triggered on download_button click
        :return:
        """
        self.__clear_error_message()
        if self.input_path:
            self.output_path = tkFileDialog.asksaveasfilename(defaultextension=".docx")
            if self.output_path:
                self.__download_generated_word_document(self.output_path)
                self.__set_success_message(Messages.SUCCESS_DOWNLOAD)
        else:
            self.__set_error_message(Messages.ERROR_NO_INPUT_PATH_SELECTED)

    def upload(self):
        """
        Uploads JSON input file

        Triggered on upload_button click
        :return:
        """
        self.__clear_error_message()
        self.main_view.disable_download_button(True)
        path = tkFileDialog.askopenfilename(parent=self.main_view, initialdir="/", title='Last opp JSON-fil')
        self.main_view.set_input_path('')
        if not path:
            pass
        elif self.__get_file_extension(path).lower() != 'json':
            self.__set_error_message(Messages.ERROR_INVALID_FILE_FORMAT)
        else:   # Valid path
            try:
                self.input_path = path
                self.main_view.set_input_path(self.input_path)
                self.__generate_word_document(self.input_path)
                self.__check_downloadable()
            except ValueError as e:
                print e
                self.__set_error_message(Messages.ERROR_INVALID_JSON)
            except Exception as e:
                print e
                self.__set_error_message(Messages.ERROR_INVALID_INPUT_CONTENT)

    def upload_template(self):
        """
        Uploads Word template

        Triggered on upload_button_template click
        :return:
        """
        self.__clear_error_message()
        self.main_view.disable_download_button(True)
        path = tkFileDialog.askopenfilename(parent=self.main_view, initialdir="/", title='Last opp Word-mal')
        self.main_view.set_input_path_template('')
        if not path:
            pass
        elif self.__get_file_extension(path).lower() != 'docx':
            self.__set_error_message(Messages.ERROR_INVALID_FILE_FORMAT)
        else:  # Valid path
            try:
                self.input_path_template = path
                self.main_view.set_input_path_template(self.input_path_template)
                self.__check_downloadable()
            except ValueError as e:
                print e
                self.__set_error_message(Messages.ERROR_INVALID_JSON)
            except Exception as e:
                print e
                self.__set_error_message(Messages.ERROR_INVALID_INPUT_CONTENT)

    def __check_downloadable(self):
        """
        Checks that both a JSON file and a Word template is uploaded.
        :return:
        """
        print 'download'
        if self.input_path and self.input_path_template:
            self.main_view.disable_download_button(False)

    def __clear_error_message(self):
        self.main_view.set_error_message('')

    def __set_error_message(self, error_message):
        self.main_view.set_success_message('')
        self.main_view.set_error_message(error_message)

    def __set_success_message(self, success_message):
        self.main_view.set_error_message('')
        self.main_view.set_success_message(success_message)

    def __generate_word_document(self, input_path):
        """
        Generates word document
        :param input_path:
        :return:
        """
        input_handler = InputHandler(input_path)

        topics = input_handler.getTopics()
        for topic in topics:
            documents = input_handler.get_documents_by_topic_id(topic['id'])
            self.export_content.add_topic(topic, documents, input_handler)

    def __download_generated_word_document(self, output_path):
        """
        Downloads docx file with the inserted values from json file.
        There is no support for for links in python-docx-template (docxtpl),
        therefore the file is first saved, and then read using python-docx (docx)
        to replace the links with working hyperlinks, before the file is written
        back to disk.
        :param output_path:
        :return:
        """
        # Python-docx-template
        template = DocxTemplate(self.input_path_template)
        template.render(self.export_content.get_content())
        template.save(self.output_path)
        # Python-docx
        word_handler = WordHandler(output_path)
        word_handler.insert_hyper_links()
        word_handler.save_word_document(output_path)
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
        return file_name_with_extension[file_extension_index+1:]
