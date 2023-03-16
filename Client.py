from enlace import *
import time
import numpy as np
from utils import *


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com3 = enlace('COM3')
        com3.enable()
        print("ON")
        imageR = "./imgs/image.png"
        logclient = "./logs/client5.txt"
        logclient = open(logclient, "w")
    

        txBuffer = open(imageR, "rb").read()
        packs = Pack(txBuffer)
        numPck = len(packs)
        lenPayload =  (numPck).to_bytes(1, byteorder='big')
        

        #Estados
        inicia = False
        validado = False

        #Handshake
        while inicia == False:
            if validado == False:
                pergunta=input("Você quer continuar (s/n):")
                if pergunta == "s":
                    com3.sendData(np.asarray(Datagrama(tipo="1", npacks=numPck)))
                    logclient.write("{}, envio, 1, 14 \n".format(Tempolocal()))
                    msgt1, nrx = com3.getData(14, 5)
                    logclient.write("{}, recebe, {}, {}\n".format(Tempolocal(),str(msgt1[0:1]), len(msgt1)))
                    validado = msgt1[0:1] == b'\x02'
                    print("Validação:", validado)
                elif pergunta == 'n':
                    logclient.close()
                    com3.disable()
                    exit()          
            else:
                inicia = True
        #Enviando dados
        cont = 1
 
        while cont <= numPck:
            print("Enviando Pacote", cont)
            pacote = Datagrama(tipo="3", npacks=numPck, num_pack=cont, payload_len=len(packs[cont-1]), payload=packs[cont-1])
            com3.sendData(np.asarray(pacote))
            logclient.write("{}, envio, 3, {}, {}, {}\n".format(Tempolocal(), len(pacote), cont, numPck))
            print("Pacote {}/{}".format(cont,numPck), pacote)
            start_timer1 = time.time()
            start_timer2 = time.time()
            msgt4, nRx = com3.getData(14,5)
            logclient.write("{}, recebe, {}, {}\n".format(Tempolocal(),str(msgt4[0:1]), len(msgt4)))

            if msgt4[0:1] == b'\x04':
                cont += 1
                msgt4 = Datagrama(tipo = "6") 
            else:
                erro = True
                print("[ERRO]")
                while erro == True:
                    print(time.time()-start_timer2)
                    if time.time()-start_timer2 > 20:
                        com3.sendData(np.asarray(Datagrama(tipo="5")))
                        logclient.write("{}, envio, 5, 14 \n".format(Tempolocal()))
                        com3.disable()
                        print("(╯ ͠° ͟ʖ ͡°)╯┻━┻")
                        exit()                    
                    elif time.time()-start_timer1 > 5:
                        print("Tentando reconecção...")
                        pacote = Datagrama(tipo="3", npacks=numPck, num_pack=cont, payload_len=len(packs[cont-1]), payload=packs[cont-1])
                        com3.sendData(np.asarray(pacote))
                        logclient.write("{}, envio, 3, {}, {}, {}\n".format(Tempolocal(), len(pacote), cont, numPck))
                        start_timer1 = time.time()
                    else:
                        msgt6, nRx = com3.getData(14,4)
                        logclient.write("{}, recebe, {}, {}\n".format(Tempolocal(),str(msgt6[0:1]), len(msgt6)))
                        if msgt6[0:1] == b'\x06':
                            print("Corrigindo contador...")
                            cont = int.from_bytes(msgt6[7:8], "big")
                            pacote = Datagrama(tipo="3", npacks=numPck, num_pack=cont, payload_len=len(packs[cont-1]), payload=packs[cont-1])
                            com3.sendData(np.asarray(pacote))
                            logclient.write("{}, envio, 3, {}, {}, {}\n".format(Tempolocal(), len(pacote), cont, numPck))
                            start_timer1 = time.time()
                            start_timer2 = time.time()
                            msgt4, nRx = com3.getData(14)
                            logclient.write("{}, recebe, {}, {}\n".format(Tempolocal(),str(msgt4[0:1]), len(msgt4)))
                            
                        
                        if msgt4[0:1] == b'\x04':
                            cont += 1
                            erro = False





        

        
         
    
        # Encerra comunicação
        logclient.close()
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