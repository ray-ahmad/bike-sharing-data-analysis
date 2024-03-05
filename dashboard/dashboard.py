import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Bike Sharing Data Analysis by Rayhan Ahmad")

if os.path.exists("../data"):
    day_df = pd.read_csv("../data/day.csv")
    hour_df = pd.read_csv("../data/hour.csv")
else:
    day_df = pd.read_csv("./data/day.csv")
    hour_df = pd.read_csv("./data/hour.csv")

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://awsimages.detik.net.id/community/media/visual/2023/02/20/program-bangkit-2023.jpeg")
    st.title('Bike Sharing Data Analysis')
    st.write("""
                - **Nama:** Rayhan Ahmad Rizalullah
                - **Email:** ray.ahmdr@gmail.com
                - **ID Dicoding:** rayhanahmadr
                - **Bangkit ID:** M119D4KY1813
            """)
    year = st.selectbox(
                label="Pilih tahun",
                options=(2011,2012)
            )
    year = 0 if year == 2011 else 1

day_df = day_df[day_df['yr'] == year]
hour_df = hour_df[hour_df['yr'] == year]

with st.container():
    st.title('Apa hari dengan penyewa casual terbanyak?')
    
    nama_hari = {
        0: 'Minggu',
        1: 'Senin',
        2: 'Selasa',
        3: 'Rabu',
        4: 'Kamis',
        5: 'Jumat',
        6: 'Sabtu'
    }

    group_weekday = day_df.groupby(by="weekday")
    days = group_weekday.weekday.first().tolist()

    registered_counts = group_weekday.registered.sum().tolist()
    casual_counts = group_weekday.casual.sum().tolist()

    fig, ax = plt.subplots()
    # Membuat stacked bar chart
    ax.bar([nama_hari[day] for day in days], casual_counts, label='Casual', color='lightcoral')
    ax.bar([nama_hari[day] for day in days], registered_counts, bottom=casual_counts, label='Registered', color='lightblue')

    ax.set_xlabel('Hari')
    ax.set_ylabel('Jumlah')
    ax.set_title('Stacked Bar Chart Peminjaman Sepeda per Hari dan Jenis Pengguna')
    ax.legend(loc='lower right')

    st.pyplot(fig)

    with st.expander("Lihat penjelasan..."):
        st.write("""Berdasarkan stacked bar chart di atas, hari Sabtu dan Minggu memiliki jumlah penyewa casual yang paling tinggi dibandingkan dengan hari-hari lainnya. Oleh karena itu, strategi pemasaran dan promosi yang tepat dapat diimplementasikan untuk meningkatkan jumlah penyewa terdaftar pada hari-hari ini. Misalnya, dengan memberikan diskon khusus bagi penyewa terdaftar pada akhir pekan, mengadakan acara khusus atau tur bagi anggota terdaftar pada hari Sabtu atau Minggu, atau menyediakan penawaran paket langganan yang menarik untuk mendorong lebih banyak orang untuk mendaftar sebagai anggota tetap.""")

with st.container():
    st.title('Apa musim dengan penyewa sepeda paling sedikit?')

    # Membuat kamus untuk memetakan angka musim ke label yang sesuai
    nama_musim = {
        1: 'Musim Semi',
        2: 'Musim Panas',
        3: 'Musim Gugur',
        4: 'Musim Dingin'
    }

    # Menghitung rata-rata jumlah peminjaman sepeda berdasarkan musim
    mean_cnt_per_season = day_df.groupby(by="season").cnt.mean()

    # Mengganti indeks angka musim dengan label musim yang sesuai
    mean_cnt_per_season.index = mean_cnt_per_season.index.map(nama_musim)

    # Data yang akan diplot
    labels = mean_cnt_per_season.index
    sizes = mean_cnt_per_season.values
    fig, ax = plt.subplots()
    colors = ['lightsalmon', 'lightcoral', 'lightgreen','lightblue']

    # Membuat pie chart
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.2f%%', startangle=140)

    # Menambahkan judul
    ax.set_title('Persentase Peminjaman Sepeda berdasarkan Musim')

    st.pyplot(fig)

    with st.expander("Lihat penjelasan..."):
        st.write("""Berdasarkan pie chart di atas, musim semi adalah musim yang mempunyai jumlah penyewa sepeda yang paling sedikit dibandingkan musim lain. Oleh karena itu, kampanye promosi dan pemasaran dapat dilakukan pada musim ini dengan fokus pada memperkenalkan penawaran khusus, diskon, atau paket promosi untuk menarik lebih banyak pelanggan. Misalnya, penawaran diskon spesial atau program referensi teman (referral) kepada pelanggan yang menyewa sepeda selama musim semi, atau mengadakan acara-acara promosi khusus yang berorientasi pada musim semi seperti tur bersepeda atau festival sepeda.""")

with st.container():
    st.title('Bagaimana tren peminjaman sepeda berubah sepanjang hari dari pagi hingga malam?')

    # Membuat fungsi untuk mengkategorikan waktu
    def categorize_time(hour):
        if hour >= 5 and hour < 11:
            return "Pagi"
        elif hour >= 11 and hour < 15:
            return "Siang"
        elif hour >= 15 and hour < 18:
            return "Sore"
        else:
            return "Malam"

    # Menambahkan kolom "time_category" yang berisi kategori waktu
    hour_df['time_category'] = hour_df['hr'].apply(categorize_time)

    # Melakukan groupby berdasarkan kategori waktu dan menghitung jumlah peminjaman sepeda
    time_category_counts = hour_df.groupby('time_category')['cnt'].mean()

    fig, ax = plt.subplots()
    ax.plot(time_category_counts.index, time_category_counts.values, marker='o')

    # Menambahkan label dan judul
    ax.set_xlabel('Waktu')
    ax.set_ylabel('Rata-rata Peminjaman Sepeda')
    ax.set_title('Tren Peminjaman Sepeda per Waktu')

    # Menampilkan grid
    plt.grid(True)

    st.pyplot(fig)

    with st.expander("Lihat penjelasan..."):
        st.write("""Berdasarkan pie chart di atas, musim semi adalah musim yang mempunyai jumlah penyewa sepeda yang paling sedikit dibandingkan musim lain. Oleh karena itu, kampanye promosi dan pemasaran dapat dilakukan pada musim ini dengan fokus pada memperkenalkan penawaran khusus, diskon, atau paket promosi untuk menarik lebih banyak pelanggan. Misalnya, penawaran diskon spesial atau program referensi teman (referral) kepada pelanggan yang menyewa sepeda selama musim semi, atau mengadakan acara-acara promosi khusus yang berorientasi pada musim semi seperti tur bersepeda atau festival sepeda.""")