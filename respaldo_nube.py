"""Respaldo automático de los datos de usuarios en un repositorio PRIVADO de GitHub.

Por qué: en Streamlit Community Cloud el disco se borra cuando la app se reinicia. Aquí, cada vez que se guarda
algo, unos segundos después se sube una copia a GitHub; y si al arrancar no existe el archivo local, se restaura
desde esa copia. Si no configuras nada, este módulo no hace nada y la app funciona igual (solo con archivo local).

Se configura con tres valores en Secrets (o variables de entorno): github_token, github_repo y, opcional, github_branch.
"""
import base64
import json
import os
import threading
import urllib.error
import urllib.request
from datetime import datetime

DEMORA_SEG = 5            # espera para juntar varios guardados seguidos en una sola subida
ARCHIVO_REMOTO = "usuarios.json"
ESTADO = {"ultimo_ok": None, "ultimo_error": None, "restaurado": False}
_candado = threading.Lock()
_timer = None


def config():
    """(token, repo, rama) o None si no está configurado."""
    token, repo, rama = (os.environ.get("ECOFEED_GITHUB_TOKEN"), os.environ.get("ECOFEED_GITHUB_REPO"),
                         os.environ.get("ECOFEED_GITHUB_BRANCH"))
    if not (token and repo):
        try:
            import streamlit as st
            token, repo = st.secrets["github_token"], st.secrets["github_repo"]
            rama = st.secrets.get("github_branch", rama)
        except Exception:
            return None
    return (str(token).strip(), str(repo).strip(), (rama or "main").strip()) if token and repo else None


def _pedir(metodo, url, token, cuerpo=None):
    datos = json.dumps(cuerpo).encode("utf-8") if cuerpo is not None else None
    req = urllib.request.Request(url, data=datos, method=metodo, headers={
        "Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
        "User-Agent": "ecofeed-respaldo", "X-GitHub-Api-Version": "2022-11-28"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def _url(repo, rama):
    return f"https://api.github.com/repos/{repo}/contents/{ARCHIVO_REMOTO}?ref={rama}"


def descargar():
    """Texto del respaldo remoto, o None si todavía no existe."""
    cfg = config()
    if not cfg:
        return None
    token, repo, rama = cfg
    try:
        r = _pedir("GET", _url(repo, rama), token)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    return base64.b64decode(r["content"]).decode("utf-8")


def subir(texto):
    """Sube el texto como nueva versión del archivo remoto (cada versión queda en el historial de GitHub)."""
    cfg = config()
    if not cfg:
        return False
    token, repo, rama = cfg
    try:
        sha = _pedir("GET", _url(repo, rama), token).get("sha")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
        sha = None
    cuerpo = {"message": f"respaldo {datetime.now().isoformat(timespec='seconds')}", "branch": rama,
              "content": base64.b64encode(texto.encode("utf-8")).decode("ascii")}
    if sha:
        cuerpo["sha"] = sha
    _pedir("PUT", f"https://api.github.com/repos/{repo}/contents/{ARCHIVO_REMOTO}", token, cuerpo)
    return True


def respaldar_ahora(ruta):
    """Sube el archivo local. Anota en ESTADO si salió bien o el motivo del error."""
    with _candado:
        try:
            if not ruta.exists():
                return False
            ok = subir(ruta.read_text(encoding="utf-8"))
            if ok:
                ESTADO.update(ultimo_ok=datetime.now().isoformat(timespec="seconds"), ultimo_error=None)
            return ok
        except Exception as e:  # noqa: BLE001 - un fallo de red no debe romper la app
            ESTADO["ultimo_error"] = f"{type(e).__name__}: {e}"[:300]
            return False


def programar(ruta):
    """Llamar después de cada guardado: junta varios guardados y sube una sola vez, en segundo plano."""
    global _timer
    if not config():
        return
    if _timer is not None:
        _timer.cancel()
    _timer = threading.Timer(DEMORA_SEG, respaldar_ahora, args=(ruta,))
    _timer.daemon = True
    _timer.start()


def restaurar(ruta):
    """Si no hay archivo local, lo reconstruye desde GitHub. Devuelve True si restauró algo."""
    if ruta.exists() or not config():
        return False
    try:
        texto = descargar()
        if not texto:
            return False
        json.loads(texto)                      # que sea un JSON válido antes de usarlo
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(texto, encoding="utf-8")
        ESTADO["restaurado"] = True
        return True
    except Exception as e:  # noqa: BLE001
        ESTADO["ultimo_error"] = f"restaurar: {type(e).__name__}: {e}"[:300]
        return False
