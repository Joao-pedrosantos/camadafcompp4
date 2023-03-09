from enlace import *
import time
import numpy as np
import random
import binascii
from utils import *


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM3"                  # Windows(variacao de)

bye = b'\xf2'
def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com3 = enlace('COM9')
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com3.enable()
        tempo = time.time()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("ON")
        #aqui você deverá gerar os dados a serem transmitidos. 
        imageR = "img/image.png"
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        #===========THIS============

        txBuffer = open(imageR, "rb").read()
        packs = Pack(txBuffer)
        lenPayloadInt = len(packs)
        lenPayload =  (lenPayloadInt).to_bytes(1, byteorder='big')

        #Estados
        handshake = 0
        enviando = 1
        estado = handshake
        validacao = 0

        #Handshake


        print("Validação:", validacao == lenPayload)
        while estado == handshake:
            if validacao != lenPayload:
                pergunta=input("Você quer continuar (s/n):")
                if pergunta == "s":
                    com3.sendData(np.asarray(Datagrama(tipo="handshake", payload=lenPayload)))
                    time.sleep(0.01)
                    validacao, nrx = com3.getData(1, 5)
                    print("Validação:", validacao == lenPayload)
                elif pergunta == 'n':
                    handshake = False
                    estado = -1
                    com3.disable()
            elif validacao == lenPayload:
                estado = enviando
     
        while estado == enviando:
            validado = True
            for i in range(0,len(packs)):
                tempo = time.time()
                if validado == True:
                    print("Tamanho do pacote:",len(packs[i]))
                    pacote = Datagrama(tipo="data", npacks=lenPayloadInt, num_pack=i, payload_len=len(packs[i]), payload=packs[i])

                    com3.sendData(np.asarray(pacote))

                    print("Pacote {}/{} Enviado:".format(i, lenPayloadInt-1), pacote)
                    time.sleep(0.1)
                    validacao, nRx = com3.getData(15)

                    print( validacao[10:11])
                    validado = validacao[10:11] == b'\x01' or validacao[10:11] == b'\x02'

                else:
                    error = True
                    while error:
                        print("Erro reenviando pacote:", i)
                        com3.sendData(np.asarray(packs[i]))
                        com3.getData(15,60)
                    error = False
            estado = -1       


        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com3.disable()       
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com3.disable()      

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()