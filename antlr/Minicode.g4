grammar Minicode;

//============================
//  REGLA INICIAL
//============================
programa
    : instruccion* EOF
    ;

//============================
//  INSTRUCCIONES PRINCIPALES
//============================
instruccion
    : declarar_var
    | asignacion
    | imprimir
    | repetir
    | condicional
    | funcion_def
    | funcion_llamada
    | comando_grafico
    | comando_musical
    | definir_polinomio
    | operar_polinomio
    | mostrar_polinomio
    | graficar_polinomio
    | NUEVALINEA
    ;

//============================
//  DECLARACIONES Y ASIGNACIÓN
//============================
declarar_var
    : DEFINIR ID (COMO expresion)? NUEVALINEA?
    ;

asignacion
    : ID '=' expresion NUEVALINEA?
    ;

//============================
//  FUNCIONES
//============================
funcion_def
    : FUNCION ID '(' parametros? ')' ':' NUEVALINEA bloque FIN
    ;

parametros
    : ID (',' ID)*
    ;

// ✅ Se admiten tanto “pepito()” como “llamar pepito”
funcion_llamada
    : LLAMAR ID ('(' argumentos? ')')? NUEVALINEA?
    | ID '(' argumentos? ')' NUEVALINEA?
    ;

argumentos
    : expresion (',' expresion)*
    ;

//============================
//  CONDICIONALES Y BUCLES
//============================
condicional
    : SI expresion ':' NUEVALINEA bloque
      (SINO ':' NUEVALINEA bloque)?
      FIN
    ;

repetir
    : REPETIR expresion VECES ':' NUEVALINEA bloque FIN
    ;

bloque
    : instruccion+
    ;

//============================
//  INSTRUCCIONES DE SALIDA
//============================
imprimir
    : (IMPRIMIR | MOSTRAR) expresion NUEVALINEA?
    ;

//============================
//  COMANDOS GRÁFICOS
//============================
comando_grafico
    : (MOVER ADELANTE expresion?
      | MOVER ATRAS expresion?
      | GIRAR (IZQUIERDA | DERECHA) expresion?
      | CAMBIAR COLOR expresion?
      | BAJAR LAPIZ
      | SUBIR LAPIZ)
      NUEVALINEA?
    ;

//============================
//  COMANDOS MUSICALES
//============================
comando_musical
    : TOCAR NOTA ID
      (DURANTE expresion SEGUNDOS)? NUEVALINEA?
    ;

//============================
//  POLINOMIOS
//============================

// Definir un polinomio simbólico
definir_polinomio
    : DEFINIR POLINOMIO ID '=' expresion NUEVALINEA?
    ;

// Mostrar el polinomio simbólicamente
mostrar_polinomio
    : MOSTRAR POLINOMIO ID NUEVALINEA?
    ;

// Graficar el polinomio en el panel
graficar_polinomio
    : GRAFICAR ID NUEVALINEA?
    ;

// Operar polinomios entre sí (preparado para SymPy)
operar_polinomio
    : (SUMAR | RESTAR | MULTIPLICAR | DIVIDIR)
      POLINOMIO ID (CON | POR) POLINOMIO ID NUEVALINEA?
    ;

//============================
//  EXPRESIONES
//============================
expresion
    : expresion op=(POR|DIV|MOD) expresion          #expMulDiv
    | expresion op=(MAS|MENOS) expresion            #expSumaResta
    | expresion op=(MENOR|MAYOR|MENORIGUAL|MAYORIGUAL|IGUAL|DIFERENTE) expresion  #expComparacion
    | expresion op=(Y|O) expresion                  #expLogica
    | expresion op=POTENCIA expresion               #expPotencia    
    | '(' expresion ')'                             #expParen
    | (MAS|MENOS) expresion                         #expSigno
    | NUMERO                                        #expNumero
    | TEXTO                                         #expTexto
    | VERDADERO                                     #expVerdadero
    | FALSO                                         #expFalso
    | ID                                            #expID
    | funcion_llamada                               #expFuncion
    ;

//============================
//  TOKENS Y LÉXICO
//============================

// --- Palabras clave generales ---
DEFINIR     : 'definir';
COMO        : 'como';
FUNCION     : 'funcion';
LLAMAR      : 'llamar';
FIN         : 'fin';
SI          : 'si';
SINO        : 'sino';
REPETIR     : 'repetir';
VECES       : 'veces';
IMPRIMIR    : 'imprimir';
MOSTRAR     : 'mostrar';

// --- Comandos gráficos ---
MOVER       : 'mover';
ADELANTE    : 'adelante';
ATRAS       : 'atras';
GIRAR       : 'girar';
IZQUIERDA   : 'izquierda';
DERECHA     : 'derecha';
CAMBIAR     : 'cambiar';
COLOR       : 'color';
BAJAR       : 'bajar';
SUBIR       : 'subir';
LAPIZ       : 'lapiz';

// --- Comandos musicales ---
TOCAR       : 'tocar';
NOTA        : 'nota';
DURANTE     : 'durante';
SEGUNDOS    : 'segundos';

// --- Polinomios ---
POLINOMIO   : 'polinomio';
GRAFICAR    : 'graficar';
SUMAR       : 'sumar';
RESTAR      : 'restar';
MULTIPLICAR : 'multiplicar';
DIVIDIR     : 'dividir';
CON         : 'con';

// --- Lógicos y valores ---
VERDADERO   : 'verdadero' | 'cierto';
FALSO       : 'falso';

// --- Operadores ---
MAS         : '+';
MENOS       : '-';
POR         : '*';
DIV         : '/';
MOD         : '%';
POTENCIA    : '**';
MENOR       : '<';
MAYOR       : '>';
MENORIGUAL  : '<=';
MAYORIGUAL  : '>=';
IGUAL       : '==' | 'es';
DIFERENTE   : '!=' | 'no es';
Y           : 'y';
O           : 'o';

// --- Literales y símbolos ---
NUMERO      : [0-9]+ ('.' [0-9]+)?;
TEXTO       : '"' (~["\\] | '\\' .)* '"' ;
ID          : [a-zA-ZáéíóúÁÉÍÓÚñÑ_][a-zA-Z0-9áéíóúÁÉÍÓÚñÑ_]* ;

// --- Formato ---
NUEVALINEA  : ('\r'? '\n')+ ;
ESPACIOS    : [ \t]+ -> skip ;
COMENTARIO  : '#' ~[\r\n]* -> skip ;
