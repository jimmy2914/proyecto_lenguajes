# minicode_ide/gui/main_window.py
import sys
import os
import traceback
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QSplitter, QSizePolicy, QTabWidget,
    QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QAction, QIcon, QDesktopServices

from gui.code_editor import CodeEditor
from gui.console_output import ConsoleOutput
from gui.help_window import HelpWindow
from gui.ast_viewer import ASTViewer
from gui.simulation_panel import SimulationPanel
from gui.tutorial_manager import TutorialManager
from gui.polinomios_panel import PolinomiosPanel
from gui.music_panel import MusicPanel


# Nota: las importaciones de antlr4 y del executor se realizan en tiempo de ejecución
# dentro de run_code() para poder capturar errores de importación y mostrarlos en la UI.

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minicode IDE")
        self.setGeometry(100, 100, 1200, 800)

        self._create_widgets()
        self._create_layouts()
        self._create_menu()
        self._create_toolbar()
        self._connect_signals()

        self.tutorial_manager = TutorialManager()
        self._load_tutorials_menu()

        # Estado actual del archivo
        self.current_file = None
        self.code_editor.document().contentsChanged.connect(self._document_modified)

        # Instalar handler global de excepciones para capturar errores no atrapados
        # y escribirlos en un log y en la consola de la aplicación.
        sys.excepthook = self._global_excepthook

    # ---------------------------
    # Creación de widgets / layouts
    # ---------------------------
    def _create_widgets(self):
        self.code_editor = CodeEditor()
        self.console_output = ConsoleOutput()
        self.ast_viewer = ASTViewer()
        self.simulation_panel = SimulationPanel()
        self.polinomios_panel = PolinomiosPanel()
        self.music_panel = MusicPanel()


    def _create_layouts(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Panel izquierdo: Editor de Código
        left_panel = QVBoxLayout()
        left_panel.addWidget(self.code_editor)

        # Panel derecho: Consola, AST, Simulación (usando QTabWidget)
        self.right_tabs = QTabWidget()
        self.right_tabs.addTab(self.console_output, "Consola")
        self.right_tabs.addTab(self.ast_viewer, "Árbol AST")
        self.right_tabs.addTab(self.simulation_panel, "Juegos")
        self.right_tabs.addTab(self.polinomios_panel, "Polinomios")
        self.right_tabs.addTab(self.music_panel, "Música")



        # Splitter para dividir el editor y los paneles de la derecha
        splitter = QSplitter(Qt.Orientation.Horizontal)
        editor_container = QWidget()
        editor_container.setLayout(left_panel)
        splitter.addWidget(editor_container)
        splitter.addWidget(self.right_tabs)
        splitter.setStretchFactor(0, 2) # Editor toma más espacio
        splitter.setStretchFactor(1, 1) # Paneles de la derecha

        main_layout.addWidget(splitter)

    # ---------------------------
    # Menú / toolbar
    # ---------------------------
    def _create_menu(self):
        menu_bar = self.menuBar()

        # Menú Archivo
        file_menu = menu_bar.addMenu("&Archivo")
        new_action = QAction("Nuevo", self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Abrir...", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Guardar", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Guardar como...", self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()

        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menú Ejecutar
        run_menu = menu_bar.addMenu("&Ejecutar")
        run_action = QAction("Ejecutar Código", self)
        run_action.triggered.connect(self.run_code)
        run_menu.addAction(run_action)

        # Menú Ayuda
        help_menu = menu_bar.addMenu("Ay&uda")
        
        help_action = QAction("Guía del Lenguaje", self)
        help_action.triggered.connect(self.show_help_window)
        help_menu.addAction(help_action)

        about_action = QAction("Acerca de...", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def _create_toolbar(self):
        toolbar = self.addToolBar("Principal")
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        # Botones de archivo
        new_btn = QPushButton("Nuevo")
        new_btn.clicked.connect(self.new_file)
        toolbar.addWidget(new_btn)

        open_btn = QPushButton("Abrir")
        open_btn.clicked.connect(self.open_file)
        toolbar.addWidget(open_btn)

        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save_file)
        toolbar.addWidget(save_btn)

        toolbar.addSeparator()

        # Botones de ejecución
        run_btn = QPushButton("Ejecutar")
        run_btn.clicked.connect(self.run_code)
        toolbar.addWidget(run_btn)

        toolbar.addSeparator()
        
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self._reset_simulation)
        toolbar.addWidget(reset_btn)

        toolbar.addSeparator()

        help_btn_action = QAction("📘 Guía", self)
        help_btn_action.setStatusTip("Ver guía del lenguaje Minicode")
        help_btn_action.triggered.connect(self.show_help_window)
        toolbar.addAction(help_btn_action)

        toolbar.addSeparator()

        # Tutoriales
        self.tutorial_combo = QComboBox(self)
        self.tutorial_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.tutorial_combo.setPlaceholderText("Abrir Tutorial")
        self.tutorial_combo.currentIndexChanged.connect(self._tutorial_selected)
        toolbar.addWidget(self.tutorial_combo)

    def _connect_signals(self):
        # Conexiones adicionales si son necesarias
        self.right_tabs.currentChanged.connect(self._on_tab_changed)

        pass

    # ---------------------------
    # Gestión de archivos
    # ---------------------------
    def _document_modified(self):
        self.setWindowTitle(f"Minicode IDE - {self.current_file if self.current_file else 'Sin título'}{'*' if self.code_editor.document().isModified() else ''}")

    def _load_tutorials_menu(self):
        self.tutorial_combo.clear()
        self.tutorial_combo.addItem("Abrir Tutorial...") # Placeholder
        for name in self.tutorial_manager.get_tutorial_names():
            self.tutorial_combo.addItem(name)

    def _tutorial_selected(self, index):
        if index > 0:  # Ignorar el placeholder
            tutorial_name = self.tutorial_combo.currentText()
            if tutorial_name.startswith("[Mapa] "):
                # Es un mapa, no un archivo de código
                map_data = self.tutorial_manager.load_map_data(tutorial_name.replace("[Mapa] ", ""))
                if map_data:
                    self.console_output.append(f"🗺️ Cargando mapa: {tutorial_name}")
                    self.simulation_panel.load_map(map_data)
                    self.current_file = f"Mapa: {tutorial_name}"
                    self.setWindowTitle(f"Minicode IDE - {self.current_file}")
                else:
                    self.console_output.append(f" No se pudo cargar el mapa {tutorial_name}")
            else:
                # Es un tutorial normal
                code = self.tutorial_manager.load_tutorial_code(tutorial_name)
                self.code_editor.setText(code)
                self.current_file = f"Tutorial: {tutorial_name}"
                self._document_modified()


    def new_file(self):
        if self.code_editor.document().isModified():
            reply = QMessageBox.question(self, "Nuevo Archivo",
                                        "¿Desea guardar los cambios antes de crear uno nuevo?",
                                        QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Save:
                self.save_file()
            elif reply == QMessageBox.StandardButton.Cancel:
                return
        self.code_editor.clear()
        self.current_file = None
        self.setWindowTitle("Minicode IDE - Sin título")
        self.code_editor.document().setModified(False)
        self.console_output.clear()
        self.console_output.append("Consola de salida:\n")
        try:
            # Si hay un mapa cargado, solo reiniciarlo, no borrarlo
            if self.simulation_panel.map_data is not None:
                self.simulation_panel.reset_map()
                self.console_output.append("(ℹ Mapa mantenido en vista)")
            else:
                self.simulation_panel.clear_canvas()
        except Exception:
            # No queremos que un fallo del panel gráfico impida crear nuevo archivo
            self.console_output.append("Warning: fallo al limpiar el panel de simulación (ignored).")

    def open_file(self):
        if self.code_editor.document().isModified():
            reply = QMessageBox.question(self, "Abrir Archivo",
                                        "¿Desea guardar los cambios antes de abrir un nuevo archivo?",
                                        QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Save:
                self.save_file()
            elif reply == QMessageBox.StandardButton.Cancel:
                return

        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo Minicode", "", "Minicode Files (*.minicode);;All Files (*)")
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as f:
                self.code_editor.setText(f.read())
            self.current_file = file_name
            self._document_modified()
            self.console_output.clear()
            self.console_output.append("Consola de salida:\n")
            try:
                # Si hay un mapa cargado, solo reiniciarlo, no borrarlo
                if self.simulation_panel.map_data is not None:
                    self.simulation_panel.reset_map()
                    self.console_output.append("(ℹ Mapa mantenido en vista)")
                else:
                    self.simulation_panel.clear_canvas()
            except Exception:
                self.console_output.append("Warning: fallo al limpiar el panel de simulación (ignored).")

    def save_file(self):
        if self.current_file and not self.current_file.startswith("Tutorial:"):
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.code_editor.toPlainText())
            self.code_editor.document().setModified(False)
            self._document_modified()
            return True
        return self.save_file_as()

    def save_file_as(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo Minicode", "", "Minicode Files (*.minicode);;All Files (*)")
        if file_name:
            if not file_name.endswith(".minicode"):
                file_name += ".minicode"
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(self.code_editor.toPlainText())
            self.current_file = file_name
            self.code_editor.document().setModified(False)
            self._document_modified()
            return True
        return False

    # ---------------------------
    # Ejecución del código (robusta)
    # ---------------------------
    def run_code(self, mode=None):
        """
        Ejecuta el código Minicode con manejo de errores, 
        soporte de modos (musical, polinomios, juegos o completo),
        y limpieza de la cola de animaciones previas.
        """

        self.console_output.clear()
        self.console_output.append("--- Ejecutando Código Minicode ---")

        # Preparar el panel gráfico antes de ejecutar
        try:
            if self.simulation_panel.map_data is None:
                self.simulation_panel.clear_canvas()
            else:
                self.console_output.append("(ℹ Mapa cargado: se conserva durante la ejecución)")
        except Exception:
            self.console_output.append("Warning: fallo al preparar el panel de simulación (ignored).")

        codigo = self.code_editor.toPlainText()

        #  Importaciones seguras en tiempo de ejecución
        try:
            project_root = os.path.dirname(os.path.dirname(__file__))
            if project_root not in sys.path:
                sys.path.insert(0, project_root)

            from antlr4 import InputStream, CommonTokenStream
            from antlr.MinicodeLexer import MinicodeLexer
            from antlr.MinicodeParser import MinicodeParser

        except Exception:
            tb = traceback.format_exc()
            self.console_output.append("--- Error de importación (ANTLR/Parser) ---")
            self.console_output.append(tb)
            with open("fatal_error.log", "a", encoding="utf-8") as f:
                f.write("--- Error de importación ---\n")
                f.write(tb + "\n")
            return

        # 2 Cargar el executor
        try:
            from core.executor import MinicodeExecutor
        except Exception:
            tb = traceback.format_exc()
            self.console_output.append("--- Error al cargar el Executor ---")
            self.console_output.append(tb)
            with open("fatal_error.log", "a", encoding="utf-8") as f:
                f.write("--- Error al cargar el Executor ---\n")
                f.write(tb + "\n")
            return

        # 3 Parsear el código
        try:
            input_stream = InputStream(codigo)
            lexer = MinicodeLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = MinicodeParser(stream)
            tree = parser.programa()
        except Exception:
            tb = traceback.format_exc()
            self.console_output.append("--- Error durante el parseo ---")
            self.console_output.append(tb)
            with open("fatal_error.log", "a", encoding="utf-8") as f:
                f.write("--- Error durante el parseo ---\n")
                f.write(tb + "\n")
            return

        # 4 Ejecutar según el modo
        try:
            if hasattr(self, 'polinomios_panel') and self.polinomios_panel is not None:
                self.polinomios_panel.clear_panel()
            executor = MinicodeExecutor(
                self.console_output, 
                self.simulation_panel, 
                polinomios_panel=self.polinomios_panel,
                music_panel=self.music_panel
            )

            if mode == "musica":
                self.console_output.append(" Ejecutando solo el entorno musical...")
                executor.entorno_musical()
            elif mode == "polinomios":
                self.console_output.append(" Ejecutando solo el entorno de polinomios...")
                executor.entorno_polinomios()
            elif mode == "juegos":
                self.console_output.append(" Ejecutando solo el entorno gráfico (mapas)...")
                executor.entorno_grafico()
            else:
                # Modo completo (normal)
                executor.visit(tree)

            self.console_output.append("--- Ejecución Finalizada ---")

        except Exception:
            tb = traceback.format_exc()
            self.console_output.append("--- Error durante la ejecución ---")
            self.console_output.append(tb)
            with open("fatal_error.log", "a", encoding="utf-8") as f:
                f.write("--- Error durante la ejecución ---\n")
                f.write(tb + "\n")


    # ---------------------------
    # AST viewer
    # ---------------------------
    def show_ast_tree(self):
        codigo = self.code_editor.toPlainText()
        try:
            # importar en tiempo de ejecución para manejar faltas
            from antlr4 import InputStream, CommonTokenStream
            from antlr.MinicodeLexer import MinicodeLexer
            from antlr.MinicodeParser import MinicodeParser

            input_stream = InputStream(codigo)
            lexer = MinicodeLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = MinicodeParser(stream)
            tree = parser.programa()
            self.ast_viewer.show_ast(tree, parser)
        except Exception:
            tb = traceback.format_exc()
            self.console_output.append("--- Error al generar AST ---")
            self.console_output.append(tb)
            with open("fatal_error.log", "a", encoding="utf-8") as f:
                f.write("--- Error al generar AST ---\n")
                f.write(tb + "\n")

    def _on_tab_changed(self, index):
        """
        Si el usuario cambia a la pestaña del AST, se genera automáticamente el árbol
        usando el código actual del editor.
        """
        try:
            # Obtener el nombre de la pestaña seleccionada
            tab_name = self.right_tabs.tabText(index)
            if tab_name == "Árbol AST":
                codigo = self.code_editor.toPlainText().strip()
                if not codigo:
                    self.console_output.append("⚠️ No hay código para generar el AST.")
                    return

                from antlr4 import InputStream, CommonTokenStream
                from antlr.MinicodeLexer import MinicodeLexer
                from antlr.MinicodeParser import MinicodeParser

                input_stream = InputStream(codigo)
                lexer = MinicodeLexer(input_stream)
                stream = CommonTokenStream(lexer)
                parser = MinicodeParser(stream)
                tree = parser.programa()

                self.ast_viewer.show_ast(tree, parser)


        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.console_output.append("--- Error al generar AST automáticamente ---")
            self.console_output.append(tb)
            with open("fatal_error.log", "a", encoding="utf-8") as f:
                f.write("--- Error al generar AST automáticamente ---\n")
                f.write(tb + "\n")

    # ---------------------------
    # Dialogo Acerca de...
    # ---------------------------
    def show_about_dialog(self):
        QMessageBox.about(self, "Acerca de Minicode IDE",
                        "Minicode IDE v1.0\n\n"
                        "Un lenguaje de programación educativo con sintaxis en español.\n"
                        "Desarrollado con Python, ANTLR4 y PyQt6.")

    def show_help_window(self):
        """Muestra la ventana de guía del lenguaje."""
        if not hasattr(self, 'help_window') or self.help_window is None:
            self.help_window = HelpWindow(self)
        
        self.help_window.show()
        self.help_window.raise_()
        self.help_window.activateWindow()

    # ---------------------------
    # Excepthook global
    # ---------------------------
    def _global_excepthook(self, exctype, value, tb_obj):
        """
        Captura excepciones no manejadas y las escribe en la consola y en fatal_error.log.
        Esto ayuda a diagnosticar cerrados inesperados del proceso.
        """
        err = ''.join(traceback.format_exception(exctype, value, tb_obj))
        try:
            # Intentar escribir en la consola de la UI si está disponible
            if hasattr(self, "console_output") and self.console_output is not None:
                self.console_output.append("\n--- Error no capturado ---")
                self.console_output.append(err)
        except Exception:
            # Si incluso escribir en la UI falla, caerá al archivo log
            pass

        # Siempre escribir en el archivo log
        try:
            with open("fatal_error.log", "a", encoding="utf-8") as f:
                f.write(err + "\n")
        except Exception:
            # si escribir al log falla, no podemos hacer más aquí
            pass
        
    def _reset_simulation(self):
        """Restaura el mapa y la simulación a su estado inicial."""
        try:
            if hasattr(self.simulation_panel, "reset_map"):
                self.simulation_panel.reset_map()
                self.console_output.append("🔁 Mapa restaurado a su estado inicial.")
            else:
                self.console_output.append("⚠️ El panel de simulación no soporta reinicio.")
        except Exception:
            tb = traceback.format_exc()
            self.console_output.append("--- Error al reiniciar el mapa ---")
            self.console_output.append(tb)
            with open("fatal_error.log", "a", encoding="utf-8") as f:
                f.write("--- Error al reiniciar el mapa ---\n")
                f.write(tb + "\n")
