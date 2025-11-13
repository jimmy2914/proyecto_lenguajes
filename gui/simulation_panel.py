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
        print(" Inicializando SimulationPanel (modo juego 2D)...")

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

        self.action_queue = []
        self._is_processing_queue = False 

        self.clear_canvas()

    def clear_canvas(self):
        """Limpia la escena y crea cuadrícula vacía. Restablece el jugador al centro."""
        print("🧹 Limpiando canvas...")
        self.scene.clear()
        self.map_data = None # Se limpia el mapa activo, pero _initial_map_data se mantiene
        self.player_item = None
        self.action_queue.clear()
        self._is_processing_queue = False 

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
                print(" player_item eliminado por Qt (ignorado).")
            self.player_item = None

        try:
            pixmap = QPixmap("assets/player.png")
            if pixmap.isNull():
                print(" No se encontró 'assets/player.png'. Usando un cuadrado azul temporal.")
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
            print(" Error en _draw_player:", traceback.format_exc())

    def _update_player_position(self):
        """Posiciona el sprite según coordenadas de celda."""
        x = self.player_x * self.cell_size + (self.cell_size - self.player_item.boundingRect().width()) / 2
        y = self.player_y * self.cell_size + (self.cell_size - self.player_item.boundingRect().height()) / 2
        if self.player_item:
            self.player_item.setPos(x, y)

    # ============================================================
    # ACCIONES: MOVER / GIRAR (UNIFICADAS EN COLA GLOBAL)
    # ============================================================
    def move_turtle(self, current_x, current_y, current_angle, direction, distance, pen_down, color_name):
        """
        Añade pasos de movimiento a la cola general.
        """
        print(f"➡️ move_turtle llamado: ({direction}, {distance})")

        try:
            steps = int(round(float(distance))) if distance is not None else 1
        except Exception:
            steps = 1

        temp_x, temp_y = self.player_x, self.player_y
        temp_angle = self.angle

        # Simular las acciones ya en la cola para obtener el punto de partida
        for action, *args in self.action_queue:
            if action == 'move':
                temp_x, temp_y = args[0], args[1]
            elif action == 'rotate':
                dir_or_deg = args[0]
                if dir_or_deg == "izquierda":
                    temp_angle = (temp_angle + 90) % 360
                elif dir_or_deg == "derecha":
                    temp_angle = (temp_angle - 90) % 360
                    if temp_angle < 0: temp_angle += 360
                else:
                    try:
                        deg = int(dir_or_deg)
                        temp_angle = deg % 360
                    except Exception:
                        pass
        
        current_temp_x, current_temp_y = temp_x, temp_y
        current_temp_angle = temp_angle

        for _ in range(max(1, steps)):
            dx, dy = self._dir_to_delta_for_temp_angle(direction, current_temp_angle)
            next_temp_x = current_temp_x + dx
            next_temp_y = current_temp_y + dy

            if not self._is_inside_map(next_temp_x, next_temp_y):
                print(" Límite del mapa alcanzado, deteniendo secuencia.")
                break
            if self.map_data and self.map_data[next_temp_y][next_temp_x] == 1:
                print(" Choque con muro, deteniendo secuencia.")
                break

            self.action_queue.append(('move', next_temp_x, next_temp_y))
            current_temp_x, current_temp_y = next_temp_x, next_temp_y # Actualizar para el siguiente paso en esta ráfaga

        print(f" Movimiento encolado (cola total: {len(self.action_queue)} acciones).")


    def rotate_player(self, direction_or_degrees):
        """
        Encola una acción de rotación en la misma cola global.
        """
        print(f" rotate_player llamado: {direction_or_degrees}")

        self.action_queue.append(('rotate', direction_or_degrees))
        print(f" Rotación encolada (cola total: {len(self.action_queue)} acciones).")

    def flush_action_queue(self):
        """
        Inicia la ejecución de todas las acciones encoladas.
        Llamar a esto una vez que el programa Minicode haya terminado de interpretar.
        """
        if not self.action_queue:
            print(" No hay acciones pendientes para ejecutar.")
            return

        if self._is_processing_queue:
            print(" Ya hay una animación en curso.")
            return

        print(f" Iniciando ejecución de {len(self.action_queue)} acciones acumuladas...")
        self._is_processing_queue = True
        self._process_next_action_in_queue()


    def _process_next_action_in_queue(self):
        """Procesa secuencialmente los movimientos/rotaciones en la cola."""
        if not self.action_queue:
            print(" Cola de acciones vacía.")
            self._is_processing_queue = False
            return

        action, *args = self.action_queue.pop(0)
        if action == "move":
            new_x, new_y = args
            self._animate_single_step(new_x, new_y)
        elif action == "rotate":
            direction = args[0]
            self._perform_rotation(direction)
            QTimer.singleShot(80, self._process_next_action_in_queue)
        else:
            print(f" Acción desconocida: {action}")
            QTimer.singleShot(80, self._process_next_action_in_queue)

    def _animate_single_step(self, new_x, new_y):
        """Anima un solo paso en la cuadrícula."""
        if not self.player_item:
            print(" No hay sprite del jugador para animar.")
            QTimer.singleShot(80, self._process_next_action_in_queue)
            return

        start_x = self.player_item.x()
        start_y = self.player_item.y()

        end_x = new_x * self.cell_size + (self.cell_size - self.player_item.boundingRect().width()) / 2
        end_y = new_y * self.cell_size + (self.cell_size - self.player_item.boundingRect().height()) / 2

        steps = 8
        duration = 25

        def animate(step=0):
            if step <= steps:
                t = step / steps
                self.player_item.setPos(start_x + (end_x - start_x) * t,
                                        start_y + (end_y - start_y) * t)
                QTimer.singleShot(duration, lambda: animate(step + 1))
            else:
                self.player_x, self.player_y = new_x, new_y
                print(f" Nueva posición lógica: ({self.player_x}, {self.player_y})")

                if self.map_data and self.map_data[new_y][new_x] == 2:
                    print(" ¡Meta alcanzada!")
                    self.action_queue.clear()
                    self._is_processing_queue = False
                    QTimer.singleShot(100, self._on_goal_reached)
                    return

                QTimer.singleShot(50, self._process_next_action_in_queue)

        animate()

    def _dir_to_delta_for_temp_angle(self, direction, temp_angle):
        """Calcula desplazamiento (dx, dy) según un ángulo temporal."""
        ang = radians(temp_angle)
        dx = round(cos(ang))
        dy = round(-sin(ang))
        if direction == "atras":
            dx *= -1
            dy *= -1
        return dx, dy

    def _perform_rotation(self, direction_or_degrees):
        """Ejecuta la rotación del jugador y actualiza el sprite."""
        if direction_or_degrees == "izquierda":
            self.angle = (self.angle + 90) % 360
        elif direction_or_degrees == "derecha":
            self.angle = (self.angle - 90) % 360
            if self.angle < 0: self.angle += 360
        else:
            try:
                deg = int(direction_or_degrees)
                self.angle = deg % 360
            except Exception:
                pass

        print(f" Jugador rotado a {self.angle}°")

        if self.player_item:
            br = self.player_item.boundingRect()
            center = br.center()
            self.player_item.setTransformOriginPoint(center)
            self.player_item.setRotation(-self.angle)

    def load_map(self, grid):
        """Dibuja un mapa desde una matriz de 0/1/2/3 y lo almacena como el mapa inicial."""
        print(" Cargando mapa...")
        self._initial_map_data = [row[:] for row in grid] # Almacenar una copia profunda
        self._load_map_internal(grid)

    def _load_map_internal(self, grid):
        """Lógica interna para dibujar el mapa sin modificar _initial_map_data."""
        self.player_item = None
        self.scene.clear()
        self.map_data = grid
        self.action_queue.clear()
        self._is_processing_queue = False

        rows = len(grid)
        cols = len(grid[0]) if rows else 0
        if rows == 0 or cols == 0:
            print(" Mapa vacío.")
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
        print(f" Mapa cargado. Inicio en ({start_x}, {start_y})")

    def reset_simulation(self):
        """Restablece la simulación al estado inicial del mapa o al lienzo en blanco."""
        print(" Reiniciando simulación...")
        if self._is_processing_queue:
            print(" Deteniendo animación actual para reiniciar.")
            # Si hay una animación en curso, la detenemos y limpiamos la cola
            self.action_queue.clear()
            self._is_processing_queue = False
            # Es posible que necesitemos un mecanismo para detener QTimer.singleShot si están pendientes,
            # pero limpiar la cola y resetear la bandera suele ser suficiente para evitar que se programen nuevos pasos.

        if self._initial_map_data:
            self._load_map_internal(self._initial_map_data) # Recargar el mapa inicial
        else:
            self.clear_canvas() # Si no hay mapa inicial, ir a un lienzo vacío

    def _is_inside_map(self, x, y):
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size

    def _on_goal_reached(self):
        """Evento al llegar a la meta."""
        print(" ¡Has llegado a la meta!")
        msg = QMessageBox()
        msg.setWindowTitle("¡Victoria!")
        msg.setText(" ¡Has llegado a la meta del laberinto!")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def get_turtle_pos(self):
        """Compatibilidad: devuelve la posición lógica en celdas."""
        print(f" Posición actual del jugador: ({self.player_x}, {self.player_y})")
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
            print(" No hay mapa cargado. Se limpia el canvas.")
            self.clear_canvas()
            return

        print("🔁 Reiniciando mapa al estado original...")

        # Guardar una copia del mapa actual (por si fue modificado)
        mapa_original = [row[:] for row in self.map_data]

        # Limpiar la escena completamente
        self.scene.clear()
        self.action_queue.clear()
        self._is_processing_queue = False
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

        print(f" Mapa reiniciado. Jugador en ({self.player_x}, {self.player_y}) con ángulo {self.angle}°.")

