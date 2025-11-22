import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Selamat Datang Di HOK")
st.write("Ini adalah halaman utama dari aplikasi dashboard HOK.")

data = pd.DataFrame(data={
    "Pemain": ["orghita", "selaluPth", "amrkan"],
    "Pendapatan": [1000000, 2000000, 3000000]
})

st.subheader("Data Pendapatan Pemain")
st.dataframe(data)

st.bar_chart(data.set_index(keys="Pemain"))

st.line_chart(data.set_index(keys="Pemain"))

fig, ax = plt.subplots()
ax.bar(data["Pemain"], data["Pendapatan"], color="green")
ax.set_ylabel("Hasil(juta)")
st.pyplot(fig)

tipe = st.selectbox("Pilih jenis grafik:", ["Bar", "Pie"])

if tipe == "Bar":
    st.bar_chart(data.set_index("Pemain"))
else:
    fig, ax = plt.subplots()
    ax.pie(data["Pendapatan"], labels=data["Pemain"], autopct="%1.1f%%")
    st.pyplot(fig)

nilai = st.slider("Tampilkan data dengan Pendapatan minimum:", 0, 150000, 5000000)
st.dataframe(data[data["Pendapatan"] >= nilai])


st.title("Sebaran Lokasi Pemain HOK")

data_peta = pd.DataFrame({
    'lokasi': ['Balikpapan', 'Samboja', 'Mahakam'],
    'lat': [-1.27, -1.10, -0.50],
    'lon': [116.83, 117.00, 117.25]
})

st.map(data_peta)

#Dashboard Pemain HOK
st.title("Dashboard Pemain HOK")

data = pd.DataFrame({
    "Pemain": ["orghita", "whitenig", "amerika"],
    "Pendapatan": [1000000, 2000000, 3000000],
    "Target": [1500000, 1000000, 3000000]
})

pemain = st.selectbox("Pilih pemain:", data["Pemain"])
row = data[data["Pemain"] == pemain].iloc[0]

st.metric("Pendapatan Saat Ini", f"{row['Pendapatan']} juta", delta=row['Pendapatan'] - row['Target'])
st.progress(row['Pendapatan'] / row['Target'])

fig, ax = plt.subplots()
ax.bar(data["Pemain"], data["Pendapatan"], color="green")
ax.set_ylabel("Pendapatan (juta)")
st.pyplot(fig)

