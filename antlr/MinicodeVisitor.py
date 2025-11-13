# Generated from Minicode.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MinicodeParser import MinicodeParser
else:
    from MinicodeParser import MinicodeParser

# This class defines a complete generic visitor for a parse tree produced by MinicodeParser.

class MinicodeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MinicodeParser#programa.
    def visitPrograma(self, ctx:MinicodeParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#instruccion.
    def visitInstruccion(self, ctx:MinicodeParser.InstruccionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#declarar_var.
    def visitDeclarar_var(self, ctx:MinicodeParser.Declarar_varContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#asignacion.
    def visitAsignacion(self, ctx:MinicodeParser.AsignacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#funcion_def.
    def visitFuncion_def(self, ctx:MinicodeParser.Funcion_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#parametros.
    def visitParametros(self, ctx:MinicodeParser.ParametrosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#funcion_llamada.
    def visitFuncion_llamada(self, ctx:MinicodeParser.Funcion_llamadaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#argumentos.
    def visitArgumentos(self, ctx:MinicodeParser.ArgumentosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#condicional.
    def visitCondicional(self, ctx:MinicodeParser.CondicionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#repetir.
    def visitRepetir(self, ctx:MinicodeParser.RepetirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#bloque.
    def visitBloque(self, ctx:MinicodeParser.BloqueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#imprimir.
    def visitImprimir(self, ctx:MinicodeParser.ImprimirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#comando_grafico.
    def visitComando_grafico(self, ctx:MinicodeParser.Comando_graficoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#comando_musical.
    def visitComando_musical(self, ctx:MinicodeParser.Comando_musicalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#definir_polinomio.
    def visitDefinir_polinomio(self, ctx:MinicodeParser.Definir_polinomioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#mostrar_polinomio.
    def visitMostrar_polinomio(self, ctx:MinicodeParser.Mostrar_polinomioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#graficar_polinomio.
    def visitGraficar_polinomio(self, ctx:MinicodeParser.Graficar_polinomioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#operar_polinomio.
    def visitOperar_polinomio(self, ctx:MinicodeParser.Operar_polinomioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#expComparacion.
    def visitExpComparacion(self, ctx:MinicodeParser.ExpComparacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#expLogica.
    def visitExpLogica(self, ctx:MinicodeParser.ExpLogicaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#expMulDiv.
    def visitExpMulDiv(self, ctx:MinicodeParser.ExpMulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#expPotencia.
    def visitExpPotencia(self, ctx:MinicodeParser.ExpPotenciaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#expFuncion.
    def visitExpFuncion(self, ctx:MinicodeParser.ExpFuncionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#expSigno.
    def visitExpSigno(self, ctx:MinicodeParser.ExpSignoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#expVerdadero.
    def visitExpVerdadero(self, ctx:MinicodeParser.ExpVerdaderoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#expTexto.
    def visitExpTexto(self, ctx:MinicodeParser.ExpTextoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#expFalso.
    def visitExpFalso(self, ctx:MinicodeParser.ExpFalsoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#expParen.
    def visitExpParen(self, ctx:MinicodeParser.ExpParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#expNumero.
    def visitExpNumero(self, ctx:MinicodeParser.ExpNumeroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#expID.
    def visitExpID(self, ctx:MinicodeParser.ExpIDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinicodeParser#expSumaResta.
    def visitExpSumaResta(self, ctx:MinicodeParser.ExpSumaRestaContext):
        return self.visitChildren(ctx)



del MinicodeParser