import socket
import random


def Cliente(PORTA):
    HOST = "YOUR_IP"
    BUFSIZ = 4096
    ADDR = (HOST,int(PORTA))
    id = random.getrandbits(32)
    client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_sock.connect(ADDR)
    jogar = False
    msg = "info"
    client_sock.send(msg.encode('utf-8'))
    resposta = client_sock.recv(BUFSIZ)
    resp1 = resposta.decode('utf-8')
    if(resp1 == "temSala"):
        jogar = True
    elif(resp1 == "semSala"):
        print("Servidor indisponivel no momento tente novamente")
        return
   
    print("Id do jogador: {}".format(id))
    continua=True
    try:
        while continua:
            if not jogar:
                dados = ("CRIAR_SALA/{}".format(id))
            else:
                dados = ("ENTRA_NA_SALA/{}".format(id))
            
            client_sock.send(dados.encode('utf-8'))
            resposta = client_sock.recv(BUFSIZ)
            if not resposta:
                break
            resp = resposta.decode('utf-8')
            print("Received from server:", resp)
            if("Você entrou na sala" in resp or "criada com Sucesso!" in resp):
                
                split = resp.split("\"")
                sala = split[1]
                split = split[2].split("!")
                if(len(split)>0):
                    par = split[1]
                jogando = True
                while jogando:
                    print("---------------QUAL A SUA JOGADA-----------------")
                    print(par)
                    jogada = int(input("Jogada: "))
                    if(jogada < 11):
                        dados = ("JOGO/{}/{}/{}".format(sala,jogada,id))
                    client_sock.send(dados.encode('utf-8'))
                    resp = ""
                    while not "Perdeu" in resp and not "Ganhou" in resp:
                        resposta = client_sock.recv(BUFSIZ)   
                        if not resposta:
                            break
                        resp = resposta.decode('utf-8')
                        print("Received from server:", resp) 
            continuar = input("Continuar[s/n]?")
            if(continuar.lower()=="n"):
                client_sock.send(b"END")
                continua=False

    except KeyboardInterrupt:
        print("Ok, saindo!!")

    client_sock.close()    
    