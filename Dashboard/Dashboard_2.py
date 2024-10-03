#--- Mengimpor modul yang diperlukan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur gaya visual seaborn
sns.set(style='dark')

#--- Mendefinisikan fungsi untuk analisis data
def analisis_rental_musim(df):  # Fungsi untuk menganalisis data berdasarkan "season"
    rental_per_season = df.groupby(by="season").cnt.nunique().reset_index()
    rental_per_season.rename(columns={"cnt": "jumlah_pelanggan"}, inplace=True)
    return rental_per_season

def analisis_rental_jam(df):  # Fungsi untuk menganalisis data berdasarkan "hr"
    rental_per_jam = df.groupby(by="hr").cnt.nunique().reset_index()
    rental_per_jam.rename(columns={"cnt": "jumlah_pelanggan"}, inplace=True)
    return rental_per_jam

def analisis_berdasarkan_cuaca(df):  # Fungsi untuk menganalisis data berdasarkan "weathersit"
    cuaca_analisis = df.groupby(by="weathersit").agg({
        "instant": "nunique",
        "cnt": "sum"
    }).reset_index()
    return cuaca_analisis

#--- Memuat data dari file CSV
day_df = pd.read_csv(r"Dashboard\day_data.csv")
hour_df = pd.read_csv(r"Dashboard\hour_data.csv")

#--- Menggunakan fungsi untuk menghasilkan analisis
favorit_season = analisis_rental_musim(day_df)
favorit_jam = analisis_rental_jam(hour_df)
favorit_cuaca = analisis_berdasarkan_cuaca(day_df)

#--- Menampilkan judul Dashboard
st.header('Dashboard Penyewaan Sepeda :bicyclist::star2:')
st.subheader("Statistik :1234:")

#--- Membuat panel samping (sidebar)
with st.sidebar:
    st.subheader("Latar Belakang")
    st.write(
        """
        Sistem penyewaan sepeda adalah generasi baru dari penyewaan sepeda tradisional di mana seluruh proses, mulai dari pendaftaran anggota, penyewaan, hingga pengembalian, telah menjadi otomatis. 
        Dengan sistem ini, pengguna dapat dengan mudah menyewa sepeda dari lokasi tertentu dan mengembalikannya di lokasi lain. Saat ini, terdapat sekitar 500 program penyewaan sepeda di seluruh dunia, 
        yang terdiri dari lebih dari 500 ribu sepeda. Saat ini, terdapat minat yang besar terhadap sistem ini karena peran pentingnya dalam isu lalu lintas, lingkungan, dan kesehatan.

        Selain aplikasi dunia nyata yang menarik dari sistem penyewaan sepeda, karakteristik data yang dihasilkan oleh sistem ini menjadikannya menarik untuk penelitian. 
        Berbeda dengan layanan transportasi lain seperti bus atau kereta bawah tanah, durasi perjalanan, waktu keberangkatan, dan lokasi kedatangan tercatat dengan jelas dalam sistem ini. 
        Fitur ini mengubah sistem penyewaan sepeda menjadi jaringan sensor virtual yang dapat digunakan untuk mendeteksi mobilitas di kota. 
        Oleh karena itu, diharapkan bahwa sebagian besar peristiwa penting di kota dapat terdeteksi melalui pemantauan data ini.
        """
    )

#--- Menampilkan kolom untuk statistik penyewaan
col1, col2, col3 = st.columns(3)

#--- Kolom untuk total penyewaan
with col1:
    total_rental = day_df['cnt'].sum()
    st.metric("Total Penyewaan", value=total_rental)

#--- Kolom untuk penyewaan pelanggan yang terdaftar
with col2:
    rental_member = day_df['registered'].sum()
    st.metric("Penyewaan Anggota", value=rental_member)

#--- Kolom untuk penyewaan pelanggan non-terdaftar
with col3:
    rental_casual = day_df['casual'].sum()
    st.metric("Penyewaan Non-Anggota", value=rental_casual)

#--- Grafik penyewaan berdasarkan musim
st.subheader("Musim Favorit Pelanggan :sunny: :cloud:")
fig, ax = plt.subplots(figsize=(20, 10))

colors_ = ["#FFFF00",  "#FFA500","#FF0000", "#D3D3D3"]

sns.barplot(
    y="jumlah_pelanggan",
    x="season",
    data=favorit_season.sort_values(by="jumlah_pelanggan", ascending=False),
    palette=colors_,
    ax=ax
)
ax.set_title("Jumlah Pelanggan berdasarkan Musim", loc="center", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

st.subheader("Deskripsi")
st.write(
    """
    1: Musim Semi
    2: Musim Panas
    3: Musim Gugur
    4: Musim Dingin 
    """
)

#--- Grafik penyewaan berdasarkan jam
st.subheader("Jam Favorit dan Tidak Favorit Pelanggan :smile::triumph:")
fig, ax = plt.subplots(figsize=(20, 10))

colors_ = ["#D3D3D3"] * 20
colors_[17] = "#FF0000"  # Warna khusus untuk jam favorit

sns.barplot(
    y="jumlah_pelanggan",
    x="hr",
    data=favorit_jam.sort_values(by="jumlah_pelanggan", ascending=False),
    palette=colors_,
    ax=ax
)
ax.set_title("Jumlah Pelanggan berdasarkan Jam", loc="center", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

#--- Grafik penyewaan casual dan registered
st.subheader("Pola Penyewaan Sepeda Pengguna Casual dan Registered")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=day_df, x='dteday', y='casual', label='Casual')
sns.lineplot(data=day_df, x='dteday', y='registered', label='Registered')
plt.title('Pola Penyewaan Sepeda Pengguna Casual dan Registered')
plt.legend()
plt.show()
st.pyplot(fig)