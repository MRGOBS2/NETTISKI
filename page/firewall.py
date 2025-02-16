import streamlit as st
import paramiko
import time


def show(klien):
    st.title("Konfigurasi Firewall")
    
    st.subheader("Blokir IP")
    #memisahkan ip dengan baris
    #list ip
    blocked_ip = st.text_area("Masukkan IP Address untuk diblokir (pisahkan dengan baris baru):").split('\n') 
    if st.button("Blokir IP"):
        for ip in blocked_ip: #untuk setiap ip di list
            command = f'/ip firewall filter add chain=forward src-address={ip} action=drop comment="Block {ip}"'
            stdin, stdout, stderr = klien.exec_command(command)
            error = stderr.read().decode().strip()
            if error:
                return error
            else:
                st.success(f"Berhasil memblokir IP: {ip}")
        time.sleep(2)
        st.rerun()
    
   
