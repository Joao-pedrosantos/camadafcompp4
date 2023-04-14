import random
import time
from fastcrc import crc16


def Datagrama(tipo="", npacks=00, num_pack=00, file_id=00, payload_len=00, error_pack=00, last_pack=00, crc=00, payload=b''):
    eop = b'\xFF\xAA\xFF\xAA'

    if tipo == "1":
        mensagem = [1, 00, 15, npacks, num_pack, file_id, error_pack, last_pack, crc, crc]
        mensagem = bytes(mensagem)
        mensagem += payload
        mensagem += eop

    else:

        crc1, crc2 = cria_crc(payload, payload_len)
        mensagem = [int(tipo[0]), 00, 00, npacks, num_pack, payload_len, error_pack, last_pack, crc1, crc2]
        mensagem = bytes(mensagem)
        mensagem += payload
        mensagem += eop
        
    return mensagem
    
def Pack(info):
    lista=[info[i:i+114] for i in range(0, len(info), 114)]
    return lista

def Tempolocal():
    return time.asctime(time.localtime())


def cria_crc(msg,msg_len):
    if msg_len == 0:
        crc1 = crc2 = 11
    else:
        crc = crc16.xmodem(msg)
        crc //= 10
        if crc == 0:
            crc = 10
        lencr = len(str(crc))
        crc1 = int(str(crc)[:lencr//2])
        crc2 = int(str(crc)[lencr//2:])
    return crc1, crc2