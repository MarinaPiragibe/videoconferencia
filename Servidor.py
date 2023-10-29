import socket
import time
import pickle
import Utils

class Servidor:
    def __init__(self):

        self.HOST = '127.0.0.1'
        self.PORTA = 9300
        self.listaSockets = []
        self.listaClientes = []
        self.ativo = False

    def recebeMensagem(self, clientSocket):
        while True:
            msg = pickle.loads(clientSocket.recv(1024))
            if msg != None:
                break	
        return msg

    def enviaMensagem(self, clientSocket, msg):
        try:
            clientSocket.sendall(pickle.dumps(msg))
            time.sleep(0.2)
        except:
            print(f'Falha ao enviar uma mensagem para {clientSocket}')


if __name__ == "__main__":
    servidor = Servidor()
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    conexao.settimeout(None)
    try:
        conexao.bind((servidor.HOST, servidor.PORTA))
        conexao.listen()
    except:
        print("Nao foi possivel conectar o Servidor")
        exit
    servidor.ativo = True

    while servidor.ativo:
        print("Lista de conexões")

        cliente, endereco = conexao.accept()
        servidor.listaSockets.append(cliente)

        usuario= servidor.recebeMensagem(cliente)
        servidor.listaClientes.append(usuario)
        Utils.imprimeListaUsuarios(servidor.listaClientes)

        servidor.enviaMensagem(cliente,servidor.listaClientes)


    