import traceback

# ============================================================
#  ENTORNO GRÁFICO (versión mapa 2D / SimulationPanel moderno)
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


    # ------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------
    def _asegurar_widget(self):
        """Verifica que exista un widget de simulación antes de usarlo."""
        if not self.simulation_widget:

            return False
        return True

    def _seguro(self, accion, *args, **kwargs):
        """Ejecuta una acción gráfica de forma segura (try/except)."""
        try:
            if self._asegurar_widget():
                accion(*args, **kwargs)
        except Exception as e:
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

        def accion():
            self.simulation_widget.move_turtle(
                self.x, self.y, self.angulo, str(direccion).lower(), distancia,
                self.lapiz_abajo, self.color_actual
            )
            self.x, self.y = self.simulation_widget.get_turtle_pos()

        self._seguro(accion)

    def girar(self, direccion, grados=90):
        """
        Gira el jugador visualmente (90° por defecto).
        - 'izquierda' o 'derecha'
        """

        def accion():
            self.simulation_widget.rotate_player(str(direccion).lower())

        # Actualizar ángulo lógico interno
        if direccion == "izquierda":
            self.angulo = (self.angulo + grados) % 360
        elif direccion == "derecha":
            self.angulo = (self.angulo - grados + 360) % 360

        self._seguro(accion)


# ============================================================
#  ENTORNO MUSICAL
# ============================================================
class EntornoMusical:
    def __init__(self, music_panel=None):
        self.music_panel = music_panel
        self.pygame_initialized = False
        
        # Importaciones para manejo de tiempo y UI
        import time
        from PyQt6.QtWidgets import QApplication
        self.time = time
        self.QApplication = QApplication
        
        # Intentar inicializar pygame para audio (stereo)
        try:
            import pygame
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.pygame = pygame
            self.pygame_initialized = True

        except Exception as e:
            self.pygame = None
        
        # Mapeo de notas en español a frecuencias (Hz)
        # Usando la escala temperada, A4 = 440 Hz
        self.note_frequencies = {
            # Octava 3
            'do3': 130.81, 'do#3': 138.59, 're3': 146.83, 're#3': 155.56,
            'mi3': 164.81, 'fa3': 174.61, 'fa#3': 185.00, 'sol3': 196.00,
            'sol#3': 207.65, 'la3': 220.00, 'la#3': 233.08, 'si3': 246.94,
            
            # Octava 4 (central)
            'do4': 261.63, 'do#4': 277.18, 're4': 293.66, 're#4': 311.13,
            'mi4': 329.63, 'fa4': 349.23, 'fa#4': 369.99, 'sol4': 392.00,
            'sol#4': 415.30, 'la4': 440.00, 'la#4': 466.16, 'si4': 493.88,
            
            # Octava 5
            'do5': 523.25, 'do#5': 554.37, 're5': 587.33, 're#5': 622.25,
            'mi5': 659.25, 'fa5': 698.46, 'fa#5': 739.99, 'sol5': 783.99,
            'sol#5': 830.61, 'la5': 880.00, 'la#5': 932.33, 'si5': 987.77,
        }

    def tocar_nota(self, nota, duracion=0.5):
        """
        Reproduce una nota musical y la visualiza en el panel.
        
        Args:
            nota: Nombre de la nota (ej: 'do', 'do4', 're#3')
            duracion: Duración en segundos
        """
        # Normalizar el nombre de la nota
        nota = nota.lower().strip()
        
        # Si no tiene octava, usar octava 4 por defecto
        if not any(char.isdigit() for char in nota):
            nota_completa = f"{nota}4"
        else:
            nota_completa = nota
        
        # Visualizar en el panel si está disponible
        if self.music_panel:
            try:
                self.music_panel.play_note(nota_completa, duracion)
            except Exception as e:
                pass
        
        # Reproducir el sonido si pygame está disponible
        if self.pygame_initialized and nota_completa in self.note_frequencies:
            try:
                self._play_sound(nota_completa, duracion)
                
                # Esperar síncronamente para que la nota termine de sonar
                # Usamos un bucle con processEvents para no congelar la UI
                start_time = self.time.time()
                while self.time.time() - start_time < duracion:
                    self.QApplication.processEvents()
                    self.time.sleep(0.01)  # Pequeña pausa para no saturar CPU
                    
            except Exception as e:
                pass
        elif nota_completa not in self.note_frequencies:
            pass
    
    def _play_sound(self, nota, duracion):
        """
        Genera sonido adaptándose dinámicamente a CUALQUIER configuración de canales (Mono, Stereo, 5.1, 7.1).
        """
        import numpy as np

        # 1. Obtener configuración EXACTA del mixer
        try:
            mix_config = self.pygame.mixer.get_init()
            if not mix_config:
                # Intentar forzar estéreo si no está iniciado, aunque el driver puede imponer otra cosa
                self.pygame.mixer.init(frequency=22050, size=-16, channels=2)
                mix_config = self.pygame.mixer.get_init()
            
            frequency, format_pygame, channels = mix_config
        except Exception as e:
            pass

        # 2. Preparar la onda base (MONO)
        sample_rate = abs(frequency)
        num_samples = int(sample_rate * duracion)
        t = np.linspace(0, duracion, num_samples, False)
        note_freq = self.note_frequencies[nota]
        
        # Onda sinusoidal
        wave_base = np.sin(2 * np.pi * note_freq * t)
        
        # Fade in/out
        fade_samples = int(sample_rate * 0.02)
        if num_samples > 2 * fade_samples:
            wave_base[:fade_samples] *= np.linspace(0, 1, fade_samples)
            wave_base[-fade_samples:] *= np.linspace(1, 0, fade_samples)

        # Convertir a 16-bit
        wave_data = (wave_base * 32767).astype(np.int16)

        # 3. Construir el array Multicanal
        try:
            if channels == 1:
                # MONO: Array 1D
                sound_array = wave_data
            else:
                # MULTICANAL (Stereo=2, Surround=6, 7.1=8, etc.)
                # Necesitamos convertir el array (N,) a (N, channels)
                # Usamos reshape para hacerlo columna y tile para repetirlo
                
                # Paso A: Convertir a columna (N, 1)
                wave_col = wave_data.reshape(-1, 1)
                
                # Paso B: Repetir esa columna 'channels' veces horizontalmente
                sound_array = np.tile(wave_col, (1, channels))
                
                # Paso C: Asegurar que sea contiguo en memoria (CRÍTICO para pygame)
                sound_array = np.ascontiguousarray(sound_array)

            # 4. Reproducir
            sound = self.pygame.sndarray.make_sound(sound_array)
            sound.play()
            
        except Exception as e:
            pass
# ============================================================
#  ENTORNO DE POLINOMIOS
# ============================================================
class EntornoPolinomios:
    def __init__(self, panel=None):
        self.panel = panel
        self.polinomios = {}

    def definir_polinomio(self, nombre, expresion_simbolica):
        self.polinomios[nombre] = expresion_simbolica
        if self.panel:
            self.panel.definir_polinomio(nombre, expresion_simbolica)

    def graficar_polinomio(self, nombre_polinomio):
        if nombre_polinomio in self.polinomios:
            expr = self.polinomios[nombre_polinomio]
            if self.panel:
                self.panel.graficar_polinomio(nombre_polinomio)
        else:
            raise Exception(f"Polinomio '{nombre_polinomio}' no definido.")
