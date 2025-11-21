from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guía del Lenguaje Minicode")
        self.resize(600, 700)
        
        layout = QVBoxLayout(self)
        
        # Visor de texto enriquecido
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setHtml(self._get_help_content())
        layout.addWidget(self.text_browser)
        
        # Botón de cerrar
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
    def _get_help_content(self):
        return """
        <h1 style="color: #2c3e50;">📘 Guía de Minicode</h1>
        <p>Bienvenido a <b>Minicode</b>, un lenguaje diseñado para aprender a programar de forma fácil y divertida.</p>
        
        <hr>
        
        <h2 style="color: #e67e22;">1. Conceptos Básicos</h2>
        <ul>
            <li><b>Comentarios:</b> Usa <code>#</code> para escribir comentarios. <br><i>Ejemplo:</i> <code># Esto es un comentario</code></li>
            <li><b>Variables:</b> Se declaran con <code>definir</code> o asignando directamente. <br><i>Ejemplo:</i> <code>definir puntos = 10</code> o <code>puntos = 10</code></li>
            <li><b>Imprimir:</b> Usa <code>imprimir</code> o <code>mostrar</code> para mensajes. <br><i>Ejemplo:</i> <code>imprimir "Hola Mundo"</code></li>
        </ul>

        <h2 style="color: #2980b9;">2. Estructuras de Control</h2>
        <h3>Condicionales (si / sino)</h3>
        <pre style="background-color: #f4f4f4; padding: 10px;">
si puntos > 5 :
    imprimir "Ganaste!"
sino :
    imprimir "Sigue intentando"
fin
        </pre>
        
        <h3>Bucles (repetir)</h3>
        <pre style="background-color: #f4f4f4; padding: 10px;">
repetir 3 veces :
    imprimir "Hola"
fin
        </pre>

        <h2 style="color: #27ae60;">3. Gráficos (Juegos 2D)</h2>
        <p>Controla al personaje en el panel de "Juegos".</p>
        <ul>
            <li><code>mover adelante [pasos]</code></li>
            <li><code>mover atras [pasos]</code></li>
            <li><code>girar derecha [grados]</code> (opcional)</li>
            <li><code>girar izquierda [grados]</code> (opcional)</li>
        </ul>
        <p><i>Ejemplo:</i></p>
        <pre style="background-color: #f4f4f4; padding: 10px;">
mover adelante 3
girar derecha
mover adelante 2
        </pre>

        <h2 style="color: #8e44ad;">4. Música</h2>
        <p>Reproduce notas musicales en el panel de "Música".</p>
        <ul>
            <li><code>tocar nota [nombre]</code>: (do, re, mi, fa, sol, la, si).</li>
            <li>Puedes especificar octava (ej: do4, sol3) y duración.</li>
        </ul>
        <p><i>Ejemplo:</i></p>
        <pre style="background-color: #f4f4f4; padding: 10px;">
tocar nota do durante 0.5 segundos
tocar nota re
tocar nota mi
        </pre>

        <h2 style="color: #c0392b;">5. Funciones</h2>
        <p>Crea tus propios comandos.</p>
        <pre style="background-color: #f4f4f4; padding: 10px;">
funcion saludar(nombre) :
    imprimir "Hola " + nombre
fin

llamar saludar("Maria")
# O simplemente:
saludar("Maria")
        </pre>
        
        <h2 style="color: #d35400;">6. Polinomios</h2>
        <p>Trabaja con matemáticas simbólicas.</p>
        <ul>
            <li><code>definir polinomio [id] = [expresion]</code></li>
            <li><code>graficar [id]</code></li>
            <li><code>mostrar polinomio [id]</code></li>
            <li><code>sumar/restar/multiplicar/dividir polinomio [p1] con/por polinomio [p2]</code></li>
        </ul>
        <pre style="background-color: #f4f4f4; padding: 10px;">
definir polinomio p1 = 2*x + 1
graficar p1
        </pre>
        """
