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
    return st.write("Silahkan Ulangi") 


st.title("Masuk ke :red[dunia]")

def koneksi():
    st.session_state['host'] = st.text_input("Masukkan IP router: ")
    st.session_state['user'] = st.text_input("Masukkan Username: ",)
    st.session_state['psw'] = st.text_input("Masukkan Password: ", type="password")
    st.session_state['port'] = st.text_input("Masukkan Port (default 22)",22)
    submit = st.button("Connect")

    if submit:
        if not (st.session_state['host'] and st.session_state['user'] and st.session_state['psw']):
            st.error("Mohon isi field login")
            
        if koneksi_ssh():
            st.success(f"Berhasil Terhubung ke {st.session_state['host']}:{st.session_state['port']}")
            st.session_state["logged_in"] = True
            st.rerun()
        else:
          st.error(f"Gagal Terhubung")

#konfigurasi ip address
def SetIp(klien):
    st.subheader("Konfigurasi IP Address")

    stdin, stdout, stderr = klien.exec_command("/interface print")
    interfaces_output = stdout.read().decode()
    stdout.read()
    

    interfaces = []
    for line in interfaces_output.strip().split("\n")[2:]:  
        parts = line.split()  
        if len(parts) > 1:  
            interface_name = parts[2]  
            interfaces.append(interface_name)
            
    ip_address = st.text_input("Masukkan IP Address:")
    interface = st.selectbox("Pilih Interface:", interfaces)

    if st.button("Set IP Address"):
        if ip_address and interface:
            command = f"/ip address add address={ip_address} interface={interface}"
            stdin, stdout, stderr = klien.exec_command(command)
            stdout.read()
            stderr.read()
            st.success("Berhasil")
        else:
            st.error("Mohon isi IP Address dan pilih Interface")

    
    #list ip address 
    stdin,stdout,stderr = klien.exec_command("/ip adddress print")
    listip = stdout.read().decode()

    
    iplist = []
    for line in listip.strip().split("\n")[0:]:  
        parts = line.split()  
        if len(parts) > 1:  
            ip_name = parts[2]  
            iplist.append(ip_name)

    st.write(iplist)

def wireless():
    st.write("wireless")

def dhcp():
    st.write("dhcp")

def firewall():
    st.write("firewall")

if "logged_in" in st.session_state:
#sidebar
    klien = koneksi_ssh()
    with st.sidebar:
        st.title(":blue[NETISKI]")
        menu = option_menu("Main Menu", ['Setting IP', 'Setting Wireless', 'Setting DHCP', 'Konfigurasi Firewall'], 
                           icons=['house', 'gear', 'gear'], menu_icon="cast", default_index=0)
        
        logout = st.button("Logout")
        if logout:
            if "logged_in" in st.session_state:
                st.session_state.clear() 
                st.rerun()
                klien.close()


    if menu == 'Setting IP':
        SetIp(klien)
    elif menu == 'Setting Wireless':
        wireless()
    elif menu == 'Setting DHCP':
        dhcp()
    elif menu == 'Konfigurasi Firewall':
        firewall()
        
else:
    koneksi()
