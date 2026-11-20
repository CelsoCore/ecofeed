"""Inventario de recomendaciones ("Para ti").

Cada tarjeta tiene una sola acción (`reto`, en infinitivo) y un texto por tono.
Convención del texto: la primera oración dice QUÉ hacer; el resto explica POR QUÉ
(la app muestra la primera oración y deja el resto en «¿Por qué?»).
Un tono en None significa que la recomendación no aplica a ese tono.
Los textos no personifican los equipos ni usan jerga forzada de videojuegos.
"""
from contenido import TONOS

TIPS = []


def _tip(id, emoji, categoria, titulo, textos, reto, dato=None, habito=None, barrera=None,
        dispositivos=(), tiempo="1 min", esfuerzo=1):
    if isinstance(textos, str):
        textos = (textos,) * 4
    por_tono = {t: x for t, x in zip(TONOS, textos) if x}
    TIPS.append({
        "id": id, "emoji": emoji, "categoria": categoria, "titulo": titulo, "textos": por_tono,
        "tonos": list(por_tono), "reto": reto, "dato": dato, "habito": habito, "barrera": barrera,
        "dispositivos": tuple(dispositivos), "tiempo": tiempo, "esfuerzo": esfuerzo,
    })


# Categorías: energia, residuos, datos, software. Orden de tonos: peque, gamer, tecnico, mayor.

# ================================================================= ENERGÍA
_tip("apagar_equipos", "💤", "energia", "Apaga al terminar",
     ("Apaga la compu cuando termines. Prendida sin usar sigue gastando luz.",
      "Apaga o suspende tu equipo cuando termines. En reposo sigue consumiendo entre 15 y 60 W.",
      "Apaga o suspende el equipo cuando termines. Un equipo encendido sin uso puede consumir entre 15 y 60 W durante horas.",
      "Apague la computadora cuando termine de usarla. Encendida sin uso sigue gastando luz y se nota en el recibo."),
     "Apagar o suspender el equipo al terminar", habito="apagar", barrera="olvido",
     dispositivos=("lap", "pc", "tab"), tiempo="10 seg", esfuerzo=1)

_tip("suspension_automatica", "⏲️", "energia", "Suspensión automática",
     (None,
      "Configura la suspensión automática en 10 minutos. Así el equipo se apaga solo si te distraes.",
      "Configura la suspensión automática a 10 minutos de inactividad. Elimina el consumo en reposo sin depender de la memoria.",
      "Pida a un familiar que active la suspensión automática. El equipo se apagará solo si lo olvida encendido."),
     "Activar la suspensión automática a 10 minutos", habito="apagar", barrera="olvido",
     dispositivos=("lap", "pc"), tiempo="2 min", esfuerzo=1)

_tip("brillo", "🔆", "energia", "Brillo más bajo",
     ("Baja el brillo de la pantalla. La batería dura más.",
      "Baja el brillo a la mitad en interiores. La pantalla es lo que más energía consume.",
      "Baja el brillo y activa el brillo automático. La pantalla es el componente de mayor consumo y el ahorro estimado ronda el 10 %.",
      "Baje el brillo de la pantalla. La batería dura más y la vista se cansa menos."),
     "Bajar el brillo de la pantalla", habito="ahorro", barrera="olvido",
     dispositivos=("cel", "tab", "lap"), tiempo="10 seg", esfuerzo=1)

_tip("modo_oscuro", "🌙", "energia", "Modo oscuro",
     (None,
      "Activa el modo oscuro. En pantallas OLED usa menos batería con fondos negros.",
      "Activa el modo oscuro si tu pantalla es OLED. Los píxeles negros no emiten luz y reducen el consumo.",
      "Active el modo oscuro del celular. Cansa menos la vista de noche y puede ahorrar batería."),
     "Activar el modo oscuro en el celular", habito="ahorro",
     dispositivos=("cel", "tab"), tiempo="1 min", esfuerzo=1)

_tip("desconectar_cargadores", "🔌", "energia", "Desenchufa el cargador",
     ("Desenchufa el cargador cuando el celular ya cargó. Enchufado sin carga gasta un poquito.",
      "Desenchufa el cargador al llegar al 100 %. Sin carga sigue gastando cerca de 0,5 W.",
      "Desconecta cargadores que no estén en uso. Cada cargador conectado sin carga consume cerca de 0,5 W las 24 horas.",
      "Desenchufe el cargador cuando ya no lo use. Enchufado sin nada conectado sigue gastando luz."),
     "Desenchufar el cargador al terminar de cargar", habito="cargadores", barrera="olvido",
     dispositivos=("cel", "tab", "lap", "audifonos"), tiempo="5 seg", esfuerzo=1)

_tip("regleta_interruptor", "🔘", "energia", "Regleta con interruptor",
     ("Usa una regleta con interruptor y apágala al irte. Así se apagan varios aparatos de una vez.",
      "Conecta tus equipos a una regleta con interruptor y apágala al terminar. Corta de una vez todos los consumos fantasma.",
      "Agrupa equipos en una regleta con interruptor. Un solo gesto elimina el consumo en espera de todo el puesto de trabajo.",
      "Use una regleta con interruptor y apáguela al terminar. Con un solo botón se desconectan varios aparatos."),
     "Conectar los equipos a una regleta con interruptor", habito="cargadores", barrera="olvido",
     dispositivos=("pc", "lap", "tv", "consola"), tiempo="5 min", esfuerzo=2)

_tip("cerrar_apps", "🧹", "energia", "Cierra lo que no usas",
     (None,
      "Cierra las apps y pestañas que no usas. Cada una sigue consumiendo procesador y batería.",
      "Cierra aplicaciones y pestañas en segundo plano. Reducen la carga del procesador y el consumo, y alargan la batería.",
      "Cierre los programas y pestañas que no usa. La computadora trabaja menos y la batería dura más."),
     "Cerrar apps y pestañas que no uso", habito="ahorro",
     dispositivos=("lap", "pc", "cel", "tab"), tiempo="30 seg", esfuerzo=1)

_tip("consola_apagado", "🎮", "energia", "Apaga la consola de verdad",
     ("Apaga la consola del todo al terminar. En reposo sigue prendida por dentro.",
      "Apaga la consola por completo, sin dejarla en suspensión. Y desactiva el inicio rápido y las descargas automáticas.",
      "Apaga la consola por completo y desactiva el inicio rápido y las descargas en reposo. La suspensión mantiene consumo y actualizaciones activas.",
      None),
     "Apagar la consola por completo al terminar", habito="apagar", barrera="olvido",
     dispositivos=("consola",), tiempo="1 min", esfuerzo=1)

_tip("tv_ahorro", "📺", "energia", "TV en modo ahorro",
     ("Apaga la tele cuando nadie la ve. Prendida sin mirar gasta luz.",
      "Activa el modo ahorro del televisor y apágalo si nadie lo ve. Baja el brillo y el consumo.",
      "Activa el modo eco del televisor, apágalo con el botón principal y no solo con el control. Reduce consumo y brillo innecesario.",
      "Apague el televisor cuando nadie lo mira y active el modo ahorro. Es una forma fácil de bajar el recibo."),
     "Activar el modo ahorro del televisor y apagarlo al no verlo", habito="ahorro",
     dispositivos=("tv",), tiempo="1 min", esfuerzo=1)

_tip("router_noche", "📡", "energia", "Router de noche",
     (None,
      "Apaga el router de noche si nadie lo usa. Pasa más de 8 horas sin hacer nada.",
      "Programa o apaga el router en la noche. Funciona las 24 horas, y la mitad de ese tiempo no se usa.",
      "Apague el router al acostarse y préndalo en la mañana. Así no gasta luz mientras duerme."),
     "Apagar el router por la noche", habito="apagar", barrera="olvido",
     dispositivos=("router",), tiempo="10 seg", esfuerzo=1)

_tip("wifi_datos", "📶", "energia", "Wi‑Fi mejor que datos",
     (None,
      "Usa Wi‑Fi en vez de datos móviles cuando puedas. Consume menos batería y energía de red.",
      "Prefiere Wi‑Fi a datos móviles para descargas y video. Consume menos batería del equipo y menos energía en la red.",
      "Use el Wi‑Fi de su casa en vez de los datos del celular. Gasta menos batería."),
     "Conectar el celular al Wi‑Fi al estar en casa", habito="ahorro",
     dispositivos=("cel", "tab"), tiempo="30 seg", esfuerzo=1)

_tip("notificaciones", "🔕", "energia", "Menos notificaciones",
     (None,
      "Desactiva las notificaciones que no necesitas. Cada aviso enciende la pantalla y consume batería.",
      "Desactiva las notificaciones innecesarias. Cada aviso despierta la pantalla y la conexión de datos.",
      "Desactive los avisos que no le sirven. El celular se enciende menos y la batería rinde más."),
     "Desactivar las notificaciones de tres apps", habito="ahorro",
     dispositivos=("cel", "tab"), tiempo="3 min", esfuerzo=1)

_tip("modo_avion_noche", "✈️", "energia", "Modo avión al dormir",
     (None,
      "Pon el celular en modo avión al dormir. Dejan de buscar señal y la batería rinde mejor.",
      "Activa el modo avión por la noche. Evita búsqueda de señal y notificaciones durante horas sin uso.",
      "Active el modo avión para dormir. No sonará y la batería durará más al día siguiente."),
     "Activar el modo avión al dormir", habito="ahorro", barrera="olvido",
     dispositivos=("cel",), tiempo="5 seg", esfuerzo=1)

_tip("carga_80", "🔋", "energia", "Carga hasta 80 %",
     ("No dejes el celular cargando toda la noche. Las baterías duran más si no se cargan siempre al 100 %.",
      "Carga entre 20 % y 80 % cuando puedas. La batería de litio se desgasta más rápido en los extremos.",
      "Mantén la carga entre 20 % y 80 % y activa el límite de carga si tu equipo lo permite. Alarga la vida útil de la batería y retrasa su reemplazo.",
      "Procure no dejar el celular cargando toda la noche. La batería dura más años si no se carga siempre hasta el tope."),
     "Cargar entre 20 % y 80 % de batería", habito="cargadores", barrera="olvido",
     dispositivos=("cel", "lap", "tab"), tiempo="Todo el día", esfuerzo=2)

_tip("calor_bateria", "🌡️", "energia", "Lejos del calor",
     ("No dejes el celular al sol ni bajo la almohada. El calor daña la batería.",
      "Evita cargar el celular al sol o bajo la almohada. El calor es lo que más desgasta una batería.",
      "Evita calor excesivo al cargar o usar el equipo. Las temperaturas altas aceleran la degradación de la batería.",
      "No deje el celular al sol ni lo cargue bajo la almohada. El calor malogra la batería."),
     "Cargar el celular en un lugar fresco y ventilado", habito="cargadores",
     dispositivos=("cel", "lap", "tab"), tiempo="Todo el día", esfuerzo=1)

_tip("audifonos_cuidado", "🎧", "energia", "Cuida los audífonos",
     ("Guarda los audífonos en su estuche. Así no se rompen ni se pierden.",
      "Guarda los audífonos en su estuche y no jales el cable. La mayoría falla por golpes y tirones.",
      "Guarda los audífonos en su estuche y evita descargarlos del todo. Alarga la vida de una batería pequeña, difícil de reemplazar.",
      "Guarde los audífonos en su estuche. Así duran más y no tiene que comprar otros."),
     "Guardar los audífonos en su estuche después de usarlos", habito="reparar",
     dispositivos=("audifonos",), tiempo="10 seg", esfuerzo=1)

# ================================================================= VIDA ÚTIL Y RAEE
_tip("reparar_ram_ssd", "🔧", "residuos", "Mejorar antes de cambiar",
     (None,
      "Si tu laptop va lenta, prueba más RAM o un SSD antes de comprar otra. Sale más barato y genera menos basura.",
      "Evalúa ampliar RAM o cambiar a SSD antes de reemplazar el equipo. Puede añadir un año o más de vida útil por una fracción del costo.",
      "Si su computadora está lenta, consulte con un técnico si se puede mejorar. Muchas veces sale más barato que comprar una nueva."),
     "Consultar una mejora de RAM o SSD antes de comprar un equipo nuevo", habito="reparar", barrera="reparar_caro",
     dispositivos=("lap", "pc"), tiempo="Una consulta", esfuerzo=3)

_tip("limpiar_polvo", "🌬️", "residuos", "Limpieza interna",
     (None,
      "Limpia el polvo de las rejillas de tu equipo cada pocos meses. Si se calienta menos, dura más.",
      "Limpia el polvo de ventiladores y rejillas con aire a presión. Menos temperatura implica menos desgaste y menos consumo del ventilador.",
      "Pida limpiar el polvo de la computadora una vez al año. Así se calienta menos y dura más."),
     "Limpiar el polvo de rejillas y ventiladores", habito="reparar",
     dispositivos=("lap", "pc", "consola"), tiempo="15 min", esfuerzo=2)

_tip("funda_protector", "🛡️", "residuos", "Funda y vidrio templado",
     ("Ponle funda y protector de pantalla al celular. Así se rompe menos si se cae.",
      "Usa funda y vidrio templado. Una pantalla rota es una de las causas más comunes de cambiar un celular que aún funciona.",
      "Usa funda y protector de pantalla. Evita roturas, que son una causa frecuente de reemplazo prematuro.",
      "Use una funda y un protector de pantalla. Así evita roturas y gastos en reparaciones."),
     "Colocar funda y protector de pantalla", habito="reparar",
     dispositivos=("cel", "tab"), tiempo="5 min", esfuerzo=1)

_tip("cambiar_bateria", "🔋", "residuos", "Cambia la batería, no el equipo",
     (None,
      "Si la batería dura poco, cámbiala en un servicio técnico antes de comprar otro equipo. Cuesta mucho menos.",
      "Si la batería se degrada, reemplázala antes de cambiar el equipo completo. Es una reparación de bajo costo que suma años de uso.",
      "Si la batería ya dura muy poco, cámbiela en un servicio técnico. Cuesta mucho menos que un celular nuevo."),
     "Cotizar el cambio de batería antes de comprar otro equipo", habito="reparar", barrera="reparar_caro",
     dispositivos=("cel", "lap", "tab"), tiempo="Una consulta", esfuerzo=3)

_tip("reacondicionado", "🔄", "residuos", "Comprar reacondicionado",
     (None,
      "Cuando necesites un equipo, mira primero los reacondicionados. Funcionan bien y evitan fabricar otro.",
      "Considera equipos reacondicionados con garantía. Evitan el carbono de fabricar uno nuevo y cuestan menos.",
      "Si necesita cambiar de equipo, revise los reacondicionados con garantía. Cuestan menos y funcionan bien."),
     "Revisar opciones reacondicionadas antes de comprar", habito="reparar", barrera="reparar_caro",
     dispositivos=("cel", "lap", "tab", "pc"), tiempo="15 min", esfuerzo=2)

_tip("comprar_necesidad", "🛒", "residuos", "¿Lo necesito o lo quiero?",
     ("Antes de pedir un aparato nuevo, pregúntate si el que tienes aún sirve.",
      "Antes de comprar, espera 7 días y pregúntate si realmente lo necesitas. Muchos cambios son por moda, no por falla.",
      "Antes de reemplazar un equipo, compara lo que realmente necesitas con lo que ya tienes. La compra más sostenible es la que no se hace.",
      "Antes de comprar un aparato nuevo, pregúntese si el que tiene aún sirve. Muchas veces sí."),
     "Esperar 7 días antes de comprar un equipo nuevo", habito="reparar",
     tiempo="7 días", esfuerzo=2)

_tip("etiqueta_eficiencia", "🏷️", "residuos", "Mira la etiqueta",
     ("Cuando compren un aparato, pide ayuda para mirar su etiqueta de energía.",
      "Al comprar, busca la etiqueta de eficiencia energética. Un equipo eficiente se paga solo con la luz que ahorra.",
      "Compara la etiqueta de eficiencia energética antes de comprar. El menor consumo se amortiza durante la vida útil.",
      "Al comprar un aparato, mire la etiqueta de eficiencia. Los más eficientes gastan menos luz."),
     "Comparar la etiqueta de eficiencia antes de comprar", habito="ahorro",
     dispositivos=("tv", "pc", "lap"), tiempo="5 min", esfuerzo=1)

_tip("cargador_usbc", "🔗", "residuos", "Un cargador para todo",
     (None,
      "Usa un cargador común (USB‑C) para tus equipos. Menos cables y cargadores significa menos basura.",
      "Unifica tus equipos en un cargador USB‑C. Reduce cables, cargadores y residuos accesorios.",
      None),
     "Usar un solo cargador USB‑C para varios equipos", habito="cargadores",
     dispositivos=("cel", "tab", "lap", "audifonos"), tiempo="Una compra", esfuerzo=2)

_tip("pilas_recargables", "🔁", "residuos", "Pilas recargables",
     ("Usa pilas recargables en los juguetes y controles. Las comunes se botan después de un tiempo.",
      "Cambia a pilas recargables en controles y accesorios. Evitas decenas de pilas desechables al año.",
      "Usa pilas recargables en mandos y accesorios. Reduces residuos peligrosos y el costo a largo plazo.",
      "Use pilas recargables en el control remoto y los relojes. Gasta menos y contamina menos."),
     "Cambiar a pilas recargables en controles y accesorios", habito="reciclar",
     dispositivos=("consola", "tv"), tiempo="Una compra", esfuerzo=2)

_tip("reciclar_acopio", "📍", "residuos", "Lleva tus equipos a un punto de acopio",
     ("Pide a un adulto que lleve los aparatos viejos a un punto de reciclaje. No van a la basura.",
      "Lleva tus equipos viejos a un punto de acopio. Tienen metales que contaminan si se botan.",
      "Entrega equipos en desuso a un punto de acopio autorizado. Perú trata cerca de 7 % de sus RAEE; cada equipo cuenta.",
      "Lleve los aparatos viejos a un punto de acopio. Es lo mejor que se puede hacer con ellos."),
     "Llevar un equipo en desuso a un punto de acopio",
     dato="Perú genera 6,5 kg de RAEE por habitante y solo cerca de 7 % recibe tratamiento (MINAM, 2023).",
     habito="reciclar", barrera="puntos", tiempo="Un día", esfuerzo=3)

_tip("pilas_acopio", "🪫", "residuos", "Pilas usadas, al acopio",
     ("Guarda las pilas gastadas en un frasco y no las botes a la basura.",
      "Junta las pilas usadas y llévalas a un punto de acopio. Tienen metales que contaminan el suelo y el agua.",
      "Almacena pilas y baterías usadas por separado y entrégalas en acopio. Contienen metales pesados.",
      "Junte las pilas usadas en un frasco y llévelas a un punto de acopio. No van a la basura."),
     "Guardar las pilas usadas en un frasco hasta llevarlas al acopio", habito="reciclar", barrera="puntos",
     tiempo="5 min", esfuerzo=1)

_tip("guardar_raee", "📦", "residuos", "No lo guardes olvidado",
     ("Si hay aparatos guardados en un cajón, pide que los lleven a reciclar.",
      "Revisa los cajones: equipos que no usas y no sirven deberían ir a acopio, no quedarse guardados.",
      "Revisa equipos almacenados sin uso. Entregarlos a tiempo recupera materiales y evita que terminen en la basura común.",
      "Revise los cajones: si hay aparatos viejos que ya no sirven, llévelos a reciclar."),
     "Revisar el cajón y separar los equipos que ya no sirven", habito="reciclar", barrera="olvido",
     tiempo="10 min", esfuerzo=1)

_tip("donar_revender", "🤝", "residuos", "Dona o revende",
     ("Un aparato que funciona puede ayudar a otra persona. Pregunta si alguien lo necesita.",
      "Si tu equipo aún funciona, dónalo o véndelo. Seguirá en uso y no se convertirá en residuo.",
      "Si el equipo funciona, dónalo o revéndelo. Extiende su vida útil y retrasa su paso a residuo.",
      "Si el aparato aún funciona, regálelo o véndalo. Otra persona lo aprovechará."),
     "Donar o vender un equipo que aún funciona", habito="reciclar", barrera="puntos",
     tiempo="Un día", esfuerzo=2)

_tip("borrar_datos", "🧽", "residuos", "Borra tus datos antes de entregar",
     (None,
      "Antes de regalar o reciclar un celular, restablécelo de fábrica y cierra tus cuentas. Así tus datos quedan protegidos.",
      "Antes de entregar un equipo, haz copia de seguridad y restablécelo de fábrica. Es la barrera principal contra la fuga de datos.",
      "Antes de regalar un celular, pida ayuda para borrar sus fotos y cuentas. Así nadie ve sus datos."),
     "Restablecer de fábrica un equipo antes de entregarlo", habito="reciclar", barrera="info",
     tiempo="15 min", esfuerzo=2)

_tip("tienda_devolucion", "🏪", "residuos", "Devolver en la tienda",
     (None,
      "Pregunta en la tienda si reciben equipos o pilas viejas al comprar uno nuevo. Algunas lo hacen.",
      "Consulta si el comercio recibe equipos usados al comprar uno nuevo. Es una vía de entrega sin esfuerzo extra.",
      "Al comprar un aparato, pregunte si recibe el viejo. Algunas tiendas lo hacen."),
     "Preguntar en la tienda si reciben equipos viejos", habito="reciclar", barrera="puntos",
     tiempo="1 min", esfuerzo=1)

_tip("lista_inventario", "📝", "residuos", "Haz tu lista de aparatos",
     ("Con un adulto, anota los aparatos de tu casa y cuáles ya no se usan.",
      "Haz una lista de tus equipos: qué tienes, cuántos años tiene cada uno y cuáles ya no usas.",
      "Elabora un inventario de dispositivos con antigüedad y estado. Permite planificar reparaciones y entregas a acopio.",
      "Anote en un cuaderno los aparatos de su casa y cuáles ya no usa."),
     "Anotar los aparatos que tengo y cuáles no uso", habito="reciclar", barrera="info",
     tiempo="10 min", esfuerzo=1)

# ================================================================= DATOS Y NUBE
_tip("depurar_archivos", "🗂️", "datos", "Borra lo que no usas",
     ("Con ayuda de un adulto, borra juegos y fotos que ya no usas.",
      "Borra apps, descargas y archivos que ya no usas. Lo guardado en la nube vive en centros de datos que funcionan siempre.",
      "Depura archivos, correos y servicios en la nube sin uso. Los centros de datos superan los 460 TWh anuales y casi 0,5 % de las emisiones.",
      "Borre fotos repetidas y archivos que ya no necesita. Libera espacio y gasta menos."),
     "Borrar 10 archivos o apps que ya no uso", habito="depurar", barrera="olvido",
     dispositivos=("cel", "lap", "pc", "tab"), tiempo="5 min", esfuerzo=1)

_tip("fotos_duplicadas", "🖼️", "datos", "Fotos repetidas",
     ("Borra las fotos repetidas o borrosas. Ocupan lugar y no sirven.",
      "Borra capturas, fotos repetidas y videos viejos. Se acumulan en tu celular y en la nube sin que lo notes.",
      "Elimina duplicados y capturas de pantalla antiguos. Reduce almacenamiento local y en nube.",
      "Borre las fotos repetidas o borrosas. Así le queda más espacio."),
     "Borrar fotos repetidas y capturas viejas", habito="depurar",
     dispositivos=("cel", "tab"), tiempo="5 min", esfuerzo=1)

_tip("bajar_spam", "📧", "datos", "Limpia el correo",
     (None,
      "Date de baja de los correos que no lees. Cada uno se guarda en servidores aunque no lo abras.",
      "Date de baja de boletines que no lees y vacía spam y papelera. Reduce almacenamiento y tráfico innecesario.",
      "Anule la suscripción a los correos que no lee y vacíe la papelera."),
     "Darme de baja de 5 correos que no leo", habito="depurar", barrera="olvido",
     dispositivos=("lap", "pc", "cel"), tiempo="5 min", esfuerzo=1)

_tip("streaming_calidad", "🎬", "datos", "Calidad de video adecuada",
     ("No hace falta ver los videos en la máxima calidad en una pantalla pequeña.",
      "En el celular, ve videos en 720p. En una pantalla pequeña casi no se nota y se transmiten menos datos.",
      "Reduce la calidad de streaming a 720p en pantallas pequeñas. Disminuye la transferencia y la carga en centros de datos.",
      "En el celular, no hace falta ver los videos en la máxima calidad. Se nota poco y gasta menos datos."),
     "Bajar la calidad de video a 720p en el celular", habito="ahorro",
     dispositivos=("cel", "tab", "tv", "lap"), tiempo="30 seg", esfuerzo=1)

_tip("musica_descargada", "🎵", "datos", "Descarga tu música",
     (None,
      "Descarga las canciones que más escuchas para no transmitirlas cada vez. Ahorras datos y energía de red.",
      "Descarga las listas que repites para no transmitirlas una y otra vez. Cada reproducción en streaming activa servidores.",
      None),
     "Descargar mi lista de música favorita", habito="ahorro",
     dispositivos=("cel", "audifonos"), tiempo="5 min", esfuerzo=1)

_tip("camara_videollamada", "🎥", "datos", "Cámara apagada si no hace falta",
     (None,
      "En llamadas grupales, apaga la cámara cuando no sea necesaria. El video es lo que más datos consume.",
      "Apaga la cámara en videollamadas cuando no sea necesaria. El video es lo que más datos transmite.",
      None),
     "Apagar la cámara en videollamadas cuando no la necesite", habito="ahorro",
     dispositivos=("lap", "pc", "cel"), tiempo="Cada llamada", esfuerzo=1)

_tip("enlaces_no_adjuntos", "🔗", "datos", "Enlace en vez de adjunto",
     (None,
      "Envía un enlace en vez de adjuntar el archivo a varias personas. Evitas copias repetidas.",
      "Comparte enlaces en lugar de adjuntar el mismo archivo a muchos destinatarios. Se evita multiplicar copias en servidores.",
      None),
     "Compartir un enlace en vez de enviar un adjunto", habito="depurar",
     dispositivos=("lap", "pc"), tiempo="Cada envío", esfuerzo=1)

# ================================================================= SOFTWARE Y HÁBITOS
_tip("actualizar_sistema", "⬆️", "software", "Mantén el sistema actualizado",
     (None,
      "Instala las actualizaciones: mejoran la seguridad y el rendimiento, y tu equipo dura más años.",
      "Instala actualizaciones del sistema. Mejoran seguridad y rendimiento, y extienden los años de soporte útil.",
      "Instale las actualizaciones que le pide el aparato. Lo mantienen seguro y funcionando bien."),
     "Instalar las actualizaciones pendientes del sistema", habito="reparar", barrera="olvido",
     dispositivos=("cel", "lap", "pc", "tab"), tiempo="10 min", esfuerzo=1)

_tip("software_eficiente", "🧩", "software", "Programas livianos",
     (None,
      "Prefiere apps y navegadores livianos. Un equipo con menos carga trabaja más rápido y consume menos.",
      "Usa software liviano: desinstala lo que no uses y prefiere versiones web o ligeras. Un equipo menos exigido dura más.",
      None),
     "Desinstalar tres programas que no uso", habito="depurar",
     dispositivos=("lap", "pc"), tiempo="5 min", esfuerzo=1)

_tip("graficos_fps", "🕹️", "software", "Gráficos justos",
     (None,
      "En tus juegos, limita los FPS a lo que tu pantalla muestra y baja los gráficos que no notas. Gastas menos energía y se calienta menos.",
      "Limita los FPS a la tasa de tu pantalla y ajusta gráficos. Un límite de FPS reduce el consumo de la tarjeta gráfica.",
      None),
     "Limitar los FPS al de mi pantalla en mis juegos", habito="ahorro",
     dispositivos=("pc", "consola", "lap"), tiempo="3 min", esfuerzo=1)

_tip("laptop_superficie", "🪟", "software", "Superficie plana",
     ("Usa la laptop sobre una mesa, no sobre la cama. Así respira mejor el ventilador.",
      "Usa la laptop sobre una superficie dura y plana. Sobre cama o sofá se tapan las entradas de aire y se calienta.",
      "Apoya la laptop sobre superficies duras. Las entradas de aire bloqueadas elevan la temperatura y aceleran el desgaste.",
      "Use la computadora portátil sobre una mesa. Sobre la cama se calienta y se malogra antes."),
     "Usar la laptop sobre una superficie plana", habito="reparar",
     dispositivos=("lap",), tiempo="Todo el día", esfuerzo=1)

_tip("bateria_hinchada", "⚠️", "software", "Batería hinchada: dejar de usar",
     ("Si un aparato se ve hinchado o huele raro, avisa a un adulto y no lo cargues.",
      "Si la batería se hincha o el equipo se calienta de más, deja de cargarlo y llévalo a un servicio técnico.",
      "Una batería hinchada es un riesgo de seguridad. Deja de usarla y entrégala a un servicio técnico o punto de acopio.",
      "Si el aparato se ve hinchado o huele raro, deje de cargarlo y llévelo a un técnico."),
     "Revisar si algún aparato tiene la batería hinchada", habito="reparar",
     dispositivos=("cel", "lap", "tab"), tiempo="2 min", esfuerzo=1)

_tip("campana", "📢", "software", "Cuéntaselo a alguien",
     ("Cuéntale a tu familia una cosa que aprendiste hoy.",
      "Cuéntale a alguien de tu círculo un dato que aprendiste aquí. Muchos no reciben información sobre cómo cuidar sus equipos.",
      "Comparte con tu entorno un dato aprendido. El 65,6 % de los encuestados dijo no recibir información suficiente en su universidad.",
      "Cuéntele a un familiar algo que haya aprendido aquí."),
     "Contar a alguien un dato que aprendí hoy", barrera="info",
     tiempo="2 min", esfuerzo=1)

_tip("aprender_huella", "📚", "software", "Aprende un poco más",
     (None,
      "Dedica 5 minutos a leer sobre residuos electrónicos. Saber dónde terminan tus equipos cambia lo que haces con ellos.",
      "Revisa un artículo sobre RAEE o centros de datos. La falta de información es una de las barreras que más se repite en el estudio.",
      None),
     "Leer un artículo corto sobre residuos electrónicos", barrera="info",
     tiempo="5 min", esfuerzo=1)

# Años extra de vida útil que logra cumplir la tarjeta: (dispositivos, años)
VIDA_EXTRA = {
    "carga_80": (("cel", "lap", "tab"), 1.0),
    "calor_bateria": (("cel", "lap", "tab"), 0.5),
    "reparar_ram_ssd": (("lap", "pc"), 1.0),
    "limpiar_polvo": (("lap", "pc", "consola"), 0.5),
    "funda_protector": (("cel", "tab"), 1.0),
    "cambiar_bateria": (("cel", "lap", "tab"), 1.5),
    "reacondicionado": (("cel", "lap", "tab", "pc"), 2.0),
    "actualizar_sistema": (("cel", "lap", "pc", "tab"), 0.5),
    "laptop_superficie": (("lap",), 0.5),
    "audifonos_cuidado": (("audifonos",), 0.5),
    "donar_revender": (("cel", "lap", "tab", "pc"), 2.0),
    "comprar_necesidad": (("cel", "lap", "tab", "pc"), 1.0),
}

TIPS_POR_ID = {t["id"]: t for t in TIPS}
