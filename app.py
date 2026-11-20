"""EcoFeed: app de informática verde basada en el informe de la UNT.

El tono de los textos cambia según la edad y el grado de estudios:
    peque (primaria) · gamer (secundaria) · tecnico (superior o adulto) · mayor.

Archivos: contenido.py (textos y dispositivos), tips.py (recomendaciones),
actividades.py (tarjetas interactivas), logica.py (cálculos y guardado).

Ejecutar con:  streamlit run app.py
"""
import html
import random
from datetime import date

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import actividades as A
import contenido as C
import ilustraciones as IL
import juego as J
import panel_admin as PA
import rutina as R
import logica as L
import tips as T

st.set_page_config(page_title="EcoFeed", page_icon="🌱", layout="wide")

# Colores (arriba, abajo) de cada tarjeta: por categoría en las recomendaciones y por tipo en las actividades
COLORES = {
    "energia": ("#0b3d2e", "#1f9d63"), "residuos": ("#5a3a06", "#d18a1f"),
    "datos": ("#0b3c4a", "#1b9bb8"), "software": ("#1f2937", "#5b6b82"),
    "mito": ("#7c2d12", "#f2762b"), "quiz": ("#1e3a8a", "#4f8df7"),
    "escenario": ("#134e4a", "#1fb5a6"), "adivina": ("#701a75", "#d946ef"),
    "calc": ("#1e293b", "#0ea5e9"), "checklist": ("#14532d", "#84cc16"),
}
NOMBRE_CAT = {"energia": "Energía", "residuos": "Residuos y vida útil", "datos": "Datos y nube", "software": "Hábitos y software"}
ETIQUETA_SALUD = {"peque": "estado", "gamer": "estado", "tecnico": "índice de cuidado", "mayor": "cuidado"}

CSS = """
<style>
#MainMenu, footer, header {visibility: hidden;}
html, body, [class*="st-"] {font-size: __BASE__;}
.block-container {padding-top: 1.2rem; max-width: 1500px;}
@keyframes pop {0% {transform: scale(.94); opacity: 0;} 100% {transform: scale(1); opacity: 1;}}
@keyframes flota {0%,100% {transform: translateY(0);} 50% {transform: translateY(-6px);}}
@keyframes brilla {0% {background-position: 0 0;} 100% {background-position: 200% 0;}}
.eco-card {position: relative; overflow: hidden; border-radius: 22px; padding: 22px 26px; color: #fff;
           background: linear-gradient(150deg, var(--c1), var(--c2)); animation: pop .35s ease-out;
           min-height: 280px; display: flex; flex-direction: column; justify-content: space-between; gap: 14px;
           box-shadow: 0 8px 24px rgba(0,0,0,.18); margin-bottom: 14px;}
.eco-card::before {content: ""; position: absolute; inset: 0; opacity: .13; pointer-events: none;
                   background-image: radial-gradient(#fff 1.5px, transparent 1.6px); background-size: 18px 18px;}
.eco-card::after {content: var(--mark); position: absolute; right: -8px; bottom: -26px; font-size: 9rem;
                  opacity: .16; transform: rotate(-8deg); pointer-events: none;}
.eco-top {display: flex; justify-content: space-between; align-items: center; gap: 8px; position: relative; z-index: 1;}
.eco-tag {background: rgba(255,255,255,.2); border-radius: 999px; padding: 4px 14px; font-weight: 700;
          font-size: .8rem; letter-spacing: .04em; text-transform: uppercase;}
.eco-pos {font-size: .8rem; opacity: .85;}
.eco-body {position: relative; z-index: 1;}
.eco-row {display: flex; align-items: center; gap: 18px;}
.eco-row > div {flex: 1; min-width: 0;}
.eco-ilus {flex: 0 0 190px !important; background: rgba(255,255,255,.14); border-radius: 24px; padding: 10px;}
.v-split .eco-row {flex-direction: row-reverse; gap: 28px;}
.v-split .eco-ilus {flex-basis: 250px !important; align-self: stretch; display: flex; align-items: center; border-radius: 18px 60px 18px 60px;}
.v-split .eco-title {font-size: 2.2rem !important;}
.v-banner .eco-row {flex-direction: column-reverse; align-items: stretch; gap: 14px;}
.v-banner .eco-ilus {flex: none !important; height: 120px; border-radius: 16px; padding: 4px; background: rgba(0,0,0,.18);}
.v-banner .eco-svg {height: 100%; width: 100%;}
.v-banner .eco-tag {border-radius: 6px;}
.v-poster .eco-row {display: block; position: relative;}
.v-poster .eco-ilus {position: absolute; right: -6px; bottom: -34px; width: 190px; background: none; padding: 0; opacity: .92;}
.v-poster .eco-title {font-size: 2.7rem !important; line-height: 1.08; max-width: 72%; letter-spacing: -.01em;}
.v-poster .eco-text {max-width: 70%;}
.v-poster .eco-tag {border-radius: 0; background: #fff; color: #111; transform: rotate(-2deg);}
.lado {border-radius: 18px; padding: 16px 18px; background: rgba(127,127,127,.10); margin-bottom: 12px; border-left: 5px solid #16a34a;}
.lado h4 {margin: 0 0 8px 0; font-size: .78rem; letter-spacing: .08em; text-transform: uppercase; opacity: .7;}
.lado .sig {display: flex; align-items: center; gap: 10px; padding: 7px 0; border-top: 1px dashed rgba(127,127,127,.35); font-size: .95rem;}
.lado .sig:first-of-type {border-top: none;}
.lado .sig i {font-style: normal; width: 30px; height: 30px; border-radius: 9px; display: grid; place-items: center; color: #fff; flex: none;}
.lado .tira {display: flex; gap: 3px; flex-wrap: wrap;}
.lado .tira span {width: 9px; height: 9px; border-radius: 2px; background: rgba(127,127,127,.3);}
.lado .tira span.ok {background: #16a34a;} .lado .tira span.mal {background: #f59e0b;} .lado .tira span.ya {outline: 2px solid #16a34a;}
.eco-fin {border-radius: 26px; padding: 34px; color: #fff; background: linear-gradient(135deg,#0b3d2e,#16a34a 70%,#facc15); margin-bottom: 14px;}
.eco-fin .n {font-size: 3.4rem; font-weight: 800; line-height: 1;}
.eco-fin .g {display: flex; gap: 28px; flex-wrap: wrap; margin-top: 18px;}
.eco-card:has(.eco-ilus)::after, .eco-q:has(.eco-ilus)::after {opacity: .05;}
.eco-svg {width: 100%; height: auto; display: block;}
@media (max-width: 640px) {.eco-row {flex-direction: column-reverse; align-items: flex-start;} .eco-ilus {flex-basis: auto !important; width: 120px;}}
.eco-emoji {font-size: 3.2rem; line-height: 1; display: inline-block; animation: flota 3s ease-in-out infinite;}
.eco-title {font-size: 2rem !important; font-weight: 800; line-height: 1.15; margin: 6px 0 8px 0; text-align: left;}
.eco-text {font-size: 1.2rem !important; line-height: 1.45; margin: 0; max-width: 34em; text-align: left;}
.eco-foot {position: relative; z-index: 1;}
.eco-chip {display: inline-block; background: rgba(255,255,255,.18); border-radius: 999px;
           padding: 3px 12px; margin: 0 6px 6px 0; font-size: .82rem;}
.eco-reto {background: rgba(0,0,0,.26); border-radius: 14px; padding: 10px 14px; font-size: .95rem; margin-top: 4px;}
.eco-q {border-radius: 22px; padding: 24px; color: #fff; background: linear-gradient(150deg,#0b3d2e,#1f9d63);
        position: relative; overflow: hidden; animation: pop .3s ease-out; min-height: 220px;}
.eco-q::after {content: var(--mark); position: absolute; right: -6px; bottom: -22px; font-size: 7.5rem; opacity: .17;}
.eco-q .eco-title {font-size: 1.7rem !important; position: relative; z-index: 1;}
.eco-q p {position: relative; z-index: 1; margin: 0; opacity: .9;}
.eco-hero {border-radius: 24px; padding: 34px 30px; color: #fff; min-height: 420px; position: relative; overflow: hidden;
           background: linear-gradient(150deg,#0b3d2e,#1f9d63 60%,#84cc16);}
.eco-hero::before {content: ""; position: absolute; inset: 0; opacity: .14;
                   background-image: radial-gradient(#fff 1.5px, transparent 1.6px); background-size: 18px 18px;}
.eco-hero .t {font-size: 3.4rem; font-weight: 800; line-height: 1.1; margin: 6px 0 8px 0; position: relative;}
.eco-hero p {font-size: 1.15rem; position: relative; opacity: .92;}
.eco-hero .eco-emoji {font-size: 4.5rem;}
.eco-res {border-radius: 16px; padding: 14px 18px; margin: 8px 0; animation: pop .3s ease-out;}
.eco-res.ok {background: rgba(34,197,94,.16); border-left: 6px solid #22c55e;}
.eco-res.no {background: rgba(245,158,11,.16); border-left: 6px solid #f59e0b;}
.eco-res b {font-size: 1.05em;}
.eco-hud {border-radius: 20px; padding: 16px; background: rgba(128,128,128,.12);}
.eco-hud .av {font-size: 2.6rem; line-height: 1;}
.eco-hud .nv {font-weight: 800; font-size: 1.1rem;}
.eco-bar {height: 12px; border-radius: 8px; background: rgba(128,128,128,.25); overflow: hidden; margin: 6px 0 10px 0;}
.eco-bar > div {height: 100%; background: linear-gradient(90deg,#22c55e,#84cc16); border-radius: 8px;}
.eco-bar.seg > div {background: repeating-linear-gradient(90deg,#22c55e 0 9px,transparent 9px 11px);}
.eco-bar.energia > div {background: linear-gradient(90deg,#f59e0b,#22c55e);}
.eco-kpi {display: flex; justify-content: space-between; font-size: .92rem; padding: 3px 0;}
.eco-week {display: flex; gap: 6px; margin: 6px 0;}
.eco-week div {flex: 1; text-align: center; border-radius: 10px; padding: 5px 0; font-size: .78rem;
               background: rgba(128,128,128,.2);}
.eco-week div.on {background: #22c55e; color: #fff; font-weight: 700;}
.eco-save {font-size: .82rem; opacity: .85; margin-top: 8px;}
.eco-badge {text-align: center; padding: 6px 2px;}
.eco-badge .e {font-size: 2rem; line-height: 1.1;}
.eco-badge .n {font-size: .8rem; line-height: 1.2;}
.eco-off {opacity: .35;}
.stButton > button {border-radius: 14px; font-weight: 600;}
@media (prefers-reduced-motion: reduce) {.eco-card, .eco-q, .eco-res, .eco-emoji {animation: none;}}
</style>
"""


FONDO = """
<style>
.stApp {background-image: radial-gradient(ellipse at 15% 0%, rgba(34,197,94,.22), transparent 45%),
        radial-gradient(ellipse at 90% 10%, rgba(250,204,21,.16), transparent 40%);}
.block-container {padding-bottom: 130px;}
.stButton > button {transition: transform .12s, box-shadow .12s;}
.stButton > button:hover:not(:disabled) {transform: translateY(-2px); box-shadow: 0 6px 18px rgba(22,163,74,.35);}
.stButton > button[kind=primary] {background: linear-gradient(90deg,#16a34a,#84cc16); border: 0; font-weight: 700;}
.stTabs [data-baseweb=tab] {font-weight: 700;}
.eco-card, .eco-q {box-shadow: 0 10px 30px rgba(0,0,0,.28), 0 0 0 1px rgba(255,255,255,.08) inset;}
.eco-hero .t {background: linear-gradient(90deg,#fff,#fde68a); -webkit-background-clip: text; background-clip: text; color: transparent;}
.run {position: fixed; left: 0; right: 0; bottom: 0; height: 96px; z-index: 0; pointer-events: none; overflow: hidden;
      background: linear-gradient(transparent, rgba(22,163,74,.20));}
.run .suelo {position: absolute; left: 0; right: 0; bottom: 20px; height: 3px; opacity: .55;
             background: repeating-linear-gradient(90deg,#16a34a 0 26px,transparent 26px 44px); animation: suelo 1.1s linear infinite;}
.run .yo, .run .ob, .run .nube {position: absolute; line-height: 1;}
.run .yo {left: 12vw; bottom: 22px; font-size: 38px; animation: salto 12s infinite;}
.run .ob {bottom: 22px; font-size: 30px; left: 0; animation: pasa 12s linear infinite;}
.run .ob.b {animation-delay: -6s;}
.run .nube {top: 6px; font-size: 26px; opacity: .35; left: 0; animation: pasa 40s linear infinite;}
@keyframes suelo {to {background-position: -44px 0;}}
@keyframes pasa {from {transform: translateX(104vw);} to {transform: translateX(-12vw);}}
@keyframes salto {0%,27%,35%,77%,85%,100% {transform: translateY(0);} 31%,81% {transform: translateY(-58px);}}
@media (prefers-reduced-motion: reduce) {.run * {animation: none !important;}}
@media (max-width: 640px) {.run {height: 56px; opacity: .35;} .run .yo {font-size: 26px; bottom: 14px;} .run .ob {font-size: 22px; bottom: 14px;} .run .suelo {bottom: 12px;} .run .nube {display: none;} .block-container {padding-bottom: 80px;}}
</style>
<div class="run"><div class="nube">☁️</div><div class="suelo"></div><div class="yo">🌱</div>
<div class="ob a">🔋</div><div class="ob b">🔌</div></div>
"""


def fondo():
    """Escena animada fija al pie de la pantalla: un brote que salta pilas y cargadores."""
    st.markdown(FONDO, unsafe_allow_html=True)


def estilos(t):
    base = {"peque": "1.12rem", "mayor": "1.28rem"}.get(t, "1rem")
    st.markdown(CSS.replace("__BASE__", base), unsafe_allow_html=True)


def esc(x):
    return html.escape(str(x))


def guardar():
    L.guardar_usuario(st.session_state.usuario, st.session_state.rec)


def avisar(msg, icono="✅", globos=False):
    """Deja un aviso para mostrarlo tras el próximo rerun."""
    st.session_state.setdefault("flash", []).append((msg, icono))
    if globos:
        st.session_state["flash_globos"] = True


def mostrar_avisos():
    s = st.session_state
    for msg, icono in s.pop("flash", []):
        st.toast(msg, icon=icono)
    if s.pop("flash_globos", False):
        st.balloons()


# ====================================================================== login
def pantalla_login():
    izq, der = st.columns([1.1, 1], gap="large")
    with izq:
        st.markdown(
            "<div class='eco-hero' style='--mark:\"🌎\"'><div class='eco-emoji'>🌱</div><div class='t'>EcoFeed</div>"
            "<p>Tarjetas cortas para aprender a cuidar tus equipos, gastar menos luz y generar menos basura electrónica.</p>"
            "<span class='eco-chip'>🔥 Para ti</span><span class='eco-chip'>🧠 Mitos y preguntas</span>"
            "<span class='eco-chip'>🎯 Misiones</span><span class='eco-chip'>🔋 Tu consumo</span></div>",
            unsafe_allow_html=True,
        )
    with der:
        t1, t2 = st.tabs(["Iniciar sesión", "Crear cuenta"])
        with t1:
            with st.form("form_login"):
                u = st.text_input("Usuario", key="login_u")
                p = st.text_input("Contraseña", type="password", key="login_p")
                ok = st.form_submit_button("Entrar", use_container_width=True, type="primary")
            if ok and L.es_admin(u, p):
                st.session_state.es_admin = True
                st.session_state.usuario = u.strip().lower()
                st.rerun()
            elif ok:
                rec, err = L.iniciar_sesion(u, p)
                if err:
                    st.error(err)
                else:
                    entrar(u.strip().lower(), rec)
        with t2:
            with st.form("form_registro"):
                u = st.text_input("Elige un usuario", key="reg_u")
                p = st.text_input("Elige una contraseña", type="password", key="reg_p")
                edad = st.radio("¿Qué grupo de edad eres?", list(C.EDADES), key="reg_edad",
                                format_func=lambda k: f"{C.EDADES[k]['emoji']} {C.EDADES[k]['etiqueta']}")
                grado = st.radio("¿Qué estudias ahora?", list(C.GRADOS), key="reg_grado", index=2,
                                 format_func=lambda k: C.GRADOS[k], horizontal=True)
                ok = st.form_submit_button("Crear cuenta", use_container_width=True, type="primary")
            if ok:
                rec, err = L.registrar_usuario(u, p, edad, grado)
                if err:
                    st.error(err)
                else:
                    entrar(u.strip().lower(), rec)
        st.caption("Usa un nombre real, estaremos al tanto de tu avance. tu contraseña es privada.")


def entrar(usuario, rec):
    s = st.session_state
    token = L.crear_sesion(usuario)
    if token:
        st.query_params["u"], st.query_params["s"] = usuario, token   # así una recarga no cierra la sesión
    s.usuario = usuario
    s.rec = rec
    s.paso = 0
    s.feed_i = 0
    s.pop("feed", None)
    s.pop("leccion", None)
    s.mostrar_resultado = False
    st.rerun()


# ====================================================================== cuestionario
def tarjeta_pregunta(emoji, titulo, sub="", ilus=""):
    sub_html = f"<p>{esc(sub)}</p>" if sub else ""
    if ilus:
        t = L.tono(st.session_state.rec) if st.session_state.get("rec") else "tecnico"
        interior = (f"<div class='eco-row'><div><div class='eco-title'>{esc(titulo)}</div>{sub_html}</div>"
                    f"<div class='eco-ilus'>{IL.svg(ilus, t)}</div></div>")
    else:
        interior = f"<div class='eco-emoji'>{emoji}</div><div class='eco-title'>{esc(titulo)}</div>{sub_html}"
    st.markdown(
        f"<div class='eco-q' style='--mark:\"{emoji}\"'>{interior}</div>",
        unsafe_allow_html=True,
    )


def entrada_horas(d, valor, t, key):
    """Primaria elige entre cuatro opciones; el resto usa un deslizador."""
    info = C.DISPOSITIVOS[d]
    etiqueta = f"{info['emoji']} {info['nombre']}"
    if t == "peque":
        opciones = [h for _, h in C.HORAS_OPCIONES]
        actual = min(opciones, key=lambda h: abs(h - valor))
        elegido = st.radio(etiqueta, opciones, index=opciones.index(actual), key=key, horizontal=True,
                           format_func=lambda h: dict((v, k) for k, v in C.HORAS_OPCIONES)[h])
        return float(elegido)
    return st.slider(etiqueta, 0.0, float(info["horas_max"]), float(valor), 0.5, key=key)


def dispositivos_con_horas(perfil):
    return [d for d in perfil["dispositivos"] if d not in C.DISPOSITIVOS_SIEMPRE_ENCENDIDOS]


def pantalla_onboarding():
    s = st.session_state
    rec = s.rec
    perfil = rec["perfil"]
    t = L.tono(rec)
    U = C.UI[t]
    lista = ["dispositivos", "horas"] + [f"h_{k}" for k in C.HABITOS] + ["barreras"]
    s.paso = max(0, min(s.get("paso", 0), len(lista) - 1))
    paso = s.paso
    clave = lista[paso]

    st.progress((paso + 1) / len(lista), text=U["pregunta_n"].format(n=paso + 1, total=len(lista)))
    izq, der = st.columns([1, 1.25], gap="large")

    # Pantalla de lección tras responder (primaria y secundaria)
    if s.get("leccion"):
        k = s.leccion
        h = C.HABITOS[k]
        v = perfil["habitos"][k]
        with izq:
            tarjeta_pregunta("😄" if v >= 4 else "🙂" if v == 3 else "💡", L.feedback_habito(k, v, t))
        with der:
            st.markdown(f"### {h['emoji']} {L.titulo_habito(k, t)}")
            st.info(h["leccion"][t], icon="💡")
            if st.button(U["continuar"], key="sig_leccion", type="primary", use_container_width=True):
                s.pop("leccion")
                s.paso += 1
                st.rerun()
        return

    if clave == "dispositivos":
        with izq:
            tarjeta_pregunta("📲", U["q_disp_t"], U["q_disp_s"], IL.POR_PASO["dispositivos"])
        with der:
            sel = []
            cols = st.columns(2)
            for i, (d, info) in enumerate(C.DISPOSITIVOS.items()):
                if cols[i % 2].checkbox(f"{info['emoji']} {info['nombre']}", value=d in perfil["dispositivos"], key=f"chk_{d}"):
                    sel.append(d)
            if st.button(U["continuar"], key="sig_disp", disabled=not sel, use_container_width=True, type="primary"):
                perfil["dispositivos"] = sel
                perfil["horas"] = {d: perfil["horas"].get(d, C.DISPOSITIVOS[d]["horas_def"]) for d in sel}
                s.paso += 1
                guardar()
                st.rerun()

    elif clave == "horas":
        with izq:
            tarjeta_pregunta("⏱️", U["q_horas_t"], U["q_horas_s"], IL.POR_PASO["horas"])
        with der:
            horas = {}
            for d in dispositivos_con_horas(perfil):
                horas[d] = entrada_horas(d, perfil["horas"].get(d, C.DISPOSITIVOS[d]["horas_def"]), t, f"sl_{d}")
            if set(perfil["dispositivos"]) & set(C.DISPOSITIVOS_SIEMPRE_ENCENDIDOS):
                st.caption("📡 El router se cuenta como encendido todo el día.")
            if st.button(U["continuar"], key="sig_horas", use_container_width=True, type="primary"):
                perfil["horas"] = L.horas_completas(perfil, horas)
                s.paso += 1
                guardar()
                st.rerun()

    elif clave.startswith("h_"):
        k = clave[2:]
        h = C.HABITOS[k]
        sub = f"{h['titulo']} (ítem {h['item']} del cuestionario)" if t == "tecnico" else ""
        with izq:
            tarjeta_pregunta(h["emoji"], L.pregunta_habito(k, t), sub, IL.POR_HABITO[k])
        with der:
            if t in ("peque", "gamer"):
                esc_ = h["escenario"]
                st.markdown(f"**{esc_['situacion']}**" if t == "peque" else "**Elige lo que más se parece a ti**")
                for i, (emoji, texto, valor) in enumerate(esc_["opciones"]):
                    if st.button(f"{emoji}  {texto}", key=f"esc_{k}_{i}", use_container_width=True):
                        perfil["habitos"][k] = valor
                        s.leccion = k
                        guardar()
                        st.rerun()
            else:
                cols = st.columns(5)
                for i, col in zip(range(1, 6), cols):
                    emoji, nombre = C.ESCALA[i]
                    if col.button(f"{emoji}\n\n{i}", key=f"esc_{k}_{i}", use_container_width=True, help=nombre):
                        perfil["habitos"][k] = i
                        s.paso += 1
                        guardar()
                        st.rerun()
                st.caption("1 = Nunca · 2 = Casi nunca · 3 = A veces · 4 = Casi siempre · 5 = Siempre")

    else:  # barreras
        with izq:
            tarjeta_pregunta("🚧", U["q_barr_t"], U["q_barr_s"], IL.POR_PASO["barreras"])
        with der:
            sel = []
            for b, info in C.BARRERAS.items():
                if st.checkbox(f"{info['emoji']} {L.texto_barrera(b, t)}", value=b in perfil["barreras"], key=f"bar_{b}"):
                    sel.append(b)
            if st.button(U["terminar"], key="fin", use_container_width=True, type="primary"):
                perfil["barreras"] = sel
                perfil["onboarded"] = True
                s.feed_i = 0
                s.pop("feed", None)
                s.mostrar_resultado = True
                guardar()
                st.rerun()

    if paso > 0 and st.button(U["atras"], key="atras"):
        s.paso -= 1
        st.rerun()


def pantalla_resultado():
    s = st.session_state
    perfil = s.rec["perfil"]
    t = L.tono(s.rec)
    U = C.UI[t]
    media = L.media_practicas(perfil)
    idx = L.indice_verde(media)
    izq, der = st.columns([1, 1.25], gap="large")
    with izq:
        tarjeta_pregunta("🏆", U["res_titulo"], "", IL.POR_PASO["resultado"])
        st.markdown(f"<div class='eco-bar energia'><div style='width:{idx}%'></div></div>", unsafe_allow_html=True)
        st.metric(U["idx_titulo"], f"{idx} / 100")
    with der:
        st.write(L.texto_resultado(perfil, t))
        for k in C.HABITOS:
            v = perfil["habitos"].get(k, 3)
            marca = "🟢" if v >= 4 else "🟡" if v == 3 else "🔴"
            st.progress(v / 5, text=f"{marca} {L.feedback_habito(k, v, t)}")
        if st.button(U["res_boton"], key="ir_feed", use_container_width=True, type="primary"):
            s.mostrar_resultado = False
            st.rerun()


# ====================================================================== panel de progreso (HUD)
def hud(t):
    s = st.session_state
    rec = s.rec
    prog = L.progreso(rec)
    H = C.HUD[t]
    res = L.resumen_actividades(rec)
    idx = L.indice_verde(L.media_practicas(rec["perfil"]))
    seg = "seg" if t in ("peque", "gamer") else ""
    dias = "".join(f"<div class='{'on' if ok else ''}' title='{d.strftime('%d/%m')}'>{et}</div>" for d, et, ok, _ in L.semana(rec))
    ver = L.verificar_guardado(s.usuario, rec)
    if ver["dias_en_disco"]:
        guardado = f"💾 {ver['dias_en_disco']} día(s) guardados en disco {'✔' if ver['coincide'] else '⚠️'}"
    else:
        guardado = "💾 Aún no hay días guardados"
    st.markdown(
        f"<div class='eco-hud'><div class='av'>{prog['avatar']}</div>"
        f"<div class='nv'>{H['nivel']} {prog['nivel']} · {esc(prog['titulo'])}</div>"
        f"<div class='eco-bar {seg}'><div style='width:{prog['xp_nivel']}%'></div></div>"
        f"<div class='eco-kpi'><span>{H['xp']}</span><b>{prog['xp']}</b></div>"
        f"<div class='eco-kpi'><span>🔥 {H['racha']}</span><b>{L.racha(rec)}</b></div>"
        f"<div class='eco-kpi'><span>🎯 {H['misiones']}</span><b>{len(prog['hechas'])}</b></div>"
        f"<div class='eco-kpi'><span>🧠 {H['act']}</span><b>{res['resueltas']}/{res['total']}</b></div>"
        f"<div class='eco-kpi'><span>⚡ {H['energia']}</span><b>{idx}</b></div>"
        f"<div class='eco-bar energia'><div style='width:{idx}%'></div></div>"
        f"<div class='eco-week'>{dias}</div><div class='eco-save'>{guardado}</div></div>",
        unsafe_allow_html=True,
    )


# ====================================================================== feed "Para ti"
def chip_ahorro(ahorro, t):
    if not ahorro or ahorro < 0.5 or t == "peque":
        return None
    if t == "gamer":
        return f"⚡ ~{L.fmt(ahorro, 0)} kWh al año"
    if t == "tecnico":
        return f"⚡ ~{L.fmt(ahorro, 0)} kWh/año · S/ {L.fmt(L.soles(ahorro), 0)} · {L.fmt(L.co2_kg(ahorro), 0)} kg CO₂"
    return f"💰 ~S/ {L.fmt(L.soles(ahorro), 0)} al año"


def tarjeta(c1, c2, marca, etiqueta, pos, emoji, titulo, texto="", pie="", ilus="", var="split"):
    texto_html = f"<div class='eco-text'>{esc(texto)}</div>" if texto else ""
    if ilus:
        t = L.tono(st.session_state.rec)
        cuerpo = (f"<div class='eco-row'><div><div class='eco-title'>{esc(titulo)}</div>{texto_html}</div>"
                  f"<div class='eco-ilus'>{IL.svg(ilus, t)}</div></div>")
    else:
        cuerpo = f"<div class='eco-emoji'>{emoji}</div><div class='eco-title'>{esc(titulo)}</div>{texto_html}"
    st.markdown(
        f"<div class='eco-card v-{var if ilus else 'none'}' style='--c1:{c1};--c2:{c2};--mark:\"{marca}\"'>"
        f"<div class='eco-top'><span class='eco-tag'>{esc(etiqueta)}</span><span class='eco-pos'>{pos}</span></div>"
        f"<div class='eco-body'>{cuerpo}</div>"
        f"<div class='eco-foot'>{pie}</div></div>",
        unsafe_allow_html=True,
    )


VAR_TIPO = {'mito': 'poster', 'adivina': 'poster', 'quiz': 'banner', 'escenario': 'banner', 'calc': 'split', 'checklist': 'split'}


def estado_ronda(rec, feed, i):
    """Una casilla por tarjeta: verde = acertada o aceptada, ámbar = fallada, contorno = la actual."""
    out = []
    for k, (tp, iid) in enumerate(feed):
        if tp == "act":
            v = rec["actividades"].get(iid)
            c = "ok" if v and v["ok"] else "mal" if v else ""
        else:
            c = "ok" if rec["retos"].get(iid) else ""
        out.append(f"<span class='{c} {'ya' if k == i else ''}'></span>")
    return "".join(out)


def panel_lado(t, feed, i, recs):
    s = st.session_state
    rec = s.rec
    sig = ""
    for tp, iid in feed[i + 1:i + 4]:
        if tp == "tip":
            c1, _ = COLORES[recs[iid]["tip"]["categoria"]]
            nombre, ic, titulo = "Recomendación", "💡", recs[iid]["titulo"]
        else:
            a = A.ACTIVIDADES_POR_ID[iid]
            c1, _ = COLORES[a["tipo"]]
            nombre, ic, titulo = C.TIPOS_ACTIVIDAD[a["tipo"]][t], a["emoji"], ""
        sig += f"<div class='sig'><i style='background:{c1}'>{ic}</i><span>{esc(nombre)}{(' · ' + esc(titulo)) if titulo else ''}</span></div>"
    if not sig:
        sig = "<div class='sig'>🏁 Es la última tarjeta de esta ronda</div>"
    res = L.resumen_actividades(rec)
    st.markdown(
        f"<div class='lado'><h4>Ronda {s.get('ronda', 1)} · {i + 1} de {len(feed)}</h4><div class='tira'>{estado_ronda(rec, feed, i)}</div></div>"
        f"<div class='lado'><h4>Sigue</h4>{sig}</div>"
        f"<div class='lado'><h4>Tus aciertos</h4><b style='font-size:1.6rem'>{res['aciertos']}</b> de {res['resueltas']} respondidas</div>",
        unsafe_allow_html=True,
    )


def fin_de_ronda(t, feed):
    s = st.session_state
    rec = s.rec
    res = L.resumen_actividades(rec)
    ret = sum(1 for v in rec["retos"].values() if v)
    falladas = sum(1 for v in rec["actividades"].values() if not v["ok"])
    st.markdown(
        f"<div class='eco-fin'><div style='opacity:.85;font-weight:700;letter-spacing:.06em'>RONDA {s.get('ronda', 1)} COMPLETA</div>"
        f"<div class='n'>{len(feed)} tarjetas</div>"
        f"<div class='g'><div><b style='font-size:1.8rem'>{res['aciertos']}</b><br>aciertos</div>"
        f"<div><b style='font-size:1.8rem'>{falladas}</b><br>por repasar</div>"
        f"<div><b style='font-size:1.8rem'>{ret}</b><br>retos aceptados</div></div></div>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    if c1.button(f"🔁 Repasar lo que fallé ({falladas})", use_container_width=True, disabled=falladas == 0, key="rep"):
        s.feed, s.feed_i, s.ronda = L.armar_feed(rec, t, "repaso"), 0, s.get("ronda", 1) + 1
        st.rerun()
    if c2.button("🎲 Nueva ronda mezclada", use_container_width=True, type="primary", key="mez"):
        s.ronda = s.get("ronda", 1) + 1
        s.feed, s.feed_i = L.armar_feed(rec, t, "mezcla", s.ronda), 0
        st.rerun()
    st.caption("¿Quieres más? En la pestaña ⚡ Desafío hay preguntas que nunca se acaban, un reto nuevo cada día y una tabla de la clase.")


def tab_feed(t, U):
    s = st.session_state
    rec = s.rec
    perfil = rec["perfil"]
    recs = {r["id"]: r for r in L.recomendar(perfil, t)}
    if "feed" not in s or s.get("feed_t") != t:
        s.feed = L.armar_feed(rec, t)
        s.feed_t = t
        s.feed_i = 0
    s.feed = [x for x in s.feed if x[0] == "act" or x[1] in recs]
    n = len(s.feed)
    if n == 0:
        s.feed, s.ronda = L.armar_feed(rec, t, "mezcla", 1), 1
        n = len(s.feed)
    s.feed_i = max(0, min(s.get("feed_i", 0), n))
    principal, lado = st.columns([2.5, 1], gap="large")
    with principal:
        if s.feed_i >= n:
            fin_de_ronda(t, s.feed)
            if st.button(U["anterior"], key="prev_fin", use_container_width=True):
                s.feed_i = n - 1
                st.rerun()
            return
        tipo, iid = s.feed[s.feed_i]
        pos = f"{s.feed_i + 1} / {n}"
        if tipo == "tip":
            mostrar_tip(recs[iid], t, U, pos)
        else:
            mostrar_actividad(A.ACTIVIDADES_POR_ID[iid], t, pos)
        b1, b2 = st.columns(2)
        if b1.button(U["anterior"], key="prev", use_container_width=True, disabled=s.feed_i == 0):
            s.feed_i -= 1
            st.rerun()
        ultimo = s.feed_i == n - 1
        if b2.button("🏁 Terminar ronda" if ultimo else U["siguiente"], key="next", use_container_width=True, type="primary"):
            s.feed_i += 1
            st.rerun()
    with lado:
        panel_lado(t, s.feed, s.feed_i, recs)


def mostrar_tip(r, t, U, pos):
    s = st.session_state
    rec = s.rec
    perfil = rec["perfil"]
    tip = r["tip"]
    c1, c2 = COLORES[tip["categoria"]]
    chips = f"<span class='eco-chip'>{NOMBRE_CAT[tip['categoria']]}</span><span class='eco-chip'>⏱ {esc(tip['tiempo'])}</span>"
    ahorro = chip_ahorro(r["ahorro"], t)
    if ahorro:
        chips += f"<span class='eco-chip'>{esc(ahorro)}</span>"
    for d in tip["dispositivos"]:
        if d in perfil["dispositivos"]:
            chips += f"<span class='eco-chip'>{C.DISPOSITIVOS[d]['emoji']} {C.DISPOSITIVOS[d]['nombre']}</span>"
    pie = chips + f"<div class='eco-reto'>🎯 {U['reto']}: {esc(L.reto_para(tip, t))}</div>"
    tarjeta(c1, c2, tip["emoji"], U["cab_feed"], pos, tip["emoji"], r["titulo"], r["corto"], pie,
            ilus=IL.clave_tip(tip["id"], tip["categoria"]), var="split")

    if r["largo"] or (tip["dato"] and t != "peque"):
        with st.expander(U["porque"]):
            if r["largo"]:
                st.write(r["largo"])
            if tip["dato"] and t != "peque":
                st.caption(f"📄 {U['dato']}: {tip['dato']}")

    a1, a2 = st.columns(2)
    like = tip["id"] in rec["likes"]
    aceptada = tip["id"] in rec["retos"]
    if a1.button(U["legusta"] if like else U["megusta"], key=f"like_{tip['id']}", use_container_width=True):
        rec["likes"].remove(tip["id"]) if like else rec["likes"].append(tip["id"])
        guardar()
        st.rerun()
    if a2.button(U["aceptada"] if aceptada else U["aceptar"], key=f"acepta_{tip['id']}",
                 disabled=aceptada, use_container_width=True):
        rec["retos"][tip["id"]] = False
        guardar()
        avisar(f"{U['reto']}: {L.reto_para(tip, t)}", "🎯")
        st.rerun()


# ---------------------------------------------------------------- actividades interactivas
RESP = {
    "peque": ("¡Muy bien!", "¡Casi! Mira esto:"), "gamer": ("Correcto.", "Casi."),
    "tecnico": ("Correcto.", "No exactamente."), "mayor": ("¡Correcto!", "No exactamente.")}


def responder(a, ok, resp, t):
    """Registra la respuesta (solo cuenta la primera vez), guarda en disco y prepara los avisos."""
    s = st.session_state
    antes = L.progreso(s.rec)["nivel"]
    if L.registrar_actividad(s.rec, a["id"], ok, resp):
        guardar()
        xp = C.XP_ACTIVIDAD_OK if ok else C.XP_ACTIVIDAD_INTENTO
        despues = L.progreso(s.rec)["nivel"]
        avisar(f"+{xp} XP" if t != "mayor" else f"+{xp} puntos", "⭐" if ok else "💡", globos=despues > antes)
    st.rerun()


def banner_resultado(ok, explica, t):
    titulo = RESP[t][0 if ok else 1]
    st.markdown(f"<div class='eco-res {'ok' if ok else 'no'}'><b>{'✅' if ok else '💡'} {titulo}</b><br>{esc(explica)}</div>",
                unsafe_allow_html=True)


def mostrar_actividad(a, t, pos):
    rec = st.session_state.rec
    c1, c2 = COLORES[a["tipo"]]
    etiqueta = C.TIPOS_ACTIVIDAD[a["tipo"]][t]
    hecha = rec["actividades"].get(a["id"])
    tx = lambda v: A.texto(v, t)
    tipo = a["tipo"]
    if tipo == "mito":
        tarjeta(c1, c2, a["emoji"], etiqueta, pos, a["emoji"], tx(a["texto"]), ilus=IL.clave_actividad(a), var=VAR_TIPO[a['tipo']])
        if hecha:
            st.caption("Tu respuesta: " + ("Verdad" if hecha["resp"] else "Mito"))
            banner_resultado(hecha["ok"], tx(a["explica"]), t)
        else:
            b1, b2 = st.columns(2)
            if b1.button("🙅 Mito", key=f"m_{a['id']}", use_container_width=True):
                responder(a, a["verdad"] is False, False, t)
            if b2.button("✅ Verdad", key=f"v_{a['id']}", use_container_width=True):
                responder(a, a["verdad"] is True, True, t)
    elif tipo in ("quiz", "escenario"):
        pregunta = tx(a["pregunta"]) if tipo == "quiz" else tx(a["situacion"])
        tarjeta(c1, c2, a["emoji"], etiqueta, pos, a["emoji"], pregunta, ilus=IL.clave_actividad(a), var=VAR_TIPO[a['tipo']])
        opciones = tx(a["opciones"])
        orden = list(range(len(opciones)))
        random.Random(a["id"]).shuffle(orden)
        if hecha:
            for i in orden:
                marca = "✅" if i == a["correcta"] else ("❌" if i == hecha["resp"] else "▫️")
                st.write(f"{marca} {opciones[i]}")
            banner_resultado(hecha["ok"], tx(a["explica"]), t)
        else:
            for i in orden:
                if st.button(opciones[i], key=f"o_{a['id']}_{i}", use_container_width=True):
                    responder(a, i == a["correcta"], i, t)
    elif tipo == "adivina":
        tarjeta(c1, c2, a["emoji"], etiqueta, pos, a["emoji"], tx(a["pregunta"]), ilus=IL.clave_actividad(a), var=VAR_TIPO[a['tipo']])
        lo, hi, paso = a["rango"]
        dec = 0 if a["respuesta"] == int(a["respuesta"]) else 1
        if hecha:
            m1, m2 = st.columns(2)
            m1.metric("Tu respuesta", f"{L.fmt(hecha['resp'], dec)} {a['unidad']}")
            m2.metric("Dato real", f"{L.fmt(a['respuesta'], dec)} {a['unidad']}")
            banner_resultado(hecha["ok"], tx(a["explica"]), t)
        else:
            val = st.slider(a["unidad"], lo, hi, a["inicial"], paso, key=f"n_{a['id']}")
            if st.button("Comprobar", key=f"nb_{a['id']}", type="primary", use_container_width=True):
                responder(a, abs(val - a["respuesta"]) <= a["tolerancia"], val, t)
    elif tipo == "calc":
        tarjeta(c1, c2, a["emoji"], etiqueta, pos, a["emoji"], tx(a["titulo"]), ilus=IL.clave_actividad(a), var=VAR_TIPO[a['tipo']])
        calculadora(a, t, hecha)
    else:  # checklist
        tarjeta(c1, c2, a["emoji"], etiqueta, pos, a["emoji"], tx(a["titulo"]), ilus=IL.clave_actividad(a), var=VAR_TIPO[a['tipo']])
        marcas = [st.checkbox(x, key=f"l_{a['id']}_{i}", value=bool(hecha), disabled=bool(hecha))
                  for i, x in enumerate(tx(a["items"]))]
        if hecha:
            st.success("✅ Reto completado")
        elif st.button("¡Listo!", key=f"lb_{a['id']}", disabled=not all(marcas), type="primary", use_container_width=True):
            responder(a, True, True, t)


def calculadora(a, t, hecha):
    perfil = st.session_state.rec["perfil"]
    D = C.DISPOSITIVOS
    kind = a["kind"]
    if kind == "reposo":
        cand = [d for d in D if D[d]["apagable"] and D[d]["w_reposo"] > 0]
        cand.sort(key=lambda d: d not in perfil["dispositivos"])
        d = st.selectbox("Aparato", cand, key=f"cd_{a['id']}", format_func=lambda k: f"{D[k]['emoji']} {D[k]['nombre']}")
        horas = st.slider("Horas al día prendido sin usar", 0.0, 24.0, 4.0, 0.5, key=f"ch_{a['id']}")
        r = L.calc("reposo", w=D[d]["w_reposo"], horas=horas)
    elif kind == "cargadores":
        n = st.slider("Cargadores enchufados sin usar", 1, 15, 4, key=f"cn_{a['id']}")
        r = L.calc("cargadores", n=n)
    else:
        cand = [d for d in ("cel", "tab", "lap")]
        cand.sort(key=lambda d: d not in perfil["dispositivos"])
        d = st.selectbox("Aparato", cand, key=f"cd_{a['id']}", format_func=lambda k: f"{D[k]['emoji']} {D[k]['nombre']}")
        horas = st.slider("Horas de pantalla al día", 0.0, 16.0, 4.0, 0.5, key=f"ch_{a['id']}")
        r = L.calc("brillo", w=D[d]["w"], horas=horas)
    cargas = r["kwh"] * 1000 / L.CELULAR_WH
    if t == "peque":
        st.markdown(f"### 🔋 × {L.fmt(cargas, 0)}")
        st.caption("Es la cantidad de cargas completas de celular que se gastan en un año.")
    elif t == "mayor":
        st.metric("Gasto al año", f"S/ {L.fmt(r['soles'], 1)}")
    else:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("kWh al año", L.fmt(r["kwh"], 1))
        m2.metric("Soles al año", f"S/ {L.fmt(r['soles'], 1)}")
        m3.metric("kg CO₂ al año", L.fmt(r["co2"], 1))
        m4.metric("Cargas de celular", L.fmt(cargas, 0))
    st.caption("Estimación con valores de referencia; no es una medición.")
    if hecha:
        st.success("✅ Hecha")
    elif st.button("Ya lo probé", key=f"cb_{a['id']}", type="primary", use_container_width=True):
        responder(a, True, True, t)


# ====================================================================== simulador RAEE
def anios(x):
    texto = str(int(x)) if x == int(x) else L.fmt(x, 1)
    return f"{texto} año" if x == 1 else f"{texto} años"


def nombre_comp(k):
    return "Reposo y cargadores" if k == "reposo" else C.DISPOSITIVOS[k]["nombre"]


def tab_simulador(t, U):
    perfil = st.session_state.rec["perfil"]
    S = C.SIM[t]
    st.subheader(S["titulo"])

    with st.expander("⚙️ " + ("Cambia las horas de uso para probar" if t != "mayor" else "Cambiar las horas de uso"), expanded=True):
        horas = dict(perfil["horas"])
        c = st.columns(2)
        for i, d in enumerate(dispositivos_con_horas(perfil)):
            info = C.DISPOSITIVOS[d]
            with c[i % 2]:
                horas[d] = st.slider(f"{info['emoji']} {info['nombre']}", 0.0, float(info["horas_max"]),
                                     float(perfil["horas"].get(d, info["horas_def"])), 0.5,
                                     key=f"sim_h_{d}_{perfil['horas'].get(d)}")
        extra_txt = {"peque": "¿Cuántos años más usarás tus aparatos?", "gamer": "Años extra de vida útil",
                     "tecnico": "Años adicionales de vida útil", "mayor": "¿Cuántos años más usará sus aparatos?"}[t]
        extra = st.slider(extra_txt, 0.5, 3.0, 1.0, 0.5, key="sim_extra")
    sim = L.simulador(dict(perfil, horas=horas), extra)
    etq = ETIQUETA_SALUD[t]
    izq, der = st.columns([1, 1.4], gap="large")

    with izq:
        for it in sim["inventario"]:
            st.progress(it["salud"] / 100, text=f"{it['emoji']} {it['nombre']}: {etq} {it['salud']} %")

    pct = f"{L.fmt(sim['pct_resid'], 0)} % menos"
    grafico = pd.DataFrame({"kWh por mes": {nombre_comp(k): v * 30 for k, v in sim["consumo"].items()}})
    with der:
        if t == "peque":
            if sim["ev_kwh_dia"] > 0.005:
                st.info("🎮 " + S["energia"].format(horas=L.fmt(sim["horas_consola_dia"])))
                st.info("📱 " + S["cargas"].format(cargas=L.fmt(sim["cargas_celular_dia"], 0)))
            else:
                st.success("🏆 " + S["cero"])
            st.warning("🗑️ " + S["chatarra"].format(kg=L.fmt(sim["resid"]), botellas=L.fmt(sim["botellas"], 0)))
            st.success("🌱 " + S["extra"].format(extra=anios(extra), kg_extra=L.fmt(sim["resid_extra"])))
        elif t == "gamer":
            if sim["ev_kwh_dia"] > 0.005:
                st.info("🎮 " + S["energia"].format(kwh_mes=L.fmt(sim["ev_kwh_dia"] * 30), horas_mes=L.fmt(sim["horas_consola_dia"] * 30, 0)))
                st.info("📱 " + S["cargas"].format(cargas_mes=L.fmt(sim["cargas_celular_dia"] * 30, 0)))
            else:
                st.success("🏆 " + S["cero"])
            st.warning("🗑️ " + S["chatarra"].format(kg=L.fmt(sim["resid"])))
            st.success("🌱 " + S["extra"].format(extra=anios(extra), kg_extra=L.fmt(sim["resid_extra"]), pct=pct))
            st.bar_chart(grafico)
        elif t == "tecnico":
            m1, m2, m3 = st.columns(3)
            m1.metric("Consumo anual", f"{L.fmt(sim['kwh_anio'], 0)} kWh")
            m2.metric("Huella eléctrica", f"{L.fmt(sim['co2_anio'], 0)} kg CO₂")
            m3.metric("Costo anual", f"S/ {L.fmt(sim['soles_anio'], 0)}")
            m4, m5, m6 = st.columns(3)
            m4.metric("Evitable", f"{L.fmt(sim['ev_kwh_anio'], 0)} kWh")
            m5.metric("Residuo anual", f"{L.fmt(sim['resid'])} kg")
            m6.metric("CO₂e de fabricación", f"{L.fmt(sim['fab'], 0)} kg/año")
            st.write(S["evitable"].format(ev_kwh=L.fmt(sim["ev_kwh_anio"], 0), ev_soles=L.fmt(sim["ev_soles"], 0), ev_co2=L.fmt(sim["ev_co2"], 0)))
            st.write(S["residuo"].format(kg=L.fmt(sim["resid"]), extra=anios(extra), kg_extra=L.fmt(sim["resid_extra"]), pct=pct))
            st.write(S["fab"].format(fab=L.fmt(sim["fab"], 0), fab_extra=L.fmt(sim["fab_extra"], 0)))
            st.bar_chart(grafico)
        else:
            st.write("💡 " + S["gasto"].format(soles_mes=L.fmt(sim["soles_anio"] / 12, 0)))
            ev_mes = sim["ev_soles"] / 12
            if ev_mes >= 0.5:
                st.warning(S["evitable"].format(ev_mes=L.fmt(ev_mes, 0)))
            else:
                st.success(S["cero"])
            st.info("🌱 " + S["chatarra"].format(extra=anios(extra)))
    st.caption("Estimaciones con potencias, vidas útiles y precios de referencia; no son mediciones de tus equipos.")


# ====================================================================== misiones, pactos y compromisos
def desafio_infinito(t):
    s = st.session_state
    rec = s.rec
    rec.setdefault("desafio", {"mejor": 0, "aciertos": 0, "total": 0})
    s.setdefault("d_seed", random.randint(1, 10**6))
    s.setdefault("d_racha", 0)
    s.setdefault("d_resp", None)
    q = L.pregunta_desafio(s.d_seed, t, rec["perfil"].get("dispositivos"))
    d = rec["desafio"]
    c = st.columns(3)
    c[0].metric("Racha actual", s.d_racha)
    c[1].metric("Mejor racha", d["mejor"])
    c[2].metric("Aciertos totales", d["aciertos"])
    st.markdown(f"<div class='eco-q' style='--mark:\"{q['emoji']}\"'><div class='eco-emoji'>{q['emoji']}</div>"
                f"<div class='eco-title'>{esc(q['enunciado'])}</div></div>", unsafe_allow_html=True)
    if s.d_resp is None:
        cols = st.columns(2)
        for i, op in enumerate(q["opciones"]):
            if cols[i % 2].button(op, key=f"d_{s.d_seed}_{i}", use_container_width=True):
                ok = i == q["correcta"]
                s.d_resp = i
                d["total"] += 1
                if ok:
                    d["aciertos"] += 1
                    s.d_racha += 1
                    d["mejor"] = max(d["mejor"], s.d_racha)
                else:
                    s.d_racha = 0
                guardar()
                st.rerun()
    else:
        ok = s.d_resp == q["correcta"]
        banner_resultado(ok, f"{q['explica']}  La respuesta era {q['opciones'][q['correcta']]}.", t)
        if st.button("Otra pregunta ➡", key="d_otra", type="primary", use_container_width=True):
            s.d_seed = random.randint(1, 10**6)
            s.d_resp = None
            st.rerun()
    st.caption("Las preguntas se generan con números al azar cada vez, así que nunca se acaban.")


def reto_dia(t):
    s = st.session_state
    rec = s.rec
    r = L.reto_del_dia(rec, t)
    if not r:
        st.info("Completa el cuestionario inicial para recibir un reto cada día.")
        return
    tip = r["tip"]
    hoy = date.today().isoformat()
    hecho = hoy in rec.setdefault("diario", {})
    c1, c2 = COLORES[tip["categoria"]]
    tarjeta(c1, c2, tip["emoji"], "Reto del día", date.today().strftime("%d/%m"), tip["emoji"], r["titulo"], r["corto"],
            f"<div class='eco-reto'>🎯 {esc(L.reto_para(tip, t))}</div>", ilus=IL.clave_tip(tip["id"], tip["categoria"]), var="poster")
    st.caption(f"Días seguidos cumpliendo el reto: {L.racha_diaria(rec)} · cada reto cumplido da {L.XP_DIARIO} XP. Mañana habrá otro distinto.")
    if hecho:
        st.success("Reto de hoy cumplido. Vuelve mañana.")
    elif st.button("✅ Hoy lo cumplí", key="reto_hoy", type="primary", use_container_width=True):
        rec["diario"][hoy] = True
        guardar()
        avisar(f"+{L.XP_DIARIO} XP", "🔥", globos=True)
        st.rerun()


def tabla_clase():
    s = st.session_state
    rec = s.rec
    st.write("**Los 10 con más XP**")
    filas = L.tabla_clase()
    if not filas:
        st.caption("Aún no hay nadie en la tabla. Completa el cuestionario inicial para aparecer.")
    for i, (u, xp, nivel, mejor) in enumerate(filas, 1):
        medalla = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
        yo = " ← tú" if u == s.usuario else ""
        st.markdown(f"**{medalla} {esc(u)}**{yo} · {xp} XP · nivel {nivel} · mejor racha {mejor}")
    oculto = st.checkbox("No quiero aparecer en la tabla", value=bool(rec.get("oculto_ranking")), key="oculto")
    if oculto != bool(rec.get("oculto_ranking")):
        rec["oculto_ranking"] = oculto
        guardar()
        st.rerun()


def linea_dia(bloques):
    mapa = R.mapa_horas(bloques)
    celdas = ""
    for h, (tipo, desp) in enumerate(mapa):
        col = R.TIPOS[tipo][2] if tipo else "rgba(127,127,127,.25)"
        borde = "box-shadow: inset 0 -5px 0 #ef4444;" if desp else ""
        celdas += f"<div title='{h:02d}:00' style='flex:1;height:34px;background:{col};{borde}'></div>"
    marcas = "".join(f"<span style='flex:1;font-size:.65rem;opacity:.7'>{h if h % 3 == 0 else ''}</span>" for h in range(24))
    leyenda = "".join(f"<span class='eco-chip' style='background:{c}22;border:1px solid {c}'>{e} {n}</span>" for e, n, c in R.TIPOS.values())
    st.markdown(f"<div style='display:flex;border-radius:10px;overflow:hidden'>{celdas}</div>"
                f"<div style='display:flex'>{marcas}</div>"
                f"<div style='margin-top:6px'>{leyenda}<span class='eco-chip' style='border:1px solid #ef4444'>🟥 Equipo encendido sin uso</span></div>",
                unsafe_allow_html=True)


def tab_dia(t, U):
    s = st.session_state
    rec = s.rec
    perfil = rec["perfil"]
    ocup = R.OCUPACIONES[rec["edad"]]
    st.markdown("### 🗓️ Mi día")
    st.caption("Cuéntanos cómo es tu día. Tus horas de estudio o trabajo se respetan: la app solo busca la energía que se pierde dentro de ellas.")
    r = rec.get("rutina")
    claves = list(ocup)
    actual = r["ocupacion"] if r and r["ocupacion"] in ocup else claves[0]
    c1, c2 = st.columns([2, 1])
    nueva = c1.selectbox("¿A qué te dedicas?", claves, index=claves.index(actual), format_func=lambda k: ocup[k], key="oc_sel")
    if c2.button("Empezar con un ejemplo", use_container_width=True, key="oc_ej"):
        rec["rutina"] = {"ocupacion": nueva, "bloques": R.plantilla(nueva, perfil.get("dispositivos"))}
        for k in [k for k in s if str(k).startswith("b_")]:
            del s[k]
        guardar()
        st.rerun()
    if not r:
        st.info("Pulsa «Empezar con un ejemplo» y ajústalo a tu día real.")
        return
    bloques = r["bloques"]
    resumen = st.container()      # el resumen va arriba, pero se calcula con lo ya guardado
    mios = [d for d in (perfil.get("dispositivos") or list(C.DISPOSITIVOS)) if d in C.DISPOSITIVOS]
    opciones = mios + list(R.PSEUDO)
    nombre = lambda k: f"{R._d(k)['emoji']} {R._d(k)['nombre']}"
    st.write("**Edita tus bloques**")
    with st.form("form_rutina"):
        nuevos = []
        for i, b in enumerate(bloques):
            e, n, _ = R.TIPOS[b["tipo"]]
            with st.expander(f"{e} {n} · {R.hora(b['ini'])} a {R.hora(b['fin'])}", expanded=False):
                a1, a2, a3 = st.columns(3)
                tipo = a1.selectbox("Actividad", list(R.TIPOS), index=list(R.TIPOS).index(b["tipo"]),
                                    format_func=lambda k: R.TIPOS[k][1], key=f"b_t{i}")
                ini = a2.number_input("Desde (hora)", 0, 23, int(b["ini"]), key=f"b_i{i}")
                fin = a3.number_input("Hasta (hora)", 0, 23, int(b["fin"]), key=f"b_f{i}")
                usa = st.multiselect("Aparatos que usas", mios, default=[d for d in b["usa"] if d in mios], format_func=nombre, key=f"b_u{i}")
                quedan = st.multiselect("Aparatos que quedan encendidos sin usarse", opciones,
                                        default=[d for d in b["quedan"] if d in opciones], format_func=nombre, key=f"b_q{i}")
                quitar = st.checkbox("Quitar este bloque", key=f"b_x{i}")
            if not quitar:
                nuevos.append({"tipo": tipo, "ini": int(ini), "fin": int(fin), "usa": usa, "quedan": quedan})
        if st.form_submit_button("💾 Guardar mi día", use_container_width=True, type="primary"):
            rec["rutina"] = {"ocupacion": nueva, "bloques": [b for b in nuevos if R.duracion(b) > 0]}
            for k in [k for k in s if str(k).startswith("b_")]:
                del s[k]
            guardar()
            avisar("Tu día quedó guardado", "🗓️")
            st.rerun()
    if st.button("➕ Agregar un bloque", key="dia_mas"):
        bloques.append({"tipo": "descanso", "ini": 12, "fin": 13, "usa": [], "quedan": []})
        guardar()
        st.rerun()

    with resumen:
        a = R.analizar(bloques, t)
        linea_dia(bloques)
        m = st.columns(3)
        m[0].metric("Horas de estudio o trabajo", f"{a['enfocadas']} h", help="Se respetan: la app no te pide reducirlas.")
        m[1].metric("Energía evitable al año", f"{L.fmt(a['kwh_anio'], 0)} kWh", help="Estimación con valores referenciales.")
        m[2].metric("Equivale a", f"S/ {L.fmt(a['soles'], 0)}", f"{L.fmt(a['co2'], 0)} kg de CO₂", delta_color="off")
        st.write("**Tus consejos de hoy, con hora**")
        if not a["consejos"]:
            st.success("Con lo que marcaste no hay energía evitable. Si cambia tu día, vuelve a ajustar los bloques.")
        for c in a["consejos"][:6]:
            st.markdown(f"<div class='lado'><b>{c['emoji']} {c['rango']}</b><br>{esc(c['texto'])}"
                        f"<br><span style='opacity:.7;font-size:.85rem'>≈ {L.fmt(c['kwh'], 1)} kWh al año · S/ {L.fmt(L.soles(c['kwh']), 1)}</span></div>",
                        unsafe_allow_html=True)
        st.caption("Estimación: usa la potencia en reposo de cada aparato (valores referenciales) por las horas que marcaste.")


def tab_desafio(t):
    a, b, c = st.tabs(["📅 Reto del día", "⚡ Desafío infinito", "🏆 Tabla"])
    with a:
        reto_dia(t)
    with b:
        desafio_infinito(t)
    with c:
        tabla_clase()


def tab_misiones(t, U):
    s = st.session_state
    rec = s.rec
    perfil = rec["perfil"]
    prog = L.progreso(rec)
    juego = t in ("peque", "gamer")

    st.subheader(U["mis_titulo"])
    if not rec["retos"]:
        st.info(U["mis_vacio"])

    hecho = {"kwh": 0.0, "co2": 0.0, "soles": 0.0, "residuo": 0.0}
    pend = {"kwh": 0.0, "co2": 0.0, "soles": 0.0, "residuo": 0.0}
    for tid, cumplido in list(rec["retos"].items()):
        tip = T.TIPS_POR_ID.get(tid)
        if tip is None:
            continue
        imp = L.impacto_mision(tid, perfil)
        nuevo = st.checkbox(f"{tip['emoji']} {L.reto_para(tip, t)}", value=cumplido, key=f"chk_reto_{tid}")
        if juego:
            st.caption(f"{U['mis_hecha']} = +{L.xp_mision(tid, perfil)} XP")
        elif t == "tecnico":
            partes = []
            if imp["kwh"] > 0.05:
                partes.append(f"{L.fmt(imp['kwh'])} kWh/año · S/ {L.fmt(imp['soles'], 0)}")
            if imp["residuo"] > 0.005:
                partes.append(f"{L.fmt(imp['residuo'], 2)} kg de residuo evitado/año")
            if imp["co2"] > 0.05:
                partes.append(f"{L.fmt(imp['co2'])} kg CO₂e/año")
            st.caption(" · ".join(partes) if partes else "Impacto cualitativo: informa y reduce barreras.")
        elif imp["soles"] >= 0.5:
            st.caption(f"Ahorro estimado: S/ {L.fmt(imp['soles'], 0)} al año")
        if nuevo != cumplido:
            antes = L.progreso(rec)["nivel"]
            rec["retos"][tid] = nuevo
            guardar()
            if nuevo:
                avisar(f"{U['mis_hecha']}: +{L.xp_mision(tid, perfil)} XP", "🏆", globos=L.progreso(rec)["nivel"] > antes)
            st.rerun()
        acum = hecho if nuevo else pend
        for k in acum:
            acum[k] += imp[k]

    if rec["retos"] and t == "tecnico":
        st.write("**Métricas estimadas de tus pactos**")
        m1, m2 = st.columns(2)
        m1.metric("Cumplidos", f"{L.fmt(hecho['kwh'])} kWh/año", f"{L.fmt(hecho['co2'])} kg CO₂e · S/ {L.fmt(hecho['soles'], 0)}")
        m2.metric("Pendientes", f"{L.fmt(pend['kwh'])} kWh/año", f"{L.fmt(pend['co2'])} kg CO₂e · S/ {L.fmt(pend['soles'], 0)}")
        st.caption(f"Residuo electrónico evitado al año: {L.fmt(hecho['residuo'], 2)} kg cumplidos y {L.fmt(pend['residuo'], 2)} kg pendientes.")
    elif rec["retos"] and t == "mayor":
        texto = f"Lleva **{len(prog['hechas'])} de {len(rec['retos'])}** compromisos cumplidos."
        total_soles = hecho["soles"] + pend["soles"]
        if total_soles >= 0.5:
            texto += f" Si cumple todos, ahorraría unos **S/ {L.fmt(total_soles, 0)} al año**."
        st.write(texto)
    elif rec["retos"] and t == "peque":
        st.write(f"¡Llevas **{len(prog['hechas'])} de {len(rec['retos'])}** misiones cumplidas!")

    st.write(f"**{U['insignias']}**")
    cols = st.columns(5)
    for i, b in enumerate(L.insignias(rec, t)):
        clase = "eco-badge" if b["ok"] else "eco-badge eco-off"
        emo = b["emoji"] if b["ok"] else "🔒"
        cols[i % 5].markdown(f"<div class='{clase}'><div class='e'>{emo}</div><div class='n'>{esc(b['nombre'])}</div></div>",
                             unsafe_allow_html=True)


# ====================================================================== diagnóstico, registro semanal y prueba de guardado
def panel_guardado(t):
    """Prueba visible de que los datos están en el disco."""
    s = st.session_state
    rec = s.rec
    ver = L.verificar_guardado(s.usuario, rec)
    st.markdown("#### 💾 Prueba de guardado")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Días en el archivo", ver["dias_en_disco"])
    c2.metric("Última fecha guardada", ver["ultimo_dia"] or "—")
    c3.metric("Actividades en el archivo", ver["actividades_en_disco"])
    c4.metric("Pantalla = archivo", "Sí ✔" if ver["coincide"] else "No ⚠️")
    st.caption(f"Archivo: {ver['ruta']} · {ver['bytes']} bytes · modificado {ver['modificado']}")
    d1, d2 = st.columns(2)
    d1.download_button("⬇️ Descargar registro semanal (CSV, abre en Excel)", L.csv_registros(rec),
                       file_name=f"ecofeed_registro_{s.usuario}.csv", mime="text/csv", use_container_width=True,
                       disabled=not rec["registros"])
    d2.download_button("⬇️ Descargar copia de mis datos (JSON)", L.json_respaldo(rec, s.usuario),
                       file_name=f"ecofeed_datos_{s.usuario}.json", mime="application/json", use_container_width=True)
    with st.expander("🎓 Cómo demostrar que se guarda (para la exposición)"):
        st.markdown(
            "1. Guarda el día de hoy y mira cómo cambia **Días en el archivo** y la hora de modificación.\n"
            "2. Cierra la pestaña y detén la app en la terminal con `Ctrl+C`.\n"
            "3. Vuelve a ejecutar `streamlit run app.py` e inicia sesión con el mismo usuario.\n"
            "4. El registro, los puntos y las actividades siguen ahí: se leen del archivo, no de la memoria.\n"
            "5. Muestra el archivo `datos/usuarios.json` abierto (la contraseña está cifrada) o descarga el CSV."
        )


def tab_consumo(t, U):
    s = st.session_state
    rec = s.rec
    perfil = rec["perfil"]
    idx = L.indice_verde(L.media_practicas(perfil))

    izq, der = st.columns([1, 1.3], gap="large")
    with izq:
        st.subheader(U["idx_titulo"])
        st.markdown(f"<div class='eco-bar energia'><div style='width:{idx}%'></div></div>", unsafe_allow_html=True)
        st.metric("Puntaje", f"{idx} / 100")
        st.write(L.texto_resultado(perfil, t))
    with der:
        st.write(f"**{U['habitos_titulo']}**")
        claves = list(C.HABITOS)
        datos = {"Tú": [perfil["habitos"].get(k, 3) for k in claves]}
        if t in ("gamer", "tecnico"):
            datos["Estudio"] = [C.HABITOS[k]["media_estudio"] for k in claves]
        st.bar_chart(pd.DataFrame(datos, index=[L.titulo_habito(k, t) for k in claves]), horizontal=True)

    st.divider()
    st.subheader(U["reg_titulo"])
    hoy = date.today()
    previo = rec["registros"].get(hoy.isoformat(), perfil["horas"])
    f1, f2 = st.columns([1, 1.3], gap="large")
    with f1:
        with st.form("form_dia"):
            vals = {}
            for d in dispositivos_con_horas(perfil):
                vals[d] = entrada_horas(d, float(previo.get(d, C.DISPOSITIVOS[d]["horas_def"])), t, f"reg_{d}")
            ok = st.form_submit_button(U["reg_boton"], use_container_width=True, type="primary")
        if ok:
            ver = L.guardar_dia(s.usuario, rec, vals, hoy)
            if ver["coincide"]:
                st.success(f"✅ Guardado y verificado en el archivo: {ver['dias_en_disco']} día(s), modificado {ver['modificado']}.")
                st.toast("Día guardado", icon="💾")
            else:
                st.error("No se pudo comprobar el guardado en el archivo.")
    with f2:
        cab = st.columns(7)
        for col, (d, et, ok_, kwh) in zip(cab, L.semana(rec)):
            col.markdown(f"<div class='eco-week'><div class='{'on' if ok_ else ''}'>{et}<br>{d.day}</div></div>", unsafe_allow_html=True)
            col.caption(f"{L.fmt(kwh, 1)} kWh" if ok_ else "—")
        filas = L.historial_filas(rec)
        if filas:
            df = pd.DataFrame(filas).set_index("fecha")[["kwh_dia"]].rename(columns={"kwh_dia": "kWh por día"})
            st.bar_chart(df)
        else:
            st.info(U["reg_vacio"])
    st.divider()
    panel_guardado(t)


# ====================================================================== perfil
def tab_perfil(t, U):
    s = st.session_state
    rec = s.rec
    perfil = rec["perfil"]
    edad = C.EDADES[rec["edad"]]
    st.subheader(f"{edad['emoji']} {s.usuario}")

    izq, der = st.columns(2, gap="large")
    with izq:
        st.write("**Mi edad y mi nivel de estudios**")
        st.caption("Con estos datos cambia el lenguaje de los textos.")
        claves_edad, claves_grado = list(C.EDADES), list(C.GRADOS)
        nueva_edad = st.selectbox("Grupo de edad", claves_edad, index=claves_edad.index(rec["edad"]),
                                  format_func=lambda k: f"{C.EDADES[k]['emoji']} {C.EDADES[k]['etiqueta']}", key="perfil_edad")
        nuevo_grado = st.selectbox("Nivel de estudios", claves_grado, index=claves_grado.index(rec["grado"]),
                                   format_func=lambda k: C.GRADOS[k], key="perfil_grado")
        if st.button("Guardar cambios", use_container_width=True):
            rec["edad"], rec["grado"] = nueva_edad, nuevo_grado
            s.feed_i = 0
            s.pop("feed", None)
            guardar()
            st.rerun()
        c1, c2 = st.columns(2)
        if c1.button(U["repetir"], use_container_width=True):
            perfil["onboarded"] = False
            s.paso = 0
            guardar()
            st.rerun()
        if c2.button(U["salir"], use_container_width=True):
            for k in ("usuario", "rec", "paso", "feed", "feed_t", "feed_i", "mostrar_resultado", "leccion"):
                s.pop(k, None)
            st.rerun()
    with der:
        with st.expander(U["datos"], expanded=True):
            for texto, fuente in C.DATOS_INFORME:
                st.write(f"• {texto} *({fuente})*")
            st.caption("Informe: nivel de conocimiento y prácticas de informática verde en estudiantes de "
                       "Ingeniería de Sistemas de la Universidad Nacional de Trujillo (n = 32).")


# ====================================================================== principal
def main():
    s = st.session_state
    if not s.get("usuario") and st.query_params.get("u") and st.query_params.get("s"):
        rec = L.validar_sesion(st.query_params["u"], st.query_params["s"])
        if rec:
            s.usuario, s.rec, s.paso, s.feed_i, s.mostrar_resultado = st.query_params["u"].strip().lower(), rec, 0, 0, False
        else:
            st.query_params.clear()
    if not s.get("usuario"):
        estilos("tecnico")
        fondo()
        pantalla_login()
        return
    if s.get("es_admin"):
        estilos("tecnico")
        fondo()
        if st.button("Cerrar sesión", key="salir_adm"):
            s.clear()
            st.rerun()
        PA.panel_admin()
        return
    t = L.tono(s.rec)
    U = C.UI[t]
    estilos(t)
    mostrar_avisos()
    fondo()
    if not s.rec["perfil"].get("onboarded"):
        pantalla_onboarding()
        return
    if s.get("mostrar_resultado"):
        pantalla_resultado()
        return
    col_hud, col_main = st.columns([1, 3.2], gap="large")
    with col_hud:
        st.markdown("### 🌱 EcoFeed")
        hud(t)
        if st.button("Cerrar sesión", key="salir", use_container_width=True):
            L.cerrar_sesion(s.usuario)
            st.query_params.clear()
            s.clear()
            st.rerun()
    with col_main:
        tabs = st.tabs([U["tab_feed"], U["tab_sim"], U["tab_mis"], U["tab_consumo"], U["tab_perfil"], "🗓️ Mi día", "⚡ Desafío", "🎮 Pausa"])
        with tabs[0]:
            tab_feed(t, U)
        with tabs[1]:
            tab_simulador(t, U)
        with tabs[2]:
            tab_misiones(t, U)
        with tabs[3]:
            tab_consumo(t, U)
        with tabs[4]:
            tab_perfil(t, U)
        with tabs[5]:
            tab_dia(t, U)
        with tabs[6]:
            tab_desafio(t)
        with tabs[7]:
            st.markdown("### 🎮 Pausa")
            st.caption("Un brote que esquiva residuos electrónicos. Juego propio, hecho para EcoFeed.")
            components.html(J.HTML, height=300)


main()
