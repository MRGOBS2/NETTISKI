import streamlit as st
import paramiko
import time

def show(klien):
    st.title("Konfigurasi Firewall")

    # Ambil daftar IP & domain yang sudah diblokir dari firewall
    coman = "/ip firewall filter print without-paging"
    stdin, stdout, stderr = klien.exec_command(coman)
    outpurr = stdout.read().decode().strip().split('\n')

    blocked_list = []

    for entry in outpurr:
        if "Block" in entry:  # Mencari baris dengan comment "Block"
            parts = entry.split("Block")  # Pisahkan teks
            if len(parts) > 1:
                blocked_item = parts[1].strip()
                blocked_list.append(blocked_item)

    # ** BLOKIR IP **
    st.subheader("Blokir IP")
    blocked_ips = st.text_area("Masukkan IP Address untuk diblokir (pisahkan dengan baris baru atau koma ','):")
    blocked_ip_list = [ip.strip() for ip in blocked_ips.split('\n') if ip.strip()]

    if st.button("Blokir IP"):
        for ip in blocked_ip_list:
            if ip in blocked_list:  # Periksa apakah IP sudah ada dalam daftar blokir
                st.warning(f"IP {ip} sudah diblokir sebelumnya.")
                continue

            command = f'/ip firewall filter add chain=forward src-address={ip} action=drop comment="Block {ip}"'
            stdin, stdout, stderr = klien.exec_command(command)
            error = stderr.read().decode().strip()
            if error:
                st.error(f"Gagal memblokir IP: {ip} - {error}")
            else:
                st.success(f"Berhasil memblokir IP: {ip}")

        time.sleep(1)
        st.rerun()

    # ** BLOKIR DOMAIN **
    st.subheader("Blokir Domain")
    blocked_domains = st.text_area("Masukkan Domain untuk diblokir (pisahkan dengan baris baru atau koma ','):")
    blocked_domain_list = [domain.strip() for domain in blocked_domains.split('\n') if domain.strip()]

    if st.button("Blokir Domain"):
        for domain in blocked_domain_list:
            if domain in blocked_list:  # Periksa apakah domain sudah ada dalam daftar blokir
                st.warning(f"Domain {domain} sudah diblokir sebelumnya.")
                continue

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

    # ** TAMPILKAN DAFTAR YANG DIBLOKIR **
    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )
    if blocked_list:
        st.write("### **Daftar IP & Domain yang Diblokir**")

        st.markdown(    #divider
            """
            <hr style="margin: 5px 0; border: 1px solid #666;" />
            """,
        unsafe_allow_html=True)    

        for idx, item in enumerate(blocked_list):
            col1, col2 = st.columns([3, 1])
            col1.write(f"{item}")

            # Tombol untuk menghapus blokir
            if col2.button("Hapus", key=f"hapus_{item}_{idx}"):
                remove_block(klien, item)
                time.sleep(1)
                st.rerun()
        st.markdown(    #divider
    """
    <hr style="margin: 5px 0; border: 1px solid #666;" />
    """,
    unsafe_allow_html=True)    

    else:
        st.info("Tidak ada IP atau domain yang diblokir.")
    
  

def remove_block(klien, item):
    # Hapus dari address-list jika domain
    remove_address_list = f'/ip firewall address-list remove [find address="{item}"]'
    # Hapus dari filter jika IP
    remove_filter = f'/ip firewall filter remove [find comment="Block {item}"]'

    commands = [remove_address_list, remove_filter]

    for command in commands:
        stdin, stdout, stderr = klien.exec_command(command)
        error = stderr.read().decode().strip()

    if error:
        st.error(f"Gagal menghapus blokir {item}: {error}")
    else:
        st.success(f"Berhasil menghapus blokir {item}")
