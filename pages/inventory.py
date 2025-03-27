import pandas as pd
import streamlit as st

# Función para cargar los datos desde el archivo Excel
def load_data():
    df = pd.read_excel("Lab_Material.xlsx", engine="openpyxl")
    return df

# Cargar los datos
st.title('🔬404 Material Management - VIBES🛰️')
df = load_data()

# Mostrar los datos
st.dataframe(df)

# Agregar un nuevo material
st.subheader('Add New Material')
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
st.subheader('Modify Material in Stock')
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
        # Actualizar los valores en el DataFrame
        df.loc[df['Material'] == material_to_modify, 'Description'] = new_description
        df.loc[df['Material'] == material_to_modify, 'Container'] = new_container
        df.loc[df['Material'] == material_to_modify, 'Location'] = new_location
        df.loc[df['Material'] == material_to_modify, 'Shelf'] = new_shelf
        df.loc[df['Material'] == material_to_modify, 'Amount'] = new_amount
        df.loc[df['Material'] == material_to_modify, 'Keywords'] = new_keywords

        # Guardar los cambios en el archivo Excel
        df.to_excel("Lab_Material.xlsx", index=False, engine="openpyxl")
        # Recargar los datos después de modificar el nuevo material
        df = load_data()
        st.success('Material successfully modified!')

# Eliminar un material
st.subheader('Delete Material in Stock')
material_to_delete = st.selectbox('Select the material to delete', df['Material'].unique())

delete_button = st.button(label='Delete Material')

if delete_button:
    df = df[df['Material'] != material_to_delete]
    df.to_excel("Lab_Material.xlsx", index=False, engine="openpyxl")
    # Recargar los datos después de eliminar el nuevo material
    df = load_data()
    st.success('Material successfully deleted!')
