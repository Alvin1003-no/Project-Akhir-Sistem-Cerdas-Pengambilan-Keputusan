import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Style import *


# Untuk Judul Interface 
st.set_page_config(page_title="Project SCPK - Menentukan Lokasi Magang Terbaik" , layout="wide")
st.markdown(visualisasi(),unsafe_allow_html=True)

# Untuk Header 
st.title("Program Pengambilan Keputusan Tempat Magang Terbaik")
st.subheader("Metode SAW")
st.write(
    "Anggota Kelompok : \n"
    "1. Yohanes Herang Aji Dharma || 123240191 \n"
    "2. Alvin Andhika Putra       || 123240193"
    )

# Untuk Tab 
Tab1 , Tab2 , Tab3 , Tab4 , Tab5 , Tab6 = st.tabs([
    "Pilih Lowongan Magang" , "Alternatif" , "Skala Kriteria" ,
    "Pembobotan Kriteria" , "Hasil Alternatif Terbaik" , "Visualisasi"
])

df = pd.read_csv('merged_internships_dataset.csv')

with Tab1:

    profile_company_count = df.groupby('profile')['company'].nunique()

    # Filter profile yang memiliki 3 perusahaan atau lebih
    valid_profiles = profile_company_count[profile_company_count >= 3].index.tolist()
    valid_profiles.sort()

    options = ["Semua Lowongan"] + valid_profiles

    pilih_lowongan = st.selectbox(
    "Pilih Lowongan Magang:",
    options=options,
    key="selected_profile"
)
    
    # Tampilkan jumlah lowongan yang ditemukan
    if pilih_lowongan == "Semua Lowongan":
        filtered_df_Tab1 = df
        st.info(f"Menampilkan semua {len(filtered_df_Tab1)} lowongan magang")
    else:
        filtered_df_Tab1 = df[df['profile'] == pilih_lowongan]
        st.success(f"Menampilkan {len(filtered_df_Tab1)} lowongan untuk posisi {pilih_lowongan}")


with Tab2 :
   if st.session_state.get('selected_profile') is None or st.session_state.get('selected_profile') == "Semua Lowongan":
        st.warning("Harap Memilih Lowongan Magang Terlebih Dahulu Di tab 1")

   else:
    jumlah_lowongan_tersedia = len(filtered_df_Tab1)

    if jumlah_lowongan_tersedia > 3:
        max_slider = jumlah_lowongan_tersedia
        default_value = min(3, max_slider)  # default 3 atau jumlah yang tersedia jika kurang
        
        jumlahAlternatif = st.slider(
            "Masukkan Jumlah Alternatif : ",min_value=3,max_value=max_slider,value=default_value,step=1,disabled=False)
        
        st.session_state.jumlah_alternatif = jumlahAlternatif #Untuk menyimpan nilai kedalam session
        daftar_perusahaan = filtered_df_Tab1['company'].unique().tolist() # ambil nilai tidak duplikat dan ubah ke format py
        

        perusahaan_terpilih = st.multiselect(
            "Pilih Perusahaan untuk Alternatif",
            options=daftar_perusahaan,
            key="multiselect_perusahaan",
            max_selections=jumlahAlternatif
            )
        
        st.session_state.pilihan_perusahaan = perusahaan_terpilih.copy() #Menyimpan salinan list perusahaan yang terpilih
        # agar data session tidak berubah 
               
        # Loop alternatif 1 -> n
        for i in range(jumlahAlternatif):
            if i < len(perusahaan_terpilih):
                nilai = perusahaan_terpilih[i]
            else:
                nilai = "(belum dipilih)"
            hasilData(nilai,"Alternatif ",i+1)
            alt = nilai
       
         
    elif jumlah_lowongan_tersedia == 3: 
            st.info(f"Hanya tersedia {jumlah_lowongan_tersedia} lowongan, akan dipilih semua sebagai alternatif secara otomatis")
            
            daftar_perusahaan = filtered_df_Tab1['company'].unique().tolist()
            jumlahAlternatif = 3  # Otomatis 3
            
            st.write(f"Alternatif yang tersedia:")
            
            pilihan_perusahaan = []
            for i, perusahaan in enumerate(daftar_perusahaan): # i=0 A1 , i=1 A2
                hasilDataBaru(perusahaan, "Alternatif ", i+1)
                pilihan_perusahaan.append(perusahaan)
            
            # Simpan ke session state
            st.session_state.pilihan_perusahaan = pilihan_perusahaan
            st.session_state.jumlah_alternatif = jumlahAlternatif
            
with Tab3:
    selected_profile = st.session_state.get('selected_profile')
    pilihan_perusahaan = st.session_state.get('pilihan_perusahaan')
    
    if selected_profile is None or selected_profile == "Semua Lowongan":
        st.warning("Harap Memilih Lowongan Magang Terlebih Dahulu Di Tab 1")
    
    elif not pilihan_perusahaan or len(pilihan_perusahaan) == 0:
        st.warning("Harap Memilih Alternatif Perusahaan Terlebih Dahulu Di Tab 2")
    else:
        st.subheader("Penentuan Skala Kriteria")
        
        # Ambil data perusahaan yang dipilih
        df_alternatif = filtered_df_Tab1[filtered_df_Tab1['company'].isin(pilihan_perusahaan)]
                                                                    # apakah nilai berada dalam list
        
        # Inisialisasi session state untuk menyimpan nilai skala
        if 'skala_kriteria' not in st.session_state:
            st.session_state.skala_kriteria = {}
            # jika var skala.. belum ada di session maka buat sebagai dictionary kosong
        
        # Daftar kriteria
        kriteria_list = ["Location", "Stipend", "Duration", "Perks", "Tipe Kerja"]

        jumlah_alternatif = len(pilihan_perusahaan)

        # Header tabel: Nama Alternatif (Perusahaan)
        # Kolom pertama untuk Kriteria, sisanya untuk setiap alternatif
        lebar_kolom = [1.5] + [1] * jumlah_alternatif
            # 1.5 untuk kolom kriteria
            # 1 untuk kolom alternatif 
            # 1 kolom kriteria + sebanyak jumlah alternatif
        cols_header = st.columns(lebar_kolom)
        with cols_header[0]:
            st.markdown("**Kriteria**")
        
        # Tampilkan nama perusahaan sebagai header kolom
        # enumrate : fungsi untuk memberi index (i) dan nilai (perusahaan) secara bersamaan 
        # pilihan perusahaan : ["A","B","C"] , iterasi 1 i=0 , perusahaan="A"
        for i, perusahaan in enumerate(pilihan_perusahaan):

            # kolom [0] untuk kriiteria
            # kolom [1 -> n] untuk alternatif 1 -> n
            with cols_header[i + 1]:
                st.markdown(f"**Alternatif {i+1}**")
                # perusahaan[:20] itu buat mengambil 20 karakter nama perusahaan 
                # kalo lebih dari 20 karakter nanti di belakang ditambah (...)
                st.caption(perusahaan[:20] + "..." if len(perusahaan) > 20 else perusahaan)
        
        
        # Looping untuk setiap kriteria
        for kriteria in kriteria_list:
            # Buat kolom dinamis untuk setiap baris kriteria
            lebar_kolom = [1.5] + [1] * jumlah_alternatif
            cols = st.columns(lebar_kolom)
            
            with cols[0]:
                with st.expander(f"{kriteria}"):
                    for j, perusahaan in enumerate(pilihan_perusahaan):
                        row = df_alternatif[df_alternatif['company'] == perusahaan]
                        if not row.empty:
                            if kriteria == "Location":
                                nilai = row['Location'].iloc[0]
                            elif kriteria == "Stipend":
                                nilai = row['Stipend'].iloc[0]
                            elif kriteria == "Duration":
                                nilai = row['Duration'].iloc[0]
                            elif kriteria == "Perks":
                                nilai = row['Perks'].iloc[0]
                            elif kriteria == "Tipe Kerja":
                                lokasi = row['Location'].iloc[0]
                                nilai = "WFH" if "Work from home" in str(lokasi) else ("WFO" if str(lokasi) not in ["N/A", "Not Available"] else "Tidak diketahui")
                            else:
                                nilai = "N/A"
                            st.write(f"**{perusahaan}:** {nilai}")
            
            # Input skala untuk setiap alternatif (1-10)
            for j, perusahaan in enumerate(pilihan_perusahaan):
                with cols[j + 1]:
                    skala_kriteria = f"skala_{kriteria}_{perusahaan}" # Untuk membedakan setiap input
                    default_value = st.session_state.skala_kriteria.get(skala_kriteria, 1)
                    
                    skala = st.number_input(
                        f"Skala {kriteria} - {perusahaan}",
                        min_value=1,
                        max_value=10,
                        value=int(default_value),
                        step=1,
                        key=skala_kriteria,
                        label_visibility="collapsed" # Hide label agar rapi
                    )
                    st.session_state.skala_kriteria[skala_kriteria] = skala
            
with Tab4:
    selected_profile = st.session_state.get('selected_profile')
    pilihan_perusahaan = st.session_state.get('pilihan_perusahaan')
    skala_kriteria = st.session_state.get('skala_kriteria', {})
    
    if selected_profile is None or selected_profile == "Semua Lowongan":
        st.warning("Harap Memilih Lowongan Magang Terlebih Dahulu Di Tab 1")
    
    elif not pilihan_perusahaan or len(pilihan_perusahaan) == 0:
        st.warning("Harap Memilih Alternatif Perusahaan Terlebih Dahulu Di Tab 2")
    
    elif not skala_kriteria:
        st.warning("Harap Mengisi Skala Kriteria Terlebih Dahulu Di Tab 3")
    
    else:
        st.caption("Atur bobot untuk setiap kriteria (total harus 100%)")
        
        # Daftar kriteria beserta jenisnya (Cost/Benefit)
        kriteria_list = [
            {"nama": "Location", "jenis": "Cost"},
            {"nama": "Stipend", "jenis": "Benefit"},
            {"nama": "Duration", "jenis": "Benefit"},
            {"nama": "Perks", "jenis": "Benefit"},
            {"nama": "Tipe Kerja", "jenis": "Benefit"}
        ]
        
        # Inisialisasi session state untuk bobot
        if 'bobot_kriteria' not in st.session_state:
            st.session_state.bobot_kriteria = {}
        
        # Tampilkan input bobot untuk setiap kriteria
        for kriteria in kriteria_list:
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col1:
                if kriteria["jenis"] == "Cost":
                    st.markdown(f"**{kriteria['nama']}**")
                else:
                    st.markdown(f"**{kriteria['nama']}**")
            
            with col2:
                key_bobot = f"bobot_{kriteria['nama']}"
                default_bobot = st.session_state.bobot_kriteria.get(key_bobot, 0)
                
                bobot = st.number_input(
                    f"Bobot {kriteria['nama']}",
                    min_value=0,
                    max_value=100,
                    value=int(default_bobot),
                    step=5,
                    key=key_bobot,
                    label_visibility="collapsed"
                )
                st.session_state.bobot_kriteria[key_bobot] = bobot
            
            with col3:
                # Kolom keterangan (read-only / disabled)
                if kriteria["jenis"] == "Cost":
                    st.text_input(
                        "Keterangan",
                        value="Semakin kecil skala, semakin baik (Cost)",
                        disabled=True,
                        key=f"ket_{kriteria['nama']}",
                        label_visibility="collapsed"
                    )
                else:
                    st.text_input(
                        "Keterangan",
                        value="Semakin besar skala, semakin baik (Benefit)",
                        disabled=True,
                        key=f"ket_{kriteria['nama']}",
                        label_visibility="collapsed"
                    )
        
        st.divider()
        
        # Hitung total bobot
        total_bobot = sum(st.session_state.bobot_kriteria.values())
        
        col_total1, col_total2, col_total3 = st.columns([1, 1, 2])
        # Lebar Kolom
        with col_total1:
            st.markdown("**Total Bobot:**")
        with col_total2:
            if total_bobot == 100:
                st.success(f"{total_bobot}% ")
            elif total_bobot < 100:
                st.warning(f"{total_bobot}% (Kurang {100 - total_bobot}%)")
            else:
                st.error(f"{total_bobot}% (Kelebihan {total_bobot - 100}%)")        

with Tab5:
    selected_profile = st.session_state.get('selected_profile')
    pilihan_perusahaan = st.session_state.get('pilihan_perusahaan')
    skala_kriteria = st.session_state.get('skala_kriteria', {})
    bobot_kriteria = st.session_state.get('bobot_kriteria', {})
    
    if selected_profile is None or selected_profile == "Semua Lowongan":
        st.warning("Harap Memilih Lowongan Magang Terlebih Dahulu Di Tab 1")
    elif not pilihan_perusahaan or len(pilihan_perusahaan) == 0:
        st.warning("Harap Memilih Alternatif Perusahaan Terlebih Dahulu Di Tab 2")
    elif not skala_kriteria:
        st.warning("Harap Mengisi Skala Kriteria Terlebih Dahulu Di Tab 3")
    elif sum(bobot_kriteria.values()) != 100:
        st.warning("Harap Mengisi Bobot Kriteria dengan total 100% Di Tab 4")
    else:
        kriteria_list = [
            {"nama": "Location", "jenis": "Cost"},
            {"nama": "Stipend", "jenis": "Benefit"},
            {"nama": "Duration", "jenis": "Benefit"},
            {"nama": "Perks", "jenis": "Benefit"},
            {"nama": "Tipe Kerja", "jenis": "Benefit"}
        ]
        
        # 1. Matriks Keputusan (X) dengan NumPy
        jumlah_alternatif = len(pilihan_perusahaan)
        jumlah_kriteria = len(kriteria_list)

        # Buat matriks X ukuran (jumlah_alternatif x jumlah_kriteria)
        X = np.zeros((jumlah_alternatif, jumlah_kriteria))

        for i, perusahaan in enumerate(pilihan_perusahaan):
            for j, kriteria in enumerate(kriteria_list):
                nama_kriteria = kriteria['nama']
                key = f"skala_{nama_kriteria}_{perusahaan}"
                X[i, j] = skala_kriteria.get(key, 0)

        # 2. Normalisasi Matriks (R) dengan NumPy (VEKTORISASI)
        R = np.zeros_like(X, dtype=float)

        for j, kriteria in enumerate(kriteria_list):
            kolom = X[:, j]  # Ambil kolom ke-j (satu kriteria)
            jenis = kriteria['jenis']
            
            if jenis == "Benefit":
                max_val = np.max(kolom)
                if max_val != 0:
                    R[:, j] = kolom / max_val
                else:
                    R[:, j] = 0
            else:  # Cost
                min_val = np.min(kolom)
                if min_val != 0:
                    R[:, j] = min_val / kolom
                    # Handle division by zero (jika ada nilai 0)
                    R[:, j] = np.where(kolom == 0, 0, R[:, j])
                else:
                    R[:, j] = 0

        # 3. Hitung Bobot dalam bentuk NumPy array
        bobot_array = np.zeros(jumlah_kriteria)
        for j, kriteria in enumerate(kriteria_list):
            nama_kriteria = kriteria['nama']
            key_bobot = f"bobot_{nama_kriteria}"
            bobot_array[j] = bobot_kriteria.get(key_bobot, 0) / 100

        # 4. Hitung Nilai Preferensi (V) dengan perkalian matriks
        # V = R × bobot (perkalian baris dengan bobot)
        nilai_preferensi = np.sum(R * bobot_array, axis=1)  

        # 5. Buat hasil_saw dengan detail perhitungan 
        hasil_saw = []
        for i, perusahaan in enumerate(pilihan_perusahaan):
            total_nilai = nilai_preferensi[i]
            detail_perhitungan = {}
            
            for j, kriteria in enumerate(kriteria_list):
                nama_kriteria = kriteria['nama']
                detail_perhitungan[nama_kriteria] = {
                    'nilai_normalisasi': round(R[i, j], 4),
                    'bobot': round(bobot_array[j], 4),
                    'kontribusi': round(R[i, j] * bobot_array[j], 4)
                }
            
            hasil_saw.append({
                'Company Name': perusahaan,
                'Hasil Perhitungan': round(total_nilai, 4),
                'Detail': detail_perhitungan
            })

        # 6. Untuk Matriks Normalisasi (ke df_normalisasi) 
        df_normalisasi = pd.DataFrame(
            R.round(4),  # Bulatkan ke 4 desimal
            index=pilihan_perusahaan,
            columns=[k['nama'] for k in kriteria_list]
        )
        # Tambahkan baris jenis kriteria
        df_normalisasi.loc['Jenis'] = [k['jenis'] for k in kriteria_list]
        
        df_hasil = pd.DataFrame(hasil_saw)
        df_hasil = df_hasil.sort_values(by='Hasil Perhitungan', ascending=False).reset_index(drop=True)
        df_hasil.index = df_hasil.index + 1
        df_hasil.reset_index(inplace=True)
        df_hasil.rename(columns={'index': 'Ranking'}, inplace=True)
        
        # Matriks Normalisasi
        st.subheader("Matriks Normalisasi (R)")
        st.caption("Nilai hasil normalisasi dari skala kriteria (Benefit: max→1, Cost: min→1)")
        st.dataframe(df_normalisasi, use_container_width=True)
        
        # Detail Perhitungan
        st.subheader("Detail Perhitungan Nilai Akhir (V)")
        st.caption("Nilai akhir = Σ (Nilai Normalisasi × Bobot)")
        
        for perusahaan in pilihan_perusahaan:
            data_perusahaan = next((item for item in hasil_saw if item['Company Name'] == perusahaan), None)
            if data_perusahaan:
                st.markdown(f"**Alternatif: {perusahaan}**")
                
                detail_data = []
                for kriteria in kriteria_list:
                    nama_kriteria = kriteria['nama']
                    det = data_perusahaan['Detail'][nama_kriteria]
                    detail_data.append({
                        'Kriteria': nama_kriteria,
                        'Jenis': kriteria['jenis'],
                        'Nilai Normalisasi (R)': det['nilai_normalisasi'],
                        'Bobot (W)': det['bobot'],
                        'Kontribusi (R×W)': det['kontribusi']
                    })
                
                df_detail = pd.DataFrame(detail_data)
                st.dataframe(df_detail, use_container_width=True, hide_index=True)
                st.markdown(f"**Total Nilai Alternatif: {data_perusahaan['Hasil Perhitungan']}**")
                st.divider()
        
        st.subheader("Hasil Peranki ngan Alternatif Terbaik (Metode SAW)")
        st.dataframe(df_hasil[['Ranking', 'Company Name', 'Hasil Perhitungan']], 
                     use_container_width=True, hide_index=True)
        
        # Kesimpulan
        if not df_hasil.empty:
            terbaik = df_hasil.iloc[0]
            company_terbaik = terbaik['Company Name']
            nilai_terbaik = terbaik['Hasil Perhitungan']
            
            # Ambil stipend dari dataset
            df_alternatif = filtered_df_Tab1[filtered_df_Tab1['company'] == company_terbaik]
            stipend_terbaik = "N/A"
            if not df_alternatif.empty:
                stipend_terbaik = df_alternatif['Stipend'].iloc[0]
            
            st.success(f"**Kesimpulan:** Tempat magang terbaik adalah **{company_terbaik}** dengan nilai SAW **{nilai_terbaik}** dan estimasi gaji {stipend_terbaik}")
        
        # Simpan hasil ke session_state untuk tab visualisasi
        st.session_state.df_hasil_saw = df_hasil
        st.session_state.matriks_normalisasi = df_normalisasi

with Tab6:
    selected_profile = st.session_state.get('selected_profile')
    pilihan_perusahaan = st.session_state.get('pilihan_perusahaan')
    df_hasil_saw = st.session_state.get('df_hasil_saw')
    
    if selected_profile is None or selected_profile == "Semua Lowongan":
        st.warning("Harap Memilih Lowongan Magang Terlebih Dahulu Di Tab 1")
    elif not pilihan_perusahaan or len(pilihan_perusahaan) == 0:
        st.warning("Harap Memilih Alternatif Perusahaan Terlebih Dahulu Di Tab 2")
    elif df_hasil_saw is None or df_hasil_saw.empty:
        st.warning("Harap Menyelesaikan Perhitungan Di Tab 5 Terlebih Dahulu")
    else:
        st.subheader("Visualisasi Hasil Perhitungan SAW")
        import matplotlib.pyplot as plt
        
        df_plot = df_hasil_saw.sort_values('Hasil Perhitungan', ascending=True)
        companies = df_plot['Company Name'].tolist()
        scores = df_plot['Hasil Perhitungan'].tolist()
        
        # Membuat 2 kolom untuk baris pertama
        col1, col2 = st.columns(2)
        
        with col1:
            # 1. Grafik (Line Chart)
            st.markdown("**1. Grafik (Line Chart)**")
            fig1, ax1 = plt.subplots(figsize=(5, 4))
            ax1.plot(df_hasil_saw['Company Name'], df_hasil_saw['Hasil Perhitungan'], marker='o', linestyle='-', color='b')
            ax1.set_xlabel('Company Name')
            ax1.set_ylabel('Hasil Perhitungan')
            ax1.set_title('Grafik Hasil Perhitungan SAW')
            ax1.grid(True, linestyle='--', alpha=0.7)
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig1, use_container_width=True)
            st.caption("Keterangan: Line chart menunjukkan perbandingan nilai SAW antar perusahaan. Titik tertinggi adalah yang terbaik.")

        with col2:
            # 2. Bar Chart (Horizontal)
            st.markdown("**2. Bar Chart (Horizontal)**")
            fig2, ax2 = plt.subplots(figsize=(5, 4))
            ax2.barh(companies, scores, color='skyblue')
            ax2.set_xlabel('Hasil Perhitungan')
            ax2.set_ylabel('Company Name')
            ax2.set_title('Bar Chart Hasil Perhitungan SAW (Horizontal)')
            st.pyplot(fig2, use_container_width=True)
            st.caption("Keterangan: Bar chart horizontal memudahkan membaca nama perusahaan. Batang terpanjang adalah pilihan terbaik.")

        st.divider() # Garis pemisah antar baris
        
        # Membuat 2 kolom untuk baris kedua
        col3, col4 = st.columns(2)
        
        with col3:
            # 3. Bar Chart (Vertikal)
            st.markdown("**3. Bar Chart (Vertikal)**")
            fig3, ax3 = plt.subplots(figsize=(5, 4))
            ax3.bar(companies, scores, color='lightgreen')
            ax3.set_xlabel('Company Name')
            ax3.set_ylabel('Hasil Perhitungan')
            ax3.set_title('Bar Chart Hasil Perhitungan SAW (Vertikal)')
            ax3.set_xticks(range(len(companies)))
            ax3.set_xticklabels(companies, rotation=45, ha='right')
            st.pyplot(fig3, use_container_width=True)
            st.caption("Keterangan: Bar chart vertikal membandingkan tinggi batang. Semakin tinggi batang, semakin direkomendasikan.")

        with col4:
            # 4. Pie Chart
            st.markdown("**4. Pie Chart**")
            fig4, ax4 = plt.subplots(figsize=(5, 4))
            ax4.pie(df_hasil_saw['Hasil Perhitungan'], labels=df_hasil_saw['Company Name'], autopct='%1.1f%%', startangle=90)
            ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax4.set_title('Pie Chart Proporsi Hasil Perhitungan SAW')
            st.pyplot(fig4, use_container_width=True)
            st.caption("Keterangan: Pie chart menampilkan persentase proporsi nilai SAW masing-masing perusahaan terhadap total.")
