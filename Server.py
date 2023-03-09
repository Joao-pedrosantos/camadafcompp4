from enlace import *
import time
import numpy as np
from utils import *

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com4 = enlace('COM5')
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com4.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Servidor Online")

        #aqui você deverá gerar os dados a serem transmitidos. 
        imageW = "./img/Img_recebida.png"
        SaveImage = open(imageW, 'wb')

        BufferRx, nrx = com4.getData(15)
 
        print(BufferRx)

        txLen = BufferRx[10:11]
        time.sleep(0.01)
        com4.sendData(np.asarray(txLen))

        PacksLen = int.from_bytes(txLen, "big")-1
        print("Recebendo dados...")
        num_pack = -1
        num_pack_v = 0
        while num_pack < PacksLen:
            head, nRx = com4.getData(10)
            txLen = int.from_bytes(head[5:6], "big")
            print("txLen",txLen)

            package, nRx = com4.getData(txLen)
            eop, nRx = com4.getData(4)
            print("EOP", eop)
            num_pack = int.from_bytes(head[4:5], "big")
            print("Pacote {}/{} Enviado:".format(num_pack, PacksLen),package)
            time.sleep(0.01)

            if num_pack == num_pack_v and eop == b'\xde\xee\xeeU':
                num_pack_v += 1
                com4.sendData(np.asarray(Datagrama(tipo="data", payload=b'\x01')))
            else:
                com4.sendData(np.asarray(Datagrama(tipo="data", payload=b'\x00')))
            SaveImage.write(package)

        SaveImage.close()
    
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