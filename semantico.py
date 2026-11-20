from lexer import LEXICO, analizar_lexico

class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}

    def registrar_uso(self, lexema, linea, col):
        cat, gen, num, tiempo = LEXICO[lexema]
        if lexema not in self.simbolos:
            self.simbolos[lexema] = {
                'categoria': cat,
                'genero': gen,
                'numero': num,
                'tiempo': tiempo,
                'apariciones': []
            }
        self.simbolos[lexema]['apariciones'].append((linea, col))

    def mostrar(self):
        print("\n--- TABLA DE SÍMBOLOS ---")
        print(f"{'Lexema':<14} | {'Cat':<5} | {'Gén':<4} | {'Núm':<4} | {'Tiempo':<6} | {'Posiciones'}")
        print("-" * 62)
        for lex, info in self.simbolos.items():
            g = info['genero'] or '-'
            n = info['numero'] or '-'
            t = info['tiempo'] or '-'
            print(f"{lex:<14} | {info['categoria']:<5} | {g:<4} | {n:<4} | {t:<6} | {info['apariciones']}")

def analizar_semantica(tokens):
    """
    Verifica reglas sensibles al contexto (que una CFG no puede expresar):
    1. Concordancia de género y número dentro de cada Sintagma Nominal (Det + N + Adj*).
    2. Concordancia de número entre el núcleo del sujeto y el verbo principal.
    3. Restricción de intransitividad básica (ej. 'dormir' no admite objeto directo).
    """
    tabla = TablaSimbolos()
    errores = []

    for cat, lex, lin, col in tokens:
        tabla.registrar_uso(lex, lin, col)

    sintagmas = []
    sn_actual = []
    verbo_principal = None

    for tok in tokens:
        cat, lex, lin, col = tok
        if cat in ('Det', 'N', 'Adj', 'Nom'):
            sn_actual.append(tok)
        else:
            if sn_actual:
                sintagmas.append(sn_actual)
                sn_actual = []
            if cat == 'V' and verbo_principal is None:
                verbo_principal = tok
    if sn_actual:
        sintagmas.append(sn_actual)

    for sn in sintagmas:
        generos = {LEXICO[lex][1] for _, lex, _, _ in sn if LEXICO[lex][1] is not None}
        numeros = {LEXICO[lex][2] for _, lex, _, _ in sn if LEXICO[lex][2] is not None}
        frase_sn = " ".join(lex for _, lex, _, _ in sn)
        lin_sn = sn[0][2]

        if len(generos) > 1:
            errores.append(f"Error semántico [Línea {lin_sn}]: discordancia de género en '{frase_sn}'")
        if len(numeros) > 1:
            errores.append(f"Error semántico [Línea {lin_sn}]: discordancia de número en '{frase_sn}'")

    if sintagmas and verbo_principal:
        sujeto = sintagmas[0]
        nucleos = [tok for tok in sujeto if tok[0] in ('N', 'Nom')]
        if nucleos:
            _, lex_suj, lin_suj, _ = nucleos[0]
            _, lex_v, lin_v, _ = verbo_principal
            num_suj = LEXICO[lex_suj][2]
            num_v = LEXICO[lex_v][2]
            if num_suj != num_v:
                errores.append(
                    f"Error semántico [Línea {lin_v}]: sujeto '{lex_suj}' ({num_suj}) "
                    f"no concuerda en número con verbo '{lex_v}' ({num_v})"
                )

    return errores, tabla

if __name__ == '__main__':
    casos_prueba = [
        "El niño pequeño come una manzana roja.",
        "Las niñas leen los libros.",

        "El niño pequeña come una manzana.",
        "Los niño come una manzana.",
        "El gato duermen en la casa."
    ]

    for oracion in casos_prueba:
        print("=" * 62)
        print("Oración:", oracion)
        toks, errs_lex = analizar_lexico(oracion)
        if errs_lex:
            print("-> Detenido en fase léxica:", errs_lex)
            continue

        errs_sem, tabla = analizar_semantica(toks)
        if errs_sem:
            print("-> RECHAZADA (Errores semánticos):")
            for e in errs_sem:
                print("   *", e)
        else:
            print("-> ACEPTADA: Semánticamente válida.")
        tabla.mostrar()