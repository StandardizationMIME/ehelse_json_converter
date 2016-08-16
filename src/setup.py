from distutils.core import setup
import py2exe

packages = ['Tkinter', 'tkFileDialog', 'docx', 'docx.shared', 'docx.oxml.shared', 'docxtpl', 'lxml._elementpath']
path_to_icon = r"hdir.ico"

setup(options={"py2exe": {"packages": packages}
               },
      windows=[{"script": 'Program.py'
                # "icon_resources": [(1, path_to_icon)]
                }]
    )