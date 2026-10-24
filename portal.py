import base64
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pydeck as pdk
import streamlit as st

# =============================================================================
# 1. Configuración General de la Página Web y Autenticación
# =============================================================================
st.set_page_config(page_title="Portal de Inteligencia - SIEC", layout="wide")


def verificar_password():
    def password_entered():
        # Verificamos que la clave exista antes de leerla
        if "password" in st.session_state and st.session_state["password"] == "ClaveInstitucional2026":
            st.session_state["password_correct"] = True
            st.session_state["password"] = "" # Limpiamos el valor en lugar de borrar la llave con 'del'
        else:
            st.session_state["password_correct"] = False
            st.session_state["password"] = ""
  if "password_correct" not in st.session_state:
    st.text_input(
        "Contraseña de Acceso Restringido:",
        type="password",
        on_change=password_entered,
        key="password",
    )
    return False
  elif not st.session_state["password_correct"]:
    st.text_input(
        "Contraseña de Acceso Restringido:",
        type="password",
        on_change=password_entered,
        key="password",
    )
    st.error("😕 Contraseña incorrecta")
    return False
  else:
    return True


# Si no se autentica correctamente, se detiene la ejecución del resto del portal
if not verificar_password():
  st.stop()


def convertir_imagen_base64(nombre_archivo):
  if os.path.exists(nombre_archivo):
    try:
      with open(nombre_archivo, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
        ext = nombre_archivo.split(".")[-1].lower()
        mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
        return f"data:{mime};base64,{encoded}"
    except Exception:
      return None
  return None


def obtener_logo_principal():
  posibles_nombres = ["logo_siec.png", "logo_siec.jpg", "Logo_SIEC.png"]
  for nombre in posibles_nombres:
    if os.path.exists(nombre):
      return convertir_imagen_base64(nombre)
  return None


def obtener_logo_minseg():
  posibles_nombres = [
      "Minseg.png",
      "Minseg.jpg",
      "minseg.png",
      "MINSEG.jpg",
      "MINSEG.png",
      "Minseg_2.jpg",
  ]
  for nombre in posibles_nombres:
    if os.path.exists(nombre):
      return convertir_imagen_base64(nombre)
  return None


logo_principal = obtener_logo_principal()
logo_minseg = obtener_logo_minseg()
logo_pn = convertir_imagen_base64("Policia_Nacional.png")
logo_senafront = convertir_imagen_base64("Servicio_Nacional_de_Fronteras.png")
logo_senan = convertir_imagen_base64("Servicio_Nacional_Aeronaval.png")

# =============================================================================
# 2. Estilos CSS Personalizados
# =============================================================================
st.markdown(
    """
    <style>
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-top: 4px solid #1E3A8A;
        margin-bottom: 15px;
    }
    .kpi-label {
        font-size: 0.85rem;
        font-weight: 500;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
        font-family: 'Segoe UI', sans-serif;
    }
    .inst-title {
        font-size: 0.80rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .inst-value {
        font-size: 1.50rem;
        font-weight: 700;
        color: #0f172a;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-top: 4px solid #1E3A8A !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        background-color: #ffffff !important;
        border-left: 1px solid #e2e8f0 !important;
        border-right: 1px solid #e2e8f0 !important;
        border-bottom: 1px solid #e2e8f0 !important;
        padding: 15px;
        margin-bottom: 20px;
    }
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    .sidebar-header {
        font-size: 0.90rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# 3. Barra Superior Institucional
# =============================================================================
st.markdown(
    """
    <div style="background-color: #0f172a; padding: 6px 15px; border-radius: 6px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; color: #ffffff; font-family: sans-serif; font-size: 0.8rem;">
        <div><b>REPÚBLICA DE PANAMÁ</b> | Ministerio de Seguridad Pública — SIEC</div>
        <div>🔐 <i>Sistema de Uso Oficial y Restringido</i></div>
    </div>
""",
    unsafe_allow_html=True,
)

with st.container(border=True):
  col_img, col_txt = st.columns([0.10, 0.90])
  with col_img:
    if logo_principal:
      st.markdown(
          f"""
                <div style="display: flex; align-items: center; justify-content: center; height: 100%;">
                    <img src="{logo_principal}" style="width: 85px; height: 85px; border-radius: 50%; object-fit: cover; border: 3px solid #1E3A8A; box-shadow: 0 4px 6px rgba(0,0,0,0.15);" alt="Logo SIEC"/>
                </div>
            """,
          unsafe_allow_html=True,
      )
    else:
      st.markdown("🛡️", unsafe_allow_html=True)
  with col_txt:
    st.markdown(
        '<h1 style="margin: 0; padding-top: 2px; font-size: 2.20rem; color:'
        ' #0f172a; font-weight: 800; font-family: sans-serif;'
        ' letter-spacing: -0.01em;">SISTEMA INTEGRADO DE ESTADÍSTICAS'
        " CRIMINALES</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-style: italic; font-size: 1.10rem; color: #475569;"
        " margin-top: 4px; margin-bottom: 0px;'>Ministerio de Seguridad Pública"
        " - Portal de Inteligencia Geoespacial y Control Logístico</p>",
        unsafe_allow_html=True,
    )

# =============================================================================
# 4. Selector Principal de Módulo
# =============================================================================
with st.container(border=True):
  st.markdown(
      '<div class="inst-title" style="margin-bottom: 8px;">🗂️ SELECCIÓN DE'
      " MÓDULO OPERATIVO</div>",
      unsafe_allow_html=True,
  )
  modulo_seleccionado = st.radio(
      "Seleccione el sistema que desea consultar:",
      options=[
          "🔫 Control y Análisis de Armas de Fuego",
          "💣 Control y Análisis de Municiones e Insumos",
          "📦 Control y Análisis de Drogas IMELFC",
          "📦 Control y Análisis de Incidencias de Posibles Drogas SITIGPOL",
      ],
      horizontal=True,
      label_visibility="collapsed",
  )


# =============================================================================
# 5. Carga e Ingesta de Datos Consolidados
# =============================================================================
@st.cache_data
def cargar_datos_armas():
  try:
    df = pd.read_excel("Base_Consolidada_5_Anos.xlsx")
    if "Fecha" in df.columns:
      df["Fecha_dt"] = pd.to_datetime(df["Fecha"], errors="coerce")
    return df
  except Exception:
    return None


@st.cache_data
def cargar_datos_municiones():
  try:
    df = pd.read_excel("Base_Municiones_5_Anos.xlsx")
    if "Fecha" in df.columns:
      df["Fecha_dt"] = pd.to_datetime(df["Fecha"], errors="coerce")
    return df
  except Exception:
    return None


@st.cache_data
def cargar_datos_drogas():
  try:
    df = pd.read_excel("Base_Drogas_5_Anos.xlsx")
    if "AÑO" in df.columns and "Año" not in df.columns:
      df["Año"] = df["AÑO"]
    if "MES" in df.columns and "Mes" not in df.columns:
      df["Mes"] = df["MES"].str.capitalize()
    if "PROCEDENCIA" in df.columns and "Provincia" not in df.columns:
      df["Provincia"] = df["PROCEDENCIA"].str.strip()
    return df
  except Exception:
    return None


@st.cache_data
def cargar_datos_drogas_sitigpol():
  try:
    archivos_posibles = [
        "consolidado_drogas_SITIGPOL.xlsx",
        "Base_Drogas_SITIGPOL.xlsx",
        "consolidado_drogas_SITIGPOL.csv",
    ]
    df = None
    for arc in archivos_posibles:
      if os.path.exists(arc):
        df = pd.read_csv(arc) if arc.endswith(".csv") else pd.read_excel(arc)
        break

    if df is not None and not df.empty:
      col_fecha = next((c for c in df.columns if "fech" in c.lower()), None)
      if col_fecha:
        df["Fecha_dt"] = pd.to_datetime(df[col_fecha], errors="coerce")
        if "Año" not in df.columns or df["Año"].isna().all():
          df["Año"] = df["Fecha_dt"].dt.year

        orden_meses = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ]
        meses_es = {i + 1: m for i, m in enumerate(orden_meses)}
        if "Mes" not in df.columns or df["Mes"].isna().all():
          df["Mes"] = df["Fecha_dt"].dt.month.map(meses_es)

      col_prov = next(
          (c for c in df.columns if "prov" in c.lower() or "juris" in c.lower()),
          "Provincia",
      )
      if col_prov in df.columns and "Provincia" not in df.columns:
        df["Provincia"] = df[col_prov].astype(str).str.strip()

      if "Cantidad_Real" in df.columns:
        df["Cantidad_Real"] = pd.to_numeric(
            df["Cantidad_Real"], errors="coerce"
        ).fillna(0)
      elif "Cantidad" in df.columns:
        df["Cantidad_Real"] = pd.to_numeric(
            df["Cantidad"]
            .astype(str)
            .str.extract(r"([\d\.,]+)")[0]
            .str.replace(",", ""),
            errors="coerce",
        ).fillna(0)
      else:
        df["Cantidad_Real"] = 1
      col_inst = next(
          (
              c
              for c in df.columns
              if "inst" in c.lower()
              or "entidad" in c.lower()
              or "zonal" in c.lower()
          ),
          None,
      )
      if col_inst:

        def est_inst(val):
          if pd.isna(val):
            return "No Especificado"
          val_str = str(val).upper().strip()
          if "AERONAVAL" in val_str:
            return "Servicio Nacional Aeronaval"
          elif "ZONA" in val_str:
            return "Policía Nacional"
          elif "BRIGADAS" in val_str or "BRIGADA" in val_str:
            return "Servicio Nacional de Fronteras"
          else:
            if any(k in val_str for k in ["PN", "POLICIA", "POLICÍA"]):
              return "Policía Nacional"
            elif any(k in val_str for k in ["SENAFRONT", "FRONTERAS"]):
              return "Servicio Nacional de Fronteras"
            elif any(k in val_str for k in ["SENAN", "SNAN"]):
              return "Servicio Nacional Aeronaval"
            return str(val).strip()

        df["Institución"] = df[col_inst].apply(est_inst)
      elif "Institución" not in df.columns:
        df["Institución"] = "Policía Nacional"
      if "Tipo" not in df.columns:
        col_t = next(
            (
                c
                for c in df.columns
                if "tipo" in c.lower() or "droga" in c.lower()
            ),
            None,
        )
        df["Tipo"] = (
            df[col_t].astype(str).str.strip() if col_t else "No Especificado"
        )

      if "Relación" not in df.columns:
        col_r = next(
            (
                c
                for c in df.columns
                if "relac" in c.lower()
                or "estat" in c.lower()
                or "verif" in c.lower()
            ),
            None,
        )
        df["Relación"] = (
            df[col_r].astype(str).str.strip() if col_r else "Incautación"
        )

    return df
  except Exception:
    return None


@st.cache_data
def cargar_datos_pandillas():
  try:
    df = pd.read_excel("GEO PANDILLAS 2026.xlsx", sheet_name="Pandillas")
    if "LAT" in df.columns and "LON" in df.columns:
      df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
      df["LON"] = pd.to_numeric(df["LON"], errors="coerce")
    return df
  except Exception:
    return None


df_pandillas = cargar_datos_pandillas()

# =============================================================================
# A. LÓGICA DEL MÓDULO DE ARMAS DE FUEGO
# =============================================================================
if modulo_seleccionado == "🔫 Control y Análisis de Armas de Fuego":
  df = cargar_datos_armas()
  if df is not None and not df.empty:
    if "Año" in df.columns:
      df["Año"] = pd.to_numeric(df["Año"], errors="coerce")
    tab_dashboard, tab_datos = st.tabs(["📊 DASHBOARD", "📋 DATOS ESCRITOS"])
    with tab_dashboard:
      with st.sidebar:
        img_sidebar_html = (
            f'<img src="{logo_principal}" style="width: 24px; height: 24px;'
            ' border-radius: 50%; object-fit: cover; border: 1.5px solid'
            ' #1E3A8A;" alt="Filtros"/>'
            if logo_principal
            else "🎛️"
        )
        st.markdown(
            f"""
                    <div class="sidebar-header">
                        {img_sidebar_html}
                        <span>PANEL DE CONTROL Y FILTROS</span>
                    </div>
                """,
            unsafe_allow_html=True,
        )

        if st.button(
            "🔄 Restablecer Filtros",
            use_container_width=True,
            type="secondary",
            key="btn_rst_armas",
        ):
          st.session_state["ano_sel"] = []
          st.session_state["prov_sel"] = []
          st.session_state["dist_sel"] = []
          st.session_state["corr_sel"] = []
          st.session_state["mes_sel"] = []
          st.session_state["verif_sel"] = []
          st.rerun()
        st.markdown("---")

        anos_disponibles = (
            sorted([int(x) for x in df["Año"].dropna().unique() if pd.notna(x)])
            if "Año" in df.columns
            else []
        )
        provincias_disponibles = (
            sorted(df["Provincia"].dropna().unique().tolist())
            if "Provincia" in df.columns
            else []
        )

        orden_meses = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ]
        meses_presentes = (
            [m for m in orden_meses if m in df["Mes"].dropna().unique()]
            if "Mes" in df.columns
            else []
        )
        col_verif_name = (
            "Verificación"
            if "Verificación" in df.columns
            else ("Relación" if "Relación" in df.columns else None)
        )
        verif_disponibles = (
            sorted(df[col_verif_name].dropna().astype(str).unique().tolist())
            if col_verif_name
            else []
        )

        with st.expander("📅 **Temporalidad y Ubicación**", expanded=True):
          ano_seleccionado = st.multiselect(
              "Año Fiscal / Operativo",
              options=anos_disponibles,
              default=[],
              key="ano_sel",
          )
          provincia_seleccionada = st.multiselect(
              "Provincia / Jurisdicción",
              options=provincias_disponibles,
              default=[],
              key="prov_sel",
          )

          df_temp_dist = df.copy()
          if provincia_seleccionada and "Provincia" in df_temp_dist.columns:
            df_temp_dist = df_temp_dist[
                df_temp_dist["Provincia"].isin(provincia_seleccionada)
            ]
          distritos_disponibles = (
              sorted(df_temp_dist["Distrito"].dropna().unique().tolist())
              if "Distrito" in df_temp_dist.columns
              else []
          )
          distrito_seleccionado = st.multiselect(
              "Distrito",
              options=distritos_disponibles,
              default=[],
              key="dist_sel",
          )

          df_temp_corr = df_temp_dist.copy()
          if distrito_seleccionado and "Distrito" in df_temp_corr.columns:
            df_temp_corr = df_temp_corr[
                df_temp_corr["Distrito"].isin(distrito_seleccionado)
            ]
          corregimientos_disponibles = (
              sorted(df_temp_corr["Corregimiento"].dropna().unique().tolist())
              if "Corregimiento" in df_temp_corr.columns
              else []
          )
          corregimiento_seleccionado = st.multiselect(
              "Corregimiento",
              options=corregimientos_disponibles,
              default=[],
              key="corr_sel",
          )

          mes_seleccionado = st.multiselect(
              "Mes", options=meses_presentes, default=[], key="mes_sel"
          )
        with st.expander("🔍 **Clasificación Operativa**", expanded=True):
          verif_seleccionada = (
              st.multiselect(
                  f"Estatus ({col_verif_name})",
                  options=verif_disponibles,
                  default=[],
                  key="verif_sel",
              )
              if col_verif_name
              else []
          )
        with st.expander("🗺️ **Capas del Mapa Geoespacial**", expanded=True):
          ver_calor = st.checkbox(
              "🔥 Mapa de Calor (Densidad Armas)", value=True
          )
          ver_puntos = st.checkbox("📍 Puntos de Incautación", value=True)
          st.markdown("---")
          st.markdown("👥 **Capas de Pandillas**")
          ver_calor_pandillas = st.checkbox(
              "🌿 Mapa de Calor (Densidad Pandillas)", value=False
          )
          ver_puntos_pandillas = st.checkbox(
              "🔵 Puntos Azules (Pandillas)", value=True
          )

        df_filtrado = df.copy()
        if ano_seleccionado and "Año" in df_filtrado.columns:
          df_filtrado = df_filtrado[df_filtrado["Año"].isin(ano_seleccionado)]
        if provincia_seleccionada and "Provincia" in df_filtrado.columns:
          df_filtrado = df_filtrado[
              df_filtrado["Provincia"].isin(provincia_seleccionada)
          ]
        if distrito_seleccionado and "Distrito" in df_filtrado.columns:
          df_filtrado = df_filtrado[
              df_filtrado["Distrito"].isin(distrito_seleccionado)
          ]
        if corregimiento_seleccionado and "Corregimiento" in df_filtrado.columns:
          df_filtrado = df_filtrado[
              df_filtrado["Corregimiento"].isin(corregimiento_seleccionado)
          ]
        if mes_seleccionado and "Mes" in df_filtrado.columns:
          df_filtrado = df_filtrado[df_filtrado["Mes"].isin(mes_seleccionado)]
        if verif_seleccionada and col_verif_name:
          df_filtrado = df_filtrado[
              df_filtrado[col_verif_name].astype(str).isin(verif_seleccionada)
          ]

        filtros_activos = sum([
            1
            for f in [
                ano_seleccionado,
                provincia_seleccionada,
                distrito_seleccionado,
                corregimiento_seleccionado,
                mes_seleccionado,
                verif_seleccionada,
            ]
            if len(f) > 0
        ])
        st.caption(f"📌 **Filtros aplicados:** `{filtros_activos}` activo(s)")

      df_pandillas_filtrado = (
          df_pandillas.copy() if df_pandillas is not None else None
      )
      if df_pandillas_filtrado is not None and not df_pandillas_filtrado.empty:
        if provincia_seleccionada and "PRO" in df_pandillas_filtrado.columns:
          prov_lower = [p.lower() for p in provincia_seleccionada]
          df_pandillas_filtrado = df_pandillas_filtrado[
              df_pandillas_filtrado["PRO"].astype(str).str.lower().isin(prov_lower)
          ]
        if distrito_seleccionado and "DIS" in df_pandillas_filtrado.columns:
          dist_lower = [d.lower() for d in distrito_seleccionado]
          df_pandillas_filtrado = df_pandillas_filtrado[
              df_pandillas_filtrado["DIS"].astype(str).str.lower().isin(dist_lower)
          ]
        if corregimiento_seleccionado and "COR" in df_pandillas_filtrado.columns:
          corr_lower = [c.lower() for c in corregimiento_seleccionado]
          df_pandillas_filtrado = df_pandillas_filtrado[
              df_pandillas_filtrado["COR"].astype(str).str.lower().isin(corr_lower)
          ]

      col1, col2, col3 = st.columns(3)
      total_reg = len(df_filtrado)
      total_armas = (
          int(df_filtrado["Cantidad"].sum())
          if "Cantidad" in df_filtrado.columns
          else total_reg
      )
      provincias_activas = (
          df_filtrado["Provincia"].nunique()
          if "Provincia" in df_filtrado.columns
          else 0
      )

      with col1:
        st.markdown(
            '<div class="kpi-card"><div class="kpi-label">TOTAL DE'
            f' REGISTROS</div><div class="kpi-value">{total_reg:,}</div></div>',
            unsafe_allow_html=True,
        )
      with col2:
        st.markdown(
            '<div class="kpi-card"><div class="kpi-label">TOTAL DE'
            f' ARMAS</div><div class="kpi-value">{total_armas:,}</div></div>',
            unsafe_allow_html=True,
        )
      with col3:
        st.markdown(
            '<div class="kpi-card"><div class="kpi-label">PROVINCIAS Y'
            ' COMARCAS</div><div'
            f' class="kpi-value">{provincias_activas}</div></div>',
            unsafe_allow_html=True,
        )

      if "Instituciones" in df_filtrado.columns:
        df_pn_inst = df_filtrado[
            df_filtrado["Instituciones"] == "Policía Nacional"
        ]
        df_sf_inst = df_filtrado[
            df_filtrado["Instituciones"] == "Servicio Nacional de Fronteras"
        ]
        df_sn_inst = df_filtrado[
            df_filtrado["Instituciones"] == "Servicio Nacional Aeronaval"
        ]

        pn_count = (
            int(df_pn_inst["Cantidad"].sum())
            if "Cantidad" in df_pn_inst.columns
            else len(df_pn_inst)
        )
        senafront_count = (
            int(df_sf_inst["Cantidad"].sum())
            if "Cantidad" in df_sf_inst.columns
            else len(df_sf_inst)
        )
        senan_count = (
            int(df_sn_inst["Cantidad"].sum())
            if "Cantidad" in df_sn_inst.columns
            else len(df_sn_inst)
        )
      else:
        pn_count, senafront_count, senan_count = 0, 0, 0

      col_inst1, col_inst2, col_inst3 = st.columns(3)
      with col_inst1:
        with st.container(border=True):
          img_pn = (
              f'<img src="{logo_pn}" style="width: 48px; height: 48px;'
              ' object-fit: contain;" alt="PN"/>'
              if logo_pn
              else "🛡️"
          )
          st.markdown(
              '<div style="display: flex; align-items: center; gap:'
              f' 15px;"><div>{img_pn}</div><div><div class="inst-title">Policía'
              f' Nacional</div><div class="inst-value">{pn_count:,} <span'
              ' style="font-size: 0.85rem; font-weight:400;'
              ' color:#64748b;">TOTAL DE ARMAS</span></div></div></div>',
              unsafe_allow_html=True,
          )
      with col_inst2:
        with st.container(border=True):
          img_sf = (
              f'<img src="{logo_senafront}" style="width: 48px; height: 48px;'
              ' object-fit: contain;" alt="SENAFRONT"/>'
              if logo_senafront
              else "🛡️"
          )
          st.markdown(
              '<div style="display: flex; align-items: center; gap:'
              f' 15px;"><div>{img_sf}</div><div><div class="inst-title">Servicio'
              ' Nac. de Fronteras</div><div'
              f' class="inst-value">{senafront_count:,} <span'
              ' style="font-size: 0.85rem; font-weight:400;'
              ' color:#64748b;">TOTAL DE ARMAS</span></div></div></div>',
              unsafe_allow_html=True,
          )
      with col_inst3:
        with st.container(border=True):
          img_sn = (
              f'<img src="{logo_senan}" style="width: 48px; height: 48px;'
              ' object-fit: contain;" alt="SENAN"/>'
              if logo_senan
              else "🛡️"
          )
          st.markdown(
              '<div style="display: flex; align-items: center; gap:'
              f' 15px;"><div>{img_sn}</div><div><div class="inst-title">Servicio'
              f' Nac. Aeronaval</div><div class="inst-value">{senan_count:,}'
              ' <span style="font-size: 0.85rem; font-weight:400;'
              ' color:#64748b;">TOTAL DE ARMAS</span></div></div></div>',
              unsafe_allow_html=True,
          )

      with st.container(border=True):
        col_t_img, col_t_txt = st.columns([0.08, 0.92])
        with col_t_img:
          if logo_minseg:
            st.markdown(
                f'<div style="display: flex; align-items: center;'
                ' justify-content: center; height: 100%;"><img'
                f' src="{logo_minseg}" style="width: 65px; height: 65px;'
                ' border-radius: 50%; object-fit: cover; border: 3px solid'
                ' #1E3A8A; box-shadow: 0px 2px 4px rgba(0,0,0,0.15);"'
                ' alt="MINSEG"/></div>',
                unsafe_allow_html=True,
            )
          else:
            st.markdown("🛡️", unsafe_allow_html=True)
        with col_t_txt:
          st.subheader(
              "DESGLOSE TÁCTICO DE ARMAS Y RELACIÓN OPERATIVA POR INSTITUCIÓN"
          )

        tab_pn, tab_sf, tab_sn = st.tabs([
            "POLICÍA NACIONAL",
            "SERVICIO NACIONAL DE FRONTERAS",
            "SERVICIO NACIONAL AERONAVAL",
        ])
        val_col = "Cantidad" if "Cantidad" in df_filtrado.columns else None
        agg_func_val = "sum" if val_col else "count"

        with tab_pn:
          with st.container(border=True):
            st.markdown("### 👮‍♂️ POLICÍA NACIONAL")
            if (
                "Instituciones" in df_filtrado.columns
                and "SubTipo" in df_filtrado.columns
                and "Relación" in df_filtrado.columns
            ):
              df_pn_sub = df_filtrado[
                  df_filtrado["Instituciones"] == "Policía Nacional"
              ]
              if not df_pn_sub.empty:
                tabla_pn = (
                    pd.crosstab(
                        df_pn_sub["SubTipo"],
                        df_pn_sub["Relación"],
                        values=df_pn_sub[val_col] if val_col else None,
                        aggfunc=agg_func_val,
                        margins=True,
                        margins_name="Total General",
                    )
                    .fillna(0)
                    .astype(int)
                )
                st.dataframe(tabla_pn, use_container_width=True)

        with tab_sf:
          with st.container(border=True):
            st.markdown("### 💂‍♂️ SERVICIO NACIONAL DE FRONTERAS")
            if (
                "Instituciones" in df_filtrado.columns
                and "SubTipo" in df_filtrado.columns
                and "Relación" in df_filtrado.columns
            ):
              df_sf_sub = df_filtrado[
                  df_filtrado["Instituciones"]
                  == "Servicio Nacional de Fronteras"
              ]
              if not df_sf_sub.empty:
                tabla_sf = (
                    pd.crosstab(
                        df_sf_sub["SubTipo"],
                        df_sf_sub["Relación"],
                        values=df_sf_sub[val_col] if val_col else None,
                        aggfunc=agg_func_val,
                        margins=True,
                        margins_name="Total General",
                    )
                    .fillna(0)
                    .astype(int)
                )
                st.dataframe(tabla_sf, use_container_width=True)

        with tab_sn:
          with st.container(border=True):
            st.markdown("### ⚓ SERVICIO NACIONAL AERONAVAL")
            if (
                "Instituciones" in df_filtrado.columns
                and "SubTipo" in df_filtrado.columns
                and "Relación" in df_filtrado.columns
            ):
              df_sn_sub = df_filtrado[
                  df_filtrado["Instituciones"] == "Servicio Nacional Aeronaval"
              ]
              if not df_sn_sub.empty:
                tabla_sn = (
                    pd.crosstab(
                        df_sn_sub["SubTipo"],
                        df_sn_sub["Relación"],
                        values=df_sn_sub[val_col] if val_col else None,
                        aggfunc=agg_func_val,
                        margins=True,
                        margins_name="Total General",
                    )
                    .fillna(0)
                    .astype(int)
                )
                st.dataframe(tabla_sn, use_container_width=True)

      with st.container(border=True):
        st.subheader("📈 EVOLUCIÓN HISTÓRICA Y VARIACIÓN INTERANUAL")
        df_hist_base = df.copy()
        if provincia_seleccionada and "Provincia" in df_hist_base.columns:
          df_hist_base = df_hist_base[
              df_hist_base["Provincia"].isin(provincia_seleccionada)
          ]
        if distrito_seleccionado and "Distrito" in df_hist_base.columns:
          df_hist_base = df_hist_base[
              df_hist_base["Distrito"].isin(distrito_seleccionado)
          ]
        if corregimiento_seleccionado and "Corregimiento" in df_hist_base.columns:
          df_hist_base = df_hist_base[
              df_hist_base["Corregimiento"].isin(corregimiento_seleccionado)
          ]
        if mes_seleccionado and "Mes" in df_hist_base.columns:
          df_hist_base = df_hist_base[
              df_hist_base["Mes"].isin(mes_seleccionado)
          ]
        if verif_seleccionada and col_verif_name:
          df_hist_base = df_hist_base[
              df_hist_base[col_verif_name].astype(str).isin(verif_seleccionada)
          ]

        if "Año" in df_hist_base.columns and not df_hist_base.empty:
          df_historico = (
              df_hist_base.groupby("Año")["Cantidad"].sum().reset_index()
              if "Cantidad" in df_hist_base.columns
              else (
                  df_hist_base.groupby("Año")
                  .size()
                  .reset_index(name="Cantidad")
              )
          )
          df_historico["Cantidad"] = df_historico["Cantidad"].astype(int)
          df_historico = df_historico.sort_values("Año")
          df_historico["Variacion_Pct"] = (
              df_historico["Cantidad"].pct_change() * 100
          )

          fig_hist = make_subplots(specs=[[{"secondary_y": True}]])
          fig_hist.add_trace(
              go.Bar(
                  x=df_historico["Año"],
                  y=df_historico["Cantidad"],
                  name="Total de Armas",
                  marker_color="#1E3A8A",
                  text=df_historico["Cantidad"],
                  textposition="inside",
                  textfont=dict(color="white", size=12),
              ),
              secondary_y=False,
          )
          fig_hist.add_trace(
              go.Scatter(
                  x=df_historico["Año"],
                  y=df_historico["Variacion_Pct"],
                  name="Variación Interanual (%)",
                  mode="lines+markers",
                  line=dict(color="#dc2626", width=3),
                  marker=dict(
                      size=8,
                      color="#ffffff",
                      line=dict(width=2, color="#dc2626"),
                  ),
              ),
              secondary_y=True,
          )

          for _, row in df_historico.iterrows():
            if pd.notna(row["Variacion_Pct"]):
              val = row["Variacion_Pct"]
              text_color = "#16a34a" if val >= 0 else "#dc2626"
              fig_hist.add_annotation(
                  x=row["Año"],
                  y=val,
                  yref="y2",
                  text=f"<b>{val:+.1f}%</b>",
                  showarrow=False,
                  ax=0,
                  ay=-30,
                  font=dict(size=11, color=text_color),
                  bgcolor="#ffffff",
                  opacity=0.98,
              )

          fig_hist.update_layout(
              height=420,
              margin={"r": 10, "t": 20, "l": 10, "b": 10},
              legend=dict(
                  orientation="h",
                  yanchor="bottom",
                  y=1.05,
                  xanchor="right",
                  x=1,
              ),
              plot_bgcolor="rgba(0,0,0,0)",
              paper_bgcolor="rgba(0,0,0,0)",
          )
          fig_hist.update_yaxes(
              title_text="<b>Total de Armas</b>",
              secondary_y=False,
              showgrid=True,
              gridcolor="#f1f5f9",
          )
          fig_hist.update_yaxes(
              title_text="<b>Variación (%)</b>",
              secondary_y=True,
              tickformat="+.1f%",
              showgrid=False,
          )
          st.plotly_chart(fig_hist, use_container_width=True)

      if len(anos_disponibles) >= 2:
        with st.container(border=True):
          st.subheader("📊 CUADRO COMPARATIVO ANUAL")
          col_comp1, col_comp2 = st.columns(2)
          with col_comp1:
            ano_base = st.selectbox(
                "Seleccionar Año Base (A)",
                options=anos_disponibles,
                index=0,
                key="ano_base",
            )
          with col_comp2:
            ano_comparacion = st.selectbox(
                "Seleccionar Año a Comparar (B)",
                options=anos_disponibles,
                index=min(1, len(anos_disponibles) - 1),
                key="ano_comp",
            )

          df_base = df[df["Año"] == int(ano_base)]
          df_comp = df[df["Año"] == int(ano_comparacion)]

          if distrito_seleccionado and "Distrito" in df.columns:
            df_base = df_base[df_base["Distrito"].isin(distrito_seleccionado)]
            df_comp = df_comp[df_comp["Distrito"].isin(distrito_seleccionado)]
          if corregimiento_seleccionado and "Corregimiento" in df.columns:
            df_base = df_base[
                df_base["Corregimiento"].isin(corregimiento_seleccionado)
            ]
            df_comp = df_comp[
                df_comp["Corregimiento"].isin(corregimiento_seleccionado)
            ]
          if mes_seleccionado and "Mes" in df.columns:
            df_base = df_base[df_base["Mes"].isin(mes_seleccionado)]
            df_comp = df_comp[df_comp["Mes"].isin(mes_seleccionado)]
          if verif_seleccionada and col_verif_name:
            df_base = df_base[
                df_base[col_verif_name].astype(str).isin(verif_seleccionada)
            ]
            df_comp = df_comp[
                df_comp[col_verif_name].astype(str).isin(verif_seleccionada)
            ]

          val_col_comp = "Cantidad" if "Cantidad" in df.columns else None
          total_base = (
              int(df_base[val_col_comp].sum())
              if val_col_comp
              else len(df_base)
          )
          total_comp = (
              int(df_comp[val_col_comp].sum())
              if val_col_comp
              else len(df_comp)
          )
          dif_registros = total_comp - total_base
          pct_cambio = (
              (dif_registros / total_base * 100) if total_base > 0 else 0
          )

          c_met1, c_met2, c_met3 = st.columns(3)
          c_met1.metric(
              f"Registro de Total de Armas {ano_base} vs {ano_comparacion}",
              f"{total_comp:,}",
              f"{pct_cambio:+.1f}% vs {ano_base} ({total_base:,})",
          )
          c_met2.metric(
              "Diferencia Neta", f"{dif_registros:+d}", "Variación global"
          )
          c_met3.metric(
              f"Total Base ({ano_base})", f"{total_base:,}", "Referencia inicial"
          )

          st.markdown("---")
          st.markdown(
              "##### 📈 Comportamiento Mensual Comparativo"
              f" ({ano_base} vs {ano_comparacion})"
          )
          if "Mes" in df.columns:
            df_base_mes = (
                df_base.groupby("Mes")[val_col_comp]
                .sum()
                .reset_index(name="Cantidad")
                if val_col_comp
                else df_base.groupby("Mes").size().reset_index(name="Cantidad")
            )
            df_comp_mes = (
                df_comp.groupby("Mes")[val_col_comp]
                .sum()
                .reset_index(name="Cantidad")
                if val_col_comp
                else df_comp.groupby("Mes").size().reset_index(name="Cantidad")
            )

            df_base_mes["Mes"] = pd.Categorical(
                df_base_mes["Mes"], categories=orden_meses, ordered=True
            )
            df_base_mes = df_base_mes.sort_values("Mes").dropna(subset=["Mes"])
            df_comp_mes["Mes"] = pd.Categorical(
                df_comp_mes["Mes"], categories=orden_meses, ordered=True
            )
            df_comp_mes = df_comp_mes.sort_values("Mes").dropna(subset=["Mes"])

            fig_comp_line = go.Figure()
            fig_comp_line.add_trace(
                go.Scatter(
                    x=df_base_mes["Mes"],
                    y=df_base_mes["Cantidad"],
                    name=str(ano_base),
                    mode="lines+markers",
                    line=dict(color="#1E3A8A", width=3),
                    marker=dict(size=8),
                )
            )
            fig_comp_line.add_trace(
                go.Scatter(
                    x=df_comp_mes["Mes"],
                    y=df_comp_mes["Cantidad"],
                    name=str(ano_comparacion),
                    mode="lines+markers",
                    line=dict(color="#dc2626", width=3),
                    marker=dict(size=8),
                )
            )
            fig_comp_line.update_layout(
                height=380,
                margin={"r": 10, "t": 20, "l": 10, "b": 10},
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                ),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#f1f5f9",
                    title_text="<b>Total de Armas</b>",
                ),
            )
            st.plotly_chart(fig_comp_line, use_container_width=True)

          st.markdown("---")
          st.markdown(
              "##### 🗺️ Desglose y Variación por Provincia"
              f" ({ano_base} vs {ano_comparacion})"
          )
          if "Provincia" in df.columns:
            prov_base = (
                df_base.groupby("Provincia")[val_col_comp]
                .sum()
                .reset_index(name=f"Base_{ano_base}")
                if val_col_comp
                else (
                    df_base.groupby("Provincia")
                    .size()
                    .reset_index(name=f"Base_{ano_base}")
                )
            )
            prov_comp = (
                df_comp.groupby("Provincia")[val_col_comp]
                .sum()
                .reset_index(name=f"Comp_{ano_comparacion}")
                if val_col_comp
                else (
                    df_comp.groupby("Provincia")
                    .size()
                    .reset_index(name=f"Comp_{ano_comparacion}")
                )
            )
            df_prov_comp = pd.merge(
                prov_base, prov_comp, on="Provincia", how="outer"
            ).fillna(0)
            df_prov_comp["Diferencia"] = (
                df_prov_comp[f"Comp_{ano_comparacion}"]
                - df_prov_comp[f"Base_{ano_base}"]
            )
            df_prov_comp["Variacion_%"] = df_prov_comp.apply(
                lambda row: (
                    (row["Diferencia"] / row[f"Base_{ano_base}"] * 100)
                    if row[f"Base_{ano_base}"] > 0
                    else 0.0
                ),
                axis=1,
            )
            df_prov_comp = df_prov_comp.sort_values(
                by=f"Comp_{ano_comparacion}", ascending=False
            ).reset_index(drop=True)
            df_prov_display = df_prov_comp.copy()
            df_prov_display["Variacion_%"] = df_prov_display[
                "Variacion_%"
            ].apply(lambda x: f"{x:+.1f}%")
            st.dataframe(df_prov_display, use_container_width=True)

      with st.container(border=True):
        st.subheader("📅 MATRIZ DE CALOR TEMPORAL (DÍAS Y MESES)")
        if "Fecha_dt" in df_filtrado.columns and not df_filtrado.empty:
          df_cal = df_filtrado.dropna(subset=["Fecha_dt"]).copy()
          if not df_cal.empty:
            dias_semana_esp = {
                0: "Lunes",
                1: "Martes",
                2: "Miércoles",
                3: "Jueves",
                4: "Viernes",
                5: "Sábado",
                6: "Domingo",
            }
            orden_dias = [
                "Domingo",
                "Lunes",
                "Martes",
                "Miércoles",
                "Jueves",
                "Viernes",
                "Sábado",
            ]
            df_cal["Dia_Semana"] = df_cal["Fecha_dt"].dt.dayofweek.map(
                dias_semana_esp
            )
            val_col_matriz = "Cantidad" if "Cantidad" in df_cal.columns else None
            df_matriz = (
                df_cal.groupby(["Mes", "Dia_Semana"])[val_col_matriz]
                .sum()
                .reset_index(name="Total_Armas")
                if val_col_matriz
                else (
                    df_cal.groupby(["Mes", "Dia_Semana"])
                    .size()
                    .reset_index(name="Total_Armas")
                )
            )
            df_matriz["Mes"] = pd.Categorical(
                df_matriz["Mes"], categories=orden_meses, ordered=True
            )
            df_matriz["Dia_Semana"] = pd.Categorical(
                df_matriz["Dia_Semana"], categories=orden_dias, ordered=True
            )
            df_matriz = df_matriz.sort_values(["Mes", "Dia_Semana"]).dropna(
                subset=["Mes", "Dia_Semana"]
            )

            fig_cal = px.density_heatmap(
                df_matriz,
                x="Mes",
                y="Dia_Semana",
                z="Total_Armas",
                color_continuous_scale="Blues",
                labels={
                    "Mes": "Meses",
                    "Dia_Semana": "Día de la Semana",
                    "Total_Armas": "Total de Armas",
                },
            )
            fig_cal.update_layout(
                height=380,
                margin={"r": 10, "t": 20, "l": 10, "b": 10},
                xaxis_title="",
                yaxis_title="",
                yaxis=dict(
                    categoryorder="array", categoryarray=orden_dias
                ),
            )
            st.plotly_chart(fig_cal, use_container_width=True)

      with st.container(border=True):
        st.subheader(
            "📍 MAPA INTERACTIVO DE INCAUTACIONES Y PANDILLAS A NIVEL NACIONAL"
        )
        view_state = pdk.ViewState(
            latitude=8.5379, longitude=-80.7821, zoom=7.5, pitch=0
        )
        layers = []
        if (
            ver_calor
            and not df_filtrado.empty
            and "Latitud" in df_filtrado.columns
        ):
          layers.append(
              pdk.Layer(
                  "HeatmapLayer",
                  data=df_filtrado,
                  get_position="[Longitud, Latitud]",
                  radius_pixels=40,
                  intensity=1,
                  threshold=0.03,
              )
          )
        if (
            ver_puntos
            and not df_filtrado.empty
            and "Latitud" in df_filtrado.columns
        ):
          layers.append(
              pdk.Layer(
                  "ScatterplotLayer",
                  data=df_filtrado,
                  get_position="[Longitud, Latitud]",
                  get_color="[220, 20, 60, 220]",
                  get_radius=400,
                  pickable=True,
                  auto_highlight=True,
              )
          )
        if (
            df_pandillas_filtrado is not None
            and not df_pandillas_filtrado.empty
            and "LAT" in df_pandillas_filtrado.columns
            and "LON" in df_pandillas_filtrado.columns
        ):
          if ver_calor_pandillas:
            layers.append(
                pdk.Layer(
                    "HeatmapLayer",
                    data=df_pandillas_filtrado,
                    get_position="[LON, LAT]",
                    radius_pixels=50,
                    intensity=1.5,
                    threshold=0.02,
                    color_range=[
                        [0, 100, 80, 25],
                        [0, 150, 100, 85],
                        [50, 200, 50, 150],
                        [100, 220, 0, 200],
                        [150, 100, 200, 230],
                        [128, 0, 128, 255],
                    ],
                )
            )
          if ver_puntos_pandillas:
            layers.append(
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df_pandillas_filtrado,
                    get_position="[LON, LAT]",
                    get_color="[34, 139, 34, 230]",
                    get_radius=500,
                    pickable=True,
                    auto_highlight=True,
                )
            )
        tooltip_html = (
            "<b>Provincia:</b> {Provincia} {PRO}<br/><b>Distrito:</b> {Distrito}"
            " {DIS}<br/><b>Corregimiento:</b> {Corregimiento}"
            " {COR}<br/><b>Arma / Pandilla:</b> {SubTipo} {PAN}<br/><b>Estatus /"
            " Lugar:</b> {Relación} {LUG}"
        )
        if layers:
          r = pdk.Deck(
              layers=layers,
              initial_view_state=view_state,
              map_style=pdk.map_styles.LIGHT,
              tooltip={
                  "html": tooltip_html,
                  "style": {
                      "backgroundColor": "#1E3A8A",
                      "color": "white",
                  },
              },
          )
          st.pydeck_chart(r)
        else:
          st.info(
              "Active al menos una capa en el panel lateral para visualizar el"
              " mapa."
          )

    with tab_datos:
      st.subheader("📋 REGISTROS COMPLETOS FILTRADOS")
      st.dataframe(df_filtrado, use_container_width=True)
  else:
    st.error("⚠️ No se pudo cargar el archivo de armas.")

# =============================================================================
# B. LÓGICA DEL MÓDULO DE MUNICIONES E INSUMOS
# =============================================================================
elif modulo_seleccionado == "💣 Control y Análisis de Municiones e Insumos":
  df_mun = cargar_datos_municiones()
  if df_mun is not None and not df_mun.empty:
    if "Años" in df_mun.columns:
      df_mun["Años"] = pd.to_numeric(df_mun["Años"], errors="coerce")
    elif "Año" in df_mun.columns:
      df_mun["Años"] = pd.to_numeric(df_mun["Año"], errors="coerce")
    tab_dashboard_m, tab_datos_m = st.tabs(["📊 DASHBOARD", "📋 DATOS ESCRITOS"])
    with tab_dashboard_m:
      with st.sidebar:
        img_sidebar_html = (
            f'<img src="{logo_principal}" style="width: 24px; height: 24px;'
            ' border-radius: 50%; object-fit: cover; border: 1.5px solid'
            ' #1E3A8A;" alt="Filtros"/>'
            if logo_principal
            else "🎛️"
        )
        st.markdown(
            f"""
                    <div class="sidebar-header">
                        {img_sidebar_html}
                        <span>PANEL DE CONTROL - MUNICIONES</span>
                    </div>
                """,
            unsafe_allow_html=True,
        )

        if st.button(
            "🔄 Restablecer Filtros",
            use_container_width=True,
            type="secondary",
            key="btn_rst_mun",
        ):
          st.session_state["ano_m_sel"] = []
          st.session_state["prov_m_sel"] = []
          st.session_state["dist_m_sel"] = []
          st.session_state["corr_m_sel"] = []
          st.session_state["mes_m_sel"] = []
          st.session_state["verif_m_sel"] = []
          st.rerun()
        st.markdown("---")

        anos_m_disp = (
            sorted([
                int(x) for x in df_mun["Años"].dropna().unique() if pd.notna(x)
            ])
            if "Años" in df_mun.columns
            else []
        )
        provincias_m_disp = (
            sorted(df_mun["Provincia"].dropna().unique().tolist())
            if "Provincia" in df_mun.columns
            else []
        )
        orden_meses = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ]
        meses_m_pres = (
            [m for m in orden_meses if m in df_mun["Mes"].dropna().unique()]
            if "Mes" in df_mun.columns
            else []
        )
        col_verif_m = (
            "Verificación"
            if "Verificación" in df_mun.columns
            else ("Relación" if "Relación" in df_mun.columns else None)
        )
        verif_m_disp = (
            sorted(df_mun[col_verif_m].dropna().astype(str).unique().tolist())
            if col_verif_m
            else []
        )

        with st.expander("📅 **Temporalidad y Ubicación**", expanded=True):
          ano_m_sel = st.multiselect(
              "Año Fiscal / Operativo",
              options=anos_m_disp,
              default=[],
              key="ano_m_sel",
          )
          provincia_m_sel = st.multiselect(
              "Provincia / Jurisdicción",
              options=provincias_m_disp,
              default=[],
              key="prov_m_sel",
          )

          df_temp_dist_m = df_mun.copy()
          if provincia_m_sel and "Provincia" in df_temp_dist_m.columns:
            df_temp_dist_m = df_temp_dist_m[
                df_temp_dist_m["Provincia"].isin(provincia_m_sel)
            ]
          distritos_m_disp = (
              sorted(df_temp_dist_m["Distrito"].dropna().unique().tolist())
              if "Distrito" in df_temp_dist_m.columns
              else []
          )
          distrito_m_sel = st.multiselect(
              "Distrito",
              options=distritos_m_disp,
              default=[],
              key="dist_m_sel",
          )

          df_temp_corr_m = df_temp_dist_m.copy()
          if distrito_m_sel and "Distrito" in df_temp_corr_m.columns:
            df_temp_corr_m = df_temp_corr_m[
                df_temp_corr_m["Distrito"].isin(distrito_m_sel)
            ]
          corregimientos_m_disp = (
              sorted(df_temp_corr_m["Corregimiento"].dropna().unique().tolist())
              if "Corregimiento" in df_temp_corr_m.columns
              else []
          )
          corregimiento_m_sel = st.multiselect(
              "Corregimiento",
              options=corregimientos_m_disp,
              default=[],
              key="corr_m_sel",
          )

          mes_m_sel = st.multiselect(
              "Mes", options=meses_m_pres, default=[], key="mes_m_sel"
          )
        with st.expander("🔍 **Clasificación Operativa**", expanded=True):
          verif_m_sel = (
              st.multiselect(
                  f"Estatus ({col_verif_m})",
                  options=verif_m_disp,
                  default=[],
                  key="verif_m_sel",
              )
              if col_verif_m
              else []
          )

        df_m_filtrado = df_mun.copy()
        if ano_m_sel and "Años" in df_m_filtrado.columns:
          df_m_filtrado = df_m_filtrado[df_m_filtrado["Años"].isin(ano_m_sel)]
        if provincia_m_sel and "Provincia" in df_m_filtrado.columns:
          df_m_filtrado = df_m_filtrado[
              df_m_filtrado["Provincia"].isin(provincia_m_sel)
          ]
        if distrito_m_sel and "Distrito" in df_m_filtrado.columns:
          df_m_filtrado = df_m_filtrado[
              df_m_filtrado["Distrito"].isin(distrito_m_sel)
          ]
        if corregimiento_m_sel and "Corregimiento" in df_m_filtrado.columns:
          df_m_filtrado = df_m_filtrado[
              df_m_filtrado["Corregimiento"].isin(corregimiento_m_sel)
          ]
        if mes_m_sel and "Mes" in df_m_filtrado.columns:
          df_m_filtrado = df_m_filtrado[df_m_filtrado["Mes"].isin(mes_m_sel)]
        if verif_m_sel and col_verif_m:
          df_m_filtrado = df_m_filtrado[
              df_m_filtrado[col_verif_m].astype(str).isin(verif_m_sel)
          ]

      col_m1, col_m2, col_m3 = st.columns(3)
      total_m_reg = len(df_m_filtrado)
      total_m_cant = (
          int(df_m_filtrado["Cantidad"].sum())
          if "Cantidad" in df_m_filtrado.columns
          else total_m_reg
      )
      provincias_m_activas = (
          df_m_filtrado["Provincia"].nunique()
          if "Provincia" in df_m_filtrado.columns
          else 0
      )

      with col_m1:
        st.markdown(
            '<div class="kpi-card"><div class="kpi-label">TOTAL DE'
            f' REGISTROS</div><div class="kpi-value">{total_m_reg:,}</div></div>',
            unsafe_allow_html=True,
        )
      with col_m2:
        st.markdown(
            '<div class="kpi-card"><div class="kpi-label">TOTAL DE'
            ' MUNICIONES</div><div'
            f' class="kpi-value">{total_m_cant:,}</div></div>',
            unsafe_allow_html=True,
        )
      with col_m3:
        st.markdown(
            '<div class="kpi-card"><div class="kpi-label">PROVINCIAS Y'
            ' COMARCAS</div><div'
            f' class="kpi-value">{provincias_m_activas}</div></div>',
            unsafe_allow_html=True,
        )

      if "Institucion" in df_m_filtrado.columns:
        df_pn_m = df_m_filtrado[
            df_m_filtrado["Institucion"] == "Policía Nacional"
        ]
        df_sf_m = df_m_filtrado[
            df_m_filtrado["Institucion"] == "Servicio Nacional de Fronteras"
        ]
        df_sn_m = df_m_filtrado[
            df_m_filtrado["Institucion"] == "Servicio Nacional Aeronaval"
        ]
        pn_m_count = (
            int(df_pn_m["Cantidad"].sum())
            if "Cantidad" in df_pn_m.columns
            else len(df_pn_m)
        )
        sf_m_count = (
            int(df_sf_m["Cantidad"].sum())
            if "Cantidad" in df_sf_m.columns
            else len(df_sf_m)
        )
        sn_m_count = (
            int(df_sn_m["Cantidad"].sum())
            if "Cantidad" in df_sn_m.columns
            else len(df_sn_m)
        )
      else:
        pn_m_count, sf_m_count, sn_m_count = 0, 0, 0

      col_im1, col_im2, col_im3 = st.columns(3)
      with col_im1:
        with st.container(border=True):
          img_pn = (
              f'<img src="{logo_pn}" style="width: 48px; height: 48px;'
              ' object-fit: contain;" alt="PN"/>'
              if logo_pn
              else "🛡️"
          )
          st.markdown(
              '<div style="display: flex; align-items: center; gap:'
              f' 15px;"><div>{img_pn}</div><div><div class="inst-title">Policía'
              f' Nacional</div><div class="inst-value">{pn_m_count:,} <span'
              ' style="font-size: 0.85rem; font-weight:400;'
              ' color:#64748b;">TOTAL MUNICIONES</span></div></div></div>',
              unsafe_allow_html=True,
          )
      with col_im2:
        with st.container(border=True):
          img_sf = (
              f'<img src="{logo_senafront}" style="width: 48px; height: 48px;'
              ' object-fit: contain;" alt="SENAFRONT"/>'
              if logo_senafront
              else "🛡️"
          )
          st.markdown(
              '<div style="display: flex; align-items: center; gap:'
              f' 15px;"><div>{img_sf}</div><div><div class="inst-title">Servicio'
              ' Nac. de Fronteras</div><div'
              f' class="inst-value">{sf_m_count:,} <span style="font-size:'
              ' 0.85rem; font-weight:400; color:#64748b;">TOTAL'
              ' MUNICIONES</span></div></div></div>',
              unsafe_allow_html=True,
          )
      with col_im3:
        with st.container(border=True):
          img_sn = (
              f'<img src="{logo_senan}" style="width: 48px; height: 48px;'
              ' object-fit: contain;" alt="SENAN"/>'
              if logo_senan
              else "🛡️"
          )
          st.markdown(
              '<div style="display: flex; align-items: center; gap:'
              f' 15px;"><div>{img_sn}</div><div><div class="inst-title">Servicio'
              f' Nac. Aeronaval</div><div class="inst-value">{sn_m_count:,}'
              ' <span style="font-size: 0.85rem; font-weight:400;'
              ' color:#64748b;">TOTAL MUNICIONES</span></div></div></div>',
              unsafe_allow_html=True,
          )

      with st.container(border=True):
        col_tm_img, col_tm_txt = st.columns([0.08, 0.92])
        with col_tm_img:
          if logo_minseg:
            st.markdown(
                f'<div style="display: flex; align-items: center;'
                ' justify-content: center; height: 100%;"><img'
                f' src="{logo_minseg}" style="width: 65px; height: 65px;'
                ' border-radius: 50%; object-fit: cover; border: 3px solid'
                ' #1E3A8A;" alt="MINSEG"/></div>',
                unsafe_allow_html=True,
            )
          else:
            st.markdown("🛡️", unsafe_allow_html=True)
        with col_tm_txt:
          st.subheader(
              "DESGLOSE TÁCTICO DE MUNICIONES Y RELACIÓN OPERATIVA POR"
              " INSTITUCIÓN"
          )

        tab_pn_m, tab_sf_m, tab_sn_m = st.tabs([
            "POLICÍA NACIONAL",
            "SERVICIO NACIONAL DE FRONTERAS",
            "SERVICIO NACIONAL AERONAVAL",
        ])
        val_col_m = "Cantidad" if "Cantidad" in df_m_filtrado.columns else None
        agg_m = "sum" if val_col_m else "count"
        sub_col_m = (
            "SubTipo"
            if "SubTipo" in df_m_filtrado.columns
            else ("Tipo" if "Tipo" in df_m_filtrado.columns else None)
        )
        rel_col_m = "Relación" if "Relación" in df_m_filtrado.columns else None

        with tab_pn_m:
          with st.container(border=True):
            st.markdown("### 👮‍♂️ POLICÍA NACIONAL")
            if (
                "Institucion" in df_m_filtrado.columns
                and sub_col_m
                and rel_col_m
            ):
              df_pn_sub_m = df_m_filtrado[
                  df_m_filtrado["Institucion"] == "Policía Nacional"
              ]
              if not df_pn_sub_m.empty:
                t_pn_m = (
                    pd.crosstab(
                        df_pn_sub_m[sub_col_m],
                        df_pn_sub_m[rel_col_m],
                        values=df_pn_sub_m[val_col_m] if val_col_m else None,
                        aggfunc=agg_m,
                        margins=True,
                        margins_name="Total General",
                    )
                    .fillna(0)
                    .astype(int)
                )
                st.dataframe(t_pn_m, use_container_width=True)

        with tab_sf_m:
          with st.container(border=True):
            st.markdown("### 💂‍♂️ SERVICIO NACIONAL DE FRONTERAS")
            if (
                "Institucion" in df_m_filtrado.columns
                and sub_col_m
                and rel_col_m
            ):
              df_sf_sub_m = df_m_filtrado[
                  df_m_filtrado["Institucion"]
                  == "Servicio Nacional de Fronteras"
              ]
              if not df_sf_sub_m.empty:
                t_sf_m = (
                    pd.crosstab(
                        df_sf_sub_m[sub_col_m],
                        df_sf_sub_m[rel_col_m],
                        values=df_sf_sub_m[val_col_m] if val_col_m else None,
                        aggfunc=agg_m,
                        margins=True,
                        margins_name="Total General",
                    )
                    .fillna(0)
                    .astype(int)
                )
                st.dataframe(t_sf_m, use_container_width=True)

        with tab_sn_m:
          with st.container(border=True):
            st.markdown("### ⚓ SERVICIO NACIONAL AERONAVAL")
            if (
                "Institucion" in df_m_filtrado.columns
                and sub_col_m
                and rel_col_m
            ):
              df_sn_sub_m = df_m_filtrado[
                  df_m_filtrado["Institucion"] == "Servicio Nacional Aeronaval"
              ]
              if not df_sn_sub_m.empty:
                t_sn_m = (
                    pd.crosstab(
                        df_sn_sub_m[sub_col_m],
                        df_sn_sub_m[rel_col_m],
                        values=df_sn_sub_m[val_col_m] if val_col_m else None,
                        aggfunc=agg_m,
                        margins=True,
                        margins_name="Total General",
                    )
                    .fillna(0)
                    .astype(int)
                )
                st.dataframe(t_sn_m, use_container_width=True)

      if len(anos_m_disp) >= 2:
        with st.container(border=True):
          st.subheader("📊 CUADRO COMPARATIVO ANUAL")
          cc1, cc2 = st.columns(2)
          with cc1:
            ano_base_m = st.selectbox(
                "Seleccionar Año Base (A)",
                options=anos_m_disp,
                index=0,
                key="ano_base_m",
            )
          with cc2:
            ano_comp_m = st.selectbox(
                "Seleccionar Año a Comparar (B)",
                options=anos_m_disp,
                index=min(1, len(anos_m_disp) - 1),
                key="ano_comp_m",
            )

          df_base_m = df_mun[df_mun["Años"] == int(ano_base_m)]
          df_comp_m = df_mun[df_mun["Años"] == int(ano_comp_m)]

          if distrito_m_sel and "Distrito" in df_mun.columns:
            df_base_m = df_base_m[
                df_base_m["Distrito"].isin(distrito_m_sel)
            ]
            df_comp_m = df_comp_m[
                df_comp_m["Distrito"].isin(distrito_m_sel)
            ]
          if corregimiento_m_sel and "Corregimiento" in df_mun.columns:
            df_base_m = df_base_m[
                df_base_m["Corregimiento"].isin(corregimiento_m_sel)
            ]
            df_comp_m = df_comp_m[
                df_comp_m["Corregimiento"].isin(corregimiento_m_sel)
            ]
          if mes_m_sel and "Mes" in df_mun.columns:
            df_base_m = df_base_m[df_base_m["Mes"].isin(mes_m_sel)]
            df_comp_m = df_comp_m[df_comp_m["Mes"].isin(mes_m_sel)]
          if verif_m_sel and col_verif_m:
            df_base_m = df_base_m[
                df_base_m[col_verif_m].astype(str).isin(verif_m_sel)
            ]
            df_comp_m = df_comp_m[
                df_comp_m[col_verif_m].astype(str).isin(verif_m_sel)
            ]

          tot_base_m = (
              int(df_base_m[val_col_m].sum())
              if val_col_m
              else len(df_base_m)
          )
          tot_comp_m = (
              int(df_comp_m[val_col_m].sum())
              if val_col_m
              else len(df_comp_m)
          )
          dif_m = tot_comp_m - tot_base_m
          pct_m = (dif_m / tot_base_m * 100) if tot_base_m > 0 else 0

          cm1, cm2, cm3 = st.columns(3)
          cm1.metric(
              "Registro de Total de Municiones"
              f" {ano_base_m} vs {ano_comp_m}",
              f"{tot_comp_m:,}",
              f"{pct_m:+.1f}% vs {ano_base_m} ({tot_base_m:,})",
          )
          cm2.metric("Diferencia Neta", f"{dif_m:+d}", "Variación global")
          cm3.metric(
              f"Total Base ({ano_base_m})",
              f"{tot_base_m:,}",
              "Referencia inicial",
          )

          st.markdown("---")
          st.markdown(
              "##### 📈 Comportamiento Mensual Comparativo"
              f" ({ano_base_m} vs {ano_comp_m})"
          )
          if "Mes" in df_mun.columns:
            mb = (
                df_base_m.groupby("Mes")[val_col_m]
                .sum()
                .reset_index(name="Cantidad")
                if val_col_m
                else df_base_m.groupby("Mes").size().reset_index(name="Cantidad")
            )
            mc = (
                df_comp_m.groupby("Mes")[val_col_m]
                .sum()
                .reset_index(name="Cantidad")
                if val_col_m
                else df_comp_m.groupby("Mes").size().reset_index(name="Cantidad")
            )
            mb["Mes"] = pd.Categorical(
                mb["Mes"], categories=orden_meses, ordered=True
            )
            mb = mb.sort_values("Mes").dropna(subset=["Mes"])
            mc["Mes"] = pd.Categorical(
                mc["Mes"], categories=orden_meses, ordered=True
            )
            mc = mc.sort_values("Mes").dropna(subset=["Mes"])

            fig_lm = go.Figure()
            fig_lm.add_trace(
                go.Scatter(
                    x=mb["Mes"],
                    y=mb["Cantidad"],
                    name=str(ano_base_m),
                    mode="lines+markers",
                    line=dict(color="#1E3A8A", width=3),
                    marker=dict(size=8),
                )
            )
            fig_lm.add_trace(
                go.Scatter(
                    x=mc["Mes"],
                    y=mc["Cantidad"],
                    name=str(ano_comp_m),
                    mode="lines+markers",
                    line=dict(color="#dc2626", width=3),
                    marker=dict(size=8),
                )
            )
            fig_lm.update_layout(
                height=380,
                margin={"r": 10, "t": 20, "l": 10, "b": 10},
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                ),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#f1f5f9",
                    title_text="<b>Total de Municiones</b>",
                ),
            )
            st.plotly_chart(fig_lm, use_container_width=True)

    with tab_datos_m:
      st.subheader("📋 REGISTROS COMPLETOS FILTRADOS - MUNICIONES")
      st.dataframe(df_m_filtrado, use_container_width=True)
  else:
    st.error("⚠️ No se pudo cargar el archivo de municiones.")

# =============================================================================
# C. LÓGICA DEL MÓDULO: CONTROL Y ANÁLISIS DE DROGAS IMELFC
# =============================================================================
elif modulo_seleccionado == "📦 Control y Análisis de Drogas IMELFC":
  df_drogas = cargar_datos_drogas()
  if df_drogas is not None and not df_drogas.empty:
    if "Año" in df_drogas.columns:
      df_drogas["Año"] = pd.to_numeric(df_drogas["Año"], errors="coerce")
    if "CANT. TON" in df_drogas.columns:
      df_drogas["CANT. TON"] = pd.to_numeric(
          df_drogas["CANT. TON"], errors="coerce"
      )
    tab_dashboard_d, tab_datos_d = st.tabs(["📊 DASHBOARD", "📋 DATOS ESCRITOS"])
    with tab_dashboard_d:
      with st.sidebar:
        img_sidebar_html = (
            f'<img src="{logo_principal}" style="width: 24px; height: 24px;'
            ' border-radius: 50%; object-fit: cover; border: 1.5px solid'
            ' #1E3A8A;" alt="Filtros"/>'
            if logo_principal
            else "🎛️"
        )
        st.markdown(
            f"""
                    <div class="sidebar-header">
                        {img_sidebar_html}
                        <span>PANEL DE CONTROL - DROGAS IMELFC</span>
                    </div>
                """,
            unsafe_allow_html=True,
        )

        if st.button(
            "🔄 Restablecer Filtros",
            use_container_width=True,
            type="secondary",
            key="btn_rst_drogas",
        ):
          st.session_state["ano_d_m_sel"] = []
          st.session_state["prov_d_m_sel"] = []
          st.session_state["tipo_d_m_sel"] = []
          st.session_state["mes_d_m_sel"] = []
          st.rerun()
        st.markdown("---")

        anos_d_disp = (
            sorted([
                int(x)
                for x in df_drogas["Año"].dropna().unique()
                if pd.notna(x)
            ])
            if "Año" in df_drogas.columns
            else []
        )
        provincias_d_disp = (
            sorted(df_drogas["Provincia"].dropna().unique().tolist())
            if "Provincia" in df_drogas.columns
            else []
        )
        tipos_d_disp = (
            sorted(df_drogas["TIPO DE DROGAS"].dropna().unique().tolist())
            if "TIPO DE DROGAS" in df_drogas.columns
            else []
        )

        orden_meses = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ]
        meses_d_pres = (
            [m for m in orden_meses if m in df_drogas["Mes"].dropna().unique()]
            if "Mes" in df_drogas.columns
            else []
        )

        with st.expander("📅 **Temporalidad y Ubicación**", expanded=True):
          ano_d_m_sel = st.multiselect(
              "Año Fiscal / Operativo",
              options=anos_d_disp,
              default=[],
              key="ano_d_m_sel",
          )
          provincia_d_m_sel = st.multiselect(
              "Procedencia (Provincia)",
              options=provincias_d_disp,
              default=[],
              key="prov_d_m_sel",
          )
          tipo_d_m_sel = st.multiselect(
              "Tipo de Droga",
              options=tipos_d_disp,
              default=[],
              key="tipo_d_m_sel",
          )
          mes_d_m_sel = st.multiselect(
              "Mes", options=meses_d_pres, default=[], key="mes_d_m_sel"
          )

        df_d_filtrado = df_drogas.copy()
        if ano_d_m_sel and "Año" in df_d_filtrado.columns:
          df_d_filtrado = df_d_filtrado[
              df_d_filtrado["Año"].isin(ano_d_m_sel)
          ]
        if provincia_d_m_sel and "Provincia" in df_d_filtrado.columns:
          df_d_filtrado = df_d_filtrado[
              df_d_filtrado["Provincia"].isin(provincia_d_m_sel)
          ]
        if tipo_d_m_sel and "TIPO DE DROGAS" in df_d_filtrado.columns:
          df_d_filtrado = df_d_filtrado[
              df_d_filtrado["TIPO DE DROGAS"].isin(tipo_d_m_sel)
          ]
        if mes_d_m_sel and "Mes" in df_d_filtrado.columns:
          df_d_filtrado = df_d_filtrado[
              df_d_filtrado["Mes"].isin(mes_d_m_sel)
          ]

        filtros_d_activos = sum([
            1
            for f in [
                ano_d_m_sel,
                provincia_d_m_sel,
                tipo_d_m_sel,
                mes_d_m_sel,
            ]
            if len(f) > 0
        ])
        st.caption(f"📌 **Filtros aplicados:** `{filtros_d_activos}` activo(s)")

      col_d1, col_d2, col_d3 = st.columns(3)
      total_ton_analizadas = (
          float(df_d_filtrado["CANT. TON"].sum())
          if "CANT. TON" in df_d_filtrado.columns
          else 0.0
      )

      if "TIPO DE DROGAS" in df_d_filtrado.columns and not df_d_filtrado.empty:
        top_droga_series = df_d_filtrado.groupby("TIPO DE DROGAS")[
            "CANT. TON"
        ].sum()
        if not top_droga_series.empty:
          top_droga_s = top_droga_series.idxmax()
          top_droga_val = top_droga_series.max()
          top_texto = f"{top_droga_s} ({top_droga_val:,.2f} T)"
        else:
          top_texto = "N/A"
      else:
        top_texto = "N/A"

      provincias_activas_d = (
          int(df_d_filtrado["Provincia"].nunique())
          if "Provincia" in df_d_filtrado.columns
          else 0
      )

      with col_d1:
        st.markdown(
            '<div class="kpi-card"><div class="kpi-label">TOTAL DROGAS'
            ' ANALIZADAS (TON)</div><div'
            f' class="kpi-value">{total_ton_analizadas:,.2f} T</div></div>',
            unsafe_allow_html=True,
        )
      with col_d2:
        st.markdown(
            '<div class="kpi-card"><div class="kpi-label">PRINCIPAL TIPO DE'
            ' DROGA</div><div class="kpi-value" style="font-size: 1.50rem;'
            " white-space: nowrap; overflow: hidden; text-overflow:"
            f' ellipsis;">{top_texto}</div></div>',
            unsafe_allow_html=True,
        )
      with col_d3:
        st.markdown(
            '<div class="kpi-card"><div class="kpi-label">PROVINCIAS ACTIVAS'
            ' (PROCEDENCIA)</div><div'
            f' class="kpi-value">{provincias_activas_d}</div></div>',
            unsafe_allow_html=True,
        )

      with st.container(border=True):
        st.subheader("📦 RESUMEN GENERAL POR TIPO DE DROGA (CANT. TON)")
        if (
            not df_d_filtrado.empty
            and "TIPO DE DROGAS" in df_d_filtrado.columns
        ):
          df_resumen_tipo = (
              df_d_filtrado.groupby("TIPO DE DROGAS")["CANT. TON"]
              .sum()
              .reset_index()
          )
          df_resumen_tipo["CANT. TON"] = df_resumen_tipo["CANT. TON"].round(4)
          df_resumen_tipo = df_resumen_tipo.sort_values(
              by="CANT. TON", ascending=False
          )
          st.dataframe(df_resumen_tipo, use_container_width=True)
        else:
          st.info("No hay datos disponibles con los filtros actuales.")

      col_gd1, col_gd2 = st.columns(2)
      with col_gd1:
        with st.container(border=True):
          st.subheader("📊 CANTIDAD DE DROGAS POR TIPO (TONELADAS)")
          if (
              not df_d_filtrado.empty
              and "TIPO DE DROGAS" in df_d_filtrado.columns
          ):
            df_bar = (
                df_d_filtrado.groupby("TIPO DE DROGAS")["CANT. TON"]
                .sum()
                .reset_index()
            )
            df_bar = df_bar.sort_values(by="CANT. TON", ascending=True)
            fig_d_bar = px.bar(
                df_bar,
                x="CANT. TON",
                y="TIPO DE DROGAS",
                orientation="h",
                text_auto=".2f",
                color="CANT. TON",
                color_continuous_scale="Blues",
            )
            fig_d_bar.update_layout(
                height=400,
                margin={"r": 10, "t": 10, "l": 10, "b": 10},
                xaxis_title="<b>Cantidad (Ton)</b>",
                yaxis_title="",
            )
            st.plotly_chart(fig_d_bar, use_container_width=True)

      with col_gd2:
        with st.container(border=True):
          st.subheader("🥧 PORCENTAJE POR TIPO DE DROGA (%)")
          if (
              not df_d_filtrado.empty
              and "TIPO DE DROGAS" in df_d_filtrado.columns
          ):
            df_pie = (
                df_d_filtrado.groupby("TIPO DE DROGAS")["CANT. TON"]
                .sum()
                .reset_index()
            )
            fig_d_pie = px.pie(
                df_pie,
                names="TIPO DE DROGAS",
                values="CANT. TON",
                hole=0.45,
                color_discrete_sequence=px.colors.sequential.Blues_r,
            )
            fig_d_pie.update_layout(
                height=400, margin={"r": 10, "t": 10, "l": 10, "b": 10}
            )
            st.plotly_chart(fig_d_pie, use_container_width=True)

      if len(anos_d_disp) >= 2:
        with st.container(border=True):
          st.subheader("📊 CUADRO COMPARATIVO ANUAL (IMELFC)")
          ccd1, ccd2 = st.columns(2)
          with ccd1:
            ano_base_d = st.selectbox(
                "Seleccionar Año Base (A)",
                options=anos_d_disp,
                index=0,
                key="ano_base_d",
            )
          with ccd2:
            ano_comp_d = st.selectbox(
                "Seleccionar Año a Comparar (B)",
                options=anos_d_disp,
                index=min(1, len(anos_d_disp) - 1),
                key="ano_comp_d",
            )

          df_base_d = df_drogas[df_drogas["Año"] == int(ano_base_d)]
          df_comp_d = df_drogas[df_drogas["Año"] == int(ano_comp_d)]

          tot_base_d = (
              float(df_base_d["CANT. TON"].sum())
              if "CANT. TON" in df_base_d.columns
              else 0.0
          )
          tot_comp_d = (
              float(df_comp_d["CANT. TON"].sum())
              if "CANT. TON" in df_comp_d.columns
              else 0.0
          )
          dif_d = tot_comp_d - tot_base_d
          pct_d = (dif_d / tot_base_d * 100) if tot_base_d > 0 else 0.0

          cd1, cd2, cd3 = st.columns(3)
          cd1.metric(
              f"Total Toneladas {ano_base_d} vs {ano_comp_d}",
              f"{tot_comp_d:,.2f} T",
              f"{pct_d:+.1f}% vs {ano_base_d} ({tot_base_d:,.2f}T)",
          )
          cd2.metric("Diferencia Neta", f"{dif_d:+,.2f} T", "Variación global")
          cd3.metric(
              f"Total Base ({ano_base_d})",
              f"{tot_base_d:,.2f} T",
              "Referencia inicial",
          )

          st.markdown("---")
          st.markdown(
              "##### 📈 Comportamiento Mensual Comparativo"
              f" ({ano_base_d} vs {ano_comp_d})"
          )
          if "Mes" in df_drogas.columns:
            mb_d = (
                df_base_d.groupby("Mes")["CANT. TON"]
                .sum()
                .reset_index(name="Cantidad")
            )
            mc_d = (
                df_comp_d.groupby("Mes")["CANT. TON"]
                .sum()
                .reset_index(name="Cantidad")
            )
            mb_d["Mes"] = pd.Categorical(
                mb_d["Mes"], categories=orden_meses, ordered=True
            )
            mb_d = mb_d.sort_values("Mes").dropna(subset=["Mes"])
            mc_d["Mes"] = pd.Categorical(
                mc_d["Mes"], categories=orden_meses, ordered=True
            )
            mc_d = mc_d.sort_values("Mes").dropna(subset=["Mes"])

            fig_ld = go.Figure()
            fig_ld.add_trace(
                go.Scatter(
                    x=mb_d["Mes"],
                    y=mb_d["Cantidad"],
                    name=str(ano_base_d),
                    mode="lines+markers",
                    line=dict(color="#1E3A8A", width=3),
                    marker=dict(size=8),
                )
            )
            fig_ld.add_trace(
                go.Scatter(
                    x=mc_d["Mes"],
                    y=mc_d["Cantidad"],
                    name=str(ano_comp_d),
                    mode="lines+markers",
                    line=dict(color="#dc2626", width=3),
                    marker=dict(size=8),
                )
            )
            fig_ld.update_layout(
                height=380,
                margin={"r": 10, "t": 20, "l": 10, "b": 10},
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                ),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#f1f5f9",
                    title_text="<b>Total Toneladas</b>",
                ),
            )
            st.plotly_chart(fig_ld, use_container_width=True)

          st.markdown("---")
          st.markdown(
              "##### 🗺️ Desglose y Variación por Procedencia"
              f" ({ano_base_d} vs {ano_comp_d})"
          )
          if "Provincia" in df_drogas.columns:
            pb_d = (
                df_base_d.groupby("Provincia")["CANT. TON"]
                .sum()
                .reset_index(name=f"Base_{ano_base_d}")
            )
            pc_d = (
                df_comp_d.groupby("Provincia")["CANT. TON"]
                .sum()
                .reset_index(name=f"Comp_{ano_comp_d}")
            )
            df_p_comp_d = pd.merge(
                pb_d, pc_d, on="Provincia", how="outer"
            ).fillna(0)
            df_p_comp_d["Diferencia"] = (
                df_p_comp_d[f"Comp_{ano_comp_d}"]
                - df_p_comp_d[f"Base_{ano_base_d}"]
            )
            df_p_comp_d["Variacion_%"] = df_p_comp_d.apply(
                lambda row: (
                    (row["Diferencia"] / row[f"Base_{ano_base_d}"] * 100)
                    if row[f"Base_{ano_base_d}"] > 0
                    else 0.0
                ),
                axis=1,
            )
            df_p_comp_d = df_p_comp_d.sort_values(
                by=f"Comp_{ano_comp_d}", ascending=False
            ).reset_index(drop=True)
            df_p_disp_d = df_p_comp_d.copy()
            df_p_disp_d["Variacion_%"] = df_p_disp_d["Variacion_%"].apply(
                lambda x: f"{x:+.1f}%"
            )
            st.dataframe(df_p_disp_d, use_container_width=True)

      with st.container(border=True):
        st.subheader("📅 MATRIZ DE CALOR TEMPORAL (MESES Y PROCEDENCIA)")
        if (
            not df_d_filtrado.empty
            and "Mes" in df_d_filtrado.columns
            and "Provincia" in df_d_filtrado.columns
        ):
          df_matriz_d = (
              df_d_filtrado.groupby(["Mes", "Provincia"])["CANT. TON"]
              .sum()
              .reset_index()
          )
          df_matriz_d["Mes"] = pd.Categorical(
              df_matriz_d["Mes"], categories=orden_meses, ordered=True
          )
          df_matriz_d = df_matriz_d.sort_values(["Mes", "Provincia"]).dropna(
              subset=["Mes"]
          )

          fig_cal_d = px.density_heatmap(
              df_matriz_d,
              x="Mes",
              y="Provincia",
              z="CANT. TON",
              color_continuous_scale="Blues",
              text_auto=".2f",
              labels={
                  "Mes": "Meses",
                  "Provincia": "Procedencia",
                  "CANT. TON": "Toneladas",
              },
          )
          fig_cal_d.update_layout(
              height=420,
              margin={"r": 10, "t": 20, "l": 10, "b": 10},
              xaxis_title="",
              yaxis_title="",
              coloraxis_colorbar=dict(title="Toneladas"),
          )
          st.plotly_chart(fig_cal_d, use_container_width=True)

          st.markdown("---")
          st.markdown(
              "##### 📝 DIAGNÓSTICO ESTADÍSTICO Y ANÁLISIS DE LA MATRIZ DE CALOR"
          )
          total_matriz = df_matriz_d["CANT. TON"].sum()
          mes_max_df = (
              df_matriz_d.groupby("Mes")["CANT. TON"].sum().reset_index()
          )
          mes_max_row = (
              mes_max_df.loc[mes_max_df["CANT. TON"].idxmax()]
              if not mes_max_df.empty
              else None
          )
          prov_max_df = (
              df_matriz_d.groupby("Provincia")["CANT. TON"].sum().reset_index()
          )
          prov_max_row = (
              prov_max_df.loc[prov_max_df["CANT. TON"].idxmax()]
              if not prov_max_df.empty
              else None
          )
          celda_pico = (
              df_matriz_d.loc[df_matriz_d["CANT. TON"].idxmax()]
              if not df_matriz_d.empty
              else None
          )
          promedio_mes = (
              df_matriz_d.groupby("Mes")["CANT. TON"].sum().mean()
              if not df_matriz_d.empty
              else 0.0
          )

          if (
              mes_max_row is not None
              and prov_max_row is not None
              and celda_pico is not None
          ):
            pct_prov_max = (
                (prov_max_row["CANT. TON"] / total_matriz * 100)
                if total_matriz > 0
                else 0.0
            )
            pct_mes_max = (
                (mes_max_row["CANT. TON"] / total_matriz * 100)
                if total_matriz > 0
                else 0.0
            )

            col_an1, col_an2 = st.columns([0.40, 0.60])
            with col_an1:
              st.markdown(
                  f"""
                                <div style="background-color: #f8fafc; border-left: 4px solid #1E3A8A; padding: 12px; border-radius: 6px; font-size: 0.88rem;">
                                    <b>📊 Indicadores Clave de Concentración:</b><br/>
                                    • <b>Mes Pico Operativo:</b> {mes_max_row['Mes']} ({mes_max_row['CANT. TON']:,.2f} Toneladas — {pct_mes_max:.1f}% del total filtrado).<br/>
                                    • <b>Provincia Dominante:</b> {prov_max_row['Provincia']} ({prov_max_row['CANT. TON']:,.2f} Toneladas — {pct_prov_max:.1f}% del volumen).<br/>
                                    • <b>Concentración Máxima Registrada:</b> {celda_pico['Provincia']} en el mes de {celda_pico['Mes']} con <b>{celda_pico['CANT. TON']:,.2f} T</b>.<br/>
                                    • <b>Promedio Mensual Procesado:</b> {promedio_mes:,.2f} Toneladas/Mes.
                                </div>
                            """,
                  unsafe_allow_html=True,
              )
            with col_an2:
              st.markdown(
                  f"""
                                <div style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 12px; border-radius: 6px; font-size: 0.88rem; color: #334155;">
                                    <b>📌 Conclusión y Diagnóstico Táctico:</b><br/>
                                    La matriz de calor denota una distribución espacial con mayor intensidad de análisis pericial en la jurisdicción de <b>{prov_max_row['Provincia']}</b>, consolidando el mayor flujo de muestras químicas ingresadas a IMELFC. 
                                    El mes de <b>{mes_max_row['Mes']}</b> muestra un repunte crítico en la carga procesada, marcando el punto de mayor exigencia logística del periodo consultado.
                                </div>
                            """,
                  unsafe_allow_html=True,
              )

      with st.container(border=True):
        st.subheader(
            "🗺️ MAPA TEMÁTICO NACIONAL: CONCENTRACIÓN DE DROGAS POR PROVINCIA"
            " (VISTA 2D PLANO)"
        )
        df_mapa_prov = (
            df_d_filtrado.groupby(["Provincia", "Latitud", "Longitud"])[
                "CANT. TON"
            ]
            .sum()
            .reset_index()
            if not df_d_filtrado.empty
            else pd.DataFrame()
        )

        if not df_mapa_prov.empty and "Latitud" in df_mapa_prov.columns:
          min_t = df_mapa_prov["CANT. TON"].min()
          max_t = df_mapa_prov["CANT. TON"].max()

          def asignar_color_azul_proporcional(val):
            if max_t == min_t:
              norm = 1.0
            else:
              norm = (val - min_t) / (max_t - min_t)
            r = int(219 - norm * (219 - 30))
            g = int(234 - norm * (234 - 58))
            b = int(254 - norm * (254 - 138))
            return [r, g, b, 230]

          df_mapa_prov["color_rgb"] = df_mapa_prov["CANT. TON"].apply(
              asignar_color_azul_proporcional
          )
          df_mapa_prov["radio_esfera"] = df_mapa_prov["CANT. TON"].apply(
              lambda x: max(2500, int((x**0.5) * 3200))
          )
          view_state_d2d = pdk.ViewState(
              latitude=8.5379, longitude=-80.7821, zoom=7.5, pitch=0
          )

          capa_provincias_2d = pdk.Layer(
              "ScatterplotLayer",
              data=df_mapa_prov,
              get_position="[Longitud, Latitud]",
              get_color="color_rgb",
              get_radius="radio_esfera",
              pickable=True,
              auto_highlight=True,
              stroked=True,
              filled=True,
              line_width_min_pixels=1.5,
          )
          tooltip_drogas_2d = {
              "html": (
                  "<b>Provincia / Procedencia:</b> {Provincia}<br/><b>Total"
                  " Analizado:</b> {CANT. TON} Toneladas"
              ),
              "style": {
                  "backgroundColor": "#1E3A8A",
                  "color": "white",
                  "fontSize": "12px",
              },
          }
          r_drogas_2d = pdk.Deck(
              layers=[capa_provincias_2d],
              initial_view_state=view_state_d2d,
              map_style=pdk.map_styles.LIGHT,
              tooltip=tooltip_drogas_2d,
          )
          st.pydeck_chart(r_drogas_2d)

          st.markdown("---")
          st.markdown(
              "##### 📝 DIAGNÓSTICO GEOESPACIAL Y ANÁLISIS DEL MAPA DE DROGAS"
          )
          total_mapa_ton = df_mapa_prov["CANT. TON"].sum()
          prov_top_mapa = (
              df_mapa_prov.loc[df_mapa_prov["CANT. TON"].idxmax()]
              if not df_mapa_prov.empty
              else None
          )
          cant_provincias_mapa = len(df_mapa_prov)
          if prov_top_mapa is not None:
            pct_top_mapa = (
                (prov_top_mapa["CANT. TON"] / total_mapa_ton * 100)
                if total_mapa_ton > 0
                else 0.0
            )
            col_m_exp1, col_m_exp2 = st.columns([0.40, 0.60])
            with col_m_exp1:
              st.markdown(
                  f"""
                                <div style="background-color: #f8fafc; border-left: 4px solid #1E3A8A; padding: 12px; border-radius: 6px; font-size: 0.88rem;">
                                    <b>🗺️ Métricas Geoespaciales Clave:</b><br/>
                                    • <b>Foco Territorial Principal:</b> {prov_top_mapa['Provincia']}.<br/>
                                    • <b>Volumen Prov. Líder:</b> <b>{prov_top_mapa['CANT. TON']:,.2f} Toneladas</b>.<br/>
                                    • <b>Participación Territorial:</b> Representa el <b>{pct_top_mapa:.1f}%</b> del volumen total filtrado.<br/>
                                    • <b>Cobertura Geográfica:</b> {cant_provincias_mapa} provincia(s) registran flujo de incautaciones.
                                </div>
                            """,
                  unsafe_allow_html=True,
              )
            with col_m_exp2:
              st.markdown(
                  f"""
                                <div style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 12px; border-radius: 6px; font-size: 0.88rem; color: #334155;">
                                    <b>📌 Interpretación del Mapa 2D de Procedencia:</b><br/>
                                    El mapa en plano 2D despliega la distribución nacional de muestras químicas remitidas al IMELFC. La escala cromática de azules asigna el tono azul marino más oscuro y un radio mayor a la provincia de <b>{prov_top_mapa['Provincia']}</b>, señalándola como el principal punto de origen o de paso de incautación.
                                </div>
                            """,
                  unsafe_allow_html=True,
              )

    with tab_datos_d:
      st.subheader("📋 REGISTROS COMPLETOS FILTRADOS - DROGAS IMELFC")
      st.dataframe(df_d_filtrado, use_container_width=True)
  else:
    st.error(
        "⚠️ No se pudo cargar el archivo 'Base_Drogas_5_Anos.xlsx'. Asegúrese"
        " de que exista en el directorio."
    )

# =============================================================================
# D. LÓGICA DEL MÓDULO: CONTROL Y ANÁLISIS DE INCIDENCIAS DE POSIBLES DROGAS SITIGPOL
# =============================================================================
elif (
    modulo_seleccionado
    == "📦 Control y Análisis de Incidencias de Posibles Drogas SITIGPOL"
):
  df_s_drogas = cargar_datos_drogas_sitigpol()
  if df_s_drogas is not None and not df_s_drogas.empty:
    if "Año" in df_s_drogas.columns:
      df_s_drogas["Año"] = pd.to_numeric(df_s_drogas["Año"], errors="coerce")
    tab_dashboard_s, tab_datos_s = st.tabs(["📊 DASHBOARD", "📋 DATOS ESCRITOS"])
    with tab_dashboard_s:
      with st.sidebar:
        img_sidebar_html = (
            f'<img src="{logo_principal}" style="width: 24px; height: 24px;'
            ' border-radius: 50%; object-fit: cover; border: 1.5px solid'
            ' #1E3A8A;" alt="Filtros"/>'
            if logo_principal
            else "🎛️"
        )
        st.markdown(
            f"""
                    <div class="sidebar-header">
                        {img_sidebar_html}
                        <span>PANEL DE CONTROL - SITIGPOL DROGAS</span>
                    </div>
                """,
            unsafe_allow_html=True,
        )

        if st.button(
            "🔄 Restablecer Filtros",
            use_container_width=True,
            type="secondary",
            key="btn_rst_sitigpol",
        ):
          st.session_state["ano_s_sel"] = []
          st.session_state["prov_s_sel"] = []
          st.session_state["tipo_s_sel"] = []
          st.session_state["mes_s_sel"] = []
          st.session_state["rel_s_sel"] = []
          st.rerun()
        st.markdown("---")

        anos_s_disp = (
            sorted([
                int(x)
                for x in df_s_drogas["Año"].dropna().unique()
                if pd.notna(x)
            ])
            if "Año" in df_s_drogas.columns
            else []
        )
        provincias_s_disp = (
            sorted(df_s_drogas["Provincia"].dropna().unique().tolist())
            if "Provincia" in df_s_drogas.columns
            else []
        )
        tipos_s_disp = (
            sorted(df_s_drogas["Tipo"].dropna().unique().tolist())
            if "Tipo" in df_s_drogas.columns
            else []
        )
        relaciones_s_disp = (
            sorted(df_s_drogas["Relación"].dropna().unique().tolist())
            if "Relación" in df_s_drogas.columns
            else []
        )

        orden_meses = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ]
        meses_s_pres = (
            [
                m
                for m in orden_meses
                if m in df_s_drogas["Mes"].dropna().unique()
            ]
            if "Mes" in df_s_drogas.columns
            else []
        )

        with st.expander("📅 **Temporalidad y Ubicación**", expanded=True):
          ano_s_sel = st.multiselect(
              "Año Fiscal / Operativo",
              options=anos_s_disp,
              default=[],
              key="ano_s_sel",
          )
          provincia_s_sel = st.multiselect(
              "Provincia / Jurisdicción",
              options=provincias_s_disp,
              default=[],
              key="prov_s_sel",
          )
          tipo_s_sel = st.multiselect(
              "Tipo / Clasificación",
              options=tipos_s_disp,
              default=[],
              key="tipo_s_sel",
          )
          mes_s_sel = st.multiselect(
              "Mes", options=meses_s_pres, default=[], key="mes_s_sel"
          )
          rel_s_sel = st.multiselect(
              "Estatus / Relación",
              options=relaciones_s_disp,
              default=[],
              key="rel_s_sel",
          )
        with st.expander("🗺️ **Capas del Mapa Geoespacial**", expanded=True):
          ver_calor_s = st.checkbox(
              "🔥 Mapa de Calor (Densidad Incautaciones)",
              value=True,
              key="chk_calor_s",
          )
          ver_puntos_s = st.checkbox(
              "📍 Puntos de Incautación", value=True, key="chk_puntos_s"
          )
          st.markdown("---")
          st.markdown("👥 **Capas de Pandillas**")
          ver_calor_pandillas_s = st.checkbox(
              "🌿 Mapa de Calor (Densidad Pandillas)",
              value=False,
              key="chk_calor_p_s",
          )
          ver_puntos_pandillas_s = st.checkbox(
              "🔵 Puntos Azules (Pandillas)", value=True, key="chk_puntos_p_s"
          )

        df_s_filtrado = df_s_drogas.copy()
        if ano_s_sel and "Año" in df_s_filtrado.columns:
          df_s_filtrado = df_s_filtrado[df_s_filtrado["Año"].isin(ano_s_sel)]
        if provincia_s_sel and "Provincia" in df_s_filtrado.columns:
          df_s_filtrado = df_s_filtrado[
              df_s_filtrado["Provincia"].isin(provincia_s_sel)
          ]
        if tipo_s_sel and "Tipo" in df_s_filtrado.columns:
          df_s_filtrado = df_s_filtrado[df_s_filtrado["Tipo"].isin(tipo_s_sel)]
        if mes_s_sel and "Mes" in df_s_filtrado.columns:
          df_s_filtrado = df_s_filtrado[df_s_filtrado["Mes"].isin(mes_s_sel)]
        if rel_s_sel and "Relación" in df_s_filtrado.columns:
          df_s_filtrado = df_s_filtrado[
              df_s_filtrado["Relación"].isin(rel_s_sel)
          ]

        filtros_s_activos = sum([
            1
            for f in [
                ano_s_sel,
                provincia_s_sel,
                tipo_s_sel,
                mes_s_sel,
                rel_s_sel,
            ]
            if len(f) > 0
        ])
        st.caption(f"📌 **Filtros aplicados:** `{filtros_s_activos}` activo(s)")

      df_pandillas_s_filtrado = (
          df_pandillas.copy() if df_pandillas is not None else None
      )
      if (
          df_pandillas_s_filtrado is not None
          and not df_pandillas_s_filtrado.empty
          and provincia_s_sel
      ):
        if "PRO" in df_pandillas_s_filtrado.columns:
          prov_s_lower = [p.lower() for p in provincia_s_sel]
          df_pandillas_s_filtrado = df_pandillas_s_filtrado[
              df_pandillas_s_filtrado["PRO"]
              .astype(str)
              .str.lower()
              .isin(prov_s_lower)
          ]

      col_s1, col_s2, col_s3 = st.columns(3)
      total_reg_s = (
          int(df_s_filtrado["Cantidad_Real"].count())
          if "Cantidad_Real" in df_s_filtrado.columns
          else len(df_s_filtrado)
      )
      total_cant_s = (
          float(df_s_filtrado["Cantidad_Real"].sum())
          if "Cantidad_Real" in df_s_filtrado.columns
          else 0.0
      )
      provincias_activas_s = (
          int(df_s_filtrado["Provincia"].nunique())
          if "Provincia" in df_s_filtrado.columns
          else 0
      )

      with col_s1:
        st.markdown(
            '<div class="kpi-card"><div class="kpi-label">TOTAL DE REGISTROS'
            ' (CONTEO DE CELDAS)</div><div'
            f' class="kpi-value">{total_reg_s:,}</div></div>',
            unsafe_allow_html=True,
        )
      with col_s2:
        st.markdown(
            '<div class="kpi-card"><div class="kpi-label">TOTAL DE POSIBLES'
            ' DROGAS INCAUTADAS</div><div'
            f' class="kpi-value">{total_cant_s:,.2f}</div></div>',
            unsafe_allow_html=True,
        )
      with col_s3:
        st.markdown(
            '<div class="kpi-card"><div class="kpi-label">PROVINCIAS Y COMARCAS'
            f' ACTIVAS</div><div class="kpi-value">{provincias_activas_s}</div></div>',
            unsafe_allow_html=True,
        )

      if "Institución" in df_s_filtrado.columns:
        df_pn_s = df_s_filtrado[
            df_s_filtrado["Institución"] == "Policía Nacional"
        ]
        df_sf_s = df_s_filtrado[
            df_s_filtrado["Institución"] == "Servicio Nacional de Fronteras"
        ]
        df_sn_s = df_s_filtrado[
            df_s_filtrado["Institución"] == "Servicio Nacional Aeronaval"
        ]

        pn_cant_s = (
            float(df_pn_s["Cantidad_Real"].sum())
            if "Cantidad_Real" in df_pn_s.columns
            else 0.0
        )
        sf_cant_s = (
            float(df_sf_s["Cantidad_Real"].sum())
            if "Cantidad_Real" in df_sf_s.columns
            else 0.0
        )
        sn_cant_s = (
            float(df_sn_s["Cantidad_Real"].sum())
            if "Cantidad_Real" in df_sn_s.columns
            else 0.0
        )
      else:
        pn_cant_s, sf_cant_s, sn_cant_s = 0.0, 0.0, 0.0

      col_is1, col_is2, col_is3 = st.columns(3)
      with col_is1:
        with st.container(border=True):
          img_pn = (
              f'<img src="{logo_pn}" style="width: 48px; height: 48px;'
              ' object-fit: contain;" alt="PN"/>'
              if logo_pn
              else "🛡️"
          )
          st.markdown(
              '<div style="display: flex; align-items: center; gap:'
              f' 15px;"><div>{img_pn}</div><div><div class="inst-title">Policía'
              f' Nacional</div><div class="inst-value">{pn_cant_s:,.2f} <span'
              ' style="font-size: 0.85rem; font-weight:400;'
              ' color:#64748b;">TOTAL INCAUTADO</span></div></div></div>',
              unsafe_allow_html=True,
          )
      with col_is2:
        with st.container(border=True):
          img_sf = (
              f'<img src="{logo_senafront}" style="width: 48px; height: 48px;'
              ' object-fit: contain;" alt="SENAFRONT"/>'
              if logo_senafront
              else "🛡️"
          )
          st.markdown(
              '<div style="display: flex; align-items: center; gap:'
              f' 15px;"><div>{img_sf}</div><div><div class="inst-title">Servicio'
              ' Nac. de Fronteras</div><div'
              f' class="inst-value">{sf_cant_s:,.2f} <span style="font-size:'
              ' 0.85rem; font-weight:400; color:#64748b;">TOTAL'
              ' INCAUTADO</span></div></div></div>',
              unsafe_allow_html=True,
          )
      with col_is3:
        with st.container(border=True):
          img_sn = (
              f'<img src="{logo_senan}" style="width: 48px; height: 48px;'
              ' object-fit: contain;" alt="SENAN"/>'
              if logo_senan
              else "🛡️"
          )
          st.markdown(
              '<div style="display: flex; align-items: center; gap:'
              f' 15px;"><div>{img_sn}</div><div><div class="inst-title">Servicio'
              f' Nac. Aeronaval</div><div class="inst-value">{sn_cant_s:,.2f}'
              ' <span style="font-size: 0.85rem; font-weight:400;'
              ' color:#64748b;">TOTAL INCAUTADO</span></div></div></div>',
              unsafe_allow_html=True,
          )

      with st.container(border=True):
        col_ts_img, col_ts_txt = st.columns([0.08, 0.92])
        with col_ts_img:
          if logo_minseg:
            st.markdown(
                f'<div style="display: flex; align-items: center;'
                ' justify-content: center; height: 100%;"><img'
                f' src="{logo_minseg}" style="width: 65px; height: 65px;'
                ' border-radius: 50%; object-fit: cover; border: 3px solid'
                ' #1E3A8A;" alt="MINSEG"/></div>',
                unsafe_allow_html=True,
            )
          else:
            st.markdown("🛡️", unsafe_allow_html=True)
        with col_ts_txt:
          st.subheader(
              "DESGLOSE TÁCTICO DE POSIBLES DROGAS SITIGPOL POR TIPO Y RELACIÓN"
              " OPERATIVA"
          )

        tab_pn_s, tab_sf_s, tab_sn_s = st.tabs([
            "POLICÍA NACIONAL",
            "SERVICIO NACIONAL DE FRONTERAS",
            "SERVICIO NACIONAL AERONAVAL",
        ])

        with tab_pn_s:
          with st.container(border=True):
            st.markdown("### 👮‍♂️ POLICÍA NACIONAL")
            if (
                "Institución" in df_s_filtrado.columns
                and "Tipo" in df_s_filtrado.columns
                and "Relación" in df_s_filtrado.columns
            ):
              df_pn_sub_s = df_s_filtrado[
                  df_s_filtrado["Institución"] == "Policía Nacional"
              ]
              if not df_pn_sub_s.empty:
                t_pn_s = (
                    pd.crosstab(
                        df_pn_sub_s["Tipo"],
                        df_pn_sub_s["Relación"],
                        values=df_pn_sub_s["Cantidad_Real"],
                        aggfunc="sum",
                        margins=True,
                        margins_name="Total General",
                    )
                    .fillna(0)
                    .round(2)
                )
                st.dataframe(t_pn_s, use_container_width=True)
              else:
                st.info("No hay registros para la Policía Nacional.")

        with tab_sf_s:
          with st.container(border=True):
            st.markdown("### 💂‍♂️ SERVICIO NACIONAL DE FRONTERAS")
            if (
                "Institución" in df_s_filtrado.columns
                and "Tipo" in df_s_filtrado.columns
                and "Relación" in df_s_filtrado.columns
            ):
              df_sf_sub_s = df_s_filtrado[
                  df_s_filtrado["Institución"]
                  == "Servicio Nacional de Fronteras"
              ]
              if not df_sf_sub_s.empty:
                t_sf_s = (
                    pd.crosstab(
                        df_sf_sub_s["Tipo"],
                        df_sf_sub_s["Relación"],
                        values=df_sf_sub_s["Cantidad_Real"],
                        aggfunc="sum",
                        margins=True,
                        margins_name="Total General",
                    )
                    .fillna(0)
                    .round(2)
                )
                st.dataframe(t_sf_s, use_container_width=True)
              else:
                st.info("No hay registros para SENAFRONT.")

        with tab_sn_s:
          with st.container(border=True):
            st.markdown("### ⚓ SERVICIO NACIONAL AERONAVAL")
            if (
                "Institución" in df_s_filtrado.columns
                and "Tipo" in df_s_filtrado.columns
                and "Relación" in df_s_filtrado.columns
            ):
              df_sn_sub_s = df_s_filtrado[
                  df_s_filtrado["Institución"] == "Servicio Nacional Aeronaval"
              ]
              if not df_sn_sub_s.empty:
                t_sn_s = (
                    pd.crosstab(
                        df_sn_sub_s["Tipo"],
                        df_sn_sub_s["Relación"],
                        values=df_sn_sub_s["Cantidad_Real"],
                        aggfunc="sum",
                        margins=True,
                        margins_name="Total General",
                    )
                    .fillna(0)
                    .round(2)
                )
                st.dataframe(t_sn_s, use_container_width=True)
              else:
                st.info("No hay registros para el SENAN.")

      if len(anos_s_disp) >= 2:
        with st.container(border=True):
          st.subheader("📊 CUADRO COMPARATIVO ANUAL (SITIGPOL)")
          ccs1, ccs2 = st.columns(2)
          with ccs1:
            ano_base_s = st.selectbox(
                "Seleccionar Año Base (A)",
                options=anos_s_disp,
                index=0,
                key="ano_base_s",
            )
          with ccs2:
            ano_comp_s = st.selectbox(
                "Seleccionar Año a Comparar (B)",
                options=anos_s_disp,
                index=min(1, len(anos_s_disp) - 1),
                key="ano_comp_s",
            )

          df_base_s = df_s_drogas[df_s_drogas["Año"] == int(ano_base_s)]
          df_comp_s = df_s_drogas[df_s_drogas["Año"] == int(ano_comp_s)]

          if provincia_s_sel and "Provincia" in df_s_drogas.columns:
            df_base_s = df_base_s[df_base_s["Provincia"].isin(provincia_s_sel)]
            df_comp_s = df_comp_s[df_comp_s["Provincia"].isin(provincia_s_sel)]
          if tipo_s_sel and "Tipo" in df_s_drogas.columns:
            df_base_s = df_base_s[df_base_s["Tipo"].isin(tipo_s_sel)]
            df_comp_s = df_comp_s[df_comp_s["Tipo"].isin(tipo_s_sel)]
          if mes_s_sel and "Mes" in df_s_drogas.columns:
            df_base_s = df_base_s[df_base_s["Mes"].isin(mes_s_sel)]
            df_comp_s = df_comp_s[df_comp_s["Mes"].isin(mes_s_sel)]
          if rel_s_sel and "Relación" in df_s_drogas.columns:
            df_base_s = df_base_s[df_base_s["Relación"].isin(rel_s_sel)]
            df_comp_s = df_comp_s[df_comp_s["Relación"].isin(rel_s_sel)]

          tot_base_s = (
              float(df_base_s["Cantidad_Real"].sum())
              if "Cantidad_Real" in df_base_s.columns
              else 0.0
          )
          tot_comp_s = (
              float(df_comp_s["Cantidad_Real"].sum())
              if "Cantidad_Real" in df_comp_s.columns
              else 0.0
          )
          dif_s = tot_comp_s - tot_base_s
          pct_s = (dif_s / tot_base_s * 100) if tot_base_s > 0 else 0.0

          cs1, cs2, cs3 = st.columns(3)
          cs1.metric(
              f"Total Posibles Drogas {ano_base_s} vs {ano_comp_s}",
              f"{tot_comp_s:,.2f}",
              f"{pct_s:+.1f}% vs {ano_base_s} ({tot_base_s:,.2f})",
          )
          cs2.metric("Diferencia Neta", f"{dif_s:+,.2f}", "Variación global")
          cs3.metric(
              f"Total Base ({ano_base_s})",
              f"{tot_base_s:,.2f}",
              "Referencia inicial",
          )

          st.markdown("---")
          st.markdown(
              "##### 📈 Comportamiento Mensual Comparativo"
              f" ({ano_base_s} vs {ano_comp_s})"
          )
          if "Mes" in df_s_drogas.columns:
            mb_s = (
                df_base_s.groupby("Mes")["Cantidad_Real"]
                .sum()
                .reset_index(name="Cantidad")
            )
            mc_s = (
                df_comp_s.groupby("Mes")["Cantidad_Real"]
                .sum()
                .reset_index(name="Cantidad")
            )
            mb_s["Mes"] = pd.Categorical(
                mb_s["Mes"], categories=orden_meses, ordered=True
            )
            mb_s = mb_s.sort_values("Mes").dropna(subset=["Mes"])
            mc_s["Mes"] = pd.Categorical(
                mc_s["Mes"], categories=orden_meses, ordered=True
            )
            mc_s = mc_s.sort_values("Mes").dropna(subset=["Mes"])

            fig_ls = go.Figure()
            fig_ls.add_trace(
                go.Scatter(
                    x=mb_s["Mes"],
                    y=mb_s["Cantidad"],
                    name=str(ano_base_s),
                    mode="lines+markers",
                    line=dict(color="#1E3A8A", width=3),
                    marker=dict(size=8),
                )
            )
            fig_ls.add_trace(
                go.Scatter(
                    x=mc_s["Mes"],
                    y=mc_s["Cantidad"],
                    name=str(ano_comp_s),
                    mode="lines+markers",
                    line=dict(color="#dc2626", width=3),
                    marker=dict(size=8),
                )
            )
            fig_ls.update_layout(
                height=380,
                margin={"r": 10, "t": 20, "l": 10, "b": 10},
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                ),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#f1f5f9",
                    title_text="<b>Total Incautado</b>",
                ),
            )
            st.plotly_chart(fig_ls, use_container_width=True)

          st.markdown("---")
          st.markdown(
              "##### 🗺️ Desglose y Variación por Provincia"
              f" ({ano_base_s} vs {ano_comp_s})"
          )
          if "Provincia" in df_s_drogas.columns:
            pb_s = (
                df_base_s.groupby("Provincia")["Cantidad_Real"]
                .sum()
                .reset_index(name=f"Base_{ano_base_s}")
            )
            pc_s = (
                df_comp_s.groupby("Provincia")["Cantidad_Real"]
                .sum()
                .reset_index(name=f"Comp_{ano_comp_s}")
            )
            df_p_comp_s = pd.merge(
                pb_s, pc_s, on="Provincia", how="outer"
            ).fillna(0)
            df_p_comp_s["Diferencia"] = (
                df_p_comp_s[f"Comp_{ano_comp_s}"]
                - df_p_comp_s[f"Base_{ano_base_s}"]
            )
            df_p_comp_s["Variacion_%"] = df_p_comp_s.apply(
                lambda row: (
                    (row["Diferencia"] / row[f"Base_{ano_base_s}"] * 100)
                    if row[f"Base_{ano_base_s}"] > 0
                    else 0.0
                ),
                axis=1,
            )
            df_p_comp_s = df_p_comp_s.sort_values(
                by=f"Comp_{ano_comp_s}", ascending=False
            ).reset_index(drop=True)
            df_p_disp_s = df_p_comp_s.copy()
            df_p_disp_s["Variacion_%"] = df_p_disp_s["Variacion_%"].apply(
                lambda x: f"{x:+.1f}%"
            )
            st.dataframe(df_p_disp_s, use_container_width=True)

      with st.container(border=True):
        st.subheader("📅 MATRIZ DE CALOR TEMPORAL (DÍAS Y MESES)")
        if "Fecha_dt" in df_s_filtrado.columns and not df_s_filtrado.empty:
          df_cal_s = df_s_filtrado.dropna(subset=["Fecha_dt"]).copy()
          if not df_cal_s.empty:
            dias_semana_esp = {
                0: "Lunes",
                1: "Martes",
                2: "Miércoles",
                3: "Jueves",
                4: "Viernes",
                5: "Sábado",
                6: "Domingo",
            }
            orden_dias = [
                "Domingo",
                "Lunes",
                "Martes",
                "Miércoles",
                "Jueves",
                "Viernes",
                "Sábado",
            ]
            df_cal_s["Dia_Semana"] = df_cal_s["Fecha_dt"].dt.dayofweek.map(
                dias_semana_esp
            )

            df_matriz_s = (
                df_cal_s.groupby(["Mes", "Dia_Semana"])["Cantidad_Real"]
                .sum()
                .reset_index(name="Total_Incautado")
            )
            df_matriz_s["Mes"] = pd.Categorical(
                df_matriz_s["Mes"], categories=orden_meses, ordered=True
            )
            df_matriz_s["Dia_Semana"] = pd.Categorical(
                df_matriz_s["Dia_Semana"], categories=orden_dias, ordered=True
            )
            df_matriz_s = df_matriz_s.sort_values(
                ["Mes", "Dia_Semana"]
            ).dropna(subset=["Mes", "Dia_Semana"])

            fig_cal_s = px.density_heatmap(
                df_matriz_s,
                x="Mes",
                y="Dia_Semana",
                z="Total_Incautado",
                color_continuous_scale="Blues",
                labels={
                    "Mes": "Meses",
                    "Dia_Semana": "Día de la Semana",
                    "Total_Incautado": "Total Incautado",
                },
            )
            fig_cal_s.update_layout(
                height=380,
                margin={"r": 10, "t": 20, "l": 10, "b": 10},
                xaxis_title="",
                yaxis_title="",
                yaxis=dict(
                    categoryorder="array", categoryarray=orden_dias
                ),
            )
            st.plotly_chart(fig_cal_s, use_container_width=True)

            st.markdown("---")
            st.markdown(
                "##### 📝 DIAGNÓSTICO ESTADÍSTICO Y ANÁLISIS DE LA MATRIZ"
                " TEMPORAL"
            )

            total_m_s = df_matriz_s["Total_Incautado"].sum()
            dia_max_s = (
                df_matriz_s.groupby("Dia_Semana")["Total_Incautado"]
                .sum()
                .idxmax()
            )
            val_dia_s = (
                df_matriz_s.groupby("Dia_Semana")["Total_Incautado"]
                .sum()
                .max()
            )
            mes_max_s = (
                df_matriz_s.groupby("Mes")["Total_Incautado"].sum().idxmax()
            )
            val_mes_s = (
                df_matriz_s.groupby("Mes")["Total_Incautado"].sum().max()
            )
            celda_pico_s = df_matriz_s.loc[
                df_matriz_s["Total_Incautado"].idxmax()
            ]
            prom_diario_s = (
                total_m_s / len(df_matriz_s) if len(df_matriz_s) > 0 else 0.0
            )

            col_as1, col_as2 = st.columns([0.40, 0.60])
            with col_as1:
              st.markdown(
                  f"""
                                <div style="background-color: #f8fafc; border-left: 4px solid #1E3A8A; padding: 12px; border-radius: 6px; font-size: 0.88rem;">
                                    <b>📊 Indicadores de Frecuencia Temporal:</b><br/>
                                    • <b>Día de Mayor Incidencia:</b> {dia_max_s} ({val_dia_s:,.2f} Unidades).<br/>
                                    • <b>Mes Pico Operativo:</b> {mes_max_s} ({val_mes_s:,.2f} Unidades).<br/>
                                    • <b>Pico Máximo Combinado:</b> {celda_pico_s['Dia_Semana']} en {celda_pico_s['Mes']} ({celda_pico_s['Total_Incautado']:,.2f} U).<br/>
                                    • <b>Promedio por Bloque Temporal:</b> {prom_diario_s:,.2f} Unidades.
                                </div>
                            """,
                  unsafe_allow_html=True,
              )
            with col_as2:
              st.markdown(
                  f"""
                                <div style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 12px; border-radius: 6px; font-size: 0.88rem; color: #334155;">
                                    <b>📌 Conclusión Táctica del Comportamiento Temporal SITIGPOL:</b><br/>
                                    El análisis multidimensional refleja una concentración crítica de intervenciones operativas durante los días <b>{dia_max_s}</b> y especialmente en el mes de <b>{mes_max_s}</b>.
                                </div>
                            """,
                  unsafe_allow_html=True,
              )

      with st.container(border=True):
        st.subheader(
            "📍 MAPA INTERACTIVO DE INCAUTACIONES Y PANDILLAS (SITIGPOL)"
        )
        view_state_s = pdk.ViewState(
            latitude=8.5379, longitude=-80.7821, zoom=7.5, pitch=0
        )
        layers_s = []

        if (
            ver_calor_s
            and not df_s_filtrado.empty
            and "Latitud" in df_s_filtrado.columns
            and "Longitud" in df_s_filtrado.columns
        ):
          layers_s.append(
              pdk.Layer(
                  "HeatmapLayer",
                  data=df_s_filtrado,
                  get_position="[Longitud, Latitud]",
                  radius_pixels=40,
                  intensity=1,
                  threshold=0.03,
              )
          )
        if (
            ver_puntos_s
            and not df_s_filtrado.empty
            and "Latitud" in df_s_filtrado.columns
            and "Longitud" in df_s_filtrado.columns
        ):
          layers_s.append(
              pdk.Layer(
                  "ScatterplotLayer",
                  data=df_s_filtrado,
                  get_position="[Longitud, Latitud]",
                  get_color="[30, 58, 138, 220]",
                  get_radius=450,
                  pickable=True,
                  auto_highlight=True,
              )
          )

        if (
            df_pandillas_s_filtrado is not None
            and not df_pandillas_s_filtrado.empty
            and "LAT" in df_pandillas_s_filtrado.columns
            and "LON" in df_pandillas_s_filtrado.columns
        ):
          if ver_calor_pandillas_s:
            layers_s.append(
                pdk.Layer(
                    "HeatmapLayer",
                    data=df_pandillas_s_filtrado,
                    get_position="[LON, LAT]",
                    radius_pixels=50,
                    intensity=1.5,
                    threshold=0.02,
                    color_range=[
                        [0, 100, 80, 25],
                        [0, 150, 100, 85],
                        [50, 200, 50, 150],
                        [100, 220, 0, 200],
                        [150, 100, 200, 230],
                        [128, 0, 128, 255],
                    ],
                )
            )
          if ver_puntos_pandillas_s:
            layers_s.append(
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df_pandillas_s_filtrado,
                    get_position="[LON, LAT]",
                    get_color="[34, 139, 34, 230]",
                    get_radius=500,
                    pickable=True,
                    auto_highlight=True,
                )
            )
        tooltip_html_s = (
            "<b>Provincia:</b> {Provincia} {PRO}<br/><b>Institución:</b>"
            " {Institución}<br/><b>Tipo / Pandilla:</b> {Tipo}"
            " {PAN}<br/><b>Cantidad:</b> {Cantidad_Real}<br/><b>Estatus:</b>"
            " {Relación}"
        )
        if layers_s:
          r_s = pdk.Deck(
              layers=layers_s,
              initial_view_state=view_state_s,
              map_style=pdk.map_styles.LIGHT,
              tooltip={
                  "html": tooltip_html_s,
                  "style": {
                      "backgroundColor": "#1E3A8A",
                      "color": "white",
                  },
              },
          )
          st.pydeck_chart(r_s)
        else:
          st.info(
              "Active al menos una capa geoespacial en el panel lateral para"
              " desplegar el mapa."
          )

        st.markdown("---")
        st.markdown(
            "##### 📝 DIAGNÓSTICO GEOESPACIAL Y ANÁLISIS DEL MAPA SITIGPOL"
        )

        if not df_s_filtrado.empty and "Provincia" in df_s_filtrado.columns:
          prov_top_s = (
              df_s_filtrado.groupby("Provincia")["Cantidad_Real"]
              .sum()
              .idxmax()
          )
          cant_top_s = (
              df_s_filtrado.groupby("Provincia")["Cantidad_Real"].sum().max()
          )
          pct_map_s = (
              (cant_top_s / total_cant_s * 100) if total_cant_s > 0 else 0.0
          )

          col_ms1, col_ms2 = st.columns([0.40, 0.60])
          with col_ms1:
            st.markdown(
                f"""
                            <div style="background-color: #f8fafc; border-left: 4px solid #1E3A8A; padding: 12px; border-radius: 6px; font-size: 0.88rem;">
                                <b>🗺️ Distribución Territorial SITIGPOL:</b><br/>
                                • <b>Provincia Dominante:</b> {prov_top_s}.<br/>
                                • <b>Volumen Foco Principal:</b> <b>{cant_top_s:,.2f} Unidades</b>.<br/>
                                • <b>Concentración Territorial:</b> {pct_map_s:.1f}% del total incautado.<br/>
                                • <b>Jurisdicciones Intervenidas:</b> {provincias_activas_s} Provincia(s)/Comarca(s).
                            </div>
                        """,
                unsafe_allow_html=True,
            )
          with col_ms2:
            st.markdown(
                f"""
                            <div style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 12px; border-radius: 6px; font-size: 0.88rem; color: #334155;">
                                <b>📌 Análisis de Solapamiento Geoespacial y Pandillerismo:</b><br/>
                                La superposición de las capas geoespaciales evidencia una fuerte correlación espacial entre los focos de incautaciones de drogas SITIGPOL y los puntos de presencia de pandillas. La provincia de <b>{prov_top_s}</b> se consolida como el nodo táctico de mayor actividad operativa.
                            </div>
                        """,
                unsafe_allow_html=True,
            )

      col_gs1, col_gs2 = st.columns(2)
      with col_gs1:
        with st.container(border=True):
          st.subheader("📊 TOTAL INCAUTADO POR TIPO (SITIGPOL)")
          if not df_s_filtrado.empty and "Tipo" in df_s_filtrado.columns:
            tipos_bar_disp = sorted(
                [str(x) for x in df_s_filtrado["Tipo"].dropna().unique()]
            )
            with st.expander(
                "⚙️ Configurar Filtro de Tipos en Gráfica de Barras",
                expanded=False,
            ):
              sel_tipos_bar = st.multiselect(
                  "Filtrar tipos a visualizar en gráfica de barras:",
                  options=tipos_bar_disp,
                  default=[],
                  placeholder="Choose options",
                  key="ms_tipos_bar_sitigpol",
              )
            df_bar_sub = (
                df_s_filtrado[
                    df_s_filtrado["Tipo"].astype(str).isin(sel_tipos_bar)
                ]
                if sel_tipos_bar
                else df_s_filtrado
            )

            if not df_bar_sub.empty:
              df_bar_s = (
                  df_bar_sub.groupby("Tipo")["Cantidad_Real"]
                  .sum()
                  .reset_index()
              )
              df_bar_s = df_bar_s.sort_values(
                  by="Cantidad_Real", ascending=True
              )
              fig_s_bar = px.bar(
                  df_bar_s,
                  x="Cantidad_Real",
                  y="Tipo",
                  orientation="h",
                  text_auto=".2f",
                  color="Cantidad_Real",
                  color_continuous_scale="Blues",
              )
              fig_s_bar.update_layout(
                  height=400,
                  margin={"r": 10, "t": 10, "l": 10, "b": 10},
                  xaxis_title="<b>Cantidad Real</b>",
                  yaxis_title="",
              )
              st.plotly_chart(fig_s_bar, use_container_width=True)
            else:
              st.warning("No hay datos para la selección realizada.")
          else:
            st.info("No hay datos para mostrar.")

      with col_gs2:
        with st.container(border=True):
          st.subheader("🥧 DISTRIBUCIÓN PORCENTUAL DE RELACIONES (%)")
          if not df_s_filtrado.empty and "Relación" in df_s_filtrado.columns:
            rel_pie_disp = sorted(
                [str(x) for x in df_s_filtrado["Relación"].dropna().unique()]
            )
            with st.expander(
                "⚙️ Configurar Filtro de Relaciones en Gráfico Circular",
                expanded=False,
            ):
              sel_rel_pie = st.multiselect(
                  "Filtrar relaciones a visualizar en gráfico porcentual:",
                  options=rel_pie_disp,
                  default=[],
                  placeholder="Choose options",
                  key="ms_rel_pie_sitigpol",
              )
            df_pie_sub = (
                df_s_filtrado[
                    df_s_filtrado["Relación"].astype(str).isin(sel_rel_pie)
                ]
                if sel_rel_pie
                else df_s_filtrado
            )

            if not df_pie_sub.empty:
              df_pie_s = (
                  df_pie_sub.groupby("Relación")["Cantidad_Real"]
                  .sum()
                  .reset_index()
              )
              fig_s_pie = px.pie(
                  df_pie_s,
                  names="Relación",
                  values="Cantidad_Real",
                  hole=0.45,
                  color_discrete_sequence=px.colors.sequential.Blues_r,
              )
              fig_s_pie.update_layout(
                  height=400, margin={"r": 10, "t": 10, "l": 10, "b": 10}
              )
              st.plotly_chart(fig_s_pie, use_container_width=True)
            else:
              st.warning("No hay datos para la selección realizada.")
          else:
            st.info("No hay datos para mostrar.")

    with tab_datos_s:
      st.subheader("📋 REGISTROS COMPLETOS FILTRADOS - DROGAS SITIGPOL")
      st.dataframe(df_s_filtrado, use_container_width=True)
  else:
    st.error(
        "⚠️ No se pudo cargar el archivo 'consolidado_drogas_SITIGPOL.xlsx'."
        " Genera el consolidado primero."
    )
