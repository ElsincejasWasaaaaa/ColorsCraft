import streamlit as st
import pandas as pd

# Cargar datos desde CSV
def cargar_datos():
    try:
        return pd.read_csv("inventario.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["id", "nombre", "tipo", "cantidad", "precio"])

# Guardar datos en CSV
def guardar_datos(df):
    df.to_csv("inventario.csv", index=False)

st.title("📦 Inventario de Pinturas 🎨")

# Cargar inventario
df = cargar_datos()

# Barra lateral para navegación
opcion = st.sidebar.radio("Selecciona una opción", ["Agregar Producto", "Ver Inventario"])

if opcion == "Agregar Producto":
    st.header("➕ Agregar Nuevo Producto")
    
    with st.form("nuevo_producto"):
        nombre = st.text_input("Nombre del producto")
        tipo = st.selectbox("Tipo", ["Latex", "Acrílica", "Esmalte"])
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio = st.number_input("Precio", min_value=0.01, step=0.01)

        submitted = st.form_submit_button("Agregar Producto")
        if submitted:
            nuevo_id = df["id"].max() + 1 if not df.empty else 1
            nuevo_producto = pd.DataFrame([{"id": nuevo_id, "nombre": nombre, "tipo": tipo, "cantidad": cantidad, "precio": precio}])
            df = pd.concat([df, nuevo_producto], ignore_index=True)
            guardar_datos(df)
            st.rerun()

elif opcion == "Ver Inventario":
    st.header("📋 Lista de Productos")

    # Filtro de tipo de pintura
    tipo_seleccionado = st.sidebar.selectbox("Filtrar por tipo de pintura", ["Todos", "Latex", "Acrílica", "Esmalte"])
    
    if tipo_seleccionado != "Todos":
        df = df[df["tipo"] == tipo_seleccionado]

    if not df.empty:
        for i, row in df.iterrows():
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1, 3, 2, 2, 2, 2, 2, 2])
            col1.write(f"**{int(row['id'])}**")
            col2.write(row["nombre"])
            col3.write(row["tipo"])
            col4.write(f"🔢 {row['cantidad']}")
            col5.write(f"💲 {row['precio']}")
            
            # Evitar error cuando la cantidad es 0
            if row["cantidad"] > 0:
                cantidad_restar = col6.number_input(
                    f"Restar {row['nombre']}",
                    min_value=1,
                    max_value=row["cantidad"],
                    step=1,
                    key=f"restar_{row['id']}"
                )
            else:
                cantidad_restar = 0  # No permite restar más si es 0
            
            if col7.button("➖ Restar", key=f"del_{row['id']}") and row["cantidad"] > 0:
                df.loc[df["id"] == row["id"], "cantidad"] -= cantidad_restar
                guardar_datos(df)
                st.rerun()

            if col8.button("❌ Eliminar", key=f"remove_{row['id']}"):
                df = df[df["id"] != row["id"]]
                guardar_datos(df)
                st.rerun()
    else:
        st.write("🚨 No hay productos en el inventario con este filtro.")
