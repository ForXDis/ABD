# Import library
import streamlit as st
import pandas as pd
from datetime import datetime

# Import fungsi dari config.py
# Pastikan view_customers, view_products, view_orders_with_customers, dan view_order_details_with_info
# sudah didefinisikan dan diekspor di config.py
from config import *

# Set konfigurasi halaman dashboard
st.set_page_config("Dashboard", page_icon="📊", layout="wide")

# Ambil data pelanggan (Ini dieksekusi saat program dimulai)
result_customers = view_customers()

df_customers = pd.DataFrame(result_customers, columns=[
    "customer_id", "name", "email", "phone", "address", "birthdate", 
])

# Hitung usia dari birthdate
df_customers['birthdate'] = pd.to_datetime(df_customers['birthdate'])
df_customers['Age'] = (datetime.now() - df_customers['birthdate']).dt.days // 365

# --- DEFINISI FUNGSI TAMPILAN ---

def tabelCustomers_dan_export():
    # Fungsi menampilkan tabel Customers + export CSV
    total_customers = df_customers.shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📦 Total Pelanggan", value=total_customers, delta="Semua Data")

    st.sidebar.header("Filter Rentang Usia")
    min_age = int(df_customers['Age'].min())
    max_age = int(df_customers['Age'].max())
    age_range = st.sidebar.slider(
        "Pilih Rentang Usia",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )

    filtered_df = df_customers[df_customers['Age'].between(*age_range)]

    st.markdown("### 📋 Tabel Data Pelanggan")
    
    showdata = st.multiselect(
        "Pilih Kolom Pelanggan yang Ditampilkan",
        options=filtered_df.columns,
        default=["customer_id", "name", "email", "phone", "address", "birthdate", "Age"]
    )
    
    st.dataframe(filtered_df[showdata], use_container_width=True) 

    @st.cache_data
    def convert_df_to_csv(_df):
        return _df.to_csv(index=False).encode('utf-8')
    
    csv = convert_df_to_csv(filtered_df[showdata])
    st.download_button(
        label="⬇️ Download Data Pelanggan sebagai CSV",
        data=csv,
        file_name='data_pelanggan.csv',
        mime='text/csv'
    )

# 📦 VISUALISASI PRODUCTS
def tampil_products():
    result_products = view_products()
    df_products = pd.DataFrame(result_products, columns=[
        "product_id", "name", "description", "price", "stock"
    ])

    st.markdown("## 📦 Data Produk")
    st.dataframe(df_products, use_container_width=True)

    st.markdown("### 📊 Grafik Stok Produk")
    st.bar_chart(df_products.set_index("name")["stock"])

    st.markdown("### 📈 Distribusi Harga Produk")
    st.line_chart(df_products.set_index("name")["price"])

# 🧾 VISUALISASI ORDERS
def tampil_orders():
    # Menggunakan nama fungsi yang BENAR dari config.py (view_orders_with_customers)
    result_orders = view_orders_with_customers() 
    
    # PERHATIAN: Kolom disesuaikan dengan 5 kolom yang dikembalikan oleh query SQL di config.py
    df_orders = pd.DataFrame(result_orders, columns=[
        "order_id", "order_date", "total_amount", "customer_name", "phone"
    ])

    df_orders["order_date"] = pd.to_datetime(df_orders["order_date"])

    st.markdown("## 🧾 Data Orders")
    st.dataframe(df_orders, use_container_width=True)

    st.markdown("### 📊 Total Penjualan per Tanggal")
    df_sales_per_date = df_orders.groupby(df_orders["order_date"].dt.date)["total_amount"].sum()
    st.bar_chart(df_sales_per_date)

    st.markdown("### 📈 Tren Penjualan dari Waktu ke Waktu")
    st.line_chart(df_sales_per_date)

# 📝 VISUALISASI ORDER DETAILS
def tampil_order_details():
    result_details = view_order_details_with_info() 
    
    # PERHATIAN: Kolom disesuaikan dengan 12 kolom yang dikembalikan oleh query SQL di config.py
    df_details = pd.DataFrame(result_details, columns=[
        "order_detail_id", "order_id", "order_date", 
        "customer_id", "customer_name", "product_id", 
        "product_name", "unit_price", "quantity", 
        "subtotal", "order_total", "phone"
    ])

    df_details["order_date"] = pd.to_datetime(df_details["order_date"])

    st.markdown("## 📝 Data Detail Transaksi")

    # Tampilkan Metrik Ringkasan
    total_revenue = df_details['order_total'].drop_duplicates().sum() # Ambil total unik untuk total_amount
    total_items_sold = df_details['quantity'].sum()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="💰 Total Pendapatan", value=f"Rp {total_revenue:,.0f}")
    with col2:
        st.metric(label="🛒 Total Produk Terjual", value=f"{total_items_sold:,.0f} unit")
        
    st.markdown("### 📋 Tabel Rinci Order Detail")
    st.dataframe(df_details, use_container_width=True)

    st.markdown("### 📈 Penjualan berdasarkan Produk (Berdasarkan Subtotal)")
    df_product_sales = df_details.groupby("product_name")["subtotal"].sum().sort_values(ascending=False)
    st.bar_chart(df_product_sales)

# --- LOGIKA UTAMA: PEMILIHAN TAMPILAN ---

st.sidebar.markdown("---")
st.sidebar.header("Pilih Tampilan Data")
st.sidebar.markdown("---") 

pilihan_tabel = st.sidebar.radio(
    "Tabel yang Ingin Ditampilkan:",
    ("Pelanggan", "Orders", "Produk", "Order Detail") 
)

# Memanggil fungsi yang sesuai dengan pilihan pengguna
if pilihan_tabel == "Pelanggan":
    st.title("👥 Dashboard Pelanggan")
    tabelCustomers_dan_export()
elif pilihan_tabel == "Orders":
    st.title("🧾 Dashboard Orders")
    tampil_orders()
elif pilihan_tabel == "Produk":
    st.title("📦 Dashboard Produk")
    tampil_products()
elif pilihan_tabel == "Order Detail":
    st.title("📝 Dashboard Order Detail")
    tampil_order_details()