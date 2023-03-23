import zlib

def Datagrama(tipo="", npacks=00, num_pack=00, file_id=00, payload_len=00, error_pack=00, last_pack=00, crc=00, payload=b''):
    eop = b'\xFF\xAA\xFF\xAA'
    crc = zlib.crc32(payload)
    #transforma o crc em bytes
    crc = crc.to_bytes(2, byteorder='big')

    if tipo == "1":        
        mensagem = [1, 00, 15, npacks, num_pack, file_id, error_pack, last_pack, 00, 00]
        mensagem = bytes(mensagem)
        mensagem += payload
        mensagem += eop
    elif tipo == "2":
        mensagem = [int(tipo[0]), 00, 00, npacks, num_pack, payload_len, error_pack, last_pack, 00, 00]
        mensagem = bytes(mensagem)
        mensagem += payload
        mensagem += eop
    else:
        mensagem = [int(tipo[0]), 00, 00, npacks, num_pack, payload_len, error_pack, last_pack, crc, 00]
        mensagem = bytes(mensagem)
        mensagem += payload
        mensagem += eop
        
    return mensagem
    
def Pack(info):
    lista=[info[i:i+114] for i in range(0, len(info), 114)]
    return lista
