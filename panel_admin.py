"""Panel del administrador (docente): quién usa la app y cómo va cada persona. Solo se llega con la cuenta admin."""
import pandas as pd
import streamlit as st

import contenido as C
import logica as L
import respaldo_nube as RN


def panel_admin():
    st.markdown("## 🛠️ Panel del administrador")
    st.caption("Solo tú ves esta pantalla. No se muestran contraseñas.")
    filas = L.filas_admin()
    df = pd.DataFrame(filas)
    hoy = pd.Timestamp.today().strftime("%Y-%m-%d")

    c = st.columns(5)
    c[0].metric("Usuarios", len(df))
    c[1].metric("Completaron la encuesta", int((df["encuesta"] == "sí").sum()) if len(df) else 0)
    c[2].metric("Activos hoy", int(df["ultimo_acceso"].str.startswith(hoy).sum()) if len(df) else 0)
    c[3].metric("Días guardados", int(df["dias_guardados"].sum()) if len(df) else 0)
    tot, ok = (int(df["actividades"].sum()), int(df["aciertos"].sum())) if len(df) else (0, 0)
    c[4].metric("Aciertos", f"{round(100 * ok / tot)} %" if tot else "—")

    if not len(df):
        st.info("Aún no hay usuarios. Comparte el enlace de la app para que se registren.")
    else:
        g1, g2 = st.columns(2, gap="large")
        with g1:
            st.write("**Usuarios por tono (edad y grado)**")
            st.bar_chart(df["tono"].value_counts(), color="#16a34a")
        with g2:
            st.write("**Promedio de cada hábito (1 a 5)**")
            prom = L.promedio_habitos()
            if prom:
                st.bar_chart(pd.Series({C.HABITOS[k]["titulo"]: v
                                        for k, v in prom.items()}), color="#f59e0b")
            else:
                st.caption("Nadie ha completado el cuestionario todavía.")

        st.write("**Personas registradas**")
        st.dataframe(df.sort_values("ultimo_acceso", ascending=False), use_container_width=True, hide_index=True)
        st.download_button("⬇️ Descargar tabla (CSV)", df.to_csv(index=False).encode("utf-8-sig"),
                           "ecofeed_usuarios.csv", "text/csv")

        st.write("**Ver el detalle de una persona**")
        u = st.selectbox("Usuario", df["usuario"], key="adm_u")
        rec = L.normalizar(L._cargar_todo()[u])
        semana = L.semana(rec)
        d1, d2 = st.columns(2, gap="large")
        with d1:
            st.caption("Consumo guardado en los últimos 7 días (kWh)")
            st.bar_chart(pd.Series({f"{d.strftime('%d/%m')}": k for d, _, _, k in semana}), color="#16a34a")
        with d2:
            hab = rec["perfil"].get("habitos", {})
            if hab:
                st.caption("Hábitos que respondió")
                st.dataframe(pd.DataFrame({"hábito": list(hab), "valor (1-5)": list(hab.values())}),
                             hide_index=True, use_container_width=True)
            else:
                st.caption("Todavía no completó el cuestionario inicial.")
        filas_h = L.historial_filas(rec)
        if filas_h:
            st.dataframe(pd.DataFrame(filas_h), hide_index=True, use_container_width=True)

    with st.expander("🛟 Respaldo automático en GitHub", expanded=not RN.config()):
        if not RN.config():
            st.error("No está configurado: si la app se reinicia, los datos se pierden. Agrega github_token y github_repo en Secrets "
                     "(ver README, sección «Que no se pierdan los datos»).")
        else:
            st.success(f"Configurado: se sube una copia a {RN.config()[1]} unos segundos después de cada guardado.")
            if RN.ESTADO["restaurado"]:
                st.info("Al arrancar, los datos se restauraron desde GitHub.")
            st.write(f"Último respaldo correcto: **{RN.ESTADO['ultimo_ok'] or 'todavía ninguno desde que arrancó la app'}**")
            if RN.ESTADO["ultimo_error"]:
                st.warning(f"Último error: {RN.ESTADO['ultimo_error']}")
            if st.button("Respaldar ahora"):
                st.success("Respaldo subido.") if RN.respaldar_ahora(L.RUTA_DATOS) else st.error("No se pudo subir. Revisa el error de arriba.")
    with st.expander("💾 Respaldo y mantenimiento"):
        st.warning("En un servidor gratuito el archivo de datos puede borrarse al reiniciar la app. "
                   "Descarga un respaldo antes de la exposición y después de cada prueba con tus compañeros.")
        st.download_button("⬇️ Descargar respaldo completo (JSON)", L.respaldo_json(), "ecofeed_respaldo.json",
                           "application/json")
        sub = st.file_uploader("Restaurar desde un respaldo (agrega las cuentas que falten)", type="json", key="adm_up")
        if sub is not None and st.button("Restaurar respaldo"):
            try:
                st.success(f"Se agregaron {L.restaurar_json(sub.getvalue().decode('utf-8'))} cuentas.")
            except Exception as e:  # noqa: BLE001
                st.error(f"No se pudo restaurar: {e}")
        if len(df):
            quien = st.selectbox("Eliminar una cuenta de prueba", df["usuario"], key="adm_del")
            if st.checkbox(f"Confirmo que quiero eliminar a «{quien}»", key="adm_conf") and st.button("Eliminar"):
                L.eliminar_usuario(quien)
                st.rerun()
