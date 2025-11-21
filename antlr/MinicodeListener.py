# Generated from Minicode.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MinicodeParser import MinicodeParser
else:
    from MinicodeParser import MinicodeParser

# This class defines a complete listener for a parse tree produced by MinicodeParser.
class MinicodeListener(ParseTreeListener):

    # Enter a parse tree produced by MinicodeParser#programa.
    def enterPrograma(self, ctx:MinicodeParser.ProgramaContext):
        pass

    # Exit a parse tree produced by MinicodeParser#programa.
    def exitPrograma(self, ctx:MinicodeParser.ProgramaContext):
        pass


    # Enter a parse tree produced by MinicodeParser#instruccion.
    def enterInstruccion(self, ctx:MinicodeParser.InstruccionContext):
        pass

    # Exit a parse tree produced by MinicodeParser#instruccion.
    def exitInstruccion(self, ctx:MinicodeParser.InstruccionContext):
        pass


    # Enter a parse tree produced by MinicodeParser#declarar_var.
    def enterDeclarar_var(self, ctx:MinicodeParser.Declarar_varContext):
        pass

    # Exit a parse tree produced by MinicodeParser#declarar_var.
    def exitDeclarar_var(self, ctx:MinicodeParser.Declarar_varContext):
        pass


    # Enter a parse tree produced by MinicodeParser#asignacion.
    def enterAsignacion(self, ctx:MinicodeParser.AsignacionContext):
        pass

    # Exit a parse tree produced by MinicodeParser#asignacion.
    def exitAsignacion(self, ctx:MinicodeParser.AsignacionContext):
        pass


    # Enter a parse tree produced by MinicodeParser#funcion_def.
    def enterFuncion_def(self, ctx:MinicodeParser.Funcion_defContext):
        pass

    # Exit a parse tree produced by MinicodeParser#funcion_def.
    def exitFuncion_def(self, ctx:MinicodeParser.Funcion_defContext):
        pass


    # Enter a parse tree produced by MinicodeParser#parametros.
    def enterParametros(self, ctx:MinicodeParser.ParametrosContext):
        pass

    # Exit a parse tree produced by MinicodeParser#parametros.
    def exitParametros(self, ctx:MinicodeParser.ParametrosContext):
        pass


    # Enter a parse tree produced by MinicodeParser#funcion_llamada.
    def enterFuncion_llamada(self, ctx:MinicodeParser.Funcion_llamadaContext):
        pass

    # Exit a parse tree produced by MinicodeParser#funcion_llamada.
    def exitFuncion_llamada(self, ctx:MinicodeParser.Funcion_llamadaContext):
        pass


    # Enter a parse tree produced by MinicodeParser#argumentos.
    def enterArgumentos(self, ctx:MinicodeParser.ArgumentosContext):
        pass

    # Exit a parse tree produced by MinicodeParser#argumentos.
    def exitArgumentos(self, ctx:MinicodeParser.ArgumentosContext):
        pass


    # Enter a parse tree produced by MinicodeParser#condicional.
    def enterCondicional(self, ctx:MinicodeParser.CondicionalContext):
        pass

    # Exit a parse tree produced by MinicodeParser#condicional.
    def exitCondicional(self, ctx:MinicodeParser.CondicionalContext):
        pass


    # Enter a parse tree produced by MinicodeParser#repetir.
    def enterRepetir(self, ctx:MinicodeParser.RepetirContext):
        pass

    # Exit a parse tree produced by MinicodeParser#repetir.
    def exitRepetir(self, ctx:MinicodeParser.RepetirContext):
        pass


    # Enter a parse tree produced by MinicodeParser#bloque.
    def enterBloque(self, ctx:MinicodeParser.BloqueContext):
        pass

    # Exit a parse tree produced by MinicodeParser#bloque.
    def exitBloque(self, ctx:MinicodeParser.BloqueContext):
        pass


    # Enter a parse tree produced by MinicodeParser#imprimir.
    def enterImprimir(self, ctx:MinicodeParser.ImprimirContext):
        pass

    # Exit a parse tree produced by MinicodeParser#imprimir.
    def exitImprimir(self, ctx:MinicodeParser.ImprimirContext):
        pass


    # Enter a parse tree produced by MinicodeParser#comando_grafico.
    def enterComando_grafico(self, ctx:MinicodeParser.Comando_graficoContext):
        pass

    # Exit a parse tree produced by MinicodeParser#comando_grafico.
    def exitComando_grafico(self, ctx:MinicodeParser.Comando_graficoContext):
        pass


    # Enter a parse tree produced by MinicodeParser#comando_musical.
    def enterComando_musical(self, ctx:MinicodeParser.Comando_musicalContext):
        pass

    # Exit a parse tree produced by MinicodeParser#comando_musical.
    def exitComando_musical(self, ctx:MinicodeParser.Comando_musicalContext):
        pass


    # Enter a parse tree produced by MinicodeParser#nota_nombre.
    def enterNota_nombre(self, ctx:MinicodeParser.Nota_nombreContext):
        pass

    # Exit a parse tree produced by MinicodeParser#nota_nombre.
    def exitNota_nombre(self, ctx:MinicodeParser.Nota_nombreContext):
        pass


    # Enter a parse tree produced by MinicodeParser#definir_polinomio.
    def enterDefinir_polinomio(self, ctx:MinicodeParser.Definir_polinomioContext):
        pass

    # Exit a parse tree produced by MinicodeParser#definir_polinomio.
    def exitDefinir_polinomio(self, ctx:MinicodeParser.Definir_polinomioContext):
        pass


    # Enter a parse tree produced by MinicodeParser#mostrar_polinomio.
    def enterMostrar_polinomio(self, ctx:MinicodeParser.Mostrar_polinomioContext):
        pass

    # Exit a parse tree produced by MinicodeParser#mostrar_polinomio.
    def exitMostrar_polinomio(self, ctx:MinicodeParser.Mostrar_polinomioContext):
        pass


    # Enter a parse tree produced by MinicodeParser#graficar_polinomio.
    def enterGraficar_polinomio(self, ctx:MinicodeParser.Graficar_polinomioContext):
        pass

    # Exit a parse tree produced by MinicodeParser#graficar_polinomio.
    def exitGraficar_polinomio(self, ctx:MinicodeParser.Graficar_polinomioContext):
        pass


    # Enter a parse tree produced by MinicodeParser#operar_polinomio.
    def enterOperar_polinomio(self, ctx:MinicodeParser.Operar_polinomioContext):
        pass

    # Exit a parse tree produced by MinicodeParser#operar_polinomio.
    def exitOperar_polinomio(self, ctx:MinicodeParser.Operar_polinomioContext):
        pass


    # Enter a parse tree produced by MinicodeParser#expComparacion.
    def enterExpComparacion(self, ctx:MinicodeParser.ExpComparacionContext):
        pass

    # Exit a parse tree produced by MinicodeParser#expComparacion.
    def exitExpComparacion(self, ctx:MinicodeParser.ExpComparacionContext):
        pass


    # Enter a parse tree produced by MinicodeParser#expLogica.
    def enterExpLogica(self, ctx:MinicodeParser.ExpLogicaContext):
        pass

    # Exit a parse tree produced by MinicodeParser#expLogica.
    def exitExpLogica(self, ctx:MinicodeParser.ExpLogicaContext):
        pass


    # Enter a parse tree produced by MinicodeParser#expMulDiv.
    def enterExpMulDiv(self, ctx:MinicodeParser.ExpMulDivContext):
        pass

    # Exit a parse tree produced by MinicodeParser#expMulDiv.
    def exitExpMulDiv(self, ctx:MinicodeParser.ExpMulDivContext):
        pass


    # Enter a parse tree produced by MinicodeParser#expPotencia.
    def enterExpPotencia(self, ctx:MinicodeParser.ExpPotenciaContext):
        pass

    # Exit a parse tree produced by MinicodeParser#expPotencia.
    def exitExpPotencia(self, ctx:MinicodeParser.ExpPotenciaContext):
        pass


    # Enter a parse tree produced by MinicodeParser#expFuncion.
    def enterExpFuncion(self, ctx:MinicodeParser.ExpFuncionContext):
        pass

    # Exit a parse tree produced by MinicodeParser#expFuncion.
    def exitExpFuncion(self, ctx:MinicodeParser.ExpFuncionContext):
        pass


    # Enter a parse tree produced by MinicodeParser#expSigno.
    def enterExpSigno(self, ctx:MinicodeParser.ExpSignoContext):
        pass

    # Exit a parse tree produced by MinicodeParser#expSigno.
    def exitExpSigno(self, ctx:MinicodeParser.ExpSignoContext):
        pass


    # Enter a parse tree produced by MinicodeParser#expVerdadero.
    def enterExpVerdadero(self, ctx:MinicodeParser.ExpVerdaderoContext):
        pass

    # Exit a parse tree produced by MinicodeParser#expVerdadero.
    def exitExpVerdadero(self, ctx:MinicodeParser.ExpVerdaderoContext):
        pass


    # Enter a parse tree produced by MinicodeParser#expTexto.
    def enterExpTexto(self, ctx:MinicodeParser.ExpTextoContext):
        pass

    # Exit a parse tree produced by MinicodeParser#expTexto.
    def exitExpTexto(self, ctx:MinicodeParser.ExpTextoContext):
        pass


    # Enter a parse tree produced by MinicodeParser#expFalso.
    def enterExpFalso(self, ctx:MinicodeParser.ExpFalsoContext):
        pass

    # Exit a parse tree produced by MinicodeParser#expFalso.
    def exitExpFalso(self, ctx:MinicodeParser.ExpFalsoContext):
        pass


    # Enter a parse tree produced by MinicodeParser#expParen.
    def enterExpParen(self, ctx:MinicodeParser.ExpParenContext):
        pass

    # Exit a parse tree produced by MinicodeParser#expParen.
    def exitExpParen(self, ctx:MinicodeParser.ExpParenContext):
        pass


    # Enter a parse tree produced by MinicodeParser#expNumero.
    def enterExpNumero(self, ctx:MinicodeParser.ExpNumeroContext):
        pass

    # Exit a parse tree produced by MinicodeParser#expNumero.
    def exitExpNumero(self, ctx:MinicodeParser.ExpNumeroContext):
        pass


    # Enter a parse tree produced by MinicodeParser#expID.
    def enterExpID(self, ctx:MinicodeParser.ExpIDContext):
        pass

    # Exit a parse tree produced by MinicodeParser#expID.
    def exitExpID(self, ctx:MinicodeParser.ExpIDContext):
        pass


    # Enter a parse tree produced by MinicodeParser#expSumaResta.
    def enterExpSumaResta(self, ctx:MinicodeParser.ExpSumaRestaContext):
        pass

    # Exit a parse tree produced by MinicodeParser#expSumaResta.
    def exitExpSumaResta(self, ctx:MinicodeParser.ExpSumaRestaContext):
        pass



del MinicodeParser