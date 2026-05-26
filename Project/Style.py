import streamlit as st

# Alternatif untuk mengatur pilihan alternatif
# Value untuk mengatur i+1

def visualisasi():
        return """
        <style> 

        .kolom{
        width : 100%;
        height : 50px;
        background-color : #262730;
        padding : 12px;
        border-radius : 10px
        }


        """
def hasilData(alternatif, label, value):
    if alternatif ==  "(belum dipilih)":
        st.markdown(
            f"""
            <p style='font-size: 13px; margin-bottom: 10px;'>{label}{value}</p>
            <p class="kolom" style="color: #FFFFFF;">Belum Dipilih</p>
            """,
            unsafe_allow_html=True      
        )
    else: 
        st.markdown(
            f"""
            <p style='font-size: 13px; margin-bottom: 10px;'>{label}{value}</p>
            <p class="kolom" style="color: #FFFFFF;">{alternatif}</p>
            """,
            unsafe_allow_html=True
        )

def hasilDataBaru(alternatif, label, value):
        st.markdown(
            f"""
            <p style='font-size: 13px; margin-bottom: 10px;'>{label}{value}</p>
            <p class="kolom" style="color: #FFFFFF;">{alternatif}</p>
            """,
            unsafe_allow_html=True
        )