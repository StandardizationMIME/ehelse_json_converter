from InputHandler import *
from WordHandler import *
from MainView import *

class MainViewController:

    main_view = None

    def __init__(self):
        self.main_view = MainView(self)

    def run(self):
        pass

if __name__ == '__main__':
    program = MainViewController()
    program.run()
