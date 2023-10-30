import pickle
import socket
from time import sleep

import Utils


class Cliente:

  def __init__(self, nome, ip):
    self.nome = nome
    self.ip = ip
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
      sleep(0.2)
    except:
      print(f'Falha ao enviar uma mensagem para {clientSocket}')


if __name__ == "__main__":
  HOST = '127.0.0.1'
  porta = 9300

  print(
      "\n\n################ Sistema de Videoconferencia ################\n\n")
  cliente = Utils.recebeCliente()

  conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  conexao.settimeout(None)
  print("Fazendo a conexão com o Servidor....")
  try:
    conexao.connect((HOST, porta))
    print(f"Conectado!")
  except Exception as e:
    print("Conexao com o servidor falhou")
    sleep(2)
    quit()
  cliente.ativo = True

  while cliente.ativo:
    cliente.enviaMensagem(conexao, cliente)
    Utils.menuCliente(conexao, cliente)

