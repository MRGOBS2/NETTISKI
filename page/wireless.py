import streamlit as st
import paramiko

def show(klien):
    st.title("Konfigurasi Wireless")
    
    ssid = st.text_input("Masukkan SSID Wireless")
    auth = st.text_input("Masukkan Password Wireless", type="password")
    connect = st.button("Proses")

    if connect:
        try:
            # Mendapatkan daftar interface wireless
            stdin, stdout, stderr = klien.exec_command("/interface wireless print")
            interfaces = stdout.read().decode()

            # Menentukan nama interface pertama yang ditemukan (default: wlan1)
            interface = None
            for line in interfaces.split("\n"):
                if 'name="' in line:
                    interface = line.split('name="')[1].split('"')[0]
                    break

            if not interface:
                st.error("⚠️ Tidak ada interface wireless yang terdeteksi.")
                return
            
            # Mengecek apakah security profile dengan nama yang sama sudah ada
            profile_name = f"passwd_{ssid}"
            stdin, stdout, stderr = klien.exec_command("/interface wireless security-profiles print")
            profiles = stdout.read().decode()
            
            if profile_name in profiles:
                # Menghapus security profile lama jika sudah ada
                klien.exec_command(f"/interface wireless security-profiles remove {profile_name}")

            # Membuat security profile baru
            klien.exec_command(f"/interface wireless security-profiles add name={profile_name} "
                               f"wpa2-pre-shared-key={auth} wpa-pre-shared-key={auth}")

            # Mengupdate konfigurasi wireless
            klien.exec_command(f"/interface wireless set {interface} ssid={ssid} "
                               f"mode=ap-bridge security-profile={profile_name}")

            st.success(f"✅ Wireless {ssid} pada interface {interface} berhasil dikonfigurasi.")
            st.rerun()
            
        except Exception as e:
            st.error(f"⚠️ Gagal konfigurasi Wireless: {str(e)}")