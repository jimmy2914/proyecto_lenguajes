# minicode_ide/gui/console_output.py
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QFont, QTextCursor # QTextCursor sigue siendo la clase correcta

class ConsoleOutput(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFont(QFont("Monospace", 10))
        self.append("Consola de salida:\n")

    def append(self, text):
        # Mueve el cursor al final antes de añadir texto
        cursor = self.textCursor()
        # ¡Corrección aquí!
        cursor.movePosition(QTextCursor.MoveOperation.End) # Usar MoveOperation.End
        self.setTextCursor(cursor)
        self.insertPlainText(text + '\n')
        self.ensureCursorVisible() # Asegura que el nuevo texto sea visible