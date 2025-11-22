import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# KONFIGURASI HALAMAN & JUDUL 
st.set_page_config(
    page_title="Dashboard Lingkungan Kaltim",
    page_icon="🌿",
    layout="centered"
)

# Menambahkan Gambar 
st.image(
    "https://images.unsplash.com/photo-1519337265831-281ec6cc8514?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
    caption="Hutan Mangrove & Konservasi Alam",
    use_container_width=True
)

st.title("🌿 Dashboard Monitoring Penanaman Mangrove")

# Deskripsi Singkat
st.markdown("""
Aplikasi ini menampilkan data visualisasi **10 lokasi kampanye** penanaman mangrove di wilayah Kalimantan Timur. 
Data mencakup jumlah pohon yang ditanam dan total donasi yang terkumpul.
""")

st.divider()

#  DATA 
data = pd.DataFrame({
    'Lokasi': [
        'Balikpapan Timur', 'Balikpapan Barat', 'Samboja', 'Muara Badak', 
        'Anggana', 'Sangatta', 'Bontang', 'Penajam', 'Tanah Grogot', 'Tenggarong'
    ],
    'Jumlah Pohon': [1200, 950, 1500, 1100, 1300, 800, 1600, 900, 750, 1050],
    'Donasi (Juta)': [120, 95, 150, 110, 130, 80, 160, 90, 75, 105],
    # Koordinat (Latitude & Longitude) untuk Peta
    'lat': [-1.216, -1.245, -1.035, -0.321, -0.554, 0.502, 0.133, -1.300, -1.895, -0.400],
    'lon': [116.936, 116.802, 117.026, 117.445, 117.450, 117.533, 117.470, 116.700, 116.210, 116.980]
})

# Menampilkan Data Mentah 
with st.expander("Lihat Data Mentah"):
    st.dataframe(data)


# PILIHAN VISUALISASI (Dropdown)
st.subheader("📊 Analisis Visualisasi")

# Dropdown Menu
pilihan = st.selectbox(
    "Pilih Jenis Visualisasi:",
    ["Bar Chart", "Line Chart", "Area Chart", "Pie Chart", "Map"]
)


# LOGIKA TAMPILAN BERDASARKAN PILIHAN

if pilihan == "Bar Chart":
    st.write("### Perbandingan Jumlah Pohon per Lokasi")
    chart_data = data.set_index("Lokasi")
    st.bar_chart(chart_data["Jumlah Pohon"], color="#2ecc71")

elif pilihan == "Line Chart":
    st.write("### Tren Donasi di Berbagai Lokasi")
    chart_data = data.set_index("Lokasi")
    st.line_chart(chart_data["Donasi (Juta)"], color="#3498db")

elif pilihan == "Area Chart":
    st.write("### Akumulasi Area Tanam (Pohon)")
    chart_data = data.set_index("Lokasi")
    st.area_chart(chart_data["Jumlah Pohon"], color="#e67e22")

elif pilihan == "Pie Chart":
    st.write("### Proporsi Donasi per Lokasi")
    fig, ax = plt.subplots()
    ax.pie(
        data["Donasi (Juta)"], 
        labels=data["Lokasi"], 
        autopct='%1.1f%%', 
        startangle=90,
        colors=plt.cm.Paired.colors
    )
    ax.axis('equal')  
    st.pyplot(fig)

elif pilihan == "Map":
    st.write("### Peta Sebaran Lokasi Penanaman")
    st.map(data, zoom=7)
