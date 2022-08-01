import dht
import machine
import time
from wifi_lib import conecta
import urequests
import gc

# atribui variáveis para os pontos D2 e D4 conectados ao sensor e do relé
r = machine.Pin(2, machine.Pin.OUT) # relé
r.value(1)
for i in range(3):
    r.value(0)
    time.sleep(0.5)
    r.value(1)
    time.sleep(0.5)
d = dht.DHT11(machine.Pin(4)) # sensor DHT11

sup = 75
inf = 70

while True:
    # medição de temperatura e umidade pelo sensor DHT11
    d.measure()
    t = d.temperature()
    h = d.humidity()

    if (r.value()==1): # Relé ligado/Ar desligado
        if h>sup:
            r.value(0) # Desiga relé/Liga ar condicionado
                
    if (r.value()==0): # Relé desligado/Ar ligado
        if h<inf:
            r.value(1) # Liga relé/Desliga ar condicionado

    print("Temp={}    Umid={}".format(t, h))

    # conecta o ESP32 à internet
    print("Conectando...")
    station = conecta("REDE_WIFI","SENHA") # rede wifi e senha removidos por privacidade
    if not station.isconnected():
        print("Não conectado!")
    else:
        print("Conectado!")
        print("Iniciando medição e gravação de dados...")
        
        # grava os dados no thingspeak através do urequests, apresenta mensagem de erro no caso de falha
        print("Gravando dados...")
        try:
            urequests.get("https://api.thingspeak.com/update?api_key=KEY_THING_SPEAK&field1={}&field2={}".format(t,h)) # key thingspeak removida por privacidade
            print("Dados gravados!")
        except:
            print("Erro na gravação!")
    gc.collect() # libera espaço na memória RAM     
    time.sleep(60)


    
