# minicode_ide/gui/code_editor.py
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor, QTextDocument
from PyQt6.QtCore import QRegularExpression

class MinicodeHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        self.highlightingRules = []

        # Palabras clave de Minicode
        keywords = [
            "decir", "definir", "como", "si", "entonces", "sino", "fin",
            "repetir", "veces", "funcion", "mostrar", "mover", "adelante",
            "atras", "girar", "izquierda", "derecha", "cambiar", "color",
            "bajar", "lapiz", "subir", "tocar", "nota", "durante", "segundos",
            "graficar", "polinomio", "verdadero", "falso", "mientras", "hacer"
        ]
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor("#5B9E4B")) # Verde oscuro
        keywordFormat.setFontWeight(QFont.Weight.Bold)
        for word in keywords:
            pattern = QRegularExpression(r"\b" + word + r"\b")
            self.highlightingRules.append((pattern, keywordFormat))

        # Números
        numberFormat = QTextCharFormat()
        numberFormat.setForeground(QColor("#D98F4F")) # Naranja
        self.highlightingRules.append((QRegularExpression(r"\b\d+(\.\d+)?\b"), numberFormat))

        # Cadenas (texto)
        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor("#4E9A06")) # Verde
        self.highlightingRules.append((QRegularExpression(r'"[^"]*"'), stringFormat))

        # Comentarios
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor("#A0A0A0")) # Gris
        commentFormat.setFontItalic(True)
        self.highlightingRules.append((QRegularExpression(r'#.*'), commentFormat))

        # Operadores
        operatorFormat = QTextCharFormat()
        operatorFormat.setForeground(QColor("#CC0000")) # Rojo
        operators = ['+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=', 'es', 'no es', 'y', 'o']
        for op in operators:
            pattern = QRegularExpression(r"\b" + QRegularExpression.escape(op) + r"\b")
            self.highlightingRules.append((pattern, operatorFormat))

        # IDs de funciones (ej. `miFuncion(`)
        functionFormat = QTextCharFormat()
        functionFormat.setForeground(QColor("#729FCF")) # Azul claro
        self.highlightingRules.append((QRegularExpression(r"\b[A-Za-z0-9_]+\("), functionFormat))


    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Monospace", 12))
        self.setTabStopDistance(20) # 4 espacios
        self.highlighter = MinicodeHighlighter(self.document())