import streamlit as st
import paramiko as prm
import time

def show(klien):
    st.title("Konfigurasi DHCP Server")

    stdin, stdout, stderr = klien.exec_command("/ip address print")
    interfaces_output = stdout.read().decode()

    interfaces = []
    for line in interfaces_output.strip().split("\n")[2:]:  
        parts = line.split()  
        if len(parts) > 1:  
            interface_name = parts[-1]  
            interfaces.append(interface_name)
            interfaces.sort()

    #Input dhcp
    inter = st.selectbox("Pilih Interface", interfaces)        
    range = st.number_input("Masukkan Jumlah User",min_value=2, max_value=250)
    st.caption("Maks : 250 User")
    start = st.text_input("Masukkan awal dhcp",1)   
    st.caption("Rekomendasi: Isi awal ip lebih tinggi dari gateway")
    #input dhcp


    stdin,stdout,stderr = klien.exec_command(f"/ip address print where interface={inter}")
    output = stdout.read().decode()
    splite = output.split("\n")[2] #pisahkan berdasarkan baris lalu ambil baris index ke-2 

    address_for_dhcp = splite.split()[-3].split("/")[0] #ip address ether atau gateway
    network_for_dhcp = splite.split()[-2] #ip network

    ipad = address_for_dhcp.split(".") #ambil address -> pisah berdasarkan titik
    prefix = f"{ipad[0]}.{ipad[1]}.{ipad[2]}" # 3 oktet pertama ip

    range_start = f"{prefix}.{start}"
    count = int(start) + int(range) - 1
    range_end = f"{prefix}.{count}"

    st.write(f"Network : {network_for_dhcp}/24")
    st.write(f"Gateway : {address_for_dhcp}")
    st.write(f"DHCP Range IP : {range_start} - {range_end}")

    if st.button("Buat DHCP Server"):
        command = [
            f"/ip pool add name=dhcp_pool_{address_for_dhcp} ranges={range_start}-{range_end}",
            f"/ip dhcp-server add name=dhcp_server_{address_for_dhcp} interface={inter} lease-time=1d address-pool=dhcp_pool_{address_for_dhcp} disabled=no",
            f"/ip dhcp-server network add address={network_for_dhcp}/24 gateway={address_for_dhcp} dns-server=8.8.8.8,8.8.4.4"
        ]
        for coman in command:
            klien.exec_command(coman)
            
        st.success("Berhasil menambah chdp")
        time.sleep(3)
        st.rerun()
    
    