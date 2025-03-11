import streamlit as st
import paramiko
import time


def show(klien):
    st.title("Konfigurasi Firewall")

    ### BLOKIR IP 
    st.subheader("Blokir IP")
    blocked_ips = st.text_area("Masukkan IP Address untuk diblokir (pisahkan dengan baris baru atau koma ','):")
    blocked_ip_list = [ip.strip() for ip in blocked_ips.split('\n') if ip.strip()]

    if st.button("Blokir IP"):
        for ip in blocked_ip_list:
            command = f'/ip firewall filter add chain=forward src-address={ip} action=drop comment="Block {ip}"'
            stdin, stdout, stderr = klien.exec_command(command)
            error = stderr.read().decode().strip()
            if error:
                st.error(f"Gagal memblokir IP: {ip} - {error}")
            else:
                st.success(f"Berhasil memblokir IP: {ip}")

        time.sleep(1)
        st.rerun()

    ### BLOKIR DOMAIN 
    st.subheader("Blokir Domain")
    blocked_domains = st.text_area("Masukkan Domain untuk diblokir (pisahkan dengan baris baru atau koma ','):")
    blocked_domain_list = [domain.strip() for domain in blocked_domains.split('\n') if domain.strip()]

    if st.button("Blokir Domain"):
        for domain in blocked_domain_list:

            commands = [
                f'/ip firewall address-list add list=BLOCKED-DOMAINS address={domain} comment="Block {domain}"',
                f'/ip firewall filter add chain=forward dst-address-list=BLOCKED-DOMAINS action=drop comment="Block {domain}"'
            ]

            for command in commands:
                stdin, stdout, stderr = klien.exec_command(command)
                error = stderr.read().decode().strip()

            if error:
                st.error(f"Gagal memblokir {domain}: {error}")
            else:
                st.success(f"Berhasil menambahkan {domain} ke daftar blokir")

        time.sleep(1)
        st.rerun()

    # coman = f'ip firewall filter pr '
    # stdin,stdout,stderr = klien.exec_command(coman)
    # outpurr = stdout.read().decode().strip().split('\n')
    # st.write(outpurr)

    coman = "/ip firewall filter print without-paging"
    stdin, stdout, stderr = klien.exec_command(coman)
    outpurr = stdout.read().decode().strip().split('\n')

    # List untuk menyimpan hasil
    blocked_list = []

    for entry in outpurr:
        if "Block" in entry:  # Mencari baris yang memiliki comment "Block ..."
            parts = entry.split("Block")  
            if len(parts) > 1:
                blocked_item = parts[1].strip()  # Mengambil nama domain/IP
                blocked_list.append(blocked_item)

    # Menampilkan di Streamlit
    if blocked_list:
        st.write("### **Daftar IP & Domain yang Diblokir**")
        for item in blocked_list:
            st.write(f"- {item}")
    else:
        st.info("Tidak ada IP atau domain yang diblokir.")


    