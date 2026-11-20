"""Ilustraciones originales en SVG para las tarjetas (hechas a mano, sin personajes ni marcas).

Cada dibujo usa dos colores: W (trazo principal, blanco) y A (acento). El acento cambia con el tono:
amarillo y con destellos para primaria y secundaria; verde menta y sobrio para adultos y mayores.
No se dibujan caras ni se da vida a los objetos.
"""

# Los dibujos van en un lienzo de 240 x 200.
ARTE = {
    "power": '<path d="M82 62 A58 58 0 1 0 158 62" fill="none" stroke="{W}" stroke-width="12" stroke-linecap="round"/><line x1="120" y1="30" x2="120" y2="98" stroke="{A}" stroke-width="14" stroke-linecap="round"/>',
    "reloj": '<circle cx="120" cy="100" r="64" fill="none" stroke="{W}" stroke-width="10"/><line x1="120" y1="100" x2="120" y2="58" stroke="{A}" stroke-width="10" stroke-linecap="round"/><line x1="120" y1="100" x2="152" y2="116" stroke="{W}" stroke-width="10" stroke-linecap="round"/><circle cx="120" cy="100" r="8" fill="{A}"/>',
    "pantalla": '<rect x="78" y="22" width="84" height="156" rx="16" fill="none" stroke="{W}" stroke-width="9"/><circle cx="120" cy="100" r="20" fill="{A}"/><g stroke="{A}" stroke-width="7" stroke-linecap="round"><line x1="120" y1="62" x2="120" y2="52"/><line x1="120" y1="138" x2="120" y2="148"/><line x1="82" y1="100" x2="92" y2="100"/><line x1="148" y1="100" x2="158" y2="100"/></g><line x1="108" y1="164" x2="132" y2="164" stroke="{W}" stroke-width="6" stroke-linecap="round"/>',
    "luna": '<path d="M150 40 A62 62 0 1 0 190 120 A50 50 0 0 1 150 40 Z" fill="{W}"/><circle cx="62" cy="52" r="7" fill="{A}"/><circle cx="196" cy="62" r="5" fill="{A}"/><circle cx="170" cy="30" r="4" fill="{A}"/>',
    "enchufe": '<rect x="82" y="86" width="76" height="62" rx="16" fill="{W}"/><rect x="100" y="40" width="12" height="52" rx="5" fill="{A}"/><rect x="128" y="40" width="12" height="52" rx="5" fill="{A}"/><path d="M120 148 V170 Q120 188 142 188 H190" fill="none" stroke="{W}" stroke-width="10" stroke-linecap="round"/>',
    "regleta": '<rect x="30" y="92" width="180" height="46" rx="14" fill="{W}"/><rect x="52" y="104" width="22" height="22" rx="6" fill="{A}"/><rect x="92" y="104" width="22" height="22" rx="6" fill="{A}"/><rect x="132" y="104" width="22" height="22" rx="6" fill="{A}"/><circle cx="184" cy="115" r="9" fill="{A}"/><path d="M30 115 H16 Q8 115 8 125 V150" fill="none" stroke="{W}" stroke-width="8" stroke-linecap="round"/>',
    "laptop": '<rect x="52" y="38" width="136" height="92" rx="10" fill="none" stroke="{W}" stroke-width="9"/><rect x="68" y="54" width="104" height="60" rx="4" fill="{A}" opacity="0.35"/><path d="M26 148 H214 L200 136 H40 Z" fill="{W}"/><line x1="76" y1="72" x2="132" y2="72" stroke="{A}" stroke-width="7" stroke-linecap="round"/><line x1="76" y1="92" x2="112" y2="92" stroke="{A}" stroke-width="7" stroke-linecap="round"/>',
    "consola": '<rect x="34" y="70" width="172" height="88" rx="44" fill="{W}"/><rect x="70" y="102" width="34" height="10" rx="4" fill="{A}"/><rect x="82" y="90" width="10" height="34" rx="4" fill="{A}"/><circle cx="152" cy="98" r="9" fill="{A}"/><circle cx="174" cy="118" r="9" fill="{A}"/>',
    "tv": '<rect x="34" y="44" width="172" height="104" rx="12" fill="none" stroke="{W}" stroke-width="9"/><rect x="50" y="60" width="140" height="72" rx="4" fill="{A}" opacity="0.4"/><path d="M92 176 H148 M120 148 V176" fill="none" stroke="{W}" stroke-width="9" stroke-linecap="round"/><polygon points="108,82 108,112 138,97" fill="{W}"/>',
    "router": '<rect x="40" y="118" width="160" height="42" rx="12" fill="{W}"/><circle cx="66" cy="139" r="6" fill="{A}"/><circle cx="86" cy="139" r="6" fill="{A}"/><line x1="70" y1="118" x2="62" y2="72" stroke="{W}" stroke-width="8" stroke-linecap="round"/><line x1="170" y1="118" x2="178" y2="72" stroke="{W}" stroke-width="8" stroke-linecap="round"/><path d="M96 92 A34 34 0 0 1 144 92" fill="none" stroke="{A}" stroke-width="8" stroke-linecap="round"/><path d="M108 104 A18 18 0 0 1 132 104" fill="none" stroke="{A}" stroke-width="8" stroke-linecap="round"/><circle cx="120" cy="112" r="5" fill="{A}"/>',
    "campana": '<path d="M120 36 C84 36 78 74 78 100 C78 124 62 136 62 144 H178 C178 136 162 124 162 100 C162 74 156 36 120 36 Z" fill="{W}"/><circle cx="120" cy="164" r="12" fill="{A}"/><line x1="120" y1="24" x2="120" y2="36" stroke="{W}" stroke-width="8" stroke-linecap="round"/>',
    "avion": '<path d="M30 112 L212 40 L170 168 L122 124 L100 156 L92 118 Z" fill="{W}"/><path d="M92 118 L212 40 L122 124 Z" fill="{A}"/>',
    "bateria": '<rect x="38" y="64" width="150" height="84" rx="16" fill="none" stroke="{W}" stroke-width="9"/><rect x="192" y="90" width="16" height="32" rx="5" fill="{W}"/><rect x="54" y="80" width="34" height="52" rx="6" fill="{A}"/><rect x="95" y="80" width="34" height="52" rx="6" fill="{A}"/><rect x="136" y="80" width="34" height="52" rx="6" fill="{A}" opacity="0.35"/>',
    "termometro": '<rect x="104" y="28" width="32" height="112" rx="16" fill="{W}"/><circle cx="120" cy="150" r="30" fill="{W}"/><circle cx="120" cy="150" r="17" fill="{A}"/><rect x="114" y="74" width="12" height="76" rx="6" fill="{A}"/><g stroke="{A}" stroke-width="6" stroke-linecap="round"><line x1="154" y1="50" x2="172" y2="50"/><line x1="154" y1="74" x2="172" y2="74"/><line x1="154" y1="98" x2="172" y2="98"/></g>',
    "audifonos": '<path d="M52 118 V104 A68 68 0 0 1 188 104 V118" fill="none" stroke="{W}" stroke-width="12" stroke-linecap="round"/><rect x="40" y="112" width="34" height="58" rx="14" fill="{A}"/><rect x="166" y="112" width="34" height="58" rx="14" fill="{A}"/>',
    "herramienta": '<g transform="rotate(45 120 100)"><rect x="110" y="22" width="20" height="156" rx="10" fill="{W}"/><rect x="100" y="22" width="40" height="30" rx="8" fill="{W}"/></g><g transform="rotate(-45 120 100)"><rect x="112" y="22" width="16" height="156" rx="8" fill="{A}"/><rect x="104" y="150" width="32" height="28" rx="6" fill="{A}"/></g>',
    "escudo": '<path d="M120 28 L184 52 V104 C184 140 156 164 120 178 C84 164 56 140 56 104 V52 Z" fill="{W}"/><path d="M120 52 L160 66 V104 C160 128 142 144 120 154 Z" fill="{A}" opacity="0.55"/>',
    "ciclo": '<path d="M62 96 A58 58 0 0 1 164 62" fill="none" stroke="{W}" stroke-width="12" stroke-linecap="round"/><polygon points="176,36 182,86 136,68" fill="{W}"/><path d="M178 104 A58 58 0 0 1 76 138" fill="none" stroke="{A}" stroke-width="12" stroke-linecap="round"/><polygon points="64,164 58,114 104,132" fill="{A}"/>',
    "decision": '<path d="M120 176 V116 M120 116 L72 70 M120 116 L168 70" fill="none" stroke="{W}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/><circle cx="72" cy="62" r="20" fill="{A}"/><circle cx="168" cy="62" r="20" fill="{W}"/><circle cx="120" cy="180" r="9" fill="{A}"/>',
    "hoja": '<path d="M120 28 C186 52 196 130 120 172 C44 130 54 52 120 28 Z" fill="{W}"/><path d="M120 172 V70" stroke="{A}" stroke-width="8" stroke-linecap="round"/><path d="M120 108 L92 84 M120 130 L150 104" stroke="{A}" stroke-width="7" stroke-linecap="round"/>',
    "reciclaje": '<path d="M76 76 H164 L154 172 H86 Z" fill="{W}"/><rect x="66" y="58" width="108" height="16" rx="6" fill="{A}"/><rect x="104" y="44" width="32" height="14" rx="5" fill="{A}"/><path d="M100 118 A20 20 0 0 1 138 112" fill="none" stroke="{A}" stroke-width="7" stroke-linecap="round"/><polygon points="146,102 146,126 124,118" fill="{A}"/><path d="M140 140 A20 20 0 0 1 102 146" fill="none" stroke="{A}" stroke-width="7" stroke-linecap="round" opacity="0.6"/>',
    "pila": '<rect x="82" y="46" width="76" height="132" rx="14" fill="{W}"/><rect x="104" y="30" width="32" height="18" rx="5" fill="{A}"/><rect x="82" y="116" width="76" height="62" rx="14" fill="{A}" opacity="0.55"/><line x1="104" y1="82" x2="136" y2="82" stroke="{A}" stroke-width="9" stroke-linecap="round"/><line x1="120" y1="66" x2="120" y2="98" stroke="{A}" stroke-width="9" stroke-linecap="round"/>',
    "caja": '<path d="M46 84 L120 54 L194 84 V160 L120 184 L46 160 Z" fill="{W}"/><path d="M46 84 L120 112 L194 84" fill="none" stroke="{A}" stroke-width="8" stroke-linejoin="round"/><path d="M120 112 V184" stroke="{A}" stroke-width="8"/><rect x="96" y="64" width="48" height="14" rx="4" fill="{A}" transform="rotate(14 120 70)"/>',
    "carpeta": '<path d="M42 62 H96 L112 82 H198 V162 H42 Z" fill="{W}"/><rect x="62" y="100" width="116" height="10" rx="5" fill="{A}"/><rect x="62" y="124" width="78" height="10" rx="5" fill="{A}"/>',
    "correo": '<rect x="38" y="56" width="164" height="112" rx="14" fill="{W}"/><path d="M44 66 L120 124 L196 66" fill="none" stroke="{A}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>',
    "musica": '<path d="M96 146 V48 L176 30 V128" fill="none" stroke="{W}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/><ellipse cx="78" cy="148" rx="24" ry="19" fill="{A}"/><ellipse cx="158" cy="130" rx="24" ry="19" fill="{A}"/>',
    "camara": '<rect x="34" y="66" width="120" height="84" rx="16" fill="{W}"/><path d="M162 98 L210 70 V146 L162 118 Z" fill="{A}"/><circle cx="64" cy="92" r="7" fill="{A}"/>',
    "megafono": '<path d="M46 88 H84 L170 44 V156 L84 112 H46 Z" fill="{W}"/><rect x="58" y="112" width="26" height="50" rx="8" fill="{A}"/><path d="M188 76 Q206 100 188 124" fill="none" stroke="{A}" stroke-width="9" stroke-linecap="round"/>',
    "globo": '<circle cx="120" cy="100" r="68" fill="none" stroke="{W}" stroke-width="9"/><ellipse cx="120" cy="100" rx="30" ry="68" fill="none" stroke="{W}" stroke-width="7"/><line x1="52" y1="100" x2="188" y2="100" stroke="{W}" stroke-width="7"/><path d="M62 66 H178 M62 134 H178" stroke="{W}" stroke-width="6" fill="none"/><circle cx="150" cy="78" r="12" fill="{A}"/>',
    "nube": '<path d="M70 146 A32 32 0 0 1 76 84 A48 48 0 0 1 168 76 A36 36 0 0 1 176 146 Z" fill="{W}"/><line x1="120" y1="168" x2="120" y2="122" stroke="{A}" stroke-width="11" stroke-linecap="round"/><polyline points="100,138 120,118 140,138" fill="none" stroke="{A}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>',
    "mito": '<path d="M120 26 L186 52 V108 C186 142 158 164 120 178 C82 164 54 142 54 108 V52 Z" fill="none" stroke="{W}" stroke-width="9"/><path d="M100 90 A20 20 0 1 1 134 104 Q120 112 120 128" fill="none" stroke="{A}" stroke-width="12" stroke-linecap="round"/><circle cx="120" cy="150" r="7" fill="{A}"/>',
    "pregunta": '<path d="M120 26 C84 26 66 54 66 80 C66 102 80 112 90 126 V142 H150 V126 C160 112 174 102 174 80 C174 54 156 26 120 26 Z" fill="{W}"/><rect x="94" y="152" width="52" height="12" rx="6" fill="{A}"/><rect x="104" y="170" width="32" height="10" rx="5" fill="{A}"/><path d="M104 84 L120 104 L136 84" fill="none" stroke="{A}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>',
    "calc": '<rect x="68" y="26" width="104" height="148" rx="14" fill="{W}"/><rect x="80" y="40" width="80" height="30" rx="6" fill="{A}"/><g fill="{A}" opacity="0.7"><circle cx="90" cy="96" r="8"/><circle cx="120" cy="96" r="8"/><circle cx="150" cy="96" r="8"/><circle cx="90" cy="124" r="8"/><circle cx="120" cy="124" r="8"/><circle cx="150" cy="124" r="8"/><circle cx="90" cy="152" r="8"/><circle cx="120" cy="152" r="8"/><circle cx="150" cy="152" r="8"/></g>',
    "check": '<rect x="62" y="34" width="116" height="146" rx="14" fill="{W}"/><rect x="92" y="24" width="56" height="22" rx="8" fill="{A}"/><polyline points="80,78 90,90 106,68" fill="none" stroke="{A}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><line x1="118" y1="80" x2="160" y2="80" stroke="{A}" stroke-width="7" stroke-linecap="round"/><polyline points="80,118 90,130 106,108" fill="none" stroke="{A}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><line x1="118" y1="120" x2="160" y2="120" stroke="{A}" stroke-width="7" stroke-linecap="round"/><line x1="80" y1="156" x2="160" y2="156" stroke="{A}" stroke-width="7" stroke-linecap="round" opacity="0.5"/>',
    "slider": '<rect x="34" y="94" width="172" height="12" rx="6" fill="{W}" opacity="0.5"/><rect x="34" y="94" width="104" height="12" rx="6" fill="{W}"/><circle cx="138" cy="100" r="24" fill="{A}"/><g stroke="{W}" stroke-width="6" stroke-linecap="round"><line x1="46" y1="136" x2="46" y2="152"/><line x1="90" y1="136" x2="90" y2="152"/><line x1="134" y1="136" x2="134" y2="152"/><line x1="178" y1="136" x2="178" y2="152"/></g>',
}

# Qué dibujo lleva cada recomendación.
POR_TIP = {
    "apagar_equipos": "power", "suspension_automatica": "reloj", "brillo": "pantalla", "modo_oscuro": "luna",
    "desconectar_cargadores": "enchufe", "regleta_interruptor": "regleta", "cerrar_apps": "laptop",
    "consola_apagado": "consola", "tv_ahorro": "tv", "router_noche": "router", "wifi_datos": "router",
    "notificaciones": "campana", "modo_avion_noche": "avion", "carga_80": "bateria", "calor_bateria": "termometro",
    "audifonos_cuidado": "audifonos", "reparar_ram_ssd": "herramienta", "limpiar_polvo": "laptop",
    "funda_protector": "escudo", "cambiar_bateria": "bateria", "reacondicionado": "ciclo",
    "comprar_necesidad": "decision", "etiqueta_eficiencia": "hoja", "cargador_usbc": "enchufe",
    "pilas_recargables": "pila", "reciclar_acopio": "reciclaje", "pilas_acopio": "pila", "guardar_raee": "caja",
    "donar_revender": "ciclo", "borrar_datos": "carpeta", "tienda_devolucion": "caja", "lista_inventario": "check",
    "depurar_archivos": "carpeta", "fotos_duplicadas": "carpeta", "bajar_spam": "correo",
    "streaming_calidad": "tv", "musica_descargada": "musica", "camara_videollamada": "camara",
    "enlaces_no_adjuntos": "nube", "actualizar_sistema": "ciclo", "software_eficiente": "laptop",
    "graficos_fps": "consola", "laptop_superficie": "laptop", "bateria_hinchada": "bateria",
    "campana": "megafono", "aprender_huella": "globo",
}

# Dibujo por tipo de actividad y excepciones por actividad.
POR_TIPO = {"mito": "mito", "quiz": "pregunta", "escenario": "decision", "adivina": "slider", "calc": "calc", "checklist": "check"}
POR_ACTIVIDAD = {
    "m_apagar_gasta": "power", "m_cargador_vacio": "enchufe", "m_carga_noche": "bateria", "m_salvapantallas": "pantalla",
    "m_nube": "nube", "m_celular_basura": "reciclaje", "m_reparar_caro": "herramienta", "m_metales": "reciclaje",
    "m_brillo": "pantalla", "m_reciclar_materiales": "reciclaje", "m_video_calidad": "tv", "m_oscuro": "luna",
    "m_reciclado_mundo": "globo", "m_peru_tratado": "globo", "m_pilas": "pila", "m_vida_util": "reloj",
    "q_pantalla": "pantalla", "q_raee": "reciclaje", "q_pilas": "pila", "q_vida_celular": "escudo",
    "q_modo_avion": "avion", "q_reciclaje_peru": "reciclaje",
    "e_cargador": "enchufe", "e_bateria": "bateria", "e_cajon": "caja", "e_video": "tv", "e_salir": "power",
    "e_pantalla_rota": "escudo", "e_nube": "nube", "e_acopio_lejos": "reciclaje",
    "n_raee_hab": "globo", "n_tratado_peru": "reciclaje", "n_reciclado_mundo": "globo", "n_raee_mundo": "globo",
    "n_latam": "globo", "n_laptop_reposo": "laptop",
    "c_reposo": "power", "c_cargadores": "enchufe", "c_brillo": "pantalla",
    "l_cargadores": "enchufe", "l_cajon": "caja", "l_pantalla": "pantalla", "l_datos": "carpeta",
}
# Preguntas del cuestionario inicial.
POR_HABITO = {"apagar": "power", "ahorro": "pantalla", "depurar": "carpeta", "reparar": "herramienta",
              "reciclar": "reciclaje", "cargadores": "enchufe"}
POR_PASO = {"dispositivos": "pantalla", "horas": "reloj", "barreras": "decision", "resultado": "hoja"}

# Colores según el tono: (principal, acento)
COLORES = {
    "peque": ("#FFFFFF", "#FFD166"), "gamer": ("#FFFFFF", "#FFD166"),
    "tecnico": ("#FFFFFF", "#BFEFD3"), "mayor": ("#FFFFFF", "#FFE9A8"),
}

# Destellos decorativos solo para primaria y secundaria (formas simples y originales)
DESTELLOS = {
    "peque": '<g fill="{A}"><polygon points="26,34 31,46 43,50 31,54 26,66 21,54 9,50 21,46"/><polygon points="214,138 218,147 227,150 218,153 214,162 210,153 201,150 210,147"/><circle cx="200" cy="36" r="5"/></g>',
    "gamer": '<g fill="{A}" opacity="0.8"><rect x="14" y="24" width="10" height="10"/><rect x="26" y="36" width="10" height="10"/><rect x="204" y="150" width="10" height="10"/><rect x="216" y="162" width="10" height="10"/></g>',
}


def clave_tip(tip_id, categoria="software"):
    return POR_TIP.get(tip_id, {"energia": "power", "residuos": "reciclaje", "datos": "nube", "software": "laptop"}[categoria])


def clave_actividad(act):
    return POR_ACTIVIDAD.get(act["id"], POR_TIPO[act["tipo"]])


def svg(clave, tono, descripcion=""):
    """Devuelve el dibujo en una sola línea de HTML (sin saltos para que Markdown no lo parta)."""
    w, a = COLORES[tono]
    cuerpo = ARTE[clave].format(W=w, A=a)
    extra = DESTELLOS.get(tono, "").format(A=a)
    desc = descripcion or clave
    return (f'<svg class="eco-svg" viewBox="0 0 240 200" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="{desc}">{cuerpo}{extra}</svg>')
