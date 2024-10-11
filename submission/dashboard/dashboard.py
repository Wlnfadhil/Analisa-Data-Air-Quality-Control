import streamlit as st

st.title('Hello, Streamlit!')
st.write('Ini adalah aplikasi Streamlit sederhana.')

# Slider untuk memilih angka
value = st.slider('Pilih angka', 0, 100, 50)
st.write('Anda memilih:', value)