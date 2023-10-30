import socket
import time
import pickle
import Utils
import threading


class Servidor:

  def __init__(self):

    self.HOST = '127.0.0.1'
    self.PORTA = 9300
    self.listaSockets = []
    self.listaClientes = []
    self.ativo = False

  def configurarNovoSocketCliente(self, socketCliente, endereco):
    servidor.listaSockets.append(socketCliente)

    cliente = servidor.recebeMensagem(socketCliente)
    servidor.listaClientes.append(cliente)
    Utils.imprimeListaClientes(servidor.listaClientes)

    conectado = True
    while conectado:
      conectado = Utils.menuServidor(servidor, socketCliente, cliente)

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
  print("\n-------------------- Servidor Iniciado --------------------")
  while servidor.ativo:
    print("Lista de conexões")

    socketCliente, endereco = conexao.accept()
    thread = threading.Thread(target=servidor.configurarNovoSocketCliente, args=[socketCliente, endereco])
    thread.start()
