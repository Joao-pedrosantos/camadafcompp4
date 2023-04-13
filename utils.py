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
        if payload_len > 0:
                crc_total = crc16.xmodem(payload)
                print("CRC total:", crc_total)
                crc = crc_total.to_bytes(2, byteorder='big')
                print("CRC:", crc)
                lencr = len(str(crc_total))
                crc1 = str(crc_total)[:lencr//2]
                crc1 = int(crc1).to_bytes(1, byteorder='big')
                crc2 = str(crc_total)[lencr//2:]
                crc2 = int(crc2).to_bytes(1, byteorder='big')
                print("CRC1:", crc1)
                print("CRC2:", crc2)
                

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