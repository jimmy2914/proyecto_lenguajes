# minicode_ide/main.py
import sys
import os
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

# Asegúrate de que el path de los módulos ANTLR sea accesible
# Si ANTLR genera en `antlr/`, necesitas añadirlo al PYTHONPATH
# Esto es una solución temporal para el desarrollo; en un empaquetado final
# se manejaría de otra forma.
sys.path.append(os.path.dirname(__file__))



from gui.tutorial_manager import TutorialManager



if __name__ == "__main__":
    tm = TutorialManager()
    print("Ruta base:", tm.tutorials_path)
    print("Archivos encontrados:", tm.get_tutorial_names())
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())