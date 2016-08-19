from distutils.core import setup
import py2exe

packages = ['Tkinter', 'tkFileDialog', 'docx', 'docx.shared', 'docx.oxml.shared', 'docxtpl', 'lxml._elementpath', 'docx.enum.text']

setup(options={"py2exe": {"packages": packages}
               },
      windows=[{"script": 'Program.py'
                }]
    )