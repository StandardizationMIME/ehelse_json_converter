import Tkinter as tk


class MainView(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)

        # Stop app on exit click
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)

        # Window properies
        tk.Toplevel.geometry(self, '300x200')
        tk.Toplevel.title(self, 'Word-eksport')

        # Window elements
        self.input_path = tk.StringVar()
        self.input_path_text_box = tk.Entry(self, textvariable=self.input_path, state='disabled')
        self.input_path_text_box.pack()

        self.upload_button = tk.Button(self, text='last opp JSON-fil')
        self.upload_button.pack()

        self.download_button = tk.Button(self, text='Last ned Word-fil')
        self.download_button.pack()

        self.error_message = tk.StringVar()
        self.error_message_label = tk.Label(self, textvariable=self.error_message)
        self.error_message_label.pack()

    def set_input_path(self, input_path):
        self.input_path.set(input_path)

    def set_error_message(self, error_message):
        self.error_message.set(error_message)
