from antlr4 import *
from antlr.MinicodeLexer import MinicodeLexer
from antlr.MinicodeParser import MinicodeParser
from antlr.MinicodeVisitor import MinicodeVisitor
from antlr4.tree.Tree import TerminalNodeImpl
from core.environments import EntornoGrafico, EntornoMusical, EntornoPolinomios
from sympy import symbols, sympify, simplify, pretty
import traceback
x = symbols('x')


class MinicodeExecutor(MinicodeVisitor):
    """
    Intérprete principal de Minicode.
    Ejecuta las instrucciones generadas por el parser (ANTLR)
    y coordina los entornos de salida (consola, gráfico, musical, polinomios).
    """

    def __init__(self, console_output, simulation_panel=None, polinomios_panel=None):
        self.console_output = console_output
        self.simulation = simulation_panel
        self.polinomios_panel = polinomios_panel
        self.call_stack = [{}]
        self.variables = {}
        self.polinomios = {}  # 🔹 Único diccionario central para polinomios
        self.funciones = {}
        self.graficos = None
        self.simulation_widget = simulation_panel


    # -----------------------------------------------------------
    # Inicialización diferida de entornos gráficos
    # -----------------------------------------------------------
    def get_graficos(self):
        if self.graficos is None:
            try:
                self.graficos = EntornoGrafico(self.simulation_widget)
            except Exception:
                tb = traceback.format_exc()
                if self.console_output:
                    self.console_output.append("--- Error iniciando entorno gráfico ---\n" + tb)
                else:
                    print("--- Error iniciando entorno gráfico ---\n" + tb)
                self.graficos = None
        return self.graficos

    # -----------------------------------------------------------
    # Manejo de scopes (funciones)
    # -----------------------------------------------------------
    def push_scope(self):
        self.call_stack.append(self.variables.copy())
        self.variables = {}

    def pop_scope(self):
        if self.call_stack:
            self.variables = self.call_stack.pop()
        else:
            raise Exception("Error interno: intento de salir de un scope sin haber entrado.")

    def get_variable_value(self, name):
        if name in self.variables:
            return self.variables[name]
        for scope in reversed(self.call_stack):
            if name in scope:
                return scope[name]
        raise Exception(f"Error: variable '{name}' no definida.")

    def set_variable_value(self, name, value):
        for scope in reversed(self.call_stack):
            if name in scope:
                scope[name] = value
                return
        self.variables[name] = value

    # -----------------------------------------------------------
    # Visitadores principales
    # -----------------------------------------------------------
    def visitPrograma(self, ctx: MinicodeParser.ProgramaContext):
        for instr in ctx.instruccion():
            self.visit(instr)

    def visitInstruccion(self, ctx: MinicodeParser.InstruccionContext):
        return self.visitChildren(ctx)

    # -----------------------------------------------------------
    # Variables
    # -----------------------------------------------------------
    def visitDeclarar_var(self, ctx: MinicodeParser.Declarar_varContext):
        nombre = ctx.ID().getText()
        valor = None
        if ctx.expresion():
            valor = self.visit(ctx.expresion())
        self.set_variable_value(nombre, valor)

    def visitAsignacion(self, ctx: MinicodeParser.AsignacionContext):
        nombre = ctx.ID().getText()
        valor = self.visit(ctx.expresion())
        self.set_variable_value(nombre, valor)

    # -----------------------------------------------------------
    # Funciones
    # -----------------------------------------------------------
    def visitFuncion_def(self, ctx: MinicodeParser.Funcion_defContext):
        nombre = ctx.ID().getText()
        parametros = []
        if ctx.parametros():
            parametros = [p.getText() for p in ctx.parametros().ID()]
        self.funciones[nombre] = {'parametros': parametros, 'cuerpo': ctx.bloque()}

    def visitFuncion_llamada(self, ctx: MinicodeParser.Funcion_llamadaContext):
        nombre = ctx.ID().getText()
        if nombre not in self.funciones:
            raise Exception(f"Error: función '{nombre}' no definida.")

        func_info = self.funciones[nombre]
        params = func_info['parametros']
        cuerpo = func_info['cuerpo']

        args = []
        if ctx.argumentos():
            args = [self.visit(e) for e in ctx.argumentos().expresion()]

        if len(params) != len(args):
            raise Exception(f"Error: la función '{nombre}' esperaba {len(params)} argumento(s) pero recibió {len(args)}.")

        self.push_scope()
        for i, p in enumerate(params):
            self.variables[p] = args[i]

        try:
            self.visit(cuerpo)
        finally:
            self.pop_scope()
        return None

    # -----------------------------------------------------------
    # Condicionales y bucles
    # -----------------------------------------------------------
    def visitCondicional(self, ctx: MinicodeParser.CondicionalContext):
        condicion = self.visit(ctx.expresion())
        if condicion:
            self.visit(ctx.bloque(0))
        elif ctx.SINO():
            self.visit(ctx.bloque(1))

    def visitRepetir(self, ctx: MinicodeParser.RepetirContext):
        veces = int(self.visit(ctx.expresion()))
        for _ in range(veces):
            self.visit(ctx.bloque())

    def visitBloque(self, ctx: MinicodeParser.BloqueContext):
        for instr in ctx.instruccion():
            self.visit(instr)

    # -----------------------------------------------------------
    # Mostrar / Imprimir
    # -----------------------------------------------------------
    def visitImprimir(self, ctx: MinicodeParser.ImprimirContext):
        valor = self.visit(ctx.expresion())
        if self.console_output:
            self.console_output.append(str(valor))
        else:
            print(str(valor))

    # -----------------------------------------------------------
    # Comandos gráficos
    # -----------------------------------------------------------
    def visitComando_grafico(self, ctx: MinicodeParser.Comando_graficoContext):
        graficos = self.get_graficos()
        if graficos is None:
            if self.console_output:
                self.console_output.append("Error: no se pudo inicializar el entorno gráfico.\n")
            else:
                print("Error: no se pudo inicializar el entorno gráfico.")
            return

        try:
            if ctx.MOVER():
                direccion = ctx.getChild(1).getText()
                distancia = 1
                if ctx.expresion():
                    distancia = self.visit(ctx.expresion())
                graficos.mover(direccion, distancia)
                return

            if ctx.GIRAR():
                direccion = ctx.getChild(1).getText()
                grados = 90
                if ctx.expresion():
                    grados = self.visit(ctx.expresion())
                graficos.girar(direccion, grados)
                return

            if ctx.CAMBIAR() and ctx.COLOR():
                color_valor = "negro"
                if ctx.expresion():
                    color_valor = self.visit(ctx.expresion())
                graficos.cambiar_color(str(color_valor))
                return

            if ctx.BAJAR() and ctx.LAPIZ():
                graficos.bajar_lapiz()
                return

            if ctx.SUBIR() and ctx.LAPIZ():
                graficos.subir_lapiz()
                return

        except Exception:
            tb = traceback.format_exc()
            if self.console_output:
                self.console_output.append("--- Error ejecutando comando gráfico ---\n" + tb)
            else:
                print("--- Error ejecutando comando gráfico ---\n" + tb)

    # -----------------------------------------------------------
    # Comandos musicales
    # -----------------------------------------------------------
    def visitComando_musical(self, ctx: MinicodeParser.Comando_musicalContext):
        nota = ctx.ID().getText()
        duracion = 0.5
        if ctx.DURANTE():
            duracion = self.visit(ctx.expresion())
        self.musica.tocar_nota(nota, duracion)

    # -----------------------------------------------------------
    # Polinomios centralizados
    # -----------------------------------------------------------
    def visitDefinir_polinomio(self, ctx):
        nombre = ctx.ID().getText()
        expr_texto = ctx.expresion().getText()
        try:
            expr = sympify(expr_texto)
            self.polinomios[nombre] = expr
            self.variables[nombre] = expr
            if self.console_output:
                self.console_output.append(f"📈 Polinomio '{nombre}' definido como: {expr}")
        except Exception as e:
            if self.console_output:
                self.console_output.append(f"❌ Error al definir polinomio '{nombre}': {e}")

    def visitMostrar_polinomio(self, ctx):
        nombre = ctx.ID().getText()
        if nombre not in self.polinomios:
            self.console_output.append(f"⚠️ Polinomio '{nombre}' no existe.")
            return
        expr = self.polinomios[nombre]
        self.console_output.append("🧮 Polinomio:")
        self.console_output.append(pretty(expr))
        if self.polinomios_panel:
            self.polinomios_panel.display_expression(expr, nombre)

    def visitOperar_polinomio(self, ctx):
        op = ctx.children[0].getText()
        p1 = ctx.ID(0).getText()
        p2 = ctx.ID(1).getText()
        if p1 not in self.polinomios or p2 not in self.polinomios:
            self.console_output.append("⚠️ Uno de los polinomios no está definido.")
            return

        expr1 = self.polinomios[p1]
        expr2 = self.polinomios[p2]

        if op == "sumar":
            resultado = simplify(expr1 + expr2)
        elif op == "restar":
            resultado = simplify(expr1 - expr2)
        elif op == "multiplicar":
            resultado = simplify(expr1 * expr2)
        elif op == "dividir":
            resultado = simplify(expr1 / expr2)
        else:
            self.console_output.append(f"⚠️ Operación '{op}' no reconocida.")
            return

        nombre_res = f"{p1}_{op}_{p2}"
        self.polinomios[nombre_res] = resultado
        self.variables[nombre_res] = resultado
        self.console_output.append(f"✅ Nuevo polinomio '{nombre_res}' = {pretty(resultado)}")
        if self.polinomios_panel:
            self.polinomios_panel.display_expression(resultado, nombre_res)

    def visitGraficar_polinomio(self, ctx):
        nombre = ctx.ID().getText()
        if nombre not in self.polinomios:
            self.console_output.append(f"⚠️ Polinomio '{nombre}' no existe.")
            return
        expr = self.polinomios[nombre]
        self.console_output.append(f"📊 Graficando polinomio '{nombre}'...")
        if self.polinomios_panel:
            self.polinomios_panel.plot_expression(expr, nombre)

    # -----------------------------------------------------------
    # Expresiones
    # -----------------------------------------------------------
    def visitExpMulDiv(self, ctx: MinicodeParser.ExpMulDivContext):
        izq = self.visit(ctx.expresion(0))
        der = self.visit(ctx.expresion(1))
        op = ctx.op.type
        if op == MinicodeParser.POR:
            return izq * der
        elif op == MinicodeParser.DIV:
            if der == 0:
                raise Exception("Error: división por cero.")
            return izq / der
        elif op == MinicodeParser.MOD:
            return izq % der

    def visitExpSumaResta(self, ctx: MinicodeParser.ExpSumaRestaContext):
        izq = self.visit(ctx.expresion(0))
        der = self.visit(ctx.expresion(1))
        op = ctx.op.type
        if op == MinicodeParser.MAS:
            return izq + der
        elif op == MinicodeParser.MENOS:
            return izq - der

    def visitExpComparacion(self, ctx: MinicodeParser.ExpComparacionContext):
        izq = self.visit(ctx.expresion(0))
        der = self.visit(ctx.expresion(1))
        op = ctx.op.type
        if op == MinicodeParser.MENOR:
            return izq < der
        elif op == MinicodeParser.MAYOR:
            return izq > der
        elif op == MinicodeParser.MENORIGUAL:
            return izq <= der
        elif op == MinicodeParser.MAYORIGUAL:
            return izq >= der
        elif op == MinicodeParser.IGUAL:
            return izq == der
        elif op == MinicodeParser.DIFERENTE:
            return izq != der

    def visitExpLogica(self, ctx: MinicodeParser.ExpLogicaContext):
        izq = self.visit(ctx.expresion(0))
        op = ctx.op.type
        if op == MinicodeParser.Y:
            if not izq:
                return False
            der = self.visit(ctx.expresion(1))
            return bool(izq and der)
        elif op == MinicodeParser.O:
            if izq:
                return True
            der = self.visit(ctx.expresion(1))
            return bool(izq or der)

    def visitExpParen(self, ctx: MinicodeParser.ExpParenContext):
        return self.visit(ctx.expresion())

    def visitExpSigno(self, ctx: MinicodeParser.ExpSignoContext):
        valor = self.visit(ctx.expresion())
        op = ctx.getChild(0).getText()
        return -valor if op == '-' else valor

    def visitExpNumero(self, ctx: MinicodeParser.ExpNumeroContext):
        return float(ctx.NUMERO().getText())

    def visitExpTexto(self, ctx: MinicodeParser.ExpTextoContext):
        return ctx.TEXTO().getText().strip('"')

    def visitExpVerdadero(self, ctx: MinicodeParser.ExpVerdaderoContext):
        return True

    def visitExpFalso(self, ctx: MinicodeParser.ExpFalsoContext):
        return False

    def visitExpID(self, ctx):
        nombre = ctx.getText()
        if nombre in self.polinomios:
            return self.polinomios[nombre]
        return self.get_variable_value(nombre)

    def visitExpFuncion(self, ctx: MinicodeParser.ExpFuncionContext):
        return self.visit(ctx.funcion_llamada())
