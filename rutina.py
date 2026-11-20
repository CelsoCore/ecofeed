"""«Mi día»: la persona describe su jornada por bloques y la app busca el consumo evitable *dentro* de ella.
No recomienda estudiar o trabajar menos: esas horas se respetan. Solo busca equipos encendidos sin uso, brillo,
apps abiertas y cargadores. Los números salen de los mismos supuestos del simulador (valores referenciales)."""
import contenido as C
import logica as L

TIPOS = {
    "dormir": ("😴", "Dormir", "#3b3f8f"), "clases": ("🏫", "Clases", "#0e7490"), "estudio": ("📚", "Estudio", "#2563eb"),
    "trabajo": ("💼", "Trabajo", "#7c3aed"), "descanso": ("🍽️", "Comida o descanso", "#d97706"),
    "ocio": ("🎮", "Ocio", "#db2777"), "traslado": ("🚌", "Fuera de casa", "#64748b"),
}
ENFOCADOS = ("estudio", "trabajo", "clases")           # horas que se respetan
SIN_USO = ("descanso", "traslado", "dormir", "ocio", "clases")   # donde un equipo prendido suele sobrar
PSEUDO = {"cargadores": {"nombre": "Cargadores enchufados", "emoji": "🔌", "w_reposo": 2 * L.W_CARGADOR_VACIO}}

OCUPACIONES = {
    "nino": {"escolar": "Estudiante de primaria"},
    "joven": {"escolar": "Estudiante de secundaria", "universitario": "Estudiante de universidad o instituto",
              "estudia_trabaja": "Trabajo y estudio", "trabajo_fuera": "Trabajo fuera de casa"},
    "adulto": {"trabajo_fuera": "Trabajo fuera de casa", "teletrabajo": "Teletrabajo", "hogar": "Hogar o negocio propio",
               "estudia_trabaja": "Trabajo y estudio"},
    "mayor": {"hogar": "Hogar", "jubilado": "Jubilado o jubilada", "trabajo_fuera": "Trabajo o negocio propio"},
}

# (tipo, inicio, fin, aparatos que usa, aparatos que quedan encendidos sin uso)
PLANTILLAS = {
    "escolar": [("dormir", 21, 6, [], ["router"]), ("traslado", 6, 8, [], []), ("clases", 8, 13, [], []),
                ("descanso", 13, 15, ["tv"], ["tv"]), ("estudio", 15, 17, ["tab", "lap"], ["lap"]),
                ("ocio", 17, 20, ["consola", "tv"], ["tv"]), ("descanso", 20, 21, [], ["cargadores"])],
    "universitario": [("dormir", 23, 7, [], ["router", "cargadores"]), ("traslado", 7, 8, ["cel"], []),
                      ("clases", 8, 13, ["lap"], []), ("descanso", 13, 14, [], ["lap"]), ("estudio", 14, 18, ["lap"], []),
                      ("traslado", 18, 19, ["cel"], []), ("ocio", 19, 23, ["cel", "consola", "tv"], ["tv", "lap"])],
    "trabajo_fuera": [("dormir", 22, 6, [], ["router", "cargadores"]), ("traslado", 6, 8, ["cel"], ["tv"]),
                      ("trabajo", 8, 13, ["lap", "pc"], []), ("descanso", 13, 14, [], ["pc", "lap"]),
                      ("trabajo", 14, 18, ["lap", "pc"], []), ("traslado", 18, 19, ["cel"], []),
                      ("ocio", 19, 22, ["tv", "cel"], ["tv"])],
    "estudia_trabaja": [("dormir", 23, 6, [], ["router", "cargadores"]), ("trabajo", 8, 13, ["lap"], []),
                        ("descanso", 13, 14, [], ["lap"]), ("trabajo", 14, 18, ["lap"], []), ("clases", 18, 21, ["lap"], []),
                        ("estudio", 21, 23, ["lap"], ["tv"])],
    "teletrabajo": [("dormir", 23, 7, [], ["router", "cargadores"]), ("trabajo", 8, 13, ["lap", "pc"], []),
                    ("descanso", 13, 15, [], ["pc", "lap"]), ("trabajo", 15, 18, ["lap", "pc"], []),
                    ("ocio", 19, 23, ["tv", "cel"], ["tv", "pc"])],
    "hogar": [("dormir", 22, 6, [], ["router"]), ("descanso", 6, 9, ["tv"], ["tv"]), ("trabajo", 9, 13, ["cel"], []),
              ("descanso", 13, 15, ["tv"], ["tv"]), ("ocio", 15, 19, ["tv", "cel"], ["tv"]), ("descanso", 19, 22, ["tv"], ["tv"])],
    "jubilado": [("dormir", 21, 6, [], ["router"]), ("descanso", 6, 10, ["tv"], ["tv"]), ("ocio", 10, 13, ["tv", "cel"], []),
                 ("descanso", 13, 16, ["tv"], ["tv"]), ("ocio", 16, 21, ["tv", "cel"], ["tv"])],
}


def plantilla(ocupacion, dispositivos):
    """Bloques de ejemplo para empezar, usando solo los aparatos que la persona tiene."""
    tiene = set(dispositivos or C.DISPOSITIVOS) | set(PSEUDO)
    out = []
    for tipo, ini, fin, usa, quedan in PLANTILLAS.get(ocupacion, PLANTILLAS["hogar"]):
        out.append({"tipo": tipo, "ini": ini, "fin": fin, "usa": [d for d in usa if d in tiene],
                    "quedan": [d for d in quedan if d in tiene]})
    return out


def duracion(b):
    return (b["fin"] - b["ini"]) % 24


def _d(clave):
    return PSEUDO.get(clave) or C.DISPOSITIVOS[clave]


def _w_sobrante(clave):
    d = _d(clave)
    return d["w_reposo"] or d.get("w", 0)       # el router no tiene reposo: gasta su potencia


ART = {"lap": "la", "tab": "la", "pc": "el", "tv": "el", "consola": "la"}


def hora(h):
    return f"{h % 24:02d}:00"


def mapa_horas(bloques):
    """Para cada hora del día: (tipo o None, hay_desperdicio)."""
    mapa = [(None, False)] * 24
    for b in bloques:
        for k in range(duracion(b)):
            mapa[(b["ini"] + k) % 24] = (b["tipo"], bool(b["quedan"]) and b["tipo"] in SIN_USO)
    return mapa


def _texto(t, peque, tu, usted):
    return peque if t == "peque" else usted if t == "mayor" else tu


def analizar(bloques, t):
    """Resumen del día y consejos con hora, ordenados por ahorro anual (kWh)."""
    bloques = [b for b in bloques if duracion(b) > 0]
    horas = {}
    for b in bloques:
        horas[b["tipo"]] = horas.get(b["tipo"], 0) + duracion(b)
    enfocadas = sum(horas.get(k, 0) for k in ENFOCADOS)
    consejos = []
    for b in bloques:
        dur, rango = duracion(b), f"{hora(b['ini'])} a {hora(b['fin'])}"
        for clave in b["quedan"]:
            if b["tipo"] not in SIN_USO:
                continue                      # durante estudio o trabajo el equipo sí se usa
            D = _d(clave)
            kwh = _w_sobrante(clave) * dur * 365 / 1000
            if kwh <= 0:
                continue
            n, e = D["nombre"].lower(), D["emoji"]
            if clave == "router":
                tx = _texto(t, f"A las {hora(b['ini'])} apaga el router: de noche nadie lo usa.",
                            f"De {rango} el router sigue prendido sin que lo uses. Apágalo al acostarte.",
                            f"De {rango} el router sigue prendido sin que nadie lo use. Apáguelo al acostarse.")
            elif clave == "cargadores":
                tx = _texto(t, "Cuando termines de cargar, saca el cargador del enchufe.",
                            f"De {rango} los cargadores quedan enchufados sin carga. Desconéctalos al terminar.",
                            f"De {rango} los cargadores quedan enchufados sin carga. Desconéctelos al terminar.")
            else:
                tx = _texto(t, f"De {rango} tu {n} queda prendido sin usarse. Apágalo al terminar.",
                            f"De {rango} tu {n} queda encendido sin que lo uses. Suspéndelo o apágalo antes de irte.",
                            f"De {rango} su {n} queda encendido sin que lo use. Suspéndalo o apáguelo al terminar.")
            consejos.append({"emoji": e, "rango": rango, "texto": tx, "kwh": kwh, "tipo": "sobrante"})
        if b["tipo"] in ENFOCADOS and dur >= 3:
            for clave in b["usa"]:
                if clave in C.DISPOSITIVOS and clave in ("lap", "pc", "tab", "tv"):
                    D = C.DISPOSITIVOS[clave]
                    kwh = L.AHORRO_BRILLO * D["w"] * dur * 365 / 1000
                    a, nm = ART.get(clave, "el"), D["nombre"].lower()
                    tx = _texto(t, f"De {rango} (hora de {b['tipo']}) baja el brillo {'de la' if a == 'la' else 'del'} {nm} y descansa los ojos un ratito.",
                                f"En tu bloque de {b['tipo']} ({rango}) baja el brillo {'de la' if a == 'la' else 'del'} {nm}. Cada 20 minutos mira a lo lejos 20 segundos.",
                                f"En su bloque de {b['tipo']} ({rango}) baje el brillo {'de la' if a == 'la' else 'del'} {nm} y descanse la vista de vez en cuando.")
                    consejos.append({"emoji": "🔆", "rango": rango, "texto": tx, "kwh": kwh, "tipo": "brillo"})
                    break
            if any(c in ("lap", "pc") for c in b["usa"]):
                D = C.DISPOSITIVOS["lap" if "lap" in b["usa"] else "pc"]
                kwh = L.AHORRO_CERRAR_APPS * D["w"] * dur * 365 / 1000
                tx = _texto(t, "Cierra lo que no uses en la compu.",
                            f"En {rango} cierra pestañas y programas que no usas: {'la laptop' if D['nombre'] == 'Laptop' else 'la PC'} trabaja menos y gasta menos.",
                            f"En {rango} cierre las ventanas y programas que no use: el equipo gasta menos.")
                consejos.append({"emoji": "🧹", "rango": rango, "texto": tx, "kwh": kwh, "tipo": "apps"})
        if b["tipo"] == "ocio" and "consola" in b["usa"] and dur >= 2:
            kwh = L.AHORRO_FPS * C.DISPOSITIVOS["consola"]["w"] * dur * 365 / 1000
            tx = _texto(t, "Cuando juegues, baja un poco la calidad del juego.",
                        f"En {rango} limita los FPS o baja los gráficos: el juego se ve casi igual y la consola gasta menos.",
                        f"En {rango} baje la calidad de los gráficos: gasta menos energía.")
            consejos.append({"emoji": "🎮", "rango": rango, "texto": tx, "kwh": kwh, "tipo": "fps"})
    consejos.sort(key=lambda c: -c["kwh"])
    total = sum(c["kwh"] for c in consejos)
    sobrante = sum(c["kwh"] for c in consejos if c["tipo"] == "sobrante")
    return {"horas": horas, "enfocadas": enfocadas, "consejos": consejos, "kwh_anio": total, "kwh_sobrante_anio": sobrante,
            "soles": L.soles(total), "co2": L.co2_kg(total), "cargas": total / (L.CELULAR_WH / 1000)}
