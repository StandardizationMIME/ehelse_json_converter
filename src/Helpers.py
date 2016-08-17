# -*- coding: utf-8 -*-

class Messages:
    # Error message
    ERROR_INVALID_FILE_FORMAT = 'Ugyldig filformat, vennligst last opp en JSON-fil.'
    ERROR_NO_INPUT_PATH_SELECTED = 'Ingen JSON-fil er valgt.'
    ERROR_INVALID_INPUT_CONTENT = 'Syntaksfeil i JSON-fil. Kan ikke behandle filen.'
    ERROR_INVALID_JSON = 'Ugyldig JSON-format.'
    ERROR_CANT_WRITE_TO_FILE = 'Kan ikke skrive til fil. Sørg for at filen ikke er åpen i andre programmer.s'
    ERROR_DEFAULT = 'Noe gikk galt, vennligst restart og prøv igjen.'
    # Success messages
    SUCCESS_DOWNLOAD = 'Fil lastet ned.'



class GuiContent:
    WINDOW_SIZE = '380x200'
    WINDOW_TITLE = 'Word-eksport'

    # Button values
    BUTTON_TEXT_OPEN_JSON = 'Åpne JSON-fil'
    BUTTON_TEXT_OPEN_WORD_TEMPLATE = 'Åpne Word-mal'
    BUTTON_TEXT_SAVE = 'Lagre Word-fil'

    # Drop down
    DROP_DOWN_VALUE_NO_SELECTED_TARGET_GROUP = 'Hele referansekatalogen'


class TemplateElements:
    NEW_PAGE = 'newpage'
    URL = 'url'
