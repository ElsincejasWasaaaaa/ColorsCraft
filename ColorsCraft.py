import streamlit as st
import pandas as pd
import os

# Función para cargar datos desde CSV con verificación de archivo
def cargar_datos(nombre_archivo, columnas):
    if os.path.exists(nombre_archivo):
        return pd.read_csv(nombre_archivo)
    return pd.DataFrame(columns=columnas)

# Función para guardar datos en CSV
def guardar_datos(df, nombre_archivo):
    df.to_csv(nombre_archivo, index=False)

# Cargar inventario y RUCs
df_inventario = cargar_datos("inventario.csv", ["id", "nombre", "tipo", "cantidad", "precio"])
df_ruc = cargar_datos("rucs.csv", ["RUC", "Empresa"])

st.title("📦 Inventario y Empresas 🎨")

# Barra lateral para navegación
opcion = st.sidebar.radio("Selecciona una opción", ["Agregar Producto", "Ver Inventario", "Agregar RUC", "Ver Lista de RUCs"])

if opcion == "Agregar Producto":
    st.header("➕ Agregar Nuevo Producto")
    with st.form("nuevo_producto"):
        nombre = st.text_input("Nombre del producto")
        tipo = st.selectbox("Tipo", ["Latex", "Acrílica", "Esmalte"])
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio = st.number_input("Precio", min_value=0.01, step=0.01)
        submitted = st.form_submit_button("Agregar Producto")

        if submitted:
            nuevo_id = df_inventario["id"].max() + 1 if not df_inventario.empty else 1
            nuevo_producto = pd.DataFrame([{ "id": nuevo_id, "nombre": nombre, "tipo": tipo, "cantidad": cantidad, "precio": precio }])
            df_inventario = pd.concat([df_inventario, nuevo_producto], ignore_index=True)
            guardar_datos(df_inventario, "inventario.csv")
            st.toast("✅ Producto agregado exitosamente")
            st.rerun()

elif opcion == "Ver Inventario":
    st.header("📋 Lista de Productos")
    tipo_seleccionado = st.sidebar.selectbox("Filtrar por tipo de pintura", ["Todos", "Latex", "Acrílica", "Esmalte"])
    df_filtrado = df_inventario if tipo_seleccionado == "Todos" else df_inventario[df_inventario["tipo"] == tipo_seleccionado]
    
    if not df_filtrado.empty:
        for _, row in df_filtrado.iterrows():
            with st.expander(f"{row['nombre']} ({row['tipo']}) - Cantidad: {row['cantidad']} - 💲{row['precio']}"):
                col1, col2 = st.columns(2)
                if row["cantidad"] > 0:
                    cantidad_restar = col1.number_input("Restar cantidad", min_value=1, max_value=row["cantidad"], step=1, key=f"restar_{row['id']}")
                    if col1.button("➖ Restar", key=f"del_{row['id']}"):
                        df_inventario.loc[df_inventario["id"] == row["id"], "cantidad"] -= cantidad_restar
                        guardar_datos(df_inventario, "inventario.csv")
                        st.toast("✅ Cantidad restada")
                        st.rerun()
                
                if col2.button("❌ Eliminar Producto", key=f"remove_{row['id']}"):
                    df_inventario = df_inventario[df_inventario["id"] != row["id"]]
                    guardar_datos(df_inventario, "inventario.csv")
                    st.toast("🚨 Producto eliminado")
                    st.rerun()
    else:
        st.write("🚨 No hay productos en el inventario con este filtro.")

elif opcion == "Agregar RUC":
    st.header("🏢 Agregar Nuevo RUC")
    with st.form("nuevo_ruc"):
        ruc = st.text_input("Número de RUC")
        empresa = st.text_input("Nombre de la empresa")
        submitted = st.form_submit_button("Agregar RUC")

        if submitted:
            if ruc in df_ruc["RUC"].values:
                st.toast("⚠️ Este RUC ya está registrado")
            else:
                nuevo_ruc = pd.DataFrame([{ "RUC": ruc, "Empresa": empresa }])
                df_ruc = pd.concat([df_ruc, nuevo_ruc], ignore_index=True)
                guardar_datos(df_ruc, "rucs.csv")
                st.toast("✅ RUC agregado exitosamente")
                st.rerun()

elif opcion == "Ver Lista de RUCs":
    st.header("🏢 Lista de Empresas y sus RUCs")
    st.write(df_ruc if not df_ruc.empty else "🚨 No hay RUCs registrados.")
