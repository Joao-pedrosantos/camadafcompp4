def Datagrama(tipo, npacks=00, num_pack=00, file_id=00, payload_len=00, error_pack=00, last_pack=00, crc=00, payload=b''):
    eop = b'\xAA\xBB\xCC\xDD'
    final = payload + eop
    if tipo == 1:#é o handshake
        mensagem = (bytes([tipo, 69, 00, npacks, num_pack, file_id, error_pack, last_pack, crc, crc]) + (final))
        
    else:
        mensagem = (bytes([tipo, 00, 00, npacks, num_pack, payload_len+1, error_pack, last_pack, crc, crc]) + (final))

    return mensagem
    
def Pack(info):
    lista=[info[i:i+114] for i in range(0, len(info), 114)]
    return lista