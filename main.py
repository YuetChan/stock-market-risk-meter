import os

from PyQt5.QtWidgets import QApplication

from widgets.s_main_window import s_main_window

# Set the value of the variable
os.environ['code_meta_dir'] = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    app = QApplication([])

    main_window = s_main_window()
    
    main_window.resize(1200, 900)
    main_window.show()

    app.exec_()
    
