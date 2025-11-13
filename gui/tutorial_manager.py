import os

class TutorialManager:
    def __init__(self):
        self.tutorials_path = os.path.join(os.path.dirname(__file__), "..", "tutorials")
        self.maps_path = os.path.join(self.tutorials_path, "maps")

    def get_tutorial_names(self):
        """Retorna todos los tutoriales y mapas disponibles."""
        names = []
        if os.path.exists(self.tutorials_path):
            for file in os.listdir(self.tutorials_path):
                if file.endswith(".minicode"):
                    names.append(file.replace(".minicode", ""))
        # Agregar mapas
        if os.path.exists(self.maps_path):
            for file in os.listdir(self.maps_path):
                if file.endswith(".map"):
                    names.append("[Mapa] " + file.replace(".map", ""))
        return sorted(names)

    def load_tutorial_code(self, name):
        """Carga código o mapa según el tipo de archivo."""
        # Archivos de código normales
        path = os.path.join(self.tutorials_path, name + ".minicode")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()

        # Mapas
        if name.startswith("[Mapa] "):
            map_name = name.replace("[Mapa] ", "")
            return self.load_map_data(map_name)
        return ""

    def load_map_data(self, map_name):
        """Carga un archivo .map y lo devuelve como matriz de enteros."""
        path = os.path.join(self.maps_path, map_name + ".map")
        if not os.path.exists(path):
            return None
        grid = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("#") or not line.strip():
                    continue
                row = [int(x) for x in line.strip().split()]
                grid.append(row)
        return grid
