import streamlit as st
import paramiko as prm
from streamlit_option_menu import option_menu
from page import SetIp, dhcp, firewall, wireless

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

def cke():
    st.write("cakaka")
    
st.set_page_config(page_title="Netiski",page_icon="cekcek.png",layout="centered")

#form koneksi ke router
def koneksi():
    st.title("Masuk ke :red[Netiski]")

    st.session_state.host = st.text_input("Masukkan IP router")
    st.session_state.user = st.text_input("Masukkan Username",)
    st.session_state.psw = st.text_input("Masukkan Password", type="password")
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
        st.image("cekcek.png",width=150)
        menu = option_menu("NETISKI",['Setting IP', 'Setting Wireless', 'Setting DHCP', 'Konfigurasi Firewall'], 
                           icons=['globe', 'wifi', 'router','shield-slash'], menu_icon="cast", default_index=0)
        
        logout = st.button("Logout")
        if logout:
            if "logged_in" in st.session_state:
                st.session_state.clear() 
                st.rerun()
                klien.close()
    


    if menu == 'Setting IP':
        SetIp.show(klien)
    elif menu == 'Setting Wireless':
        wireless.show(klien)
    elif menu == 'Setting DHCP':
        dhcp.show(klien)
    elif menu == 'Konfigurasi Firewall':
        firewall.show(klien)
    elif menu == 'Setting':
        setting.show(klien)
        
else:
    koneksi()


