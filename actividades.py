"""Actividades interactivas de "Para ti" (se mezclan con las recomendaciones).

Tipos: mito, quiz, escenario, adivina, calc, checklist.
Cada texto tiene dos versiones: "ni" (primaria) y "gen" (el resto). Si falta "ni", se usa "gen".
Los escenarios están en tercera persona para que sirvan en cualquier tono.
Las cifras de las tarjetas «adivina» salen del informe (MINAM 2023; Baldé et al. 2022 y 2024).
"""

ACTIVIDADES = []


def _a(id, tipo, categoria, emoji, **datos):
    ACTIVIDADES.append({"id": id, "tipo": tipo, "categoria": categoria, "emoji": emoji, **datos})


def _v(ni, gen=None):
    return {"ni": ni, "gen": gen if gen is not None else ni}


# ================================================================= ¿MITO O VERDAD?
_a("m_apagar_gasta", "mito", "energia", "💤",
   texto=_v("Apagar y prender la compu gasta más luz que dejarla prendida todo el día.",
            "Apagar y volver a encender un equipo gasta más energía que dejarlo encendido."),
   verdad=False,
   explica=_v("Mito. Prender gasta un poquito solo un instante. Si no la vas a usar, apagarla ahorra.",
              "Mito. El pico de encendido dura muy poco. Si no vas a usar el equipo por un rato, apagarlo o suspenderlo ahorra."))

_a("m_cargador_vacio", "mito", "energia", "🔌",
   texto=_v("Un cargador enchufado sin celular no gasta nada de luz.",
            "Un cargador enchufado sin dispositivo conectado no consume energía."),
   verdad=False,
   explica=_v("Mito. Gasta muy poquito, pero está enchufado todo el día. Con varios cargadores se suma.",
              "Mito. Consume poco (cerca de 0,5 W), pero funciona las 24 horas y con varios cargadores se acumula."))

_a("m_carga_noche", "mito", "energia", "🌙",
   texto=_v("Dejar el celular cargando toda la noche es lo mejor para su batería.",
            "Cargar el celular toda la noche hasta el 100 % es lo mejor para su batería."),
   verdad=False,
   explica=_v("Mito. A la batería le conviene no estar siempre llena. Cargar entre 20 % y 80 % la hace durar más.",
              "Mito. Las baterías de litio se desgastan más al estar siempre al 100 %. Entre 20 % y 80 % duran más años."))

_a("m_salvapantallas", "mito", "energia", "🌀",
   texto=_v("Las imágenes que se mueven cuando la compu descansa ahorran energía.",
            "El salvapantallas animado ahorra energía."),
   verdad=False,
   explica=_v("Mito. Lo que ahorra es apagar la pantalla o poner la compu en reposo.",
              "Mito. Ahorra la pantalla apagada y la suspensión, no un protector con movimiento."))

_a("m_nube", "mito", "datos", "☁️",
   texto=_v("Lo que guardas en internet no gasta electricidad.",
            "Lo que guardas en la nube no consume energía."),
   verdad=False,
   explica=_v("Mito. Se guarda en computadoras gigantes que están prendidas todo el tiempo.",
              "Mito. Se almacena en centros de datos que funcionan 24 horas y suman más de 460 TWh al año en el mundo."))

_a("m_celular_basura", "mito", "residuos", "🗑️",
   texto=_v("Un celular que ya no prende puede ir a la basura de la casa.",
            "Un celular que ya no funciona puede ir a la basura común."),
   verdad=False,
   explica=_v("Mito. Tiene metales que contaminan. Debe ir a un punto de reciclaje de aparatos.",
              "Mito. Contiene metales que contaminan suelo y agua. Debe ir a un punto de acopio de RAEE."))

_a("m_reparar_caro", "mito", "residuos", "🔧",
   texto=_v("Arreglar un aparato siempre cuesta más que comprar otro.",
            "Reparar un equipo siempre cuesta más que comprar uno nuevo."),
   verdad=False,
   explica=_v("Mito. Muchas veces arreglarlo sale más barato, por ejemplo cambiar solo la batería.",
              "Mito. Depende de la falla. Cambiar una batería o ampliar la memoria suele costar bastante menos que un equipo nuevo. El 31,3 % del estudio pensaba lo contrario."))

_a("m_metales", "mito", "residuos", "⚗️",
   texto=_v("Los aparatos viejos tienen metales que contaminan si se botan.",
            "Los equipos electrónicos desechados contienen metales que contaminan si no se tratan."),
   verdad=True,
   explica=_v("Verdad. Por eso los aparatos viejos van a puntos especiales.",
              "Verdad. Por eso los RAEE deben recibir tratamiento especializado."))

_a("m_brillo", "mito", "energia", "🔆",
   texto=_v("Bajar el brillo ayuda a que la batería dure más.",
            "Bajar el brillo de la pantalla ayuda a que la batería dure más."),
   verdad=True,
   explica=_v("Verdad. La pantalla es lo que más batería gasta.",
              "Verdad. La pantalla es el componente que más energía consume en un celular."))

_a("m_reciclar_materiales", "mito", "residuos", "♻️",
   texto=_v("De un aparato viejo se pueden recuperar materiales para hacer cosas nuevas.",
            "Del reciclaje de equipos electrónicos se pueden recuperar materiales valiosos."),
   verdad=True,
   explica=_v("Verdad. Se recuperan metales y piezas, y así se fabrica menos desde cero.",
              "Verdad. Se recuperan metales y componentes, lo que reduce la extracción de materia prima."))

_a("m_video_calidad", "mito", "datos", "🎬",
   texto=_v("Ver un video en calidad altísima gasta más datos que en calidad normal.",
            "Ver video en la máxima calidad transmite más datos y consume más energía que en calidad media."),
   verdad=True,
   explica=_v("Verdad. Más calidad significa más datos viajando por internet.",
              "Verdad. Más resolución implica más datos transmitidos y más trabajo para los servidores."))

_a("m_oscuro", "mito", "energia", "🌑",
   texto=_v("El modo oscuro ahorra batería en todas las pantallas.",
            "El modo oscuro ahorra batería en cualquier tipo de pantalla."),
   verdad=False,
   explica=_v("Mito. Solo ayuda en pantallas OLED, donde el negro apaga la luz de cada punto.",
              "Mito. Solo ahorra de forma notable en pantallas OLED, donde los píxeles negros no emiten luz."))

_a("m_reciclado_mundo", "mito", "residuos", "🌍",
   texto=_v("En el mundo casi toda la basura electrónica se recicla bien.",
            "En el mundo, la mayor parte de los residuos electrónicos se recicla de forma segura."),
   verdad=False,
   explica=_v("Mito. Solo cerca de 2 de cada 10 se recicla de forma segura.",
              "Mito. Solo 22,3 % se recolecta y recicla de forma segura (Baldé et al., 2024)."))

_a("m_peru_tratado", "mito", "residuos", "🇵🇪",
   texto=_v("En Perú casi todos los aparatos viejos reciben un tratamiento especial.",
            "En Perú, la mayoría de los RAEE recibe tratamiento especializado."),
   verdad=False,
   explica=_v("Mito. Solo cerca de 7 de cada 100 reciben ese tratamiento.",
              "Mito. Solo cerca de 7 % (14 700 de 205 mil toneladas) recibió tratamiento especializado (MINAM, 2023)."))

_a("m_pilas", "mito", "residuos", "🔋",
   texto=_v("Las pilas gastadas pueden ir al tacho de la basura de siempre.",
            "Las pilas usadas pueden desecharse junto con la basura doméstica."),
   verdad=False,
   explica=_v("Mito. Las pilas tienen metales que contaminan. Se llevan a un punto de acopio.",
              "Mito. Contienen metales pesados. Deben entregarse en un punto de acopio."))

_a("m_vida_util", "mito", "residuos", "⏳",
   texto=_v("Usar un aparato más años ayuda a producir menos basura electrónica.",
            "Alargar la vida útil de un equipo reduce residuos y emisiones de fabricación."),
   verdad=True,
   explica=_v("Verdad. Si dura más, no hace falta fabricar otro tan pronto.",
              "Verdad. Cada año extra de uso baja los residuos anuales y el carbono de fabricar un reemplazo."))

# ================================================================= PREGUNTA RÁPIDA
_a("q_pantalla", "quiz", "energia", "📱",
   pregunta=_v("¿Qué parte del celular gasta más batería?", "¿Qué componente del celular suele consumir más batería?"),
   opciones=["La pantalla", "La funda", "El cable", "El botón de volumen"], correcta=0,
   explica=_v("La pantalla. Por eso bajar el brillo ayuda.",
              "La pantalla. Por eso bajar el brillo y apagarla rápido ayuda."))

_a("q_raee", "quiz", "residuos", "🗑️",
   pregunta=_v("A los aparatos eléctricos y electrónicos que ya no sirven se les llama…",
               "¿Qué significa RAEE?"),
   opciones=_v(["Basura electrónica", "Juguetes", "Cables nuevos", "Pilas cargadas"],
               ["Residuos de aparatos eléctricos y electrónicos", "Reciclaje de aparatos económicos", "Redes de acceso eléctrico", "Registro ambiental de energía"]),
   correcta=0,
   explica=_v("Se les llama basura electrónica, o RAEE.",
              "Residuos de aparatos eléctricos y electrónicos. Es el residuo de más rápido crecimiento en el mundo."))

_a("q_pilas", "quiz", "residuos", "🪫",
   pregunta=_v("¿A dónde van las pilas gastadas?", "¿Dónde deben entregarse las pilas usadas?"),
   opciones=_v(["A un punto de reciclaje", "Al patio", "Al lavadero", "Al tacho común"],
               ["En un punto de acopio", "En el tacho común", "En el desagüe", "En el campo"]),
   correcta=0,
   explica=_v("Van a un punto de reciclaje, porque tienen metales que contaminan.",
              "En un punto de acopio. Contienen metales pesados que contaminan agua y suelo."))

_a("q_vida_celular", "quiz", "residuos", "⏳",
   pregunta=_v("¿Qué ayuda a que un celular dure más años?", "¿Qué acción alarga más la vida útil de un celular?"),
   opciones=_v(["Funda y protector de pantalla", "Dejarlo siempre al sol", "Cargarlo hasta que se caliente", "Tirarlo para probar"],
               ["Funda, protector y cargar entre 20 % y 80 %", "Cargarlo siempre al 100 %", "Usarlo al sol mientras carga", "Reiniciarlo cada hora"]),
   correcta=0,
   explica=_v("La funda y el protector evitan golpes y roturas.",
              "Protegerlo de golpes y no exponer la batería a extremos de carga ni de calor."))

_a("q_modo_avion", "quiz", "energia", "✈️",
   pregunta=_v("Si no vas a usar el celular en toda la noche, ¿qué le conviene?", "Para dormir, ¿qué ayuda más a la batería del celular?"),
   opciones=_v(["Modo avión", "Brillo al máximo", "Abrir muchas apps", "Subir el volumen"],
               ["Activar el modo avión", "Subir el brillo", "Abrir juegos", "Quitar la funda"]),
   correcta=0,
   explica=_v("El modo avión evita que busque señal toda la noche.",
              "El modo avión evita la búsqueda constante de señal y las notificaciones."))

_a("q_reciclaje_peru", "quiz", "residuos", "📍",
   pregunta=_v("¿Qué haces con un aparato viejo que ya no funciona?", "¿Qué es lo más adecuado para un equipo que ya no funciona?"),
   opciones=_v(["Llevarlo a un punto de acopio", "Botarlo a la calle", "Quemarlo", "Enterrarlo en el jardín"],
               ["Entregarlo en un punto de acopio autorizado", "Dejarlo en la vereda", "Quemarlo", "Enterrarlo"]),
   correcta=0,
   explica=_v("Se lleva a un punto de acopio.",
              "Entregarlo en un punto de acopio. Quemarlo o enterrarlo libera sustancias tóxicas."))

# ================================================================= ¿QUÉ HARÍAS? (escenarios)
_a("e_cargador", "escenario", "energia", "🔌",
   situacion=_v("El celular de Marco llegó al 100 % y él va a salir de casa. ¿Qué es lo mejor?",
                "El celular de Marco llegó al 100 % y él va a salir de casa. ¿Qué es lo mejor?"),
   opciones=["Desenchufar el cargador de la pared", "Dejarlo enchufado para mañana", "Cargarlo otra vez", "Taparlo con una manta"],
   correcta=0,
   explica=_v("Desenchufar el cargador evita que siga gastando luz sin hacer nada.",
              "Desenchufarlo evita el consumo en vacío y reduce el calor."))

_a("e_bateria", "escenario", "residuos", "🔋",
   situacion=_v("La laptop de Lucía dura solo 20 minutos con batería, pero todo lo demás funciona bien. ¿Qué conviene?",
                "La laptop de Lucía solo dura 20 minutos con batería, pero todo lo demás funciona bien. ¿Qué conviene?"),
   opciones=["Cambiar la batería", "Comprar una laptop nueva", "Botarla", "Guardarla en un cajón"],
   correcta=0,
   explica=_v("Cambiar la batería cuesta mucho menos y la laptop sigue sirviendo.",
              "Cambiar la batería es más barato y evita fabricar y desechar un equipo completo."))

_a("e_cajon", "escenario", "residuos", "📦",
   situacion=_v("Diego encontró tres celulares viejos en un cajón. Uno aún funciona. ¿Qué hace?",
                "Diego encontró tres celulares viejos en un cajón. Uno aún funciona. ¿Qué es lo mejor?"),
   opciones=["Donar el que funciona y llevar los otros a acopio", "Botar los tres a la basura", "Dejarlos otro año en el cajón", "Regalar los tres sin borrar nada"],
   correcta=0,
   explica=_v("Uno sigue ayudando a alguien y los otros se reciclan bien.",
              "El que funciona sigue en uso (previo borrado de datos) y los demás se reciclan correctamente."))

_a("e_video", "escenario", "datos", "🎬",
   situacion=_v("Camila va a ver una serie en su celular. ¿Qué ajuste ahorra más datos sin que casi se note?",
                "Camila va a ver una serie en su celular. ¿Qué ajuste ahorra más datos sin que casi se note?"),
   opciones=["Bajar la calidad a 720p", "Subir a la máxima calidad", "Abrir la serie en tres pantallas", "Reiniciar el celular"],
   correcta=0,
   explica=_v("En una pantalla chica, casi no se nota la diferencia.",
              "En pantallas pequeñas la diferencia visual es mínima y se transmiten menos datos."))

_a("e_salir", "escenario", "energia", "💻",
   situacion=_v("Sofía va a salir a almorzar y volverá en 3 horas. ¿Qué hace con su laptop?",
                "Sofía va a salir a almorzar y volverá en 3 horas. ¿Qué hace con su laptop?"),
   opciones=["La apaga o la suspende", "La deja encendida con todo abierto", "Sube el brillo al máximo", "La deja cargando con el brillo alto"],
   correcta=0,
   explica=_v("Si no se usa, mejor apagada o en reposo.",
              "Apagar o suspender corta el consumo en reposo, que puede estar entre 15 y 60 W."))

_a("e_pantalla_rota", "escenario", "residuos", "📱",
   situacion=_v("A Mateo le gusta un celular nuevo, pero el suyo solo tiene la pantalla rayada y funciona bien. ¿Qué es mejor?",
                "Mateo quiere cambiar de celular porque el suyo tiene la pantalla rayada, pero funciona bien. ¿Qué es mejor?"),
   opciones=["Ponerle un protector y seguir usándolo", "Comprar otro ya", "Tirar el celular", "Dejarlo de usar"],
   correcta=0,
   explica=_v("Si todavía funciona, un protector basta y no se fabrica otro.",
              "Si funciona, el protector resuelve el problema y evita fabricar un equipo nuevo."))

_a("e_nube", "escenario", "datos", "☁️",
   situacion=_v("Valeria tiene 3 000 fotos, muchas repetidas, en su celular y en la nube. ¿Qué hace?",
                "Valeria tiene 3 000 fotos, muchas repetidas, en su celular y en la nube. ¿Qué es lo mejor?"),
   opciones=["Borrar las repetidas y las borrosas", "Guardarlas todas para siempre", "Subir más copias", "Comprar más espacio"],
   correcta=0,
   explica=_v("Menos fotos guardadas significa menos energía en los servidores.",
              "Menos archivos almacenados reduce la energía que usan los centros de datos."))

_a("e_acopio_lejos", "escenario", "residuos", "📍",
   situacion=_v("Andrea no sabe dónde llevar un televisor viejo. ¿Qué puede hacer primero?",
                "Andrea no sabe dónde llevar un televisor viejo. ¿Qué puede hacer primero?"),
   opciones=["Buscar o preguntar por un punto de acopio o campaña", "Dejarlo en la calle", "Romperlo", "Quemarlo"],
   correcta=0,
   explica=_v("Hay que averiguar el lugar correcto antes de botarlo.",
              "Averiguar dónde se recibe es el primer paso. El 65,6 % del estudio dijo que hay pocos puntos de acopio."))

# ================================================================= ADIVINA EL DATO
_a("n_raee_hab", "adivina", "residuos", "🇵🇪",
   pregunta=_v("¿Cuántos kilos de basura electrónica genera cada persona en Perú al año?",
               "¿Cuántos kg de RAEE genera cada habitante de Perú al año?"),
   unidad="kg", rango=(0.0, 20.0, 0.5), inicial=10.0, respuesta=6.5, tolerancia=2.0,
   explica=_v("Son 6,5 kilos por persona, como unas 6 botellas grandes de agua llenas.",
              "Son 6,5 kg por habitante, unas 205 mil toneladas en total (MINAM, 2023)."))

_a("n_tratado_peru", "adivina", "residuos", "🔬",
   pregunta=_v("De cada 100 aparatos viejos en Perú, ¿cuántos reciben tratamiento especial?",
               "¿Qué porcentaje de los RAEE de Perú recibe tratamiento especializado?"),
   unidad="%", rango=(0.0, 100.0, 1.0), inicial=50.0, respuesta=7.0, tolerancia=5.0,
   explica=_v("Solo unos 7 de cada 100.", "Solo cerca de 7 % (MINAM, 2023)."))

_a("n_reciclado_mundo", "adivina", "residuos", "🌍",
   pregunta=_v("De toda la basura electrónica del mundo, ¿cuántos de cada 100 se reciclan de forma segura?",
               "¿Qué porcentaje de los residuos electrónicos del mundo se recolecta y recicla de forma segura?"),
   unidad="%", rango=(0.0, 100.0, 1.0), inicial=50.0, respuesta=22.3, tolerancia=8.0,
   explica=_v("Solo unos 22 de cada 100.", "22,3 % (Baldé et al., 2024)."))

_a("n_raee_mundo", "adivina", "residuos", "🌐",
   pregunta=_v("¿Cuántos millones de toneladas de basura electrónica se hicieron en el mundo en un año?",
               "¿Cuántos millones de toneladas de residuos electrónicos se generaron en el mundo en 2022?"),
   unidad="millones de toneladas", rango=(0.0, 150.0, 1.0), inicial=75.0, respuesta=62.0, tolerancia=15.0,
   explica=_v("Fueron 62 millones de toneladas.", "62 millones de toneladas (Baldé et al., 2024)."))

_a("n_latam", "adivina", "residuos", "🌎",
   pregunta=_v("En América Latina, ¿cuántos de cada 100 aparatos viejos se reciclan?",
               "¿Qué porcentaje de los residuos electrónicos de América Latina se recicla?"),
   unidad="%", rango=(0.0, 100.0, 1.0), inicial=50.0, respuesta=3.0, tolerancia=4.0,
   explica=_v("Solo unos 3 de cada 100.", "Solo cerca de 3 % (Baldé et al., 2022)."))

_a("n_laptop_reposo", "adivina", "energia", "💻",
   pregunta=_v("Una laptop prendida sin usar 4 horas al día, ¿cuántos kWh gasta en un año?",
               "Una laptop encendida sin uso 4 horas al día, ¿cuántos kWh consume en un año? (supuesto: 15 W en reposo)"),
   unidad="kWh", rango=(0.0, 200.0, 1.0), inicial=100.0, respuesta=21.9, tolerancia=10.0,
   explica=_v("Son unos 22 kWh. Parece poco, pero con varios aparatos y todos los días se suma.",
              "15 W × 4 h × 365 días = 21,9 kWh. Con varios equipos y todos los días se acumula."))

# ================================================================= CALCULADORAS
_a("c_reposo", "calc", "energia", "🧮", kind="reposo",
   titulo=_v("¿Cuánta luz gasta un aparato prendido sin usar?", "Calculadora de consumo en reposo"))
_a("c_cargadores", "calc", "energia", "🧮", kind="cargadores",
   titulo=_v("¿Cuánta luz gastan los cargadores enchufados?", "Calculadora de cargadores en vacío"))
_a("c_brillo", "calc", "energia", "🧮", kind="brillo",
   titulo=_v("¿Cuánto ahorra bajar el brillo?", "Calculadora de ahorro por brillo"))

# ================================================================= MINI RETOS (listas)
_a("l_cargadores", "checklist", "energia", "🔌",
   titulo=_v("Mini reto: caza cargadores", "Revisión de cargadores"),
   items=_v(["Busca cuántos cargadores están enchufados en tu casa", "Desenchufa los que no estén cargando nada", "Cuéntale a alguien lo que encontraste"],
            ["Contar cuántos cargadores están enchufados sin uso", "Desenchufar los que no están cargando", "Revisar de nuevo en la noche"]))

_a("l_cajon", "checklist", "residuos", "📦",
   titulo=_v("Mini reto: el cajón de aparatos", "Revisión del cajón de equipos"),
   items=_v(["Con un adulto, abre un cajón donde haya aparatos", "Separa los que ya no sirven", "Pregunta dónde se pueden llevar a reciclar"],
            ["Revisar cajones o cajas con equipos en desuso", "Separar los que no funcionan de los que sí", "Buscar el punto de acopio más cercano"]))

_a("l_pantalla", "checklist", "energia", "🔆",
   titulo=_v("Mini reto: pantallas amigas", "Revisión de pantallas"),
   items=_v(["Baja el brillo de tu pantalla", "Cierra las apps que no uses", "Apaga la pantalla al terminar"],
            ["Bajar el brillo y activar el brillo automático", "Cerrar apps y pestañas sin uso", "Reducir el tiempo de apagado de pantalla"]))

_a("l_datos", "checklist", "datos", "🗂️",
   titulo=_v("Mini reto: ordena tu celular", "Limpieza digital de 10 minutos"),
   items=_v(["Con ayuda, borra 5 fotos repetidas", "Borra 2 juegos o apps que no usas", "Vacía la papelera de fotos"],
            ["Borrar 10 fotos repetidas o capturas", "Desinstalar 3 apps sin uso", "Vaciar la papelera y los correos no deseados"]))

ACTIVIDADES_POR_ID = {a["id"]: a for a in ACTIVIDADES}


def texto(valor, tono):
    """Elige la versión de un texto según el tono (primaria usa «ni»)."""
    if isinstance(valor, dict) and "ni" in valor:
        return valor["ni"] if tono == "peque" else valor["gen"]
    return valor
