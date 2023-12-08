import subprocess
import time
import tkinter as tk
import random

mac_adresleri = []
yerel_ag = 0
def tara():
    global  mac_adresleri
    global yerel_ag
    komut = "arp -a"
    sonuc = subprocess.check_output(komut, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).decode('utf-8')
    ikilenen_macler = set()

    sonuc = sonuc.split("\n")[3:]

    for a in sonuc:
        bolum = a.split()
        if len(bolum) == 3:
            ip, mac, _ = bolum
            if ip.endswith('.1'):
                    yerel_ag = ip.split('.')[0:3]
                    yerel_ag = '.'.join(yerel_ag)
            if mac!="ff-ff-ff-ff-ff-ff":
                mac_adresleri.append((ip, mac))

    ip_mac = set()
    for a in mac_adresleri:
        if a[1] in ip_mac:
            ikilenen_macler.add(a[1])
        else:
            ip_mac.add(a[1])

    return ikilenen_macler

def ip_degistir():

    # IP Adresini değiştir
    ip_adresi = f'{yerel_ag}.{random.randint(1, 254)}'

    if ip_adresi not in [item[0] for item in mac_adresleri]:
        ip_command = f'netsh interface ipv4 set address name="Ethernet" static {ip_adresi} 255.255.255.0 {yerel_ag}.1'
        subprocess.run(ip_command, shell=True, check=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        # DNS Ayarla
        dns_command = 'netsh interface ipv4 set dns name="Ethernet" static 8.8.8.8'
        subprocess.run(dns_command, shell=True, check=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        ip_degistir()

if __name__ == "__main__":
    onceki_ikilenen_macler = []

    while True:
        mac_adresleri.clear()
        suanki_ikilenen_macler = tara()

        if suanki_ikilenen_macler!=[] and suanki_ikilenen_macler != onceki_ikilenen_macler:
            if suanki_ikilenen_macler:
                pencere = tk.Tk()
                genislik = pencere.winfo_screenwidth()
                yukseklik = pencere.winfo_screenheight()
                pencere.geometry("450x200+{}+{}".format(genislik-458,yukseklik-279))
                pencere.title("Uyarı!")
                pencere.attributes('-alpha', 0.8)
                pencere.configure(bg='#FFCCCC')
                label = tk.Label(pencere, text=f"Aynı MAC adresine ait birden fazla IP adresi bulunuyor!\n{suanki_ikilenen_macler}")
                label.configure(bg='#FFCCCC')
                label.pack()
                pencere.after(1000, ip_degistir)
                pencere.mainloop()

            onceki_ikilenen_macler = suanki_ikilenen_macler
            suanki_ikilenen_macler.clear()

        time.sleep(60)
