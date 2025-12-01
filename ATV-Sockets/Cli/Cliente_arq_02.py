from encodings import utf_8
import socket

HOST = ' 192.168.56.1'
PORT = 60000

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

nome_arq_str = input ("Digite o nome do arquivo desejado: ") # Recebe nome do arquivo
nome_arq = nome_arq_str.encode('utf-8') # Nome do arquivo para bytes

tamanho = len(nome_arq) # Obtem len do nome do arquivo
tamanho = tamanho.to_bytes(1,'big') # tamanho em um byte

udp_socket.sendto(tamanho, (HOST,PORT)) # send len do nome
udp_socket.sendto(nome_arq, (HOST,PORT)) # send nome

data, src = udp_socket.recvfrom(1) # Recebe o STATUS 0 ou 1 em 1 byte
data = int.from_bytes(data,"big") # byte para inteiro
print ('Status de: ' , src , '-->' , data)

if data == 1: 
    data, src = udp_socket.recvfrom(4) # Recebe tamanho do arquivo
    tam_arq =  int.from_bytes(data,'big') # byte para inteiro
    T_a_gravar = tam_arq
    bytes_do_arq = b"" # Armazenara os todos os bytes do arquivo
    while T_a_gravar > 0:
        data, src = udp_socket.recvfrom(4096)
        bytes_do_arq += data
        T_a_gravar -= 4096
        
    with open(f"{nome_arq_str}", "wb") as arquivo : # Escreve arquivo
        arquivo.write(bytes_do_arq)
        
else:
    print("Arquivo não encontrado.")

udp_socket.close()
print('Fim Cliente')


