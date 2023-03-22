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
        com3 = enlace('/dev/ttyACM0')
        com3.enable()
        print("ON")
        imageR = "./imgs/image.png"
        logclient = "./logs/client1.txt"
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
                    print("Enviando pacote de início")
                    com3.sendData(np.asarray(Datagrama(tipo="1", npacks=numPck)))
                    print("Enviei pacote de início")
                    logclient.write("{}, envio, 1, 14 \n".format(Tempolocal()))
                    print("Escrevi o log")
                    msgt1, nrx = com3.getData(14)
                    logclient.write("{}, recebe, {}, {}\n".format(Tempolocal(),str(msgt1[0:1]), len(msgt1)))
                    print("Escrevi o log 2")
                    validado = msgt1[0:1] == b'\x02'
                    print("Validação: ", validado)
                elif pergunta == 'n':
                    print("Encerrando comunicação...")
                    logclient.close()
                    com3.disable()
                    exit()          
            else:
                inicia = True
        #Enviando dados
        cont = 1
 
        while cont <= numPck:
            #print("Enviando Pacote", cont)
            pacote = Datagrama(tipo="3", npacks=numPck, num_pack=cont, payload_len=len(packs[cont-1]), payload=packs[cont-1])
            com3.sendData(np.asarray(pacote))
            logclient.write("{}, envio, 3, {}, {}, {}\n".format(Tempolocal(), len(pacote), cont, numPck))
            print(f"Escrevi o log de envio do pacote: {cont}")
            print("Pacote {}/{}".format(cont,numPck), pacote)
            start_timer1 = time.time()
            start_timer2 = time.time()
            fudeu = 0
            
            if com3.rx.getBufferLen()<14:
                print("Esperando resposta do servidor...")
                while com3.rx.getBufferLen()<14:
                    if time.time()-start_timer2 > 20:
                        com3.sendData(np.asarray(Datagrama(tipo="5")))
                        logclient.write("{}, envio, 5, 14 \n".format(Tempolocal()))
                        com3.disable()
                        print("Tempo de espera excedido. Encerrando comunicação...")
                        exit()
                    elif time.time()-start_timer1 > 5:
                        fudeu +=1
                        print("Tentando reconectar...")
                        pacote = Datagrama(tipo="3", npacks=numPck, num_pack=cont, payload_len=len(packs[cont-1]), payload=packs[cont-1])
                        com3.sendData(np.asarray(pacote))
                        logclient.write("{}, envio, 3, {}, {}, {}\n".format(Tempolocal(), len(pacote), cont, numPck))
                        print(f"Escrevi o log de envio do pacote: {cont}")
                        print("Pacote {}/{}".format(cont,numPck), pacote)
                        start_timer1 = time.time()
                        start_timer2 = time.time()
                        if fudeu == 3:
                            print("Tentativas excedidas. Encerrando comunicação...")
                            com3.disable()
                            exit()
                    else:
                        pass
            msgt4, nRx = com3.getData(14)
            

            logclient.write("{}, recebe, {}, {}\n".format(Tempolocal(),str(msgt4[0:1]), len(msgt4)))
            print(f"Escrevi o log de recebimento do pacote: {cont}. Estamos {cont/numPck*100}% prontos.")     


            if msgt4[0:1] == b'\x04':
                cont += 1
                msgt4 = Datagrama(tipo = "6") 
            
            else:
                erro = True
                print("Servidor acusou erro no pacote. Tentando reenviar...")

                while erro == True:


                    if time.time()-start_timer2 > 20:
                        com3.sendData(np.asarray(Datagrama(tipo="5")))
                        logclient.write("{}, envio, 5, 14 \n".format(Tempolocal()))
                        com3.disable()
                        print("Tempo de espera excedido. Encerrando comunicação...")
                                           
                    elif time.time()-start_timer1 > 5:
                        print("Tentando reconectar...")
                        pacote = Datagrama(tipo="3", npacks=numPck, num_pack=cont, payload_len=len(packs[cont-1]), payload=packs[cont-1])
                        com3.sendData(np.asarray(pacote))
                        logclient.write("{}, envio, 3, {}, {}, {}\n".format(Tempolocal(), len(pacote), cont, numPck))
                        print(f"Tentei reenviar o pacote {cont}")
                        start_timer1 = time.time()
                    else:
                        pacote = Datagrama(tipo="3", npacks=numPck, num_pack=cont, payload_len=len(packs[cont-1]), payload=packs[cont-1])
                        com3.sendData(np.asarray(pacote))
                        logclient.write("{}, envio, 3, {}, {}, {}\n".format(Tempolocal(), len(pacote), cont, numPck))
                        print(f"Tentei reenviar o pacote {cont}")
                        if com3.rx.getIsEmpty() == False:
                            msgt6, nRx = com3.getData(14)
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
                    
                        
                            if msgt6[0:1] == b'\x04':
                                cont += 1
                                print("ta certo")
                                erro = False

                        else:
                            print("ainda ta zuado")
                            print("Tentar de novo pq ninguem é de ferro")
                            erro = True




        

        
         
    
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