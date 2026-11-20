import re

LEXICO = {}

def registrar(palabra, cat, gen=None, num=None, tiempo=None):
    LEXICO[palabra] = (cat, gen, num, tiempo)

for w, g, n in [('el','m','s'),('la','f','s'),('los','m','p'),('las','f','p'),
                ('un','m','s'),('una','f','s'),('unos','m','p'),('unas','f','p')]:
    registrar(w, 'Det', g, n)

for s, g in [('niño','m'),('niña','f'),('perro','m'),('gato','m'),('libro','m'),
             ('casa','f'),('mesa','f'),('profesor','m'),('ciudad','f'),('parque','m'),('manzana','f')]:
    registrar(s, 'N', g, 's')
    registrar(s + ('es' if s[-1] in 'dr' else 's'), 'N', g, 'p')

for s in ['bonit','rápid','pequeñ','nuev','viej','roj']:
    for suf, g, n in [('o','m','s'),('a','f','s'),('os','m','p'),('as','f','p')]:
        registrar(s + suf, 'Adj', g, n)

for s in ['grande','fácil']:
    registrar(s, 'Adj', None, 's')
    registrar(s + 's', 'Adj', None, 'p')

for v in [('come','comen','comió','comieron'),('compra','compran','compró','compraron'),
          ('lee','leen','leyó','leyeron'),('ve','ven','vio','vieron'),
          ('corre','corren','corrió','corrieron'),('duerme','duermen','durmió','durmieron')]:
    for w, n, t in zip(v, 'spsp', ['pres','pres','pret','pret']):
        registrar(w, 'V', None, n, t)

for w in ['rápidamente','ayer','hoy','mucho']:
    registrar(w, 'Adv')

for w in ['en','con','de','a','para','sobre']:
    registrar(w, 'Prep')

for w in ['ana','luis']:
    registrar(w, 'Nom', None, 's')

def analizar_lexico(texto):
    """
    Recibe texto fuente y retorna:
    - tokens: lista de tuplas (tipo, lexema, linea, columna)
    - errores: lista de strings con errores léxicos detectados
    """
    tokens = []
    errores = []
    for num_linea, linea in enumerate(texto.splitlines(), 1):
        for match in re.finditer(r'\S+', linea):
            raw = match.group()
            col = match.start() + 1
            limpio = raw.rstrip('.').lower()

            if not re.match(r'^[a-záéíóúñ]+$', limpio):
                errores.append(f"Error léxico [Línea {num_linea}, Col {col}]: carácter inválido en '{raw}'")
            elif limpio not in LEXICO:
                errores.append(f"Error léxico [Línea {num_linea}, Col {col}]: palabra fuera del vocabulario '{limpio}'")
            else:
                categoria = LEXICO[limpio][0]
                tokens.append((categoria, limpio, num_linea, col))
    return tokens, errores

if __name__ == '__main__':
    pruebas = [
        "El niño come una manzana.",
        "La niña bonita lee un libro nuevo.",
        "El perro123 corre en el parque",
        "Ana juega en la casa"
    ]
    for p in pruebas:
        print("=" * 55)
        print("Entrada:", p)
        toks, errs = analizar_lexico(p)
        print("Tokens :", toks)
        if errs:
            print("Errores:", errs)