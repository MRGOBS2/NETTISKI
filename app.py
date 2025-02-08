import streamlit as st
import paramiko as prm
from streamlit_option_menu import option_menu


def koneksi_ssh():
  try:
    klien = prm.SSHClient()
    klien.set_missing_host_key_policy(prm.AutoAddPolicy())
    klien.connect(
      hostname=st.session_state['host'],
      port=st.session_state['port'],
      username=st.session_state['user'],
      password=st.session_state['psw']
    )
    return klien
  except Exception as e:
    st.error("Kesalahan : {e}")
    return none 


st.title("Masuk ke :red[dunia]")

def koneksi():
    st.session_state['host'] = st.text_input("Masukkan IP router: ",st.session_state.get('host',''))
    st.session_state['user'] = st.text_input("Masukkan Username: ",st.session_state.get('user',''))
    st.session_state['psw'] = st.text_input("Masukkan Password: ", type="password", value=st.session_state.get('psw',''))
    st.session_state['port'] = st.text_input("Masukkan Port (default 22)",st.session_state.get('port','22'))
    submit = st.button("Connect")

    if submit:
      koneksi_ssh()
      try:
          st.success(f"Berhasil Terhubung ke {st.session_state['host']}:{st.session_state['port']}")
          st.session_state["logged_in"] = True
      except Exception as e:
          st.error(f"Gagal Terhubung: {e}")

def dashboard():
  if "logged_in" in st.session_state:
    klien = koneksi_ssh()
    if klien:
      stdin,stdout,stderr = klien.exec_command("/system resource print\nip ad pr\nsystem identity pr\nip dhcp-server pr")
      router_info = stdout.read().decode() 
      st.title("Router Dashboard")
      st.text("Informasi router:")
      st.code(router_info)
  else:
    st.warning("Mohon login")

# Mengatur state login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = ''

# Sidebar menu
with st.sidebar:
    st.title(":blue[NETISKI]")
    menu = option_menu("Main Menu", ['Buat Koneksi', 'Setting IP', 'Setting Wireless', 'Setting DHCP', 'Konfigurasi Firewall'], 
                        icons=['house', 'gear', 'gear', 'gear'], menu_icon="cast", default_index=0)

if menu == 'Buat Koneksi':
    koneksi()
else:
    # Cek apakah sudah login
    if not st.session_state["logged_in"]:
        st.warning("Silakan login terlebih dahulu di menu 'Buat Koneksi'")
    else:
        if menu == 'Setting IP':
            st.write('IP Configuration Menu')
        elif menu == 'Setting Wireless':
            dashboard()
        elif menu == 'Setting DHCP':
            st.write('DHCP Configuration Menu')
        elif menu == 'Konfigurasi Firewall':
            st.write('Firewall Configuration Menu')
