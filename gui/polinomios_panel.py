from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sympy import symbols, lambdify, latex
import numpy as np

class PolinomiosPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Polinomios")
        
        # Layout principal del panel
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Área de desplazamiento
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True) # ¡Crucial para que el widget interno se expanda!
        self.main_layout.addWidget(self.scroll_area)

        # Contenedor para los polinomios dentro del área de desplazamiento
        self.scroll_content_widget = QWidget()
        # Definir una política de tamaño para el contenido del scroll para que se ajuste.
        self.scroll_content_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        self.scroll_area.setWidget(self.scroll_content_widget)
        
        # Layout para añadir los polinomios (dentro del scroll_content_widget)
        self.polinomios_layout = QVBoxLayout(self.scroll_content_widget)
        # Añadir un stretch al final para que los widgets se peguen arriba y no se extiendan innecesariamente
        self.polinomios_layout.addStretch(1) 
        self.scroll_content_widget.setLayout(self.polinomios_layout)

        # Atributos para mantener una referencia al último par de canvas y ejes añadido.
        self._last_added_expr_canvas = None
        self._last_added_expr_ax = None
        self._last_added_plot_canvas = None
        self._last_added_plot_figure = None
        self._last_added_plot_ax = None
        
        # Lista para guardar los "grupos" de (expr_canvas, plot_canvas) por nombre
        self.polinomio_groups = [] 

    # ------------------------------------------------------------
    # Limpia todo el contenido del panel, eliminando todos los polinomios mostrados.
    # ------------------------------------------------------------
    def clear_panel(self):

        if self.polinomios_layout.count() > 0:
            last_item = self.polinomios_layout.itemAt(self.polinomios_layout.count() - 1)
            if last_item and last_item.spacerItem():
                self.polinomios_layout.takeAt(self.polinomios_layout.count() - 1)

        while self.polinomios_layout.count():
            item = self.polinomios_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater() 
        
        # Limpiar las referencias internas
        self.polinomio_groups.clear()
        self._last_added_expr_canvas = None
        self._last_added_expr_ax = None
        self._last_added_plot_canvas = None
        self._last_added_plot_figure = None
        self._last_added_plot_ax = None

        # Redibujar el scroll_content_widget para asegurar que se actualice la vista
        self.scroll_content_widget.update()
        
        # Volver a añadir el stretch al final
        self.polinomios_layout.addStretch(1)


    # ------------------------------------------------------------
    # Crea un nuevo slot visual para un polinomio y muestra la expresión simbólica.
    # ------------------------------------------------------------
    def display_expression(self, expr, nombre="polinomio"):
        # Remover el stretch temporalmente para añadir el nuevo widget
        last_item = self.polinomios_layout.takeAt(self.polinomios_layout.count() - 1)

        # Crear un nuevo contenedor para este polinomio (expresión y gráfica)
        polinomio_group_widget = QWidget()
        # Aplicar una política de tamaño para el widget de grupo también
        polinomio_group_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        group_layout = QVBoxLayout(polinomio_group_widget) 
        polinomio_group_widget.setLayout(group_layout)
        
        # Canvas para la expresión simbólica (arriba)
        expr_canvas = FigureCanvas(Figure(figsize=(6, 0.8))) # Altura reducida a 0.8
        expr_ax = expr_canvas.figure.add_subplot(111)
        expr_ax.axis("off")  # ocultar ejes
        group_layout.addWidget(expr_canvas) 

        # Canvas para la gráfica (debajo de la expresión)
        plot_figure = Figure(figsize=(6, 3)) 
        plot_canvas = FigureCanvas(plot_figure)
        plot_ax = plot_canvas.figure.add_subplot(111) 
        plot_ax.axis("off") 
        plot_canvas.draw() 
        group_layout.addWidget(plot_canvas) 

        try:
            latex_expr = latex(expr)
            expr_ax.text(
                0, 1, f"${nombre}(x) = {latex_expr}$",
                horizontalalignment='left',
                verticalalignment='top',
                fontsize=14
            )
            expr_canvas.figure.tight_layout(pad=0.1)
            expr_canvas.draw()
        except Exception as e:
            expr_ax.text(0.5, 0.5, f"Error en expresión: {e}", ha='center', va='center')
            expr_canvas.draw()
        
        # Añadir este grupo al layout principal de polinomios
        self.polinomios_layout.addWidget(polinomio_group_widget)

        # Volver a añadir el stretch al final del layout
        self.polinomios_layout.addItem(last_item)

        # Actualizar las referencias al último par de canvases y axes creados
        self._last_added_expr_canvas = expr_canvas
        self._last_added_expr_ax = expr_ax
        self._last_added_plot_canvas = plot_canvas
        self._last_added_plot_figure = plot_figure
        self._last_added_plot_ax = plot_ax 

        # Guardar el grupo completo para poder referenciarlo por nombre más tarde
        self.polinomio_groups.append({
            "name": nombre,
            "expr_canvas": expr_canvas,
            "expr_ax": expr_ax,
            "plot_canvas": plot_canvas,
            "plot_figure": plot_figure,
            "plot_ax": plot_ax
        })

    def plot_expression(self, expr, name="polinomio"):
        target_group = None
        
        # 1. Intentar encontrar un grupo ya existente con el mismo nombre
        for group in reversed(self.polinomio_groups): 
            if group["name"] == name:
                target_group = group
                break
        
        if target_group is None:

            if self._last_added_plot_ax and self.polinomio_groups and self.polinomio_groups[-1]["name"] == name:
                target_group = self.polinomio_groups[-1]
            else:
                # 3. Si no hay un slot adecuado, crear uno nuevo con display_expression
                self.display_expression(expr, name) 
                target_group = self.polinomio_groups[-1] # El que acabamos de crear

        # Ahora que tenemos el target_group, podemos graficar
        plot_ax = target_group["plot_ax"]
        plot_canvas = target_group["plot_canvas"]

        plot_ax.clear() # Limpia los ejes antes de graficar
        
        x_sym = symbols("x")
        f = lambdify(x_sym, expr, "numpy")

        # Rango por defecto, puedes ajustarlo o hacerlo configurable
        xs = np.linspace(-10, 10, 400) 
        try:
            ys = f(xs)
            # Manejar posibles valores infinitos o NaN para evitar errores de ploteo
            finite_mask = np.isfinite(ys)
            plot_ax.plot(xs[finite_mask], ys[finite_mask], label=f"{name}(x)", linewidth=2)
            plot_ax.legend()
            plot_ax.grid(True)
            plot_ax.set_title(f"Gráfica de {name}(x)")
            plot_ax.set_xlabel("x")
            plot_ax.set_ylabel("y")
        except Exception as e:
            plot_ax.text(0.5, 0.5, f"Error al graficar: {e}", ha="center", va="center")
            plot_ax.set_title(f"Error en Gráfica de {name}(x)") # Añadir título de error
            plot_ax.axis("off") # Ocultar ejes si hay un error grave de graficado

        plot_canvas.draw()