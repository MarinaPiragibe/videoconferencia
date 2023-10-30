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

  def configurarNovoCliente(self, cliente, endereco):
    servidor.listaSockets.append(cliente)

    usuario = servidor.recebeMensagem(cliente)
    servidor.listaClientes.append(usuario)
    Utils.imprimeListaUsuarios(servidor.listaClientes)

    conectado = True
    while conectado:
      msg = servidor.recebeMensagem(cliente)
      if msg == "listagem":
        servidor.enviaMensagem(cliente, servidor.listaClientes)
      
      if msg == "buscarNome":
        clienteProcurado = servidor.recebeMensagem(cliente)
        print("Buscando o cliente ", clienteProcurado, "\n")
        for p in servidor.listaClientes:
          if (p.nome == clienteProcurado):
            servidor.enviaMensagem(cliente, p)
        servidor.enviaMensagem(cliente, [])
      if msg == "desligar":
        try:
          cliente.close()
          print("Desconectando o cliente ", usuario.nome, "\n")
          servidor.listaSockets.remove(cliente)
          servidor.listaClientes.remove(usuario)
          conectado = False
        except:
          print("Erro ao desconectar o cliente")
          break

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

    cliente, endereco = conexao.accept()
    thread = threading.Thread(target=servidor.configurarNovoCliente,
                              args=[cliente, endereco])
    thread.start()
