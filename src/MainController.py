import tkFileDialog

from ExportContent import *
from InputHandler import *
from WordHandler import *
from MainView import *


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

        # Target groups
        self.target_groups_dict = {}

        # Export content
        self.export_content = ExportContent()
        self.input_handler = None

    def download(self):
        """
        Downloads word document

        Triggered on download_button click
        :return:
        """
        self.__clear_messages()
        if self.input_path:
            self.output_path = tkFileDialog.asksaveasfilename(defaultextension=".docx")
            if self.output_path:
                self.__download_generated_word_document(self.output_path)
                self.__set_success_message(Messages.SUCCESS_DOWNLOAD)
                try:
                    pass
                except ValueError as e:
                    print e
                    self.__set_error_message(Messages.ERROR_INVALID_JSON)
                except Exception as e:
                    print e
                    self.__set_error_message(Messages.ERROR_INVALID_INPUT_CONTENT)
        else:
            self.__set_error_message(Messages.ERROR_NO_INPUT_PATH_SELECTED)

    def upload(self):
        """
        Uploads JSON input file

        Triggered on upload_button click
        :return:
        """
        self.__clear_messages()
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
                self.input_handler = InputHandler(self.input_path)
                self.set_target_groups_drop_down_option()
                self.main_view.set_input_path(self.input_path)
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
        self.__clear_messages()
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

    def set_target_groups_drop_down_option(self):
        """
        Updates target_groups_drop_down values from JSON file.
        The default value is not touched.
        :return:
        """
        options = self.main_view.target_groups_drop_down.children['menu']
        options.delete(1, 'end')  # Clear drop down

        target_groups = self.input_handler.getTargetGroups()

        for target_group in target_groups:
            target_group_name = target_group['name']
            self.target_groups_dict[target_group_name] = target_group['id']
            options.add_command(label=target_group_name, command=lambda v=self.main_view.selected_target_group, l=target_group_name: v.set(l))

    def __check_downloadable(self):
        """
        Checks that both a JSON file and a Word template is uploaded.
        :return:
        """
        if self.input_path and self.input_path_template:
            self.main_view.disable_download_button(False)

    def __clear_messages(self):
        self.main_view.set_error_message('')
        self.main_view.set_success_message('')

    def __set_error_message(self, error_message):
        self.main_view.set_success_message('')
        self.main_view.set_error_message(error_message)

    def __set_success_message(self, success_message):
        self.main_view.set_error_message('')
        self.main_view.set_success_message(success_message)

    def __generate_word_document(self):
        """
        Generates word document
        :param input_path:
        :return:
        """
        topics = self.input_handler.getTopics()
        for topic in topics:
            documents = self.input_handler.get_documents_by_topic_id(topic['id'])
            self.export_content.add_topic(topic, documents, self.input_handler, 0)

    def __generate_word_document_based_on_target_groups(self, target_group_id):
        topics = self.input_handler.getTopics()
        for topic in topics:
            documents = self.input_handler.get_documents_by_topic_id(topic['id'])
            self.export_content.add_topic(topic, documents, self.input_handler, target_group_id)

    def __download_generated_word_document(self, output_path):  # TODO: look at documentation
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

        self.export_content.reset_list()    # Reset list, to make sure it is not repeated on multiple downloads
        if self.main_view.selected_target_group.get() == Messages.DROP_DOWN_VALUE_NO_SELECTED_TARGET_GROUP: # If no target group is selected
            self.__generate_word_document()
        else:
            target_group = self.input_handler.getTargetGroupById(self.target_groups_dict[self.main_view.selected_target_group.get()])
            self.__generate_word_document_based_on_target_groups(target_group['id'])
        content = self.export_content.get_content()
        template.render(content)
        try:
            template.save(self.output_path)

            # Python-docx - replace links and save
            word_handler = WordHandler(output_path)
            word_handler.insert_hyper_links()
            word_handler.save_word_document(output_path)
            print
        except IOError as e:
            self.__set_error_message(Messages.ERROR_CANT_WRITE_TO_FILE)
        except Exception as e:
            self.__set_error_message(Messages.ERROR_DEFAULT)
            print e

    def __get_file_path(self, full_path):
        """
        Returns folder path.
        input: 'c:/folder/file.json', returns 'c:/folder'
        :param full_path:
        :return:
        """
        end_of_path_index = full_path.rfind('/')  # Last occurrence of '/'
        return full_path[:end_of_path_index]

    def __get_file_name(self, full_path):
        """
        Returns filename.
        input: 'c:/folder/file.json', returns 'file.json'
        :param full_path:
        :return:
        """
        file_name_with_extension = full_path[len(self.__get_file_path(full_path)) + 1:]
        file_extension_index = file_name_with_extension.rfind('.docx')
        return file_name_with_extension[:file_extension_index]

    def __get_file_extension(self, full_path):
        """
        Returns file extension.
        input: 'c:/folder/file.json', returns 'json'
        :param full_path:
        :return:
        """
        file_name_with_extension = full_path[len(self.__get_file_path(full_path)) + 1:]
        file_extension_index = file_name_with_extension.rfind('.')
        return file_name_with_extension[file_extension_index+1:]
