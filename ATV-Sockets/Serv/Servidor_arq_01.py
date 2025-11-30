import socket , os 

Host = ''
Port = 60000

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((Host,Port))

status1 = 1 ; status0 = 0 # Duas variáveis para status, em bytes
status1 = status1.to_bytes(1,'big') ; status0 = status0.to_bytes(1,'big')
solicit = 64
while solicit > 0:
    print('On-line...Esperando...')
    Tam_nome_arq, cliente = udp_socket.recvfrom(1) # Recebe len do nome
    Tam_nome_arq = int.from_bytes(Tam_nome_arq,"big") # byte para inteiro
    print("len do nome do arquivo requisitado: ", Tam_nome_arq)

    nome_arq, cliente = udp_socket.recvfrom(Tam_nome_arq) # Recebe nome do arquivo
    nome_arq = nome_arq.decode("utf-8") # bytes para str
    print("Arquivo requisitado: ", nome_arq)

    try: 
        if os.path.isfile(nome_arq) == True: # Se arquivo existir:
            udp_socket.sendto(status1, (cliente)) # send status 1
            tam_arq = os.path.getsize(nome_arq) # Obtem tamnho do arquivo
            tam_arq_b = tam_arq.to_bytes(4,"big") # str para bytes
            udp_socket.sendto(tam_arq_b, (cliente)) # send tamanho do arquivo
            solicit -=1
            with open (f"{nome_arq}", 'rb') as arquivo:
                while tam_arq > 0:
                    a_enviar = arquivo.read(4096)
                    udp_socket.sendto(a_enviar, (cliente))
                    tam_arq -= 4096
        else: 
            udp_socket.sendto(status0, (cliente))
            solicit -=1
    except:
        udp_socket.sendto(status0, (cliente))
        solicit -=1
udp_socket.close()
print('Fim Servidor')
