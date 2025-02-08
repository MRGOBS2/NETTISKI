import streamlit as st
from routeros_api import RouterOsApiPool

st.set_page_config(
    page_title="IAAS COy",
    page_icon="👋",
)

st.write("# Welcome to NetTiski! 👋")

# st.sidebar.image("Screenshot_2025-01-22_143357-removebg-preview.png", use_container_width=True, )  # Updated parameter

st.sidebar.header("Menu Utama")
menu = st.sidebar.selectbox(
    "Pilih menu:",
    ["Home", "Buat Koneksi", "Setting Jaringan", "Pengaturan"]
)

def connect_to_mikrotik(ip, username, password, port=8728):
    try:
        api_pool = RouterOsApiPool(host=ip, username=username, password=password, port=port)
        api = api_pool.get_api()
        return api, api_pool
    except Exception as e:
        return None, str(e)

if menu == "Home":
    st.markdown(
        """
        ## Selamat Datang di Aplikasi Streamlit
        Aplikasi ini dapat digunakan untuk pengaturan jaringan mikrotik dengan mudah dan cepat
        """
    )

elif menu == "Buat Koneksi":
    st.markdown("### Buat Koneksi ke Mikrotik")
    ip_address = st.text_input("Masukkan IP Address:")
    username = st.text_input("Masukkan Username:")
    password = st.text_input("Masukkan Password:", type="password")
    port = st.text_input("Masukkan Port:", value="8728")
    
    if st.button("Buat Koneksi"):
        if ip_address and username and password and port:
            api, result = connect_to_mikrotik(ip_address, username, password, int(port))
            if api:
                st.success(f"Berhasil terhubung ke Mikrotik di {ip_address}:{port} dengan username {username}.")
                st.markdown("#### Informasi Router:")
                system_resource = api.get_resource('/system/resource')
                resource_info = system_resource.get()[0]
                st.json(resource_info)
                api.disconnect()
            else:
                st.error(f"Gagal terhubung ke Mikrotik: {result}")
        else:
            st.error("Harap isi semua data untuk membuat koneksi.")

elif menu == "Setting Jaringan":
    st.markdown("### Pengaturan Jaringan")
    ip_address = st.text_input("Masukkan IP Address:")
    subnet_mask = st.text_input("Masukkan Subnet Mask:")
    gateway = st.text_input("Masukkan Gateway:")
    if st.button("Simpan Pengaturan"):
        st.success("Pengaturan jaringan berhasil disimpan!")

elif menu == "Pengaturan":
    st.markdown("### Pengaturan Mikrotik")
    option = st.radio(
        "Pilih aksi:",
        ["Hubungkan ke Mikrotik", "Lihat Status Mikrotik"]
    )
    
    if option == "Hubungkan ke Mikrotik":
        ip_address = st.text_input("Masukkan IP Address:")
        username = st.text_input("Masukkan Username:")
        password = st.text_input("Masukkan Password:", type="password")
        port = st.text_input("Masukkan Port:", value="8728")
        
        if st.button("Hubungkan"):
            api, result = connect_to_mikrotik(ip_address, username, password, int(port))
            if api:
                st.success(f"Berhasil terhubung ke Mikrotik di {ip_address}:{port}.")
                api.disconnect()
            else:
                st.error(f"Gagal terhubung ke Mikrotik: {result}")

    elif option == "Lihat Status Mikrotik":
        st.markdown("#### Informasi Status:")
        st.text("IP Address: 192.168.88.1")
        st.text("Status: Terhubung")
        st.text
