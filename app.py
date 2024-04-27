import requests
from gtts import gTTS 
import speech_recognition as konusma 
import time
import os
from playsound import playsound 
from PIL import Image
from io import BytesIO

konusturma = konusma.Recognizer()


def textiKonustur(mesaj):
    donustur = gTTS(text=mesaj,lang="tr",slow=False)
    dosya = "gelencevap.mp3"
    donustur.save(dosya)
    time.sleep(1)
    playsound(dosya)
    os.remove(dosya)

def getirYardim(mesaj):
    url = "https://open-ai21.p.rapidapi.com/chatgpt"

    payload = {
	    "messages": [
		    {
			    "role": "user",
			    "content": mesaj
		    }
	    ],
	    "web_access": False
    }
    headers = {
	    "content-type": "application/json",
	    "X-RapidAPI-Key": "PUT_YOUR_RAPIDAPI_KEY",
	    "X-RapidAPI-Host": "open-ai21.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    print(f"Zekai : {data['result']}")
    textiKonustur(data['result'])
    


def resimOlustur(mesaj):
    url = "https://open-ai21.p.rapidapi.com/texttoimage2"

    payload = { "text": mesaj }
    headers = {
	    "content-type": "application/json",
	    "X-RapidAPI-Key": "PUT_YOUR_RAPIDAPI_KEY",
	    "X-RapidAPI-Host": "open-ai21.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
            olusturulanresim = response.json()["generated_image"]
            resim_response = requests.get(olusturulanresim)
            with open("olusturulan_image.jpg", "wb") as file:
                 file.write(resim_response.content)
            resim = Image.open(BytesIO(resim_response.content))
            resim.show()
            print("Zekai : Resim başarıyla oluşturuldu.")
            textiKonustur("Resim başarıyla oluşturuldu.")
    else:
            print("API'den beklenmeyen bir yanıt geldi. Durum kodu: ",response.status_code)   



def asistan():
    while True:
        try:
            with konusma.Microphone() as konus:
                print("Zekai : Hoşgeldiniz ben asistanınız Zekai. Size nasıl yardımcı olabilirim?")
                textiKonustur("Hoşgeldiniz ben asistanınız Zekai. Size nasıl yardımcı olabilirim")
                print("Zekai : Asistan ile devam etmek için 'asistan' diyebilir")
                textiKonustur("Asistan ile devam etmek için asistan diyebilir")
                print("Zekai : Resim oluşturmak için 'resim oluştur' diyebilirsiniz.")
                textiKonustur("Resim oluşturmak için resim oluştur diyebilirsiniz")
                print("Zekai : Sizleri dinliyorum...")
                konusturma.adjust_for_ambient_noise(konus,duration=0.2)
                dinlenenSesimiz = konusturma.listen(konus)
                dinlendiginde = konusturma.recognize_google(dinlenenSesimiz,language='tr-tr')
                dinlendiginde = dinlendiginde.lower()

                if "programı kapat" in dinlendiginde:
                    print("Zekai : Program kapatılıyor. İyi günler dilerim :)")
                    textiKonustur("Program kapatılıyor. İyi günler dilerim")
                    time.sleep(3)
                    exit()
                if "asistan" in dinlendiginde:
                    print("Zekai : Asistana hoş geldiniz size nasıl yardımcı olabilirim?")
                    textiKonustur("Asistana hoş geldiniz size nasıl yardımcı olabilirim")
                    while True:
                        print("Zekai : Sizi dinliyorum...")  
                        konusturma.adjust_for_ambient_noise(konus,duration=0.2)
                        dinlenenSesimiz = konusturma.listen(konus)
                        dinlendiginde = konusturma.recognize_google(dinlenenSesimiz,language='tr-tr')
                        dinlendiginde = dinlendiginde.lower()
                        if "programı kapat" in dinlendiginde:
                                print("Zekai : Program kapatılıyor. İyi günler dilerim :)")
                                textiKonustur("Program kapatılıyor. İyi günler dilerim")
                                time.sleep(3)
                                exit()
                        else:
                            getirYardim(dinlendiginde) 
                if "resim oluştur" in dinlendiginde:
                    print("Zekai : Oluşturmak istediğiniz resmi tarif ediniz.")
                    textiKonustur("Oluşturmak istediğiniz resmi tarif ediniz.")
                    konusturma.adjust_for_ambient_noise(konus,duration=0.2)
                    dinlenenSesimiz = konusturma.listen(konus)
                    dinlendiginde = konusturma.recognize_google(dinlenenSesimiz,language='tr-tr')
                    dinlendiginde = dinlendiginde.lower()
                    print("Zekai : Sizi dinliyorum...")
                    print("Zekai : Resim oluşturuluyor lütfen bekleyiniz...")
                    textiKonustur("Resim oluşturuluyor lütfen bekleyiniz")     
                    resimOlustur(dinlendiginde)
                    print("Zekai : Sizi menüye yönlendiriyorum...")
                    textiKonustur("Sizi menüye yönlendiriyorum")
                    time.sleep(3)             
        except konusma.RequestError:
            textiKonustur("Sistemde bir sorun tespit edildi")
        except konusma.UnknownValueError:
            textiKonustur("Sizi anlayamadım")
            print("Zekai : Sizi menüye aktariyorum...")
            textiKonustur("Sizi menüye aktarıyorum")
            time.sleep(3)

if __name__ == "__main__":
     asistan()                    
