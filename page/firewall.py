import streamlit as st
import paramiko
import time


def show(klien):
    st.title("Konfigurasi Firewall")

    ### BLOKIR IP 
    st.subheader("Blokir IP")
    blocked_ips = st.text_area("Masukkan IP Address untuk diblokir (pisahkan dengan koma atau baris baru):")
    blocked_ip_list = [ip.strip() for ip in blocked_ips.replace('\n', ',').split(',') if ip.strip()]

    if st.button("Blokir IP"):
        for ip in blocked_ip_list:
            command = f'/ip firewall filter add chain=forward src-address={ip} action=drop comment="Block {ip}"'
            stdin, stdout, stderr = klien.exec_command(command)
            error = stderr.read().decode().strip()
            if error:
                st.error(f"Gagal memblokir IP: {ip} - {error}")
            else:
                st.success(f"Berhasil memblokir IP: {ip}")

        time.sleep(2)
        st.rerun()

    ### BLOKIR DOMAIN 
    st.subheader("Blokir Domain")
    blocked_domains = st.text_area("Masukkan Domain untuk diblokir (pisahkan dengan koma atau baris baru):")
    blocked_domain_list = [domain.strip() for domain in blocked_domains.replace('\n', ',').split(',') if domain.strip()]

    if st.button("Blokir Domain"):
        for domain in blocked_domain_list:

            perintah = [
                f'/ip firewall address-list add list=BLOCKED-DOMAINS address={domain} timeout=1d',
                f'/ip firewall filter add chain=forward dst-address-list=BLOCKED-DOMAINS action=drop comment="Block {domain}"'
            ]

            for command in perintah:
                stdin, stdout, stderr = klien.exec_command(command)
                error = stderr.read().decode().strip()
                if error:
                    st.error(f"Gagal memblokir {domain}: {error}")
                else:
                    st.success(f"Berhasil menambahkan {domain} ke daftar blokir")

        time.sleep(2)
        st.rerun()
