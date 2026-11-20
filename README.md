# EcoFeed (v3)

App de informática verde basada en el informe de la UNT (n = 32). Hecha con Streamlit y Python.

## Cómo ejecutarla
```
pip install -r requirements.txt
streamlit run app.py
```

## Archivos
- `app.py`: pantallas (login, cuestionario, "Para ti", simulador, misiones, diagnóstico, perfil).
- `contenido.py`: dispositivos (8), hábitos, barreras, textos por tono, insignias, simulador.
- `tips.py`: 46 recomendaciones (energía, residuos y vida útil, datos y nube, hábitos y software).
- `actividades.py`: 43 tarjetas interactivas (mitos, preguntas, casos, adivina el dato, calculadoras, mini retos).
- `logica.py`: cálculos, XP, racha y guardado verificable.
- `datos/usuarios.json`: se crea solo al registrar el primer usuario.

## Tonos por edad y grado
`peque` (primaria) · `gamer` (secundaria) · `tecnico` (superior y adultos) · `mayor`.
En primaria y secundaria los hábitos se preguntan con una escena de 3 opciones (valen 5, 3 y 1) y después se
muestra una explicación corta. En los demás tonos se usa la escala 1 a 5 del informe.

## Prueba de que el registro se guarda
En «Mi energía» o «Diagnóstico» hay un panel con los días leídos desde el archivo, la fecha del último día,
la hora de modificación y si lo que se ve en pantalla coincide con el disco. También se puede descargar el
registro en CSV (abre en Excel) y una copia en JSON. Para la exposición: guardar un día, detener la app con
Ctrl+C, volver a ejecutarla, entrar con el mismo usuario y ver que todo sigue ahí.

## Valores que debes reemplazar por fuentes citadas
Potencias, vidas útiles, pesos y CO₂ de fabricación (`contenido.py`), y en `logica.py`: FACTOR_CO2,
PRECIO_KWH, HORAS_REPOSO_EVITABLE, W_CARGADOR_VACIO, AHORRO_BRILLO, AHORRO_CERRAR_APPS, AHORRO_FPS.
Son valores de referencia, no mediciones.

## Antes de publicarla
Para uso público hacen falta una base de datos (en vez de un archivo), hosting, consentimiento de padres
o tutores para menores y una política de datos.

## Ilustraciones
Las tarjetas llevan dibujos propios en SVG (`ilustraciones.py`): enchufe, pantalla, batería, reciclaje, etc.
Son originales, sin personajes, sin caras en los objetos y sin material con derechos de autor. El color de acento cambia por tono
(amarillo con destellos para primaria y secundaria; verde menta sobrio para adultos y mayores).

## Fin de ronda
Al llegar a la última tarjeta aparece «Ronda completa» con tus aciertos. Desde ahí puedes repasar lo que fallaste
o empezar una ronda nueva mezclada (primero lo que aún no resolviste). El panel de la derecha muestra el avance de la ronda y lo que sigue.

## Administrador
Define `admin_user` y `admin_pass` (ver `.streamlit/secrets.toml.example`). Entra con esa cuenta en la misma pantalla de login y verás el panel del administrador.
Los demás usuarios entran normal. La clave del admin nunca va en el código.

## Publicar para que lo usen desde el celular
1. Sube la carpeta a un repositorio de GitHub (el `.gitignore` ya excluye `datos/` y `secrets.toml`).
2. En share.streamlit.io: New app, elige el repositorio, archivo `app.py`.
3. En Advanced settings > Secrets pega `admin_user` y `admin_pass`.
4. Comparte el enlace que te da (termina en .streamlit.app).

## Para que no se acabe
Pestaña ⚡ Desafío: reto nuevo cada día (5 XP), desafío infinito (preguntas con números al azar calculadas con los mismos supuestos del simulador) y tabla de la clase (con apodos; cada persona puede ocultarse).

## Mi día
Pestaña 🗓️ Mi día: la persona arma su jornada en bloques y la app marca dónde se pierde energía (equipos encendidos sin uso, brillo, apps, cargadores) con consejos con hora. No pide reducir estudio ni trabajo.

## Pruebas
`python -m unittest discover -s tests`

## Sesión
Al iniciar sesión el enlace lleva un código que vence en 24 horas para que recargar la página no cierre la sesión. Cerrar sesión lo borra.

## Que no se pierdan los datos
En la nube gratuita el disco se borra al reiniciar la app. EcoFeed sube una copia de `usuarios.json` a un repositorio privado de GitHub
unos segundos después de cada guardado, y si al arrancar no encuentra el archivo, lo restaura desde ahí. Cada versión queda en el historial de GitHub.
1. En GitHub crea un repositorio **privado** nuevo, por ejemplo `ecofeed-datos`, marcando «Add a README file» (así existe la rama main).
2. Settings (de tu cuenta) → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token.
   Repository access: *Only select repositories* y elige `ecofeed-datos`. Permissions → Repository permissions → **Contents: Read and write**.
3. En Streamlit Cloud: tu app → Settings → Secrets, agrega `github_token` y `github_repo` (ver `.streamlit/secrets.toml.example`).
4. Entra como administrador: en «Respaldo automático en GitHub» debe decir «Configurado». Pulsa «Respaldar ahora» y revisa que aparezca el archivo en el repositorio.
El repositorio de datos debe ser privado: el archivo contiene los usuarios y las claves cifradas.

## Dónde está cada cosa
- Cuenta de administrador: `admin_user` y `admin_pass` en Secrets (`logica.py`, funciones `config_admin` y `es_admin`).
- Textos de pantalla: `app.py` (avisos con `st.caption`), `contenido.py` (textos por tono), `tips.py` (recomendaciones), `actividades.py` (actividades), `rutina.py` (consejos de «Mi día»).
