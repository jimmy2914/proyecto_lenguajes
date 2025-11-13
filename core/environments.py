import traceback

# ============================================================
# 🟩 ENTORNO GRÁFICO (versión mapa 2D / SimulationPanel moderno)
# ============================================================
class EntornoGrafico:
    def __init__(self, simulation_widget=None):
        """
        Inicializa el entorno gráfico conectado al SimulationPanel.
        """
        self.simulation_widget = simulation_widget
        self.x = 0
        self.y = 0
        self.angulo = 0
        self.lapiz_abajo = True
        self.color_actual = "negro"

        print("🟢 Entorno gráfico inicializado (modo mapa 2D).")

    # ------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------
    def _asegurar_widget(self):
        """Verifica que exista un widget de simulación antes de usarlo."""
        if not self.simulation_widget:
            print("⚠️ No hay widget de simulación disponible. Se omite la acción gráfica.")
            return False
        return True

    def _seguro(self, accion, *args, **kwargs):
        """Ejecuta una acción gráfica de forma segura (try/except)."""
        try:
            if self._asegurar_widget():
                accion(*args, **kwargs)
        except Exception as e:
            print(f"❌ Error ejecutando acción gráfica: {e}")
            traceback.print_exc()

    # ------------------------------------------------------------
    # Comandos gráficos
    # ------------------------------------------------------------
    def mover(self, direccion, distancia=1):
        """
        Mueve el jugador según la dirección y cantidad de pasos.
        - 'adelante' y 'atras' usan el ángulo actual.
        - dirección puede ser texto sin comillas (adelante, atras).
        """
        print(f"MOVER {direccion} {distancia} paso(s).")

        def accion():
            self.simulation_widget.move_turtle(
                self.x, self.y, self.angulo, str(direccion).lower(), distancia,
                self.lapiz_abajo, self.color_actual
            )
            self.x, self.y = self.simulation_widget.get_turtle_pos()
            print(f"📍 Posición actual del jugador: ({self.x}, {self.y})")

        self._seguro(accion)

    def girar(self, direccion, grados=90):
        """
        Gira el jugador visualmente (90° por defecto).
        - 'izquierda' o 'derecha'
        """
        print(f"GIRAR {direccion} {grados} grados.")

        def accion():
            self.simulation_widget.rotate_player(str(direccion).lower())

        # Actualizar ángulo lógico interno
        if direccion == "izquierda":
            self.angulo = (self.angulo + grados) % 360
        elif direccion == "derecha":
            self.angulo = (self.angulo - grados + 360) % 360

        self._seguro(accion)

    def cambiar_color(self, color):
        """Cambia el color actual del jugador o del lápiz (si aplica)."""
        self.color_actual = str(color)
        print(f"🎨 CAMBIAR COLOR a {self.color_actual}.")
        # En este modo, el color no dibuja líneas, pero lo conservamos.
        self._seguro(self.simulation_widget.update)

    def bajar_lapiz(self):
        """Activa el trazo (solo relevante en modo tortuga clásico)."""
        self.lapiz_abajo = True
        print("🖊️ BAJAR LÁPIZ.")

    def subir_lapiz(self):
        """Desactiva el trazo (solo relevante en modo tortuga clásico)."""
        self.lapiz_abajo = False
        print("✋ SUBIR LÁPIZ.")



# ============================================================
# 🟦 ENTORNO MUSICAL
# ============================================================
class EntornoMusical:
    def __init__(self):
        print("🎵 Entorno musical inicializado.")

    def tocar_nota(self, nota, duracion=0.5):
        """
        Simula la reproducción de una nota musical.
        En versiones futuras se integrará una librería de audio real.
        """
        print(f"TOCAR NOTA: {nota} durante {duracion} segundos.")
        # Aquí se podría usar `pygame.mixer` o `pyaudio` en el futuro.


# ============================================================
# 🟥 ENTORNO DE POLINOMIOS
# ============================================================
class EntornoPolinomios:
    def __init__(self, panel=None):
        self.panel = panel
        self.polinomios = {}
        print("📈 Entorno de polinomios inicializado.")

    def definir_polinomio(self, nombre, expresion_simbolica):
        self.polinomios[nombre] = expresion_simbolica
        print(f"DEFINIR POLINOMIO '{nombre}' como '{expresion_simbolica}'.")
        if self.panel:
            self.panel.definir_polinomio(nombre, expresion_simbolica)

    def graficar_polinomio(self, nombre_polinomio):
        if nombre_polinomio in self.polinomios:
            expr = self.polinomios[nombre_polinomio]
            print(f"GRAFICAR POLINOMIO '{nombre_polinomio}' ({expr}).")
            if self.panel:
                self.panel.graficar_polinomio(nombre_polinomio)
        else:
            raise Exception(f"Polinomio '{nombre_polinomio}' no definido.")
