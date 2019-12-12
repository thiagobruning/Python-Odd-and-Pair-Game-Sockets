import socket
from threading import Thread, Lock
import time

SALA = []
lock_jogada = Lock()
def temSala():
    for a in SALA:
        if(a.estaAberta()):
            return True
    return False

class Jogo:
    def __init__(self, salas=[]):
         self.salas = salas
         self.cont = 0
    def getCont(self):
        return self.cont
    def contProx(self):
        self.cont=self.cont+1

class Jogada:
    def __init__(self, jogador,jogada):
        self.jogador = jogador
        self.jogada = jogada
    
    def getJogador(self):
        return self.jogador
    
    def getJogada(self):
        return self.jogada

class Sala:
    def __init__(self, numero, jogadores=[],jogada=[]):
        self.numero = numero
        self.jogadores = jogadores
        self.jogada = jogada
        self.aberta = True
        self.situcao = "padrao"
        
    def getFirstJogador(self):
        return self.jogadores[0]

    def ganhador(self):
        if(len(self.jogadores)>= 2):
            if((self.jogada[0].jogada+self.jogada[1].jogada)%2 == 0):
                return "par"
            elif (self.jogada[0].jogada+self.jogada[1].jogada == 0):
                return "impar"
            else:
                return "impar"
        else:
            return "nada"

    def limparJogada(self):
        lock_jogada.acquire()

        self.jogada = []

        lock_jogada.release()

    def numJogadore(self):
        return  len(self.jogadores)

    def numJogada(self):
        return len(self.jogada)

    def addJogada(self,jogada):
        lock_jogada.acquire()
        pode = True
        for j in self.jogada:
            if j.jogador == jogada.getJogador():
                pode = False
        if pode:
            self.jogada.append(jogada)
        lock_jogada.release()
        
    def jogadorPar(self):
        if(self.situcao == "padrao"):
            self.situacao = "um jogou"
            return False
        elif(self.situacao == "um jogou"):
            self.situacao == "padrao"
            return True 

    def addJogador(self,jogador):
        lock_jogada.acquire()

        self.jogadores.append(jogador)
    
        lock_jogada.release()

    def fecharSala(self):
        self.aberta = False
    
    def estaAberta(self):
        return self.aberta
    
             
jogo = Jogo()
class Sockts(Thread):
    def __init__(self, addr, recurso):
        Thread.__init__(self)
        self.client_sock = recurso
        self.addr = addr
        self.numSala = -1
        print("SOCKET CRIADO!")
    def run(self):
        while True:
            try:
                data = self.client_sock.recv(BUFSIZ)
            except:
                break
            if not data or data.decode('utf-8') == 'END':
                break
            print("Received from client {}: {}".format(self.addr,data.decode('utf-8')))
            try:
                data = data.decode('utf-8')
                if(data == "info"):
                    if(temSala()):
                        msg = "temSala"
                    else:
                        msg = "naoTem"
                        if(len(SALA)>0):
                            msg = "semSala"
                    self.client_sock.send(msg.encode('utf-8'))   
                else:
                    comando = data.split("/")
                    msg = self.funcoes(comando)
                    self.client_sock.send(msg.encode('utf-8'))
                    time.sleep(2)
                    self.numSala = int(comando[1])
                    if self.numSala < len(SALA):
                        if(SALA[self.numSala]):
                            SALA[self.numSala].limparJogada()
            except KeyboardInterrupt:
                print("Exited by user")
        self.client_sock.close()
        print("Desconectado")
    def funcoes(self,comando):
        if comando[0] == "CRIAR_SALA":
            print("Estou criando uma SALA..")
            lock_jogada.acquire()
            SALA.append(Sala(jogo.getCont()))
            SALA[jogo.getCont()].addJogador(int(comando[1]))
            lock_jogada.release()
            msg  = "Sala \"{}\" criada com Sucesso! Você agora é Par".format(SALA[jogo.getCont()].numero)
            jogo.contProx()
        elif comando[0] == "ENTRA_NA_SALA":
            msg  = "Não tem nenhuma SALA aberta, crie a sua!"
            for s in SALA:
                if(not s.estaAberta()):
                    print(s.numero,"Não esta aberta")
                if(s.estaAberta()):
                    print(s.numero,"Esta Aberta")
                    s.addJogador(comando[1])
                    s.fecharSala()
                    msg = ("Você entrou na sala: \"{}\" ! Você agora é Impar".format(s.numero))
                    return msg
        elif comando[0] == "JOGO":
            self.numSala = int(comando[1])
            flag = True
            while SALA[self.numSala].numJogadore() > 0:
                jogada = int(comando[2])
                jogador = int(comando[3])
                SALA[self.numSala].addJogada(Jogada(jogador,jogada))

                if(SALA[self.numSala].numJogada() == 1 and flag):
                    print("Primeira Jogada Realizada")
                    flag = False
                if(SALA[self.numSala].numJogada()==2):
                    print("Segunda jogada realizada jogador:{}".format(jogador))
                    print("primeiro jogador:{}".format(SALA[self.numSala].getFirstJogador()))
                if(SALA[self.numSala].numJogada()>1):
                    if(SALA[self.numSala].ganhador() == "nada"):
                        "nada"
                    elif(SALA[self.numSala].ganhador() == "par"):
                        print("PAR",jogador,SALA[self.numSala].getFirstJogador(),jogador-SALA[self.numSala].getFirstJogador())
                    
                        if((jogador - SALA[self.numSala].getFirstJogador())==0):
                            return "Deu Par - Você Ganhou!"
                        else:
                            return "Deu Par - Você Perdeu!"
                    elif(SALA[self.numSala].ganhador() == "impar"):
                        print("IMPAR",jogador,SALA[self.numSala].getFirstJogador(),jogador-SALA[self.numSala].getFirstJogador())
                        if((jogador - SALA[self.numSala].getFirstJogador()) != 0):
                            return "Deu Impar - Você Ganhou!"
                        else:
                            return "Deu Impar - Você Perdeu!"
            jogador = None   
        else: 
            jogador = None 
            msg ="nada aconteceu"
        return msg  

HOST ="YOUR_IP"
BUFSIZ = 4024
cont=0


def Server(PORTA):
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ADDR = (HOST, int(PORTA))
    server_socket.bind(ADDR)
    server_socket.listen(5)
    #socket sera destruido apos uso
    server_socket.setsockopt( socket.SOL_SOCKET,socket.SO_REUSEADDR, 1 ) 
    while True:
        print('Server waiting for connection...')
        client_sock, addr = server_socket.accept()
        print('Client connected from: ', addr)
        recurso = client_sock
        sockets = Sockts(addr,recurso)
        sockets.start()
        
    server_socket.close()