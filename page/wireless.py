import streamlit as st
import paramiko as prm

def show(klien):
    st.title('Konfigurasi Wireless')
    ssid = st.text_input("Masukkan SSID Wireless")
    auth = st.text_input("Masukkan Password Wireless", type="password")
    connect = st.button("Proses")

    if connect:
        try:

            stdin, stdout, stderr = klien.exec_command("/interface wireless print")
            interfaces = stdout.read().decode()
         
            if interface in interfaces:
                
                stdin, stdout, stderr = klien.exec_command(f'/interface wireless security-profiles add name=passwd_wifi '
                                                            f'wpa2-pre-shared-key={auth} wpa-pre-shared-key={auth}')
                # Membaca output dari perintah untuk debugging
                st.write(stdout.read().decode()) 
                st.write(stderr.read().decode())  

                
                stdin, stdout, stderr = klien.exec_command(f'/interface wireless set {interface} ssid={ssid} '
                                                            f'mode=ap-bridge security-profile=passwd_wifi')
                #
                st.write(stdout.read().decode())  
                st.write(stderr.read().decode())  

                st.success(f"✅ Wireless {ssid} pada interface {interface} berhasil dikonfigurasi.")
            else:
                
                st.write(f"⚠️ Interface {interface} tidak ditemukan. Menambahkan interface baru...")

                # Menambahkan interface wireless baru
                stdin, stdout, stderr = klien.exec_command(f"/interface wireless add name={interface} disabled=no")
                st.write(stdout.read().decode()) 
                st.write(stderr.read().decode())  

                
                stdin, stdout, stderr = klien.exec_command(f'/interface wireless security-profiles add name=passwd_wifi '
                                                            f'wpa2-pre-shared-key={auth} wpa-pre-shared-key={auth}')
                st.write(stdout.read().decode())  
                st.write(stderr.read().decode())  

                
                stdin, stdout, stderr = klien.exec_command(f'/interface wireless set {interface} ssid={ssid} '
                                                            f'mode=ap-bridge security-profile=passwd_wifi')
                st.write(stdout.read().decode())  
                st.write(stderr.read().decode())  

                st.success(f"✅ Wireless {ssid} pada interface {interface} berhasil dikonfigurasi.")
                
        except Exception as e:
            st.error(f"⚠️ Gagal konfigurasi Wireless: {str(e)}")