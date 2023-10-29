import pickle
import socket
from time import sleep
import time

class Cliente:
    def __init__(self, nome, ip):
        self.nome = nome
        self.ip  = ip
        self.ativo = False
        pass

    def recebeMensagem(self, clientSocket):
        while True:
            msg = pickle.loads(clientSocket.recv(1024))
            if msg != None:
                break	
        return msg

    def enviaMensagem(self, clientSocket, msg):
        try:
            clientSocket.send(pickle.dumps(msg))
            time.sleep(0.2)
        except:
            print(f'Falha ao enviar uma mensagem para {clientSocket}')

def recebeUsuario():
    nome = input('> Informe seu usuario ')
    ip = input('> Informe seu IP ')
    usuario = Cliente(nome, ip)
    return usuario

def imprimeListaUsuarios(listaUsuarios):
    for usuario in listaUsuarios:
        print(usuario)

if __name__ == "__main__":
    HOST = '127.0.0.1'
    porta =  9300

    print("------ Sistema de Videoconferencia ------")
    usuario = recebeUsuario()

    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    conexao.settimeout(None)
    print("Tentando a conexao com o Servidor")
    try:
        conexao.connect((HOST, porta))
        print(f"Conectado")
    except Exception as e:
        print("Conexao com o servidor falhou")
        sleep(2)
        quit()
    usuario.ativo = True

    while usuario.ativo:
        usuario.enviaMensagem(conexao, usuario.nome)
        listaUsuarios = usuario.recebeMensagem(conexao)
        imprimeListaUsuarios(listaUsuarios)

