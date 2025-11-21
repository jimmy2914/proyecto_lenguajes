from PyQt6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QGraphicsRectItem, QMessageBox, QPushButton, QVBoxLayout, QWidget, QApplication
)
from PyQt6.QtGui import QPen, QBrush, QColor, QPixmap, QPainter
from PyQt6.QtCore import Qt, QTimer
from math import cos, sin, radians
import sys

class SimulationPanel(QGraphicsView):
    def __init__(self):
        super().__init__()
        

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setBackgroundBrush(QBrush(QColor("#DDDDDD")))
        self.setFixedSize(420, 420)

        self.grid_size = 10
        self.cell_size = 40
        self._initial_map_data = None # Almacenar el mapa inicial
        self.map_data = None

        self.player_item = None
        self.player_x = 0
        self.player_y = 0
        self.angle = 0  # 0=derecha, 90=arriba, 180=izquierda, 270=abajo


        self.clear_canvas()

    def clear_canvas(self):
        """Limpia la escena y crea cuadrícula vacía. Restablece el jugador al centro."""
        self.scene.clear()
        self.map_data = None # Se limpia el mapa activo, pero _initial_map_data se mantiene
        self.player_item = None

        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = QGraphicsRectItem(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                rect.setPen(QPen(QColor("#AAAAAA")))
                rect.setBrush(QBrush(QColor("#FFFFFF")))
                self.scene.addItem(rect)

        mid = self.grid_size // 2
        self.player_x, self.player_y = mid, mid
        self.angle = 0 # Asegurarse que el ángulo también se resetee
        self._draw_player()

    def _draw_player(self):
        """Crea o actualiza el sprite del jugador."""
        if self.player_item is not None:
            try:
                if self.player_item.scene() is not None:
                    self.scene.removeItem(self.player_item)
            except RuntimeError:
                pass 
            self.player_item = None

        try:
            pixmap = QPixmap("assets/player.png")
            if pixmap.isNull():
                rect = QGraphicsRectItem(0, 0, 30, 30)
                rect.setBrush(QBrush(QColor("blue")))
                self.player_item = rect
            else:
                pixmap = pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)
                self.player_item = QGraphicsPixmapItem(pixmap)

            self.scene.addItem(self.player_item)

            br = self.player_item.boundingRect()
            center_x = br.width() / 2
            center_y = br.height() / 2
            self.player_item.setTransformOriginPoint(center_x, center_y)

            self._update_player_position()
            self.player_item.setRotation(-self.angle)
        except Exception:
            import traceback

    def _update_player_position(self):
        """Posiciona el sprite según coordenadas de celda."""
        x = self.player_x * self.cell_size + (self.cell_size - self.player_item.boundingRect().width()) / 2
        y = self.player_y * self.cell_size + (self.cell_size - self.player_item.boundingRect().height()) / 2
        if self.player_item:
            self.player_item.setPos(x, y)

    # ============================================================
    # ACCIONES: MOVER / GIRAR (SÍNCRONAS)
    # ============================================================
    def move_turtle(self, current_x, current_y, current_angle, direction, distance, pen_down, color_name):
        """
        Mueve el jugador síncronamente, bloqueando hasta terminar la animación.
        """

        try:
            steps = int(round(float(distance))) if distance is not None else 1
        except Exception:
            steps = 1

        # Importar módulos necesarios para la espera
        import time
        from PyQt6.QtWidgets import QApplication

        for _ in range(max(1, steps)):
            # Calcular siguiente posición lógica
            dx, dy = self._dir_to_delta(direction, self.angle)
            next_x = self.player_x + dx
            next_y = self.player_y + dy

            # Validar colisiones
            if not self._is_inside_map(next_x, next_y):
                print(" Límite del mapa alcanzado.")
                break
            if self.map_data and self.map_data[next_y][next_x] == 1:
                print(" Choque con muro.")
                break

            # Animar el paso (interpolación)
            if self.player_item:
                start_pos = self.player_item.pos()
                end_x_px = next_x * self.cell_size + (self.cell_size - self.player_item.boundingRect().width()) / 2
                end_y_px = next_y * self.cell_size + (self.cell_size - self.player_item.boundingRect().height()) / 2
                
                # Animación suave de 250ms por paso
                duration = 0.25
                start_time = time.time()
                while time.time() - start_time < duration:
                    t = (time.time() - start_time) / duration
                    # Interpolación lineal
                    new_x = start_pos.x() + (end_x_px - start_pos.x()) * t
                    new_y = start_pos.y() + (end_y_px - start_pos.y()) * t
                    self.player_item.setPos(new_x, new_y)
                    
                    QApplication.processEvents()
                    time.sleep(0.01)
                
                # Asegurar posición final exacta
                self.player_item.setPos(end_x_px, end_y_px)

            # Actualizar posición lógica
            self.player_x, self.player_y = next_x, next_y

            # Verificar meta
            if self.map_data and self.map_data[self.player_y][self.player_x] == 2:
                self._on_goal_reached()
                return

    def rotate_player(self, direction_or_degrees):
        """
        Gira el jugador síncronamente.
        """
  
        import time
        from PyQt6.QtWidgets import QApplication

        # Calcular ángulo destino
        start_angle = self.angle
        target_angle = start_angle
        
        if direction_or_degrees == "izquierda":
            target_angle = (start_angle + 90) % 360
        elif direction_or_degrees == "derecha":
            target_angle = (start_angle - 90) % 360
            if target_angle < 0: target_angle += 360
        else:
            try:
                deg = int(direction_or_degrees)
                target_angle = deg % 360
            except Exception:
                pass
        
        # Animación de rotación
        if self.player_item:
            # Determinar la dirección más corta de giro
            diff = (target_angle - start_angle + 180) % 360 - 180
            final_angle_anim = start_angle + diff
            
            duration = 0.2
            start_time = time.time()
            while time.time() - start_time < duration:
                t = (time.time() - start_time) / duration
                current_anim_angle = start_angle + diff * t
                
                self.player_item.setRotation(-current_anim_angle)
                QApplication.processEvents()
                time.sleep(0.01)
            
            self.player_item.setRotation(-target_angle)

        # Actualizar ángulo lógico final
        self.angle = target_angle



    def _dir_to_delta(self, direction, angle):
        """Calcula desplazamiento (dx, dy) según el ángulo actual."""
        ang = radians(angle)
        dx = round(cos(ang))
        dy = round(-sin(ang))
        if direction == "atras":
            dx *= -1
            dy *= -1
        return dx, dy

    def load_map(self, grid):
        """Dibuja un mapa desde una matriz de 0/1/2/3 y lo almacena como el mapa inicial."""
        self._initial_map_data = [row[:] for row in grid] # Almacenar una copia profunda
        self._load_map_internal(grid)

    def _load_map_internal(self, grid):
        """Lógica interna para dibujar el mapa sin modificar _initial_map_data."""
        self.player_item = None
        self.scene.clear()
        self.map_data = grid

        rows = len(grid)
        cols = len(grid[0]) if rows else 0
        if rows == 0 or cols == 0:
            return

        self.grid_size = rows
        self.cell_size = min(400 // rows, 400 // cols)

        start_x, start_y = cols // 2, rows // 2

        for y, row in enumerate(grid):
            for x, val in enumerate(row):
                color = "#FFFFFF"
                if val == 1:
                    color = "#555555"  # muro
                elif val == 2:
                    color = "#00CC66"  # meta
                elif val == 3:
                    color = "#66AAFF"  # inicio
                    start_x, start_y = x, y

                rect = QGraphicsRectItem(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                rect.setPen(QPen(Qt.GlobalColor.black))
                rect.setBrush(QBrush(QColor(color)))
                self.scene.addItem(rect)

        self.player_x, self.player_y = start_x, start_y
        self.angle = 0
        self._draw_player()


    def reset_simulation(self):
        """Restablece la simulación al estado inicial del mapa o al lienzo en blanco."""


        if self._initial_map_data:
            self._load_map_internal(self._initial_map_data) # Recargar el mapa inicial
        else:
            self.clear_canvas() # Si no hay mapa inicial, ir a un lienzo vacío

    def _is_inside_map(self, x, y):
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size

    def _on_goal_reached(self):
        """Evento al llegar a la meta."""
        msg = QMessageBox()
        msg.setWindowTitle("¡Victoria!")
        msg.setText(" ¡Has llegado a la meta del laberinto!")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def get_turtle_pos(self):
        """Compatibilidad: devuelve la posición lógica en celdas."""
        return self.player_x, self.player_y
    
    def reset_map(self):
        """
        Restaura completamente el mapa actual a su estado inicial:
        - Limpia la escena
        - Redibuja el mapa desde los datos guardados
        - Reposiciona el jugador en el punto de inicio
        - Reinicia el ángulo y la cola de animaciones
        """
        if not self.map_data:

            self.clear_canvas()
            return

        # Guardar una copia del mapa actual (por si fue modificado)
        mapa_original = [row[:] for row in self.map_data]

        # Limpiar la escena completamente
        self.scene.clear()
        self.player_item = None

        rows = len(mapa_original)
        cols = len(mapa_original[0])
        self.grid_size = rows
        self.cell_size = min(400 // rows, 400 // cols)

        start_x, start_y = cols // 2, rows // 2

        # Redibujar todas las celdas
        for y, row in enumerate(mapa_original):
            for x, val in enumerate(row):
                color = "#FFFFFF"
                if val == 1:
                    color = "#555555"  # muro
                elif val == 2:
                    color = "#00CC66"  # meta
                elif val == 3:
                    color = "#66AAFF"  # inicio
                    start_x, start_y = x, y

                rect = QGraphicsRectItem(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                rect.setPen(QPen(Qt.GlobalColor.black))
                rect.setBrush(QBrush(QColor(color)))
                self.scene.addItem(rect)

        # Restaurar estado inicial del jugador
        self.player_x, self.player_y = start_x, start_y
        self.angle = 0
        self.map_data = mapa_original
        self._draw_player()


