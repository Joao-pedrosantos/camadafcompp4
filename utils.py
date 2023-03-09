def Datagrama(tipo="", npacks=00, num_pack=00, file_id=00, payload_len=00, error_pack=00, last_pack=00, crc=00, payload=b''):
    eop = b'\xAA\xBB\xCC\xDD'
    if tipo == "data":
        mensagem = [2, 00, 00, npacks, num_pack, payload_len+1, error_pack, last_pack, crc, crc]
        mensagem = bytes(mensagem)
        mensagem += payload
        mensagem += eop
        
    elif tipo == "handshake":
        mensagem = [1, 00, 00, npacks, num_pack, file_id, error_pack, last_pack, crc, crc]
        mensagem = bytes(mensagem)
        mensagem += payload
        mensagem += eop
        
    return mensagem
    
def Pack(info):
    lista=[info[i:i+114] for i in range(0, len(info), 114)]
    return lista