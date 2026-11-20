# Avance Proyecto TLP02-2026: Analizador Léxico y Semántico

Implementación en Python de las fases de **Análisis Léxico** (`lexer.py`) y **Análisis Semántico** (`semantico.py`) para un subconjunto controlado del español, explorando los límites entre lenguajes regulares, libres de contexto y sensibles al contexto en la Jerarquía de Chomsky.

## 1. Especificación Léxica (`lexer.py`)

El analizador léxico transforma el texto de entrada en una secuencia de tokens estructurados como tuplas `(tipo, lexema, línea, columna)` mediante expresiones regulares y un diccionario morfológico:

| Categoría (Token) | Expresión Regular / Patrón | Ejemplos |
| :--- | :--- | :--- |
| `Det` (Determinante) | `^(el\|la\|los\|las\|un\|una\|unos\|unas)$` | `el`, `una`, `los` |
| `N` (Sustantivo) | `^[a-záéíóúñ]+$` (en lexicón nominal) | `niño`, `manzana`, `libros` |
| `Adj` (Adjetivo) | `^[a-záéíóúñ]+$` (en lexicón adjetival) | `pequeño`, `roja`, `grandes` |
| `V` (Verbo) | `^[a-záéíóúñ]+$` (flexión presente/pretérito) | `come`, `leyeron`, `duerme` |
| `Adv` (Adverbio) | `^(rápidamente\|ayer\|hoy\|mucho)$` | `rápidamente`, `hoy` |
| `Prep` (Preposición) | `^(en\|con\|de\|a\|para\|sobre)$` | `en`, `para`, `sobre` |
| `Nom` (Nombre propio) | `^(ana\|luis)$` | `ana`, `luis` |

**Manejo de errores léxicos:** Reporta línea y columna exacta ante caracteres no alfabéticos (`perro123`, símbolos inválidos) o lexemas fuera del vocabulario controlado.

## 2. Analizador Semántico y Tabla de Símbolos (`semantico.py`)

El módulo semántico construye una **Tabla de Símbolos** registrando los atributos morfológicos (`categoría`, `género`, `número`, `tiempo` y posiciones de aparición) de cada token y ejecuta verificaciones sensibles al contexto:

1. **Concordancia nominal interna:** Verifica que `Det`, `N` y `Adj` dentro de un mismo sintagma nominal compartan género (`m`/`f`) y número (`s`/`p`).
2. **Concordancia sujeto-verbo:** Verifica que el número gramatical del núcleo del sujeto coincida con la flexión de número del verbo principal.

## 3. Reflexión Teórica: ¿Por qué estas verificaciones exceden una CFG?

Según la **Jerarquía de Chomsky**, una Gramática Libre de Contexto (Tipo 2) modela relaciones jerárquicas locales mediante un autómata de pila, pero carece de memoria transversal para imponer restricciones de igualdad de atributos a distancia sin duplicar exponencialmente sus reglas de producción.

* Validar que un determinante, un sustantivo y múltiples adjetivos compartan simultáneamente género y número, o que el núcleo del sujeto concuerde con un verbo separado por modificadores, corresponde a propiedades **sensibles al contexto (Tipo 1)**.
* Delegar estas reglas al analizador semántico mediante una **Tabla de Símbolos** mantiene la gramática compacta y permite emitir mensajes de error precisos con línea y causa.

## 4. Ejecución de Pruebas

```bash
python3 lexer.py
python3 semantico.py
