import streamlit as st

# Title of the application
st.title('Drawing to Gaming')

# Sidebar for user inputs
st.sidebar.header('User Input')

# Upload drawing image
uploaded_file = st.sidebar.file_uploader('Choose an image...', type=['png', 'jpg', 'jpeg'])

# Display uploaded image
if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

# Process the uploaded image
if st.sidebar.button('Convert Drawing to Game'):
    if uploaded_file is not None:
        # Here, the logic to convert drawing to gaming element would go.
        st.sidebar.success('Image converted to gaming element!')
    else:
        st.sidebar.error('Please upload an image first.')