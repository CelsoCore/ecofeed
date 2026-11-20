"""Lógica de EcoFeed: usuarios, tono por edad y grado, consumo, misiones y simulador RAEE.

No usa Streamlit, así que se puede probar con Python normal.
"""
import random
import threading
import csv
import hashlib
import hmac
import io
import json
import re
import secrets
from datetime import date, datetime, timedelta
from pathlib import Path

import actividades as A
import contenido as C
import tips as T

RUTA_DATOS = Path(__file__).parent / "datos" / "usuarios.json"

# Supuestos del modelo (valores de referencia, ajústalos en tu informe)
HORAS_REPOSO_EVITABLE = 2.0   # horas al día que un equipo queda encendido sin usar si nunca lo apagas
W_CARGADOR_VACIO = 0.5        # vatios que gasta un cargador enchufado sin carga
AHORRO_BRILLO = 0.10          # fracción del consumo en uso que se ahorra con brillo bajo
AHORRO_CERRAR_APPS = 0.05     # fracción del consumo de laptop y PC que se ahorra cerrando apps
FACTOR_CO2 = 0.20             # kg de CO₂ por kWh (valor referencial, cámbialo por la fuente que cites)
PRECIO_KWH = 0.75             # soles por kWh (valor referencial, ajústalo con tu recibo de luz)
CONSOLA_W = 100               # vatios de una consola jugando (para la analogía de videojuegos)
CELULAR_WH = 15               # Wh de una carga completa de celular
HORAS_ROUTER_NOCHE = 8        # horas de la noche en que nadie usa el router
AHORRO_FPS = 0.15             # fracción del consumo de juego que se ahorra limitando FPS
XP_MISION = {1: 15, 2: 25, 3: 40}   # XP base de una misión según su esfuerzo
XP_DIARIO = 5                 # XP por cumplir el reto del día
XP_REGISTRO = 5               # XP por cada día guardado


def fmt(x, decimales=1):
    """Formato con coma decimal: fmt(3.456, 1) -> '3,5'."""
    return f"{x:.{decimales}f}".replace(".", ",")


# ---------------------------------------------------------------- usuarios
# Streamlit atiende a cada persona en un hilo distinto. Este candado evita que dos guardados simultáneos
# lean el mismo archivo y uno pise al otro (leer, cambiar y escribir debe ocurrir de una sola vez).
_CANDADO = threading.RLock()


def _con_candado(f):
    import functools

    @functools.wraps(f)
    def envoltura(*a, **k):
        with _CANDADO:
            return f(*a, **k)
    return envoltura


_RESTAURADO = {"intentado": False}


def _cargar_todo():
    if not RUTA_DATOS.exists() and not _RESTAURADO["intentado"]:
        _RESTAURADO["intentado"] = True        # una sola vez por arranque
        try:
            import respaldo_nube
            respaldo_nube.restaurar(RUTA_DATOS)
        except Exception:
            pass
    try:
        return json.loads(RUTA_DATOS.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _guardar_todo(datos):
    RUTA_DATOS.parent.mkdir(parents=True, exist_ok=True)
    tmp = RUTA_DATOS.with_suffix(".tmp")
    tmp.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    if RUTA_DATOS.exists():                    # copia de seguridad local de la versión anterior
        try:
            RUTA_DATOS.with_suffix(".bak").write_bytes(RUTA_DATOS.read_bytes())
        except OSError:
            pass
    tmp.replace(RUTA_DATOS)
    try:
        import respaldo_nube
        respaldo_nube.programar(RUTA_DATOS)    # sube la copia a GitHub unos segundos después
    except Exception:
        pass


def _hash(clave, sal):
    return hashlib.pbkdf2_hmac("sha256", clave.encode("utf-8"), bytes.fromhex(sal), 200_000).hex()


def perfil_vacio():
    return {"dispositivos": [], "horas": {}, "habitos": {}, "barreras": [], "onboarded": False}


def normalizar(rec):
    """Completa los campos que faltan en cuentas creadas con versiones anteriores."""
    rec.setdefault("grado", C.GRADO_POR_EDAD[rec["edad"]])
    rec.setdefault("likes", [])
    rec.setdefault("guardados", [])
    rec.setdefault("retos", {})
    rec.setdefault("registros", {})
    rec.setdefault("actividades", {})
    return rec


@_con_candado
def registrar_usuario(usuario, clave, edad, grado):
    usuario = usuario.strip().lower()
    if len(usuario) < 3:
        return None, "El usuario debe tener al menos 3 caracteres."
    if len(clave) < 4:
        return None, "La contraseña debe tener al menos 4 caracteres."
    if edad not in C.EDADES or grado not in C.GRADOS:
        return None, "Elige tu grupo de edad y tu nivel de estudios."
    cfg = config_admin()
    if cfg and usuario == cfg[0]:
        return None, "Ese usuario no está disponible."
    datos = _cargar_todo()
    if usuario in datos:
        return None, "Ese usuario ya existe. Inicia sesión."
    sal = secrets.token_hex(16)
    datos[usuario] = {
        "sal": sal, "hash": _hash(clave, sal), "edad": edad, "grado": grado,
        "perfil": perfil_vacio(), "registros": {}, "likes": [], "guardados": [], "retos": {},
        "actividades": {}, "creado": datetime.now().isoformat(timespec="seconds"),
    }
    _guardar_todo(datos)
    return datos[usuario], ""


def iniciar_sesion(usuario, clave):
    usuario = usuario.strip().lower()
    rec = _cargar_todo().get(usuario)
    if rec is None or not hmac.compare_digest(rec["hash"], _hash(clave, rec["sal"])):
        return None, "Usuario o contraseña incorrectos."
    rec = normalizar(rec)
    rec["ultimo_acceso"] = datetime.now().isoformat(timespec="seconds")
    guardar_usuario(usuario, rec)
    return rec, ""


@_con_candado
def guardar_usuario(usuario, rec):
    datos = _cargar_todo()
    clave = usuario.strip().lower()
    previa = datos.get(clave, {}).get("sesion")
    if previa and "sesion" not in rec:
        rec["sesion"] = previa            # la copia en pantalla no conoce el código de sesión: no lo borres
    datos[clave] = rec
    _guardar_todo(datos)


# ---------------------------------------------------------------- sesión que sobrevive a recargar la página
HORAS_SESION = 24


def _hash_token(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


@_con_candado
def crear_sesion(usuario):
    """Devuelve un código al azar para el enlace. En el archivo solo se guarda su huella y cuándo vence."""
    usuario = usuario.strip().lower()
    datos = _cargar_todo()
    if usuario not in datos:
        return None
    token = secrets.token_urlsafe(24)
    datos[usuario]["sesion"] = {"huella": _hash_token(token),
                                "vence": (datetime.now() + timedelta(hours=HORAS_SESION)).isoformat(timespec="seconds")}
    _guardar_todo(datos)
    return token


def validar_sesion(usuario, token):
    rec = _cargar_todo().get((usuario or "").strip().lower())
    ses = (rec or {}).get("sesion")
    if not ses or not token:
        return None
    if datetime.fromisoformat(ses["vence"]) < datetime.now() or not hmac.compare_digest(ses["huella"], _hash_token(token)):
        return None
    return normalizar(rec)


@_con_candado
def cerrar_sesion(usuario):
    datos = _cargar_todo()
    if usuario in datos and datos[usuario].pop("sesion", None) is not None:
        _guardar_todo(datos)


# ---------------------------------------------------------------- tono según edad y grado
def tono(rec):
    """peque (primaria), gamer (secundaria), tecnico (superior o adulto) o mayor."""
    edad = rec["edad"]
    grado = rec.get("grado") or C.GRADO_POR_EDAD[edad]
    if edad == "mayor":
        return "mayor"
    if edad == "nino" or (edad == "joven" and grado == "primaria"):
        return "peque"
    if edad == "joven" and grado == "secundaria":
        return "gamer"
    return "tecnico"


def pregunta_habito(clave, t):
    return C.HABITOS[clave]["preguntas"][t]


def titulo_habito(clave, t):
    h = C.HABITOS[clave]
    return h["titulo_juego"] if t in ("peque", "gamer") else h["titulo"]


def texto_barrera(clave, t):
    return C.BARRERAS[clave]["textos"][t]


def titulo_para(tip, t):
    return tip["titulo"]


def texto_para(tip, t):
    return tip["textos"][t]


def reto_para(tip, t):
    return tip["reto"]


def partir(texto):
    """Primera oración (la acción) y el resto (el porqué)."""
    partes = re.split(r"(?<=[.!?])\s+", texto.strip(), maxsplit=1)
    return partes[0], (partes[1] if len(partes) > 1 else "")


def horas_de(perfil, d):
    """Horas diarias de uso: 24 para lo que siempre está encendido (router)."""
    if d in C.DISPOSITIVOS_SIEMPRE_ENCENDIDOS:
        return 24.0
    return perfil["horas"].get(d, 0)


# ---------------------------------------------------------------- índice de prácticas (como en el informe)
def media_practicas(perfil):
    vals = [perfil["habitos"][k] for k in C.HABITOS if k in perfil["habitos"]]
    return sum(vals) / len(vals) if vals else None


def nivel_baremo(media):
    for limite, nombre in C.BAREMO:
        if media <= limite:
            return nombre
    return C.BAREMO[-1][1]


def nombre_nivel(media, t):
    """Nombre del nivel: baremo del informe o rango de juego según el tono."""
    nivel = nivel_baremo(media)
    if t in ("peque", "gamer"):
        return C.RANGOS_JUEGO[[n for _, n in C.BAREMO].index(nivel)]
    return nivel


def indice_verde(media):
    """Convierte la media (1 a 5) en un puntaje de 0 a 100."""
    return round((media - 1) / 4 * 100)


def texto_resultado(perfil, t):
    media = media_practicas(perfil)
    dif = media - C.MEDIA_ESTUDIO_PRACTICAS
    return C.RESULTADO[t].format(
        idx=indice_verde(media), media=fmt(media, 2), nivel=nombre_nivel(media, t),
        est=fmt(C.MEDIA_ESTUDIO_PRACTICAS, 2), dif=f"{dif:+.2f}".replace(".", ","),
    )


def feedback_habito(clave, valor, t):
    est = C.HABITOS[clave]["media_estudio"]
    rango = "alto" if valor >= 4 else "medio" if valor == 3 else "bajo"
    return C.FEEDBACK[t][rango].format(
        titulo=titulo_habito(clave, t), valor=valor, est=fmt(est, 2),
        dif=f"{valor - est:+.2f}".replace(".", ","),
    )


# ---------------------------------------------------------------- consumo
def _falta(perfil, habito):
    """0 si el hábito se cumple siempre (5), 1 si nunca (1)."""
    return (5 - perfil["habitos"].get(habito, 3)) / 4


def _uso_kwh_dia(perfil, d):
    return horas_de(perfil, d) * C.DISPOSITIVOS[d]["w"] / 1000


def consumo_dia(perfil):
    """kWh por día por dispositivo, más 'reposo' (equipos encendidos sin uso y cargadores sin carga)."""
    res = {d: _uso_kwh_dia(perfil, d) for d in perfil["dispositivos"]}
    reposo = 0.0
    for d in perfil["dispositivos"]:
        info = C.DISPOSITIVOS[d]
        if info["apagable"]:
            reposo += HORAS_REPOSO_EVITABLE * _falta(perfil, "apagar") * info["w_reposo"] / 1000
    n_carga = sum(1 for d in perfil["dispositivos"] if C.DISPOSITIVOS[d]["carga"])
    reposo += n_carga * W_CARGADOR_VACIO * 24 / 1000 * _falta(perfil, "cargadores")
    res["reposo"] = reposo
    return res


def co2_kg(kwh):
    return kwh * FACTOR_CO2


def soles(kwh):
    return kwh * PRECIO_KWH


def calc(kind, **p):
    """Calculadoras de las tarjetas interactivas. Devuelve kWh/año, soles/año y kg CO₂/año."""
    if kind == "reposo":
        kwh = p["w"] * p["horas"] * 365 / 1000
    elif kind == "cargadores":
        kwh = p["n"] * W_CARGADOR_VACIO * 24 * 365 / 1000
    elif kind == "brillo":
        kwh = AHORRO_BRILLO * p["w"] * p["horas"] * 365 / 1000
    else:
        kwh = 0.0
    return {"kwh": kwh, "soles": soles(kwh), "co2": co2_kg(kwh)}


def ahorro_anual(tip_id, perfil):
    """Ahorro estimado en kWh al año si la persona cumple la misión; None si no se puede estimar."""
    devs = perfil["dispositivos"]
    D = C.DISPOSITIVOS
    apagables = [d for d in devs if D[d]["apagable"]]
    n_carga = sum(1 for d in devs if D[d]["carga"])
    uso = {d: _uso_kwh_dia(perfil, d) for d in devs}
    reposo = lambda lista: sum(HORAS_REPOSO_EVITABLE * D[d]["w_reposo"] * 365 / 1000 for d in lista)
    if tip_id in ("apagar_equipos", "suspension_automatica"):
        lista = [d for d in apagables if d in ("lap", "pc", "tab")] if tip_id == "apagar_equipos" else [d for d in apagables if d in ("lap", "pc")]
        return reposo(lista) * _falta(perfil, "apagar")
    if tip_id == "consola_apagado":
        return reposo([d for d in apagables if d == "consola"]) * _falta(perfil, "apagar") if "consola" in devs else None
    if tip_id == "brillo":
        return AHORRO_BRILLO * sum(uso.get(d, 0) for d in ("cel", "tab", "lap")) * 365 * _falta(perfil, "ahorro")
    if tip_id == "tv_ahorro":
        return AHORRO_BRILLO * uso.get("tv", 0) * 365 * _falta(perfil, "ahorro") if "tv" in devs else None
    if tip_id in ("desconectar_cargadores", "regleta_interruptor"):
        return n_carga * W_CARGADOR_VACIO * 24 * 365 / 1000 * _falta(perfil, "cargadores")
    if tip_id == "cerrar_apps":
        return AHORRO_CERRAR_APPS * sum(uso.get(d, 0) for d in ("lap", "pc")) * 365
    if tip_id == "router_noche":
        return HORAS_ROUTER_NOCHE * D["router"]["w"] * 365 / 1000 if "router" in devs else None
    if tip_id == "graficos_fps":
        return AHORRO_FPS * sum(uso.get(d, 0) for d in ("pc", "consola")) * 365
    return None


def impacto_mision(tip_id, perfil):
    """Impacto anual estimado de una misión: kWh, CO₂ (kg), soles, residuo evitado (kg) y CO₂ de fabricación evitado (kg)."""
    kwh = ahorro_anual(tip_id, perfil) or 0.0
    residuo = fab = 0.0
    if tip_id in T.VIDA_EXTRA:
        devs, extra = T.VIDA_EXTRA[tip_id]
        for d in devs:
            if d in perfil["dispositivos"]:
                i = C.DISPOSITIVOS[d]
                residuo += i["peso_kg"] / i["vida_anios"] - i["peso_kg"] / (i["vida_anios"] + extra)
                fab += i["co2_fab_kg"] / i["vida_anios"] - i["co2_fab_kg"] / (i["vida_anios"] + extra)
    return {"kwh": kwh, "co2": co2_kg(kwh) + fab, "soles": soles(kwh), "residuo": residuo, "fab": fab}


# ---------------------------------------------------------------- recomendaciones y feed
def recomendar(perfil, t):
    """Recomendaciones ordenadas de más a menos importantes para esta persona y este tono."""
    devs = perfil["dispositivos"]
    lista = []
    for tip in T.TIPS:
        if t not in tip["tonos"]:
            continue
        tip_devs = tip["dispositivos"]
        comunes = [d for d in tip_devs if d in devs]
        if tip_devs and not comunes:
            continue
        puntaje = 1.0
        if tip["habito"]:
            puntaje += 5 - perfil["habitos"].get(tip["habito"], 3)
        if tip["barrera"] in perfil["barreras"]:
            puntaje += 2
        if comunes:
            puntaje += min(max(horas_de(perfil, d) for d in comunes), 8) / 8
        texto = texto_para(tip, t)
        corto, largo = partir(texto)
        lista.append({
            "id": tip["id"], "tip": tip, "titulo": titulo_para(tip, t), "texto": texto,
            "corto": corto, "largo": largo, "puntaje": puntaje, "ahorro": ahorro_anual(tip["id"], perfil),
        })
    lista.sort(key=lambda x: (-x["puntaje"], x["id"]))
    return lista


def _intercalar_tipos(items):
    """Reparte las actividades por tipo para que dos seguidas no sean iguales."""
    grupos = {}
    for a in items:
        grupos.setdefault(a["tipo"], []).append(a)
    orden = []
    while any(grupos.values()):
        for tipo in list(grupos):
            if grupos[tipo]:
                orden.append(grupos[tipo].pop(0))
    return orden


def armar_feed(rec, t, modo="normal", semilla=0):
    """Lista de (tipo, id) que mezcla recomendaciones y actividades.

    Primero lo pendiente (una recomendación, una actividad, ...) y al final lo ya resuelto.
    El orden se calcula una vez por sesión y no cambia mientras la persona avanza.
    """
    perfil = rec["perfil"]
    hechos = {tid for tid, ok in rec["retos"].items() if ok}
    resueltas = set(rec.get("actividades", {}))
    tips_ord = recomendar(perfil, t)
    if modo == "repaso":
        # solo lo que falló, más las recomendaciones que aún no aceptó como reto
        falladas = [("act", a["id"]) for a in A.ACTIVIDADES if rec["actividades"].get(a["id"], {}).get("ok") is False]
        tips_p = [("tip", r["id"]) for r in tips_ord if r["id"] not in hechos][:6]
        return falladas + tips_p
    if modo == "mezcla":
        todo = [("tip", r["id"]) for r in tips_ord] + [("act", a["id"]) for a in A.ACTIVIDADES]
        random.Random(semilla).shuffle(todo)
        # lo no resuelto primero, para que cada ronda traiga algo distinto
        nuevos = [x for x in todo if (x[0] == "tip" and x[1] not in hechos) or (x[0] == "act" and x[1] not in resueltas)]
        resto = [x for x in todo if x not in nuevos]
        return nuevos + resto
    tips_pend = [r["id"] for r in tips_ord if r["id"] not in hechos]
    tips_hechos = [r["id"] for r in tips_ord if r["id"] in hechos]
    acts_pend = [a["id"] for a in _intercalar_tipos([a for a in A.ACTIVIDADES if a["id"] not in resueltas])]
    acts_hechas = [a["id"] for a in A.ACTIVIDADES if a["id"] in resueltas]
    feed = []
    i = j = 0
    while i < len(tips_pend) or j < len(acts_pend):
        if i < len(tips_pend):
            feed.append(("tip", tips_pend[i])); i += 1
        if j < len(acts_pend):
            feed.append(("act", acts_pend[j])); j += 1
        if i < len(tips_pend) and (len(feed) % 3 == 2):
            feed.append(("tip", tips_pend[i])); i += 1
    feed += [("act", x) for x in acts_hechas] + [("tip", x) for x in tips_hechos]
    return feed


# ---------------------------------------------------------------- actividades
def registrar_actividad(rec, act_id, ok, resp=None):
    """Guarda el resultado de una actividad. Devuelve True si era nueva (solo cuenta la primera vez)."""
    if act_id in rec["actividades"]:
        return False
    rec["actividades"][act_id] = {"ok": bool(ok), "resp": resp, "ts": datetime.now().isoformat(timespec="seconds")}
    return True


def resumen_actividades(rec):
    acts = rec.get("actividades", {})
    return {"resueltas": len(acts), "aciertos": sum(1 for v in acts.values() if v["ok"]),
            "total": len(A.ACTIVIDADES)}


# ---------------------------------------------------------------- misiones, XP, racha e insignias
def xp_mision(tip_id, perfil):
    tip = T.TIPS_POR_ID[tip_id]
    return XP_MISION[tip["esfuerzo"]] + min(round(ahorro_anual(tip_id, perfil) or 0) // 5, 20)


def progreso(rec):
    """Misiones aceptadas y cumplidas, XP y nivel de juego."""
    perfil = rec["perfil"]
    hechas = [tid for tid, ok in rec["retos"].items() if ok and tid in T.TIPS_POR_ID]
    acts = rec.get("actividades", {})
    xp = sum(xp_mision(tid, perfil) for tid in hechas)
    xp += sum(C.XP_ACTIVIDAD_OK if v["ok"] else C.XP_ACTIVIDAD_INTENTO for v in acts.values())
    xp += XP_REGISTRO * len(rec["registros"])
    xp += XP_DIARIO * len(rec.get("diario", {}))
    nivel = xp // 100 + 1
    return {
        "aceptadas": len(rec["retos"]), "hechas": hechas, "xp": xp, "nivel": nivel,
        "xp_nivel": xp % 100, "titulo": C.NIVELES_JUEGO[min(nivel - 1, len(C.NIVELES_JUEGO) - 1)],
        "avatar": C.AVATAR_NIVEL[min(nivel - 1, len(C.AVATAR_NIVEL) - 1)],
    }


def racha(rec, hoy=None):
    """Días seguidos con registro, contando hacia atrás desde hoy (o desde ayer si hoy aún no se guardó)."""
    hoy = hoy or date.today()
    dias = set(rec["registros"])
    d = hoy if hoy.isoformat() in dias else hoy - timedelta(days=1)
    n = 0
    while d.isoformat() in dias:
        n += 1
        d -= timedelta(days=1)
    return n


def insignias(rec, t):
    prog = progreso(rec)
    res_act = resumen_actividades(rec)
    res = []
    for b in C.BADGES:
        tipo, valor = b["cond"]
        if tipo == "hechas":
            ok = len(prog["hechas"]) >= valor
        elif tipo == "aceptadas":
            ok = prog["aceptadas"] >= valor
        elif tipo == "alguna":
            ok = any(i in prog["hechas"] for i in valor)
        elif tipo == "actividades":
            ok = res_act["resueltas"] >= valor
        elif tipo == "aciertos":
            ok = res_act["aciertos"] >= valor
        else:  # registros
            ok = len(rec["registros"]) >= valor
        res.append({"emoji": b["emoji"], "nombre": b["nombres"][t], "ok": ok})
    return res


# ---------------------------------------------------------------- registro semanal y prueba de guardado
def horas_completas(perfil, horas):
    """Horas del día para guardar: lo que la persona anotó más el router (24 h)."""
    res = {d: horas.get(d, 0) for d in perfil["dispositivos"]}
    for d in C.DISPOSITIVOS_SIEMPRE_ENCENDIDOS:
        if d in res:
            res[d] = 24.0
    return res


def kwh_registro(perfil, horas_dia):
    """kWh de un día guardado (uso de cada dispositivo)."""
    return sum(h * C.DISPOSITIVOS[d]["w"] / 1000 for d, h in horas_dia.items() if d in C.DISPOSITIVOS)


def guardar_dia(usuario, rec, horas, hoy=None):
    """Guarda las horas de hoy en el archivo y devuelve la verificación leyendo el archivo de nuevo."""
    hoy = hoy or date.today()
    rec["registros"][hoy.isoformat()] = horas_completas(rec["perfil"], horas)
    guardar_usuario(usuario, rec)
    return verificar_guardado(usuario, rec)


def verificar_guardado(usuario, rec):
    """Compara lo que hay en pantalla con lo que hay realmente en el archivo del disco."""
    usuario = usuario.strip().lower()
    en_disco = _cargar_todo().get(usuario, {})
    reg_disco = en_disco.get("registros", {})
    existe = RUTA_DATOS.exists()
    stat = RUTA_DATOS.stat() if existe else None
    return {
        "ruta": str(RUTA_DATOS),
        "existe": existe,
        "bytes": stat.st_size if stat else 0,
        "modificado": datetime.fromtimestamp(stat.st_mtime).strftime("%d/%m/%Y %H:%M:%S") if stat else "—",
        "dias_en_disco": len(reg_disco),
        "dias_en_pantalla": len(rec["registros"]),
        "coincide": reg_disco == rec["registros"] and en_disco.get("actividades", {}) == rec.get("actividades", {}),
        "ultimo_dia": max(reg_disco) if reg_disco else None,
        "actividades_en_disco": len(en_disco.get("actividades", {})),
    }


def semana(rec, hoy=None):
    """Los últimos 7 días: [(fecha, etiqueta, guardado, kWh)]."""
    hoy = hoy or date.today()
    dias_es = ["L", "M", "X", "J", "V", "S", "D"]
    res = []
    for k in range(6, -1, -1):
        d = hoy - timedelta(days=k)
        reg = rec["registros"].get(d.isoformat())
        res.append((d, dias_es[d.weekday()], reg is not None, kwh_registro(rec["perfil"], reg) if reg else 0.0))
    return res


def historial_filas(rec):
    """Una fila por día guardado, ordenada por fecha."""
    filas = []
    for iso in sorted(rec["registros"]):
        h = rec["registros"][iso]
        kwh = kwh_registro(rec["perfil"], h)
        fila = {"fecha": iso}
        for d in C.DISPOSITIVOS:
            fila[f"horas_{d}"] = h.get(d, "")
        fila.update({"kwh_dia": round(kwh, 3), "soles_dia": round(soles(kwh), 2), "co2_kg_dia": round(co2_kg(kwh), 3)})
        filas.append(fila)
    return filas


def csv_registros(rec):
    """CSV con los registros diarios (con BOM para que Excel lo abra bien)."""
    filas = historial_filas(rec)
    campos = ["fecha"] + [f"horas_{d}" for d in C.DISPOSITIVOS] + ["kwh_dia", "soles_dia", "co2_kg_dia"]
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=campos, delimiter=";")
    w.writeheader()
    w.writerows(filas)
    return "﻿" + buf.getvalue()


def json_respaldo(rec, usuario):
    """Copia de los datos de la persona sin contraseña."""
    copia = {k: v for k, v in rec.items() if k not in ("sal", "hash")}
    copia["usuario"] = usuario
    return json.dumps(copia, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- simulador RAEE
def salud_dispositivo(d, perfil):
    """0 a 100 según qué tan bien se cuidan los hábitos que protegen a ese dispositivo."""
    vals = [perfil["habitos"].get(h, 3) for h in C.HABITOS_POR_DISPOSITIVO[d]]
    return round(sum(vals) / len(vals) / 5 * 100)


def simulador(perfil, extra_anios=1.0):
    """Traduce el uso de dispositivos en energía, costo, CO₂ y residuos electrónicos."""
    cons = consumo_dia(perfil)
    kwh_dia = sum(cons.values())
    ev_dia = cons["reposo"]
    resid = resid_extra = fab = fab_extra = 0.0
    inventario = []
    for d in perfil["dispositivos"]:
        i = C.DISPOSITIVOS[d]
        resid += i["peso_kg"] / i["vida_anios"]
        resid_extra += i["peso_kg"] / (i["vida_anios"] + extra_anios)
        fab += i["co2_fab_kg"] / i["vida_anios"]
        fab_extra += i["co2_fab_kg"] / (i["vida_anios"] + extra_anios)
        inventario.append({"id": d, "nombre": i["nombre"], "emoji": i["emoji"],
                           "peso": i["peso_kg"], "salud": salud_dispositivo(d, perfil)})
    return {
        "consumo": cons, "kwh_dia": kwh_dia, "kwh_anio": kwh_dia * 365,
        "co2_anio": co2_kg(kwh_dia * 365), "soles_anio": soles(kwh_dia * 365),
        "ev_kwh_dia": ev_dia, "ev_kwh_anio": ev_dia * 365, "ev_soles": soles(ev_dia * 365),
        "ev_co2": co2_kg(ev_dia * 365),
        "resid": resid, "resid_extra": resid_extra,
        "pct_resid": (1 - resid_extra / resid) * 100 if resid else 0.0,
        "fab": fab, "fab_extra": fab_extra, "inventario": inventario,
        "horas_consola_dia": ev_dia / (CONSOLA_W / 1000),
        "cargas_celular_dia": ev_dia / (CELULAR_WH / 1000),
        "botellas": resid,  # 1 botella de agua de 1 litro pesa cerca de 1 kg
    }


# ---------------------------------------------------------------- administrador
def config_admin():
    """(usuario, clave) del administrador desde st.secrets o variables de entorno; None si no está configurado.
    La clave nunca se escribe en el código para que no quede en el repositorio."""
    import os
    u = os.environ.get("ECOFEED_ADMIN_USER")
    p = os.environ.get("ECOFEED_ADMIN_PASS")
    if not (u and p):
        try:
            import streamlit as st
            u, p = st.secrets["admin_user"], st.secrets["admin_pass"]
        except Exception:
            return None
    return (str(u).strip().lower(), str(p)) if u and p else None


def es_admin(usuario, clave):
    cfg = config_admin()
    if not cfg:
        return False
    return hmac.compare_digest(usuario.strip().lower(), cfg[0]) & hmac.compare_digest(clave, cfg[1])


def filas_admin():
    """Una fila por persona con lo que necesita ver el docente. No incluye contraseñas ni hashes."""
    filas = []
    for u, rec in _cargar_todo().items():
        rec = normalizar(rec)
        p = rec["perfil"]
        res = resumen_actividades(rec)
        prog = progreso(rec)
        media = media_practicas(p) if p.get("habitos") else None
        filas.append({
            "usuario": u, "edad": C.EDADES[rec["edad"]]["etiqueta"], "grado": C.GRADOS.get(rec["grado"], rec["grado"]),
            "tono": tono(rec), "ocupacion": (rec.get("rutina") or {}).get("ocupacion", "—"), "encuesta": "sí" if p.get("onboarded") else "no",
            "nivel": prog["nivel"], "xp": prog["xp"], "actividades": res["resueltas"], "aciertos": res["aciertos"],
            "retos_hechos": len(prog["hechas"]), "desafio_aciertos": rec.get("desafio", {}).get("aciertos", 0), "dias_reto": len(rec.get("diario", {})), "dias_guardados": len(rec["registros"]),
            "media_practicas": round(media, 2) if media else None,
            "nivel_practicas": nivel_baremo(media) if media else "—",
            "creado": rec.get("creado", "—")[:16].replace("T", " "),
            "ultimo_acceso": rec.get("ultimo_acceso", "—")[:16].replace("T", " "),
        })
    return filas


def promedio_habitos():
    """Media de cada hábito (1 a 5) entre quienes completaron el cuestionario inicial."""
    acum = {k: [] for k in C.HABITOS}
    for rec in _cargar_todo().values():
        h = rec.get("perfil", {}).get("habitos", {})
        for k in acum:
            if k in h:
                acum[k].append(h[k])
    return {k: round(sum(v) / len(v), 2) for k, v in acum.items() if v}


def respaldo_json():
    return json.dumps(_cargar_todo(), ensure_ascii=False, indent=2)


@_con_candado
def restaurar_json(texto):
    """Mezcla un respaldo con lo que hay: no borra cuentas existentes, agrega las que faltan. Devuelve cuántas agregó."""
    nuevo = json.loads(texto)
    if not isinstance(nuevo, dict):
        raise ValueError("El archivo no tiene el formato esperado.")
    datos = _cargar_todo()
    agregadas = 0
    for u, rec in nuevo.items():
        if isinstance(rec, dict) and "hash" in rec and "sal" in rec and u not in datos:
            datos[u] = rec
            agregadas += 1
    _guardar_todo(datos)
    return agregadas


@_con_candado
def eliminar_usuario(usuario):
    datos = _cargar_todo()
    return datos.pop(usuario, None) is not None and (_guardar_todo(datos) or True)


# ---------------------------------------------------------------- desafío infinito y reto del día
def _opciones(rng, correcta, dec=2, unidad=""):
    """Cuatro opciones distintas con la correcta mezclada. Devuelve (textos, índice correcto)."""
    cand = {round(correcta, dec)}
    for f in (2, 0.5, 1.5, 3, 0.25, 4, 0.75, 5, 8, 10):
        cand.add(round(correcta * f, dec))
    paso = 10 ** -dec
    j = 1
    while len(cand) < 6:          # respaldo para números muy chicos: sumar y restar un paso
        cand.update({round(correcta + j * paso, dec), round(max(correcta - j * paso, 0), dec)})
        j += 1
    cand.discard(round(correcta, dec))
    malas = rng.sample(sorted(cand), 3)
    todas = malas + [round(correcta, dec)]
    rng.shuffle(todas)
    return [f"{fmt(v, dec)}{unidad}" for v in todas], todas.index(round(correcta, dec))


def pregunta_desafio(semilla, t, dispositivos=None):
    """Genera una pregunta nueva con números al azar usando los mismos supuestos del simulador.
    Con la misma semilla sale siempre la misma pregunta, así que alcanza para probarla."""
    rng = random.Random(semilla)
    claves = [d for d in (dispositivos or C.DISPOSITIVOS) if d in C.DISPOSITIVOS and C.DISPOSITIVOS[d]["w"] > 0] or list(C.DISPOSITIVOS)
    d = rng.choice(claves)
    D = C.DISPOSITIVOS[d]
    nombre = D["nombre"].lower()
    h = rng.choice([1, 2, 3, 4, 5, 6, 8])
    kwh_dia = D["w"] * h / 1000
    tipos = ["cargas", "kwh"] if t == "peque" else ["kwh", "soles", "cargas", "co2", "reposo", "residuo"]
    k = rng.choice(tipos)
    if k == "cargas" and round(kwh_dia / (CELULAR_WH / 1000)) < 2:
        k = "kwh"
    if k == "kwh":
        e = f"Un {nombre} de {D['w']} vatios está encendido {h} h. ¿Cuánta energía gasta en kWh?"
        ops, i = _opciones(rng, kwh_dia, 3, " kWh")
        ex = f"{D['w']} W × {h} h ÷ 1000 = {fmt(kwh_dia, 3)} kWh."
    elif k == "soles":
        mes = kwh_dia * 30 * PRECIO_KWH
        e = f"Un {nombre} de {D['w']} W se usa {h} h al día durante un mes. ¿Cuánto cuesta en soles (S/ {PRECIO_KWH} por kWh)?"
        ops, i = _opciones(rng, mes, 2, " soles")
        ex = f"{D['w']} W × {h} h × 30 días ÷ 1000 × {PRECIO_KWH} = {fmt(mes, 2)} soles."
    elif k == "cargas":
        n = kwh_dia / (CELULAR_WH / 1000)
        e = f"Con la energía que gasta un {nombre} en {h} h, ¿cuántas cargas completas de celular salen? (1 carga = {CELULAR_WH} Wh)"
        if t == "peque":
            e = f"Si un {nombre} está prendido {h} horas, gasta energía. ¿Con esa energía, cuántos celulares se cargan?"
        ops, i = _opciones(rng, round(n), 0, " celulares")
        ex = f"{D['w']} W × {h} h = {D['w'] * h} Wh. Dividido entre {CELULAR_WH} Wh por carga son unas {round(n)}."
    elif k == "co2":
        anual = kwh_dia * 365 * FACTOR_CO2
        e = f"Un {nombre} de {D['w']} W se usa {h} h cada día. ¿Cuántos kg de CO₂ genera en un año? (referencial: {FACTOR_CO2} kg por kWh)"
        ops, i = _opciones(rng, anual, 1, " kg")
        ex = f"{fmt(kwh_dia, 3)} kWh × 365 × {FACTOR_CO2} = {fmt(anual, 1)} kg de CO₂."
    elif k == "reposo":
        wr = D["w_reposo"] or 1
        anual = wr * h * 365 / 1000
        e = f"Un {nombre} se queda en reposo (sin usarse) {wr} W durante {h} h al día. ¿Cuántos kWh se pierden en un año?"
        ops, i = _opciones(rng, anual, 1, " kWh")
        ex = f"{wr} W × {h} h × 365 ÷ 1000 = {fmt(anual, 1)} kWh al año."
    else:
        kg = D["peso_kg"] / D["vida_anios"]
        e = f"Un {nombre} pesa {D['peso_kg']} kg y dura {D['vida_anios']} años. ¿Cuántos kg de residuo electrónico genera por año de uso?"
        ops, i = _opciones(rng, kg, 2, " kg")
        ex = f"{D['peso_kg']} kg ÷ {D['vida_anios']} años = {fmt(kg, 2)} kg por año."
    return {"emoji": D["emoji"], "enunciado": e, "opciones": ops, "correcta": i, "explica": ex, "tipo": k}


def reto_del_dia(rec, t, hoy=None):
    """Una recomendación distinta cada día (según la fecha), tomada de las que más le convienen a la persona."""
    hoy = hoy or date.today()
    lista = recomendar(rec["perfil"], t)
    return lista[hoy.toordinal() % len(lista)] if lista else None


def racha_diaria(rec, hoy=None):
    hoy = hoy or date.today()
    d = rec.get("diario", {})
    n, dia = 0, hoy if hoy.isoformat() in d else hoy - timedelta(days=1)
    while dia.isoformat() in d:
        n += 1
        dia -= timedelta(days=1)
    return n


def tabla_clase(limite=10):
    """Ranking por XP con apodos. Quien lo desactiva en su perfil no aparece."""
    filas = []
    for u, rec in _cargar_todo().items():
        rec = normalizar(rec)
        if rec.get("oculto_ranking") or not rec["perfil"].get("onboarded"):
            continue
        pr = progreso(rec)
        filas.append((u, pr["xp"], pr["nivel"], rec.get("desafio", {}).get("mejor", 0)))
    return sorted(filas, key=lambda f: -f[1])[:limite]
