import streamlit as st
import paramiko as prm

#konfigurasi ip address
def show(klien):
    st.subheader("Konfigurasi IP Address")

    #ambil interface
    stdin, stdout, stderr = klien.exec_command("/interface print")
    interfaces_output = stdout.read().decode()
    stdout.read()
    st.session_state.com = True

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
            st.success("Berhasil")
        else:
            st.error("Mohon isi IP Address dan pilih Interface")

     
    #list ip address 
    

    if "com" in st.session_state:
        stdin,stdout,stderr = klien.exec_command("/ip address print")
        output = stdout.read().decode()
        iplist = []
        for lis in output.split("\n")[2:]:  
            parts = lis.split()  
            if len(parts) >= 4:  # Pastikan data cukup untuk diambil
                if len(parts) == 5:
                    status = parts[1]  # Jika ada status (misal "X")
                    address = parts[2]
                    network = parts[3]
                    interface = parts[4]
                else:
                    status = ""  # Jika status kosong
                    address = parts[1]
                    network = parts[2]
                    interface = parts[3]

                if status == "":
                    status = "Aktif"
                elif status == "D":
                    status = "Dinamis"
                elif status == "X":
                    status == "Disable"
                elif status == "I":
                    status = "Invalid"
                

                iplist.append({
                    "address":address,
                    "network":network,
                    "interface" : interface,
                    "status":status
                })
        st.subheader("Daftar IP Address")
        # cek = output.split("\n")[2:]
        st.table(iplist)

