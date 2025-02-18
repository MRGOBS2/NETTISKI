import streamlit as st
import paramiko as prm
import pandas as pd

#konfigurasi ip address
def show(klien):
    title, popover = st.columns([8,2]) 
    with title:
        st.title("Konfigurasi IP Address")
    with popover:
        with st.popover("Status"):
            st.write("D : Dynamic-IP diberikan secara dinamis atau otomatis")
            st.write("X : Disabled-IP Address dinonaktifkan")
            st.write("I : Invalid-IP Address tidak valid")
            st.write("R : Aktif-IP Address aktif dan dapat digunakan")

    #list ip address 
    stdin,stdout,stderr = klien.exec_command("/ip address print")
    output = stdout.read().decode()
    iplist = []
    for lis in output.split("\n")[2:]:  
        parts = lis.split()  
        if len(parts) >= 4:  #pastikan data ada setidaknya 4 dari index,status,address,network,interface
            if len(parts) == 5: #jika memiliki status
                index = parts[0]
                status = parts[1]  # Jika ada status (misal "X")
                address = parts[2]
                network = parts[3]
                interface = parts[-1]
            else:
                index = parts[0]
                status = ""  # Jika status kosong
                address = parts[1]
                network = parts[2]
                interface = parts[-1]

            if status == "":
                status = "Aktif"
            elif status == "D":
                status = "Dynamic"
            elif status == "X":
                status = "Disabled"
            elif status == "I":
                status = "Invalid"
            

            iplist.append({
                "index" : index,
                "Address":address,
                "Network":network,
                "Interface" : interface,
                "Status":status
            })

    a,b,c,d,e = st.columns([2.5,2,1.5,1.3,2.5])
    a.write("**ADDRESS**")
    b.write("**NETWORK**")
    c.write("**INTERFACE**")
    d.write("**STATUS**")
    e.write("**AKSI**")

    st.markdown(    #divider
    """
    <hr style="margin: 5px 0; border: 1px solid #666;" />
    """,
    unsafe_allow_html=True)

    for i in iplist:
        address,network,interface,status,aksi = st.columns([2.5,2,1.5,1.3,2.5])
        with address:
            st.write(i["Address"])
        with network:
            st.write(i["Network"])
        with interface:
            st.write(i["Interface"])
        with status:
            st.write(i["Status"])
        with aksi:
            hapus,edit = st.columns(2)
             #edit button and key for every address
            with hapus:                        
                if st.button("Hapus", key=f"hapus for {i['Address']}"):
                    stdin,stdout,stderr = klien.exec_command(f"/ip address remove numbers={i['index']}")
                    st.rerun()
            with edit:
                with st.popover("Edit"):
                    edit_ip = st.text_input("Maukkan IP Address",key=f"Edit ip for {i['Address']}")
                    edit_interface = st.text_input("Masukkan interface",key=f"Edit interface for {i['Address']}")  
                    if st.button("Edit IP",key=f"tombol_edit_{i['Address']}"):
                        klien.exec_command(f"/ip address set numbers={i['index']} address={i['Address']}")
                        
                
                    
        
    st.markdown(    #divider
    """
    <hr style="margin: 20px 0; border: 1px solid #666;" />
    """,
    unsafe_allow_html=True)
    

    #setting ip address    
    stdin, stdout, stderr = klien.exec_command("/interface print") #ambil interface
    interfaces_output = stdout.read().decode()
    
    interfaces = []
    for line in interfaces_output.strip().split("\n")[3:]:  
        parts = line.split()  
        if len(parts) > 1:  
            interface_name = parts[2]  
            interfaces.append(interface_name)
            
    ip_address = st.text_input("Masukkan IP Address: ")
    interface = st.selectbox("Pilih Interface:", interfaces)

    if st.button("Set IP Address"):
        if ip_address and interface:
            cek = ip_address.split(".")
            if len(cek) == 4:
                command = [
                    f"/ip address add address={ip_address} interface={interface}",
                    f"/ip firewall nat add chain=srcnat src-address={ip_address} action=masquerade"
                ]
                for i in command:
                    klien.exec_command(i)
                st.success("Berhasil")
                st.rerun()
            else:
                st.warning("Mohon Masukkan format IP yang benar")
        else:
            st.error("Mohon isi IP Address dan pilih Interface")

     
    