import random
import time


def Datagrama(tipo="", npacks=00, num_pack=00, file_id=00, payload_len=00, error_pack=00, last_pack=00, crc=00, payload=b''):
    eop = b'\xFF\xAA\xFF\xAA'
    if tipo == "1":
        mensagem = [1, 00, 15, npacks, num_pack, file_id, error_pack, last_pack, crc, crc]
        mensagem = bytes(mensagem)
        mensagem += payload
        mensagem += eop

    elif tipo == "2":
        mensagem = [2, 00, 00, npacks, num_pack, payload_len, error_pack, last_pack, crc, crc]
        mensagem = bytes(mensagem)
        mensagem += payload
        mensagem += eop

    elif tipo == "3":
        mensagem = [3, 00, 00, npacks, num_pack, payload_len, error_pack, last_pack, crc, crc]
        mensagem = bytes(mensagem)
        mensagem += payload
        mensagem += eop

    elif tipo == "4":
        mensagem = [4, 00, 00, npacks, num_pack, payload_len, error_pack, last_pack, crc, crc]
        mensagem = bytes(mensagem)
        mensagem += payload
        mensagem += eop

    elif tipo == "5":
        mensagem = [5, 00, 00, npacks, num_pack, payload_len, error_pack, last_pack, crc, crc]
        mensagem = bytes(mensagem)
        mensagem += payload
        mensagem += eop

    elif tipo == "6":
        mensagem = [6, 00, 00, npacks, num_pack, payload_len, error_pack, last_pack, crc, crc]
        mensagem = bytes(mensagem)
        mensagem += payload
        mensagem += eop
        
    return mensagem
    
def Pack(info):
    lista=[info[i:i+114] for i in range(0, len(info), 114)]
    return lista

def Teste(cont):
    i = random.randint(0,100)
    if i<3 and cont<141-7:
        return cont+random.randint(2,7)
    else:
        return cont+1

def Tempolocal():
    return time.asctime(time.localtime())