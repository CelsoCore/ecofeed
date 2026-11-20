"""Contenido base de EcoFeed: tonos, dispositivos, hábitos, barreras y textos de interfaz.

Tonos de comunicación (se eligen con logica.tono):
    peque    primaria o niños: frases cortas y ejemplos concretos, preguntas con escenas.
    gamer    secundaria: directo y concreto, sin tecnicismos.
    tecnico  universidad, instituto o adultos: kWh, CO₂, soles, obsolescencia y economía circular.
    mayor    adultos mayores: claro, paso a paso, en soles, letra grande.

Las recomendaciones están en tips.py y las actividades interactivas en actividades.py.
Las cifras marcadas como "estudio" salen del informe "Nivel de conocimiento y
prácticas de informática verde ... Universidad Nacional de Trujillo"
(Tablas 3 a 7 y la introducción).
"""

TONOS = ("peque", "gamer", "tecnico", "mayor")

# ---------------------------------------------------------------- edad y grado
EDADES = {
    "nino": {"etiqueta": "Niño (6–12 años)", "emoji": "🧒"},
    "joven": {"etiqueta": "Joven (13–29 años)", "emoji": "🧑"},
    "adulto": {"etiqueta": "Adulto (30–59 años)", "emoji": "🧑‍💼"},
    "mayor": {"etiqueta": "Mayor (60+ años)", "emoji": "👵"},
}
GRADOS = {
    "primaria": "Primaria",
    "secundaria": "Secundaria",
    "superior": "Universidad o instituto",
    "ninguno": "Ya no estudio",
}
GRADO_POR_EDAD = {"nino": "primaria", "joven": "superior", "adulto": "superior", "mayor": "ninguno"}

# ---------------------------------------------------------------- dispositivos (inventario)
# w = vatios en uso. w_reposo = vatios si se deja encendido sin usar.
# apagable = se puede apagar o suspender. carga = se carga con cargador.
# peso_kg, vida_anios y co2_fab_kg (CO₂e de fabricación) son valores de referencia:
# reemplázalos por las fuentes que cites en tu informe.
DISPOSITIVOS = {
    "cel": {"nombre": "Celular", "emoji": "📱", "w": 5, "w_reposo": 0, "horas_def": 4.0, "horas_max": 16,
            "peso_kg": 0.2, "vida_anios": 3, "co2_fab_kg": 70, "apagable": False, "carga": True},
    "tab": {"nombre": "Tablet", "emoji": "📲", "w": 8, "w_reposo": 1.5, "horas_def": 2.0, "horas_max": 16,
            "peso_kg": 0.5, "vida_anios": 4, "co2_fab_kg": 90, "apagable": True, "carga": True},
    "lap": {"nombre": "Laptop", "emoji": "💻", "w": 45, "w_reposo": 15, "horas_def": 3.0, "horas_max": 16,
            "peso_kg": 2.2, "vida_anios": 4, "co2_fab_kg": 300, "apagable": True, "carga": True},
    "pc": {"nombre": "PC de escritorio", "emoji": "🖥️", "w": 150, "w_reposo": 60, "horas_def": 3.0, "horas_max": 16,
           "peso_kg": 10.0, "vida_anios": 6, "co2_fab_kg": 450, "apagable": True, "carga": False},
    "consola": {"nombre": "Consola de videojuegos", "emoji": "🎮", "w": 100, "w_reposo": 10, "horas_def": 2.0, "horas_max": 16,
                "peso_kg": 3.5, "vida_anios": 7, "co2_fab_kg": 200, "apagable": True, "carga": False},
    "tv": {"nombre": "Televisor", "emoji": "📺", "w": 80, "w_reposo": 1, "horas_def": 3.0, "horas_max": 16,
           "peso_kg": 12.0, "vida_anios": 8, "co2_fab_kg": 350, "apagable": True, "carga": False},
    "router": {"nombre": "Router de Wi‑Fi", "emoji": "📡", "w": 8, "w_reposo": 0, "horas_def": 24.0, "horas_max": 24,
               "peso_kg": 0.4, "vida_anios": 5, "co2_fab_kg": 50, "apagable": False, "carga": False},
    "audifonos": {"nombre": "Audífonos o parlante", "emoji": "🎧", "w": 1, "w_reposo": 0, "horas_def": 2.0, "horas_max": 16,
                  "peso_kg": 0.2, "vida_anios": 2.5, "co2_fab_kg": 20, "apagable": False, "carga": True},
}
DISPOSITIVOS_SIEMPRE_ENCENDIDOS = ("router",)   # no se pregunta por horas: 24 al día

# Hábitos que cuidan a cada dispositivo (para la "salud" del inventario)
HABITOS_POR_DISPOSITIVO = {
    "cel": ["ahorro", "cargadores", "reparar"],
    "tab": ["ahorro", "cargadores", "apagar", "reparar"],
    "lap": ["apagar", "ahorro", "reparar", "cargadores"],
    "pc": ["apagar", "reparar", "depurar"],
    "consola": ["apagar", "reparar", "reciclar"],
    "tv": ["apagar", "ahorro", "reciclar"],
    "router": ["apagar", "reciclar"],
    "audifonos": ["cargadores", "reparar", "reciclar"],
}

# Respuestas de tiempo de uso para primaria (en vez del deslizador)
HORAS_OPCIONES = [
    ("Casi nada · menos de 1 hora", 0.5),
    ("Un ratito · 1 a 2 horas", 1.5),
    ("Bastante · 3 a 4 horas", 3.5),
    ("Mucho · 5 horas o más", 6.0),
]

# ---------------------------------------------------------------- hábitos (ítems 6 a 11 del cuestionario)
# preguntas: una por tono. escenario: pregunta con 3 opciones para primaria (valen 5, 3 y 1).
# leccion: lo que se aprende justo después de responder (primaria y secundaria).
# media_estudio y acuerdo_estudio vienen de la Tabla 4.
HABITOS = {
    "apagar": {
        "item": 6, "emoji": "💤", "titulo": "Apagar o suspender equipos", "titulo_juego": "Apagar al terminar",
        "preguntas": {
            "peque": "¿Apagas la compu o la tablet cuando terminas de usarla?",
            "gamer": "Cuando terminas de usar tu laptop o PC, ¿la apagas o la suspendes?",
            "tecnico": "¿Apagas o suspendes tu laptop o PC cuando no la estás usando?",
            "mayor": "¿Apaga o suspende su computadora cuando ya no la está usando?",
        },
        "escenario": {"situacion": "Terminaste de jugar en la compu. ¿Qué haces?",
                      "opciones": [("🛑", "La apago", 5), ("💤", "La dejo en reposo", 3), ("🏃", "Me voy y la dejo prendida", 1)]},
        "leccion": {
            "peque": "Una compu prendida sigue gastando luz aunque nadie la esté usando.",
            "gamer": "Un equipo encendido sin uso consume entre 15 y 60 W. Apagarlo o suspenderlo es el ahorro más fácil.",
        },
        "media_estudio": 3.59, "acuerdo_estudio": 53.1,
    },
    "ahorro": {
        "item": 7, "emoji": "🔆", "titulo": "Ahorro de energía y brillo", "titulo_juego": "Brillo bajo",
        "preguntas": {
            "peque": "¿Bajas el brillo de la pantalla para que la batería dure más?",
            "gamer": "¿Activas el modo ahorro o bajas el brillo para que la batería dure más?",
            "tecnico": "¿Activas el modo de ahorro de energía o bajas el brillo de la pantalla?",
            "mayor": "¿Baja el brillo de la pantalla o activa el ahorro de batería?",
        },
        "escenario": {"situacion": "Estás en el celular y la pantalla brilla mucho. ¿Qué haces?",
                      "opciones": [("🔅", "Bajo el brillo", 5), ("🤷", "Depende del día", 3), ("🌞", "Siempre al máximo", 1)]},
        "leccion": {
            "peque": "La pantalla es lo que más batería gasta. Con menos brillo, la batería dura más.",
            "gamer": "La pantalla es lo que más energía consume: menos brillo significa más horas de batería.",
        },
        "media_estudio": 3.44, "acuerdo_estudio": 56.3,
    },
    "depurar": {
        "item": 8, "emoji": "🗂️", "titulo": "Borrar lo que ya no necesitas", "titulo_juego": "Borrar lo que no uso",
        "preguntas": {
            "peque": "¿Borras (con ayuda) fotos, juegos o apps que ya no usas?",
            "gamer": "¿Borras apps, fotos y archivos que ya no usas, incluso los de la nube?",
            "tecnico": "¿Eliminas archivos, correos, apps o servicios en la nube que ya no necesitas?",
            "mayor": "¿Borra fotos, correos o archivos que ya no necesita?",
        },
        "escenario": {"situacion": "Tu celular está lleno de fotos repetidas y juegos que ya no usas. ¿Qué haces?",
                      "opciones": [("🗑️", "Borro lo que no uso", 5), ("🤔", "Borro a veces", 3), ("📦", "Lo dejo todo ahí", 1)]},
        "leccion": {
            "peque": "Lo que guardas en internet vive en computadoras gigantes que gastan mucha electricidad.",
            "gamer": "Los archivos de la nube viven en centros de datos que funcionan las 24 horas.",
        },
        "media_estudio": 3.00, "acuerdo_estudio": 34.4,
    },
    "reparar": {
        "item": 9, "emoji": "🔧", "titulo": "Reparar antes de reemplazar", "titulo_juego": "Reparar antes de botar",
        "preguntas": {
            "peque": "Si un aparato se malogra, ¿piden que lo arreglen antes de botarlo?",
            "gamer": "Si tu equipo falla o va lento, ¿intentas repararlo o mejorarlo antes de comprar uno nuevo?",
            "tecnico": "¿Reparas o actualizas tus equipos (RAM, SSD) en lugar de cambiarlos de inmediato?",
            "mayor": "Si un equipo se malogra, ¿lo manda a reparar antes de comprar uno nuevo?",
        },
        "escenario": {"situacion": "La tablet de tu casa se malogró. ¿Qué hacen?",
                      "opciones": [("🔧", "La llevan a reparar", 5), ("🤷", "A veces la reparan", 3), ("🛒", "Compran otra", 1)]},
        "leccion": {
            "peque": "Arreglar un aparato evita que se vuelva basura electrónica antes de tiempo.",
            "gamer": "Cada año extra que usas un equipo baja los residuos y el carbono de fabricar uno nuevo.",
        },
        "media_estudio": 2.78, "acuerdo_estudio": 18.8,
    },
    "reciclar": {
        "item": 10, "emoji": "♻️", "titulo": "Reciclar equipos en desuso", "titulo_juego": "Reciclar aparatos viejos",
        "preguntas": {
            "peque": "¿Tu familia lleva los aparatos viejos a un lugar de reciclaje?",
            "gamer": "¿Llevas tus equipos viejos a un punto de acopio en vez de tirarlos?",
            "tecnico": "¿Entregas tus equipos electrónicos en desuso a puntos de reciclaje o acopio?",
            "mayor": "¿Lleva los aparatos viejos a un lugar de reciclaje en vez de botarlos a la basura?",
        },
        "escenario": {"situacion": "Hay un celular viejo que ya no prende. ¿Qué pasa con él?",
                      "opciones": [("♻️", "Va a un punto de reciclaje", 5), ("📦", "Se guarda en un cajón", 3), ("🗑️", "Va a la basura", 1)]},
        "leccion": {
            "peque": "Los aparatos viejos tienen metales que contaminan el agua y la tierra. Por eso van a puntos especiales.",
            "gamer": "En Perú solo cerca del 7 % de los residuos electrónicos recibe tratamiento especializado.",
        },
        "media_estudio": 2.09, "acuerdo_estudio": 9.4,
    },
    "cargadores": {
        "item": 11, "emoji": "🔋", "titulo": "Desconectar cargadores", "titulo_juego": "Desenchufar el cargador",
        "preguntas": {
            "peque": "¿Desenchufas el cargador cuando el celular ya cargó?",
            "gamer": "¿Desconectas el cargador cuando tu dispositivo ya llegó al 100 %?",
            "tecnico": "¿Desconectas los cargadores y regletas cuando no los utilizas?",
            "mayor": "¿Desenchufa el cargador cuando ya no lo usa?",
        },
        "escenario": {"situacion": "El celular ya llegó al 100 %. ¿Qué haces con el cargador?",
                      "opciones": [("🔌", "Lo desenchufo", 5), ("🤷", "A veces", 3), ("😴", "Lo dejo enchufado", 1)]},
        "leccion": {
            "peque": "Un cargador enchufado gasta un poquito de energía aunque no esté cargando nada.",
            "gamer": "Un cargador sin carga gasta cerca de 0,5 W. Con varios cargadores y 24 horas, se acumula.",
        },
        "media_estudio": 3.16, "acuerdo_estudio": 50.0,
    },
}

ESCALA = {
    1: ("😟", "Nunca"),
    2: ("🙁", "Casi nunca"),
    3: ("😐", "A veces"),
    4: ("🙂", "Casi siempre"),
    5: ("😄", "Siempre"),
}

# Baremo del informe (Tabla 7): límite superior de cada nivel.
BAREMO = [(1.80, "Muy bajo"), (2.60, "Bajo"), (3.40, "Medio"), (4.20, "Alto"), (5.00, "Muy alto")]
RANGOS_JUEGO = ["Principiante", "Aprendiz verde", "Explorador eco", "Guardián eco", "Maestro eco"]
MEDIA_ESTUDIO_PRACTICAS = 3.01

# Resultado del cuestionario por tono. Marcadores: {idx} {media} {nivel} {est} {dif}
RESULTADO = {
    "peque": "¡Tu barra de energía verde está en {idx} de 100! Tu rango es «{nivel}».",
    "gamer": "Tu barra de energía verde marca {idx}/100 y tu rango es «{nivel}». El promedio de los estudiantes del estudio es {est} sobre 5.",
    "tecnico": "Tu índice de prácticas es {media} sobre 5 (nivel {nivel} según el baremo del informe). El promedio del estudio fue {est} (Medio), una diferencia de {dif}.",
    "mayor": "Su puntaje es {idx} de 100 y su nivel es «{nivel}».",
}
# Feedback por hábito. Marcadores: {titulo} {valor} {est} {dif}
FEEDBACK = {
    "peque": {
        "alto": "¡Muy bien! En «{titulo}» ya lo haces genial.",
        "medio": "En «{titulo}» vas bien. Con una misión más mejoras.",
        "bajo": "«{titulo}» será tu primera misión. ¡Tú puedes!",
    },
    "gamer": {
        "alto": "«{titulo}»: lo tienes dominado.",
        "medio": "«{titulo}»: vas por la mitad. Una misión más y subes.",
        "bajo": "«{titulo}»: es tu punto más bajo. Empieza por aquí.",
    },
    "tecnico": {
        "alto": "«{titulo}»: {valor}/5, por encima del promedio del estudio ({est}).",
        "medio": "«{titulo}»: {valor}/5 (estudio: {est}; diferencia {dif}).",
        "bajo": "«{titulo}»: {valor}/5. Es una brecha prioritaria (estudio: {est}).",
    },
    "mayor": {
        "alto": "En «{titulo}» lo está haciendo muy bien.",
        "medio": "En «{titulo}» va bien y puede mejorar un poco.",
        "bajo": "«{titulo}» es lo primero que le conviene mejorar.",
    },
}

# ---------------------------------------------------------------- barreras (ítems 16 a 18 + una extra)
BARRERAS = {
    "puntos": {
        "emoji": "📍",
        "textos": {
            "peque": "No sé dónde se llevan los aparatos viejos",
            "gamer": "No sé dónde dejar mis equipos viejos o casi no hay puntos de reciclaje cerca",
            "tecnico": "No sé dónde llevar mis equipos viejos o hay pocos puntos de acopio",
            "mayor": "No sé dónde llevar los aparatos viejos",
        },
        "estudio": "65,6 % no está de acuerdo con que haya suficientes puntos de acopio (ítem 16).",
    },
    "info": {
        "emoji": "📚",
        "textos": {
            "peque": "Nadie me ha explicado cómo cuidar los aparatos",
            "gamer": "Nadie me explicó cómo cuidar o desechar mis equipos",
            "tecnico": "No recibo información suficiente sobre cómo usar y desechar mis equipos",
            "mayor": "No tengo información clara sobre cómo desechar mis equipos",
        },
        "estudio": "65,6 % no recibe información suficiente en su universidad (ítem 17).",
    },
    "reparar_caro": {
        "emoji": "💸",
        "textos": {
            "peque": "Creo que es más fácil comprar uno nuevo",
            "gamer": "Reparar parece más caro o complicado que comprar uno nuevo",
            "tecnico": "Reparar me parece más costoso o complicado que comprar uno nuevo",
            "mayor": "Reparar me parece caro o complicado",
        },
        "estudio": "31,3 % piensa que reparar es más costoso o complicado (ítem 18).",
    },
    "olvido": {
        "emoji": "⏰",
        "textos": {
            "peque": "Se me olvida",
            "gamer": "Se me olvida o no tengo tiempo",
            "tecnico": "Se me olvida o no tengo tiempo",
            "mayor": "Se me olvida",
        },
        "estudio": "Esta opción no está en el cuestionario del estudio; la agregamos en la app.",
    },
}

# ---------------------------------------------------------------- textos de la interfaz por tono
UI = {
    "peque": {
        "sub": "Aprende, juega y cuida el planeta",
        "tab_feed": "🔥 Para ti", "tab_sim": "🎮 Simulador", "tab_mis": "⭐ Misiones",
        "tab_consumo": "🔋 Mi energía", "tab_perfil": "👤 Yo",
        "q_disp_t": "¿Qué aparatos usas?", "q_disp_s": "Toca los que usas",
        "q_horas_t": "¿Cuánto usas cada aparato al día?", "q_horas_s": "Elige la opción que más se parezca",
        "q_barr_t": "¿Qué te cuesta más?", "q_barr_s": "Marca lo que te pase. Puedes dejarlo vacío",
        "continuar": "Siguiente ➡", "terminar": "¡Ver mi resultado! 🏆", "atras": "⬅ Atrás",
        "pregunta_n": "Pregunta {n} de {total}",
        "res_titulo": "¡Terminaste las preguntas!", "res_boton": "Ver mis tarjetas ➡",
        "cab_feed": "Para ti", "dato": "Dato curioso", "reto": "Misión", "porque": "👀 ¿Por qué?",
        "aceptar": "⭐ ¡Acepto la misión!", "aceptada": "✅ Misión aceptada",
        "megusta": "🤍 Me gusta", "legusta": "💚 Me gustó",
        "anterior": "⬅ Anterior", "siguiente": "Siguiente ➡",
        "mis_titulo": "Tus misiones", "mis_vacio": "Todavía no tienes misiones. Toca ⭐ en una tarjeta para aceptar una.",
        "mis_hecha": "Misión cumplida", "insignias": "Tus insignias",
        "idx_titulo": "Tu barra de energía verde", "habitos_titulo": "Cómo vas en cada cosa",
        "reg_titulo": "Anota tu día de hoy", "reg_boton": "Guardar mi día",
        "reg_vacio": "Cuando guardes tu primer día, aquí aparecerá tu semana.",
        "salir": "🚪 Salir", "repetir": "🔄 Repetir las preguntas",
        "datos": "📄 Datos de la investigación",
    },
    "gamer": {
        "sub": "Sube de nivel mientras cuidas tus equipos",
        "tab_feed": "🔥 Para ti", "tab_sim": "🎮 Simulador", "tab_mis": "🏆 Misiones",
        "tab_consumo": "⚡ Mi energía", "tab_perfil": "👤 Perfil",
        "q_disp_t": "¿Qué equipos usas?", "q_disp_s": "Marca todos los que uses",
        "q_horas_t": "¿Cuántas horas al día usas cada uno?", "q_horas_s": "Un cálculo aproximado basta",
        "q_barr_t": "¿Qué te frena?", "q_barr_s": "Marca lo que te pase. Puedes dejarlo vacío",
        "continuar": "Siguiente ➡", "terminar": "Ver mi resultado 🏆", "atras": "⬅ Atrás",
        "pregunta_n": "Pregunta {n} de {total}",
        "res_titulo": "Tu resultado inicial", "res_boton": "Ver mis tarjetas ➡",
        "cab_feed": "Para ti", "dato": "Dato del informe", "reto": "Misión", "porque": "👀 ¿Por qué?",
        "aceptar": "🎯 Aceptar misión", "aceptada": "✅ Misión aceptada",
        "megusta": "🤍 Me gusta", "legusta": "💚 Te gusta",
        "anterior": "⬅ Anterior", "siguiente": "Siguiente ➡",
        "mis_titulo": "Tus misiones", "mis_vacio": "No tienes misiones activas. Acepta una desde 🔥 Para ti.",
        "mis_hecha": "Misión cumplida", "insignias": "Logros",
        "idx_titulo": "Tu barra de energía verde", "habitos_titulo": "Tus hábitos frente al promedio del estudio",
        "reg_titulo": "Registrar el día de hoy", "reg_boton": "Guardar el día",
        "reg_vacio": "Guarda tu primer día y aquí verás tu semana.",
        "salir": "🚪 Cerrar sesión", "repetir": "🔄 Repetir el cuestionario",
        "datos": "📄 Datos del informe",
    },
    "tecnico": {
        "sub": "Gestiona tu huella digital y tus residuos electrónicos",
        "tab_feed": "🔥 Para ti", "tab_sim": "🔬 Simulador RAEE", "tab_mis": "🤝 Pactos",
        "tab_consumo": "📊 Diagnóstico", "tab_perfil": "👤 Perfil",
        "q_disp_t": "¿Qué dispositivos forman tu parque tecnológico?", "q_disp_s": "Marca todos los que uses",
        "q_horas_t": "¿Cuántas horas diarias usas cada dispositivo?", "q_horas_s": "Un cálculo aproximado basta",
        "q_barr_t": "¿Qué barreras percibes?", "q_barr_s": "Marca las que apliquen. Puedes dejarlo vacío",
        "continuar": "Continuar ➡", "terminar": "Ver mi diagnóstico ✅", "atras": "⬅ Atrás",
        "pregunta_n": "Pregunta {n} de {total}",
        "res_titulo": "Diagnóstico inicial", "res_boton": "Ver mis recomendaciones ➡",
        "cab_feed": "Para ti", "dato": "Del informe", "reto": "Compromiso", "porque": "👀 Fundamento",
        "aceptar": "🤝 Asumir pacto", "aceptada": "✅ Pacto asumido",
        "megusta": "🤍 Útil", "legusta": "💚 Útil",
        "anterior": "⬅ Anterior", "siguiente": "Siguiente ➡",
        "mis_titulo": "Pactos de desintoxicación tecnológica",
        "mis_vacio": "No has asumido pactos. Acepta uno desde 🔥 Para ti.",
        "mis_hecha": "Cumplido", "insignias": "Hitos",
        "idx_titulo": "Índice de prácticas", "habitos_titulo": "Prácticas frente al promedio del estudio (escala 1 a 5)",
        "reg_titulo": "Registro diario de uso", "reg_boton": "Guardar el día de hoy",
        "reg_vacio": "Cuando guardes tu primer día, aquí aparecerá el historial semanal.",
        "salir": "🚪 Cerrar sesión", "repetir": "🔄 Repetir el cuestionario",
        "datos": "📄 Datos del informe",
    },
    "mayor": {
        "sub": "Cuide su bolsillo y el planeta con sus aparatos",
        "tab_feed": "🔥 Consejos", "tab_sim": "💡 Mi gasto", "tab_mis": "✅ Compromisos",
        "tab_consumo": "📊 Mi nivel", "tab_perfil": "👤 Perfil",
        "q_disp_t": "¿Qué aparatos usa?", "q_disp_s": "Marque todos los que use",
        "q_horas_t": "¿Cuántas horas al día usa cada aparato?", "q_horas_s": "Un cálculo aproximado basta",
        "q_barr_t": "¿Qué le dificulta cuidar sus aparatos?", "q_barr_s": "Marque lo que le pase. Puede dejarlo vacío",
        "continuar": "Continuar ➡", "terminar": "Ver mi resultado ✅", "atras": "⬅ Atrás",
        "pregunta_n": "Pregunta {n} de {total}",
        "res_titulo": "Su resultado", "res_boton": "Ver los consejos ➡",
        "cab_feed": "Consejo", "dato": "Del informe", "reto": "Compromiso", "porque": "👀 ¿Por qué?",
        "aceptar": "✅ Me comprometo", "aceptada": "✅ Compromiso asumido",
        "megusta": "🤍 Me gusta", "legusta": "💚 Me gusta",
        "anterior": "⬅ Anterior", "siguiente": "Siguiente ➡",
        "mis_titulo": "Mis compromisos", "mis_vacio": "Aún no tiene compromisos. Toque «Me comprometo» en un consejo.",
        "mis_hecha": "Cumplido", "insignias": "Logros",
        "idx_titulo": "Su puntaje", "habitos_titulo": "Cómo va en cada hábito",
        "reg_titulo": "Anotar el día de hoy", "reg_boton": "Guardar el día de hoy",
        "reg_vacio": "Cuando guarde su primer día, aquí aparecerá su semana.",
        "salir": "🚪 Cerrar sesión", "repetir": "🔄 Repetir las preguntas",
        "datos": "📄 Datos del informe",
    },
}

# Etiquetas del panel lateral (HUD) por tono
HUD = {
    "peque": {"titulo": "Tu progreso", "nivel": "Nivel", "xp": "XP", "racha": "Días seguidos",
              "energia": "Energía verde", "misiones": "Misiones cumplidas", "act": "Tarjetas resueltas"},
    "gamer": {"titulo": "Tu progreso", "nivel": "Nivel", "xp": "XP", "racha": "Racha",
              "energia": "Energía verde", "misiones": "Misiones cumplidas", "act": "Actividades resueltas"},
    "tecnico": {"titulo": "Resumen", "nivel": "Nivel", "xp": "Puntos", "racha": "Racha de registro",
                "energia": "Índice de prácticas", "misiones": "Pactos cumplidos", "act": "Actividades resueltas"},
    "mayor": {"titulo": "Mi avance", "nivel": "Nivel", "xp": "Puntos", "racha": "Días seguidos",
              "energia": "Mi puntaje", "misiones": "Compromisos cumplidos", "act": "Preguntas resueltas"},
}

# Nombre de cada tipo de tarjeta interactiva por tono
TIPOS_ACTIVIDAD = {
    "mito": {"peque": "¿Mito o verdad?", "gamer": "¿Mito o realidad?", "tecnico": "¿Mito o realidad?", "mayor": "¿Mito o verdad?"},
    "quiz": {"peque": "Pregunta rápida", "gamer": "Pregunta rápida", "tecnico": "Pregunta rápida", "mayor": "Pregunta rápida"},
    "escenario": {"peque": "¿Qué harías?", "gamer": "¿Qué harías?", "tecnico": "Caso práctico", "mayor": "¿Qué haría usted?"},
    "adivina": {"peque": "Adivina el número", "gamer": "Adivina el dato", "tecnico": "Estima el dato", "mayor": "Adivine el dato"},
    "calc": {"peque": "Calculadora", "gamer": "Calculadora", "tecnico": "Calculadora de impacto", "mayor": "Calculadora"},
    "checklist": {"peque": "Mini reto", "gamer": "Mini reto", "tecnico": "Lista de verificación", "mayor": "Lista de tareas"},
}

# ---------------------------------------------------------------- niveles de juego, insignias, XP
NIVELES_JUEGO = ["Principiante", "Aprendiz", "Explorador", "Guardián", "Maestro eco"]
AVATAR_NIVEL = ["🌱", "🌿", "🌳", "🌎", "🏆"]
XP_ACTIVIDAD_OK = 10
XP_ACTIVIDAD_INTENTO = 3

# cond: ("hechas", n) misiones cumplidas | ("aceptadas", n) | ("alguna", [ids]) alguna cumplida
#       ("registros", n) días guardados | ("actividades", n) tarjetas resueltas | ("aciertos", n)
BADGES = [
    {"id": "primer_paso", "emoji": "🌱", "cond": ("hechas", 1),
     "nombres": {"peque": "Primer paso", "gamer": "Primer logro", "tecnico": "Primer pacto cumplido", "mayor": "Primer compromiso"}},
    {"id": "triple", "emoji": "🔥", "cond": ("hechas", 3),
     "nombres": {"peque": "Tres misiones", "gamer": "Combo x3", "tecnico": "Tres pactos cumplidos", "mayor": "Tres compromisos"}},
    {"id": "aceptadas", "emoji": "🧭", "cond": ("aceptadas", 5),
     "nombres": {"peque": "Explorador", "gamer": "Explorador de misiones", "tecnico": "Cartera de cinco pactos", "mayor": "Cinco compromisos"}},
    {"id": "ahorro", "emoji": "⚡", "cond": ("alguna", ["apagar_equipos", "desconectar_cargadores", "brillo", "regleta_interruptor"]),
     "nombres": {"peque": "Héroe del ahorro", "gamer": "Cazador de energía fantasma", "tecnico": "Reducción de consumo en reposo", "mayor": "Ahorrador de energía"}},
    {"id": "bateria", "emoji": "🔋", "cond": ("alguna", ["carga_80", "calor_bateria"]),
     "nombres": {"peque": "Cuidador de baterías", "gamer": "Guardián de la batería", "tecnico": "Gestión de vida útil de batería", "mayor": "Cuidador de la batería"}},
    {"id": "raee", "emoji": "♻️", "cond": ("alguna", ["reciclar_acopio", "guardar_raee", "donar_revender", "pilas_acopio"]),
     "nombres": {"peque": "Cazador de chatarra", "gamer": "Recolector de equipos viejos", "tecnico": "Gestión responsable de RAEE", "mayor": "Reciclador"}},
    {"id": "constante", "emoji": "📅", "cond": ("registros", 3),
     "nombres": {"peque": "3 días anotados", "gamer": "Tres registros", "tecnico": "Tres días de registro", "mayor": "Tres días anotados"}},
    {"id": "curioso", "emoji": "🧠", "cond": ("actividades", 5),
     "nombres": {"peque": "Mente curiosa", "gamer": "Curioso", "tecnico": "Cinco actividades resueltas", "mayor": "Cinco preguntas resueltas"}},
    {"id": "sabio", "emoji": "🎓", "cond": ("aciertos", 10),
     "nombres": {"peque": "Súper sabio", "gamer": "Experto", "tecnico": "Diez aciertos", "mayor": "Diez aciertos"}},
]

# ---------------------------------------------------------------- simulador RAEE (textos por tono)
SIM = {
    "peque": {
        "titulo": "Tus aparatos",
        "energia": "Cada día se desperdician **{horas} horas de consola** de energía en aparatos prendidos sin usar.",
        "cero": "¡Cero desperdicio! Tus aparatos no gastan energía de más.",
        "cargas": "Con esa energía se podrían cargar **{cargas} celulares**.",
        "chatarra": "Cada año tus aparatos se vuelven **{kg} kg de basura electrónica**, como **{botellas} botellas de agua** llenas.",
        "extra": "Si los usas **{extra} más**, la basura baja a **{kg_extra} kg**.",
    },
    "gamer": {
        "titulo": "Tus equipos",
        "energia": "Tus equipos desperdician **{kwh_mes} kWh al mes** en reposo y cargadores: unas **{horas_mes} horas de consola** a tope.",
        "cero": "Tus equipos no desperdician energía por reposo ni cargadores.",
        "cargas": "Esa energía alcanzaría para **{cargas_mes} cargas completas de celular** al mes.",
        "chatarra": "Tus equipos generan **{kg} kg de basura electrónica al año** a su ritmo de reemplazo.",
        "extra": "Si los usas **{extra} más**, bajas a **{kg_extra} kg** ({pct}).",
    },
    "tecnico": {
        "titulo": "Parque tecnológico",
        "consumo": "Consumo estimado: **{kwh_anio} kWh/año** (≈ {co2_anio} kg CO₂ y S/ {soles_anio}).",
        "evitable": "Consumo evitable (reposo y cargadores): **{ev_kwh} kWh/año**, S/ {ev_soles} y {ev_co2} kg CO₂.",
        "residuo": "Tu parque tecnológico genera **{kg} kg de residuos al año**. Con **{extra}** más de vida útil baja a **{kg_extra} kg** ({pct}).",
        "fab": "El carbono de fabricación amortizado pasa de **{fab} a {fab_extra} kg CO₂e/año**: alargar la vida útil es economía circular aplicada y una respuesta a la obsolescencia programada.",
    },
    "mayor": {
        "titulo": "Lo que gastan sus aparatos",
        "gasto": "Sus aparatos gastan unos **S/ {soles_mes} al mes** de luz.",
        "evitable": "Apagándolos y desenchufando los cargadores podría ahorrar unos **S/ {ev_mes} al mes**.",
        "cero": "Ya no desperdicia energía por dejar aparatos encendidos. ¡Muy bien!",
        "chatarra": "Si cuida sus aparatos y los usa **{extra}** más, generará menos basura electrónica.",
    },
}

# ---------------------------------------------------------------- datos del informe
DATOS_INFORME = [
    ("Los centros de datos del mundo superan los 460 TWh y causan cerca del 0,5 % de las emisiones de CO₂.", "Kamiya (2024)"),
    ("Se generan 62 millones de toneladas de residuos electrónicos al año; solo 22,3 % se recolecta y recicla de forma segura.", "Baldé et al. (2024)"),
    ("Para 2030 se proyectan más de 82 millones de toneladas de residuos electrónicos.", "Baldé et al. (2024)"),
    ("América Latina produce 1,3 millones de toneladas de basura electrónica al año y recicla solo 3 %.", "Baldé et al. (2022)"),
    ("Perú genera 205 mil toneladas de RAEE al año (6,5 kg por habitante) y solo 14 700 t, cerca de 7 %, recibieron tratamiento especializado.", "MINAM (2023)"),
]
