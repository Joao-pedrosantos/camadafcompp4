from enlace import *
import time
import numpy as np
from utils import *

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com4 = enlace('COM4')
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com4.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("ON")
        #aqui você deverá gerar os dados a serem transmitidos. 
        imageW = "./imgs/recebidaCopia.png"
        SaveImage = open(imageW, 'wb')
        logserver = "./logs/server5.txt"
        logserver = open(logserver, "w")
        ocioso = True 

        while ocioso == True:
            print("Ocioso")
            msgt1, nrx = com4.getData(14)
            logserver.write("{}, recebe, {}, {}\n".format(Tempolocal(),str(msgt1[0:1]), len(msgt1)))
            if msgt1[0:1] == b'\x01':
                if msgt1[2:3] == b'\x0F':
                    ocioso = False
            time.sleep(1)
        print("Estou vivo!!!")

        com4.sendData(np.asarray(Datagrama(tipo="2")))
        logserver.write("{}, envio, 2, 14 \n".format(Tempolocal()))
        cont = 1
        numPck = int.from_bytes(msgt1[3:4], "big")

        while cont <= numPck:
            print("Recebendo Pacote",cont)

            msgt3, nrx = com4.getData(10,2)
            totlen = nrx

            payload_len = int.from_bytes(msgt3[5:6], "big")
            payload, nrx = com4.getData(payload_len,2)
            totlen += nrx
            eop, nrx = com4.getData(4,2)
            totlen += nrx
            logserver.write("{}, envio, 3, {}, {}, {}\n".format(Tempolocal(), totlen, cont, numPck))
            print("Pacote {}/{}".format(cont,numPck), payload)
            n_pack = int.from_bytes(msgt3[4:5], "big")
            if msgt3[0:1] == b'\x03':
                msgt3 = Datagrama(tipo="6")
                if n_pack == cont:
                    if eop == b'\xFF\xAA\xFF\xAA':
                        start_timer1 = time.time()
                        start_timer2 = time.time()
                        cont += 1
                        com4.sendData(np.asarray(Datagrama(tipo="4")))
                        logserver.write("{}, envio, 4, 14 \n".format(Tempolocal()))
                        SaveImage.write(payload)
                    else:
                        print("EOP errado: esparado:{}, recebido:{}".format(b'\xFF\xAA\xFF\xAA', eop))
                else:
                    print("[ERRO]Número de pacote errado: esparado:{}, recebido:{}".format(cont, n_pack))
                    time.sleep(0.1)
                    com4.sendData(np.asarray(Datagrama(tipo="6", last_pack=cont)))
                    logserver.write("{}, envio, 6, 14 \n".format(Tempolocal()))
            else:
                time.sleep(1)
                print("Tempo passado do último envio:",time.time()-start_timer2)
                if time.time()-start_timer2 > 20:
                    ocioso = True
                    com4.sendData(np.asarray(Datagrama(tipo="5")))
                    logserver.write("{}, envio, 5, 14 \n".format(Tempolocal()))
                    print("¯\_(ツ)_/¯")
                    com4.disable()
                    exit()
                elif time.time()-start_timer1 > 2:
                    com4.sendData(np.asarray(Datagrama(tipo="4")))
                    logserver.write("{}, envio, 4, 14 \n".format(Tempolocal()))
                    start_timer1 = time.time()
                    erro = False

        SaveImage.close()
        logserver.close()
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com4.disable()        
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com4.disable()        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()