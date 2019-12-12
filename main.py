from cliente import Cliente
from servidor import Server

if __name__ == '__main__':
    while True:
        print("PAR OU IMPAR")
        print("1 -INICAR SERVIDOR")
        print("2 - INICIAR CLIENTE")

        opcao = int(input("Opcao: "))
        if(opcao == 1):
            porta = input("Qual a porta: ")
            Server(porta)
        elif(opcao == 2):
            porta = input("Qual a porta: ")
            Cliente(porta)
        else:
            print("DIGITE UMA OPÇÃO VALIDA!")