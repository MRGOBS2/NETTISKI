import streamlit as st
import paramiko as prm
from streamlit_option_menu import option_menu
from page import SetIp, setting, dhcp, firewall

#koneksi ssh ke router
def koneksi_ssh():
  try:
    klien = prm.SSHClient()
    klien.set_missing_host_key_policy(prm.AutoAddPolicy())
    klien.connect(
      hostname=st.session_state.host,
      port=st.session_state.port,
      username=st.session_state.user,
      password=st.session_state.psw
    )
    return klien
  except Exception as e:
    return st.write("Silahkan Ulangi") 


st.title("Masuk ke :red[Netiski]")

#form koneksi ke router
def koneksi():
    st.session_state.host = st.text_input("Masukkan IP router: ")
    st.session_state.user = st.text_input("Masukkan Username: ",)
    st.session_state.psw = st.text_input("Masukkan Password: ", type="password")
    st.session_state.port = st.text_input("Masukkan Port (default 22)",22)
    submit = st.button("Connect")

    if submit:
        if not (st.session_state.host and st.session_state.user and st.session_state.psw):
            st.error("Mohon isi form login")
            
        if koneksi_ssh():
            st.success(f"Berhasil Terhubung ke {st.session_state.host}:{st.session_state.port}")
            st.session_state.logged_in = True
            st.rerun()
        else:
          st.error(f"Gagal Terhubung")

if "logged_in" in st.session_state:
#sidebar
    klien = koneksi_ssh()
    with st.sidebar:
        st.title(":blue[NETISKI]")
        menu = option_menu("Main Menu", ['Setting IP', 'Setting Wireless', 'Setting DHCP', 'Konfigurasi Firewall'], 
                           icons=['house', 'gear', 'gear'], menu_icon="cast", default_index=0)
        col1,col2 = st.columns(2)
        with col1:
            logout = st.button("Logout")
            if logout:
                if "logged_in" in st.session_state:
                    st.session_state.clear() 
                    st.rerun()
                    klien.close()
        with col2:
            st.button("Setting")


    if menu == 'Setting IP':
        SetIp.show(klien)
    elif menu == 'Setting Wireless':
        setting.show()
    elif menu == 'Setting DHCP':
        dhcp.show(klien)
    elif menu == 'Konfigurasi Firewall':
        firewall.show(klien)
        
else:
    koneksi()
