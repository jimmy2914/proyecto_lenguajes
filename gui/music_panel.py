# minicode_ide/gui/music_panel.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
)
from PyQt6.QtCore import Qt, QRectF, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QBrush, QPen, QFont, QPainter


class PianoKey(QGraphicsRectItem):
    """Representa una tecla individual del piano."""
    
    def __init__(self, x, y, width, height, note_name, is_black=False):
        super().__init__(x, y, width, height)
        self.note_name = note_name
        self.is_black = is_black
        self.default_color = QColor(0, 0, 0) if is_black else QColor(255, 255, 255)
        self.highlight_color = QColor(100, 200, 255)
        
        # Configurar apariencia
        self.setBrush(QBrush(self.default_color))
        self.setPen(QPen(QColor(0, 0, 0), 2))
        
        # Etiqueta de nota (solo para teclas blancas)
        if not is_black:
            self.label = QGraphicsTextItem(note_name, self)
            self.label.setDefaultTextColor(QColor(100, 100, 100))
            font = QFont("Arial", 8)
            self.label.setFont(font)
            # Posicionar la etiqueta en la parte inferior de la tecla
            label_width = self.label.boundingRect().width()
            self.label.setPos(x + (width - label_width) / 2, y + height - 20)
    
    def highlight(self):
        """Resalta la tecla cuando se toca."""
        self.setBrush(QBrush(self.highlight_color))
    
    def reset(self):
        """Restaura el color original de la tecla."""
        self.setBrush(QBrush(self.default_color))


class MusicPanel(QWidget):
    """Panel de música con visualización de piano."""
    
    def __init__(self):
        super().__init__()
        self.keys = {}  # Diccionario de teclas: nota -> PianoKey
        self.current_note = None
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz de usuario."""
        layout = QVBoxLayout(self)
        
        # Título y estado
        header_layout = QHBoxLayout()
        title_label = QLabel("🎹 Panel Musical")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Botón de limpiar
        clear_btn = QPushButton("Limpiar")
        clear_btn.clicked.connect(self.clear_panel)
        header_layout.addWidget(clear_btn)
        
        layout.addLayout(header_layout)
        
        # Etiqueta de estado
        self.status_label = QLabel("Esperando comandos musicales...")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.status_label)
        
        # Vista del piano
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setStyleSheet("background-color: #f0f0f0;")
        layout.addWidget(self.view)
        
        # Crear el teclado del piano
        self._create_piano()
        
        # Timer para resetear las teclas después de resaltarlas
        self.reset_timer = QTimer()
        self.reset_timer.timeout.connect(self._reset_highlighted_key)
    
    def _create_piano(self):
        """Crea el teclado del piano con 2 octaves."""
        # Dimensiones de las teclas
        white_key_width = 40
        white_key_height = 150
        black_key_width = 25
        black_key_height = 100
        
        # Notas en español (2 octavas)
        # Patrón: do, do#, re, re#, mi, fa, fa#, sol, sol#, la, la#, si
        notes_pattern = [
            ('do', False), ('do#', True), ('re', False), ('re#', True), 
            ('mi', False), ('fa', False), ('fa#', True), ('sol', False), 
            ('sol#', True), ('la', False), ('la#', True), ('si', False)
        ]
        
        # Crear 2 octavas (do3 a si4)
        octaves = [3, 4]
        x_offset = 20
        
        # Primero crear todas las teclas blancas
        white_x = x_offset
        for octave in octaves:
            for note, is_black in notes_pattern:
                if not is_black:
                    note_name = f"{note}{octave}"
                    key = PianoKey(white_x, 20, white_key_width, white_key_height, 
                                   note_name, is_black=False)
                    self.scene.addItem(key)
                    self.keys[note_name] = key
                    white_x += white_key_width
        
        # Luego crear las teclas negras encima
        black_positions = [0.7, 1.7, 3.7, 4.7, 5.7]  # Posiciones relativas de teclas negras
        for octave in octaves:
            octave_offset = (octave - 3) * 7 * white_key_width
            for i, pos in enumerate(black_positions):
                black_x = x_offset + octave_offset + pos * white_key_width
                
                # Determinar el nombre de la nota negra
                black_notes = ['do#', 're#', 'fa#', 'sol#', 'la#']
                note_name = f"{black_notes[i]}{octave}"
                
                key = PianoKey(black_x, 20, black_key_width, black_key_height, 
                               note_name, is_black=True)
                self.scene.addItem(key)
                self.keys[note_name] = key
        
        # Ajustar el tamaño de la escena
        self.scene.setSceneRect(0, 0, white_x + 20, white_key_height + 40)
    
    def play_note(self, note_name, duration=0.5):
        """
        Visualiza la nota tocada en el piano.
        
        Args:
            note_name: Nombre de la nota (ej: 'do', 'do4', 're#3')
            duration: Duración en segundos
        """
        # Normalizar el nombre de la nota
        note_name = note_name.lower().strip()
        
        # Si no tiene octava, usar octava 4 por defecto
        if not any(char.isdigit() for char in note_name):
            note_name = f"{note_name}4"
        
        # Actualizar estado
        self.status_label.setText(f"🎵 Tocando: {note_name} ({duration}s)")
        
        # Resetear la nota anterior si existe
        if self.current_note and self.current_note in self.keys:
            self.keys[self.current_note].reset()
            
        self.current_note = note_name
        
        # Resaltar la tecla si existe
        if note_name in self.keys:
            key = self.keys[note_name]
            key.highlight()
            
            # Programar el reseteo de la tecla
            self.reset_timer.stop()
            self.reset_timer.start(int(duration * 1000))
        else:
            # Si la nota no existe en el piano, mostrar mensaje
            available_notes = ', '.join(list(self.keys.keys())[:12])
            self.status_label.setText(
                f"⚠️ Nota '{note_name}' no encontrada. "
                f"Notas disponibles: {available_notes}..."
            )
    
    def _reset_highlighted_key(self):
        """Resetea la tecla resaltada actualmente."""
        if self.current_note and self.current_note in self.keys:
            self.keys[self.current_note].reset()
        self.current_note = None
        self.status_label.setText("Esperando comandos musicales...")
    
    def clear_panel(self):
        """Limpia el panel y resetea todas las teclas."""
        # Resetear todas las teclas
        for key in self.keys.values():
            key.reset()
        
        self.current_note = None
        self.status_label.setText("Panel limpiado. Esperando comandos musicales...")
        self.reset_timer.stop()
