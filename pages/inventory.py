import pandas as pd
import streamlit as st

def load_data():
    try:
        df = pd.read_excel("Lab_Material.xlsx", engine="openpyxl")
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

df = load_data()
if df is not None:
    st.dataframe(df)
else:
    st.warning("No se pudo cargar el archivo.")

def save_data(df):
    df.to_excel("Lab_Material.xlsx", index=False, engine="openpyxl")

st.subheader('📦 Inventory Management')

if st.button("🔍 Go to Search and Filters"):
    st.switch_page("app")

# Agregar un nuevo material
st.subheader('➕ Add New Material')
with st.form(key='add_form'):
    material = st.text_input('Material')
    description = st.text_input('Description')
    container = st.text_input('Container')
    location = st.text_input('Location')
    shelf = st.text_input('Shelf')
    amount = st.number_input('Amount', min_value=0)
    keywords = st.text_input('Keywords')

    submit_button = st.form_submit_button(label='Add Material')

    if submit_button:
        new_material = pd.DataFrame({
            'Material': [material],
            'Description': [description],
            'Container': [container],
            'Location': [location],
            'Shelf': [shelf],
            'Amount': [amount],
            'Keywords': [keywords]
        })
        
        df = pd.concat([df, new_material], ignore_index=True)
        df.to_excel("Lab_Material.xlsx", index=False, engine="openpyxl")
        # Recargar los datos después de agregar el nuevo material
        df = load_data()
        st.success('Material successfully added!')

# Modificar un material existente
st.subheader('✏️ Modify Material in Stock')
material_to_modify = st.selectbox('Select the material to modify: ', df['Material'].unique())
selected_material = df[df['Material'] == material_to_modify].iloc[0]

# Formulario para modificar el material
with st.form(key='modify_form'):
    new_description = st.text_input('Description', value=selected_material['Description'])
    new_container = st.text_input('Container', value=selected_material['Container'])
    new_location = st.text_input('Location', value=selected_material['Location'])
    new_shelf = st.text_input('Shelf', value=selected_material['Shelf'])
    new_amount = st.number_input('Amount', value=selected_material['Amount'])
    new_keywords = st.text_input('Keywords', value=selected_material['Keywords'])

    # Agregar el botón de envío dentro del formulario
    submit_button = st.form_submit_button(label='Modify Material')

    if submit_button:
        df.loc[df['Material'] == material_to_modify, ['Description', 'Container', 'Location', 'Shelf', 'Amount', 'Keywords']] = [
            new_description, new_container, new_location, new_shelf, new_amount, new_keywords
        ]
        save_data(df)
        st.success('Material successfully modified!')

# Eliminar un material
st.subheader('🗑️ Delete Material')
material_to_delete = st.selectbox('Select the material to delete:', df['Material'].unique())

delete_button = st.button(label='Delete Material')

if delete_button:
    df = df[df['Material'] != material_to_delete]
    save_data(df)
    st.success('Material successfully deleted!')
