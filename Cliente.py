import pickle
import socket
from time import sleep
import Utils


class Cliente:

  def __init__(self, nome, ip, porta):
    self.nome = nome
    self.ip = ip
    self.porta = porta
    self.ativo = False

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

  print("\n\n################ Sistema de Videoconferencia ################\n\n")
  #Cria objeto Cliente com os parametros inseridos
  cliente = Utils.recebeCliente()

  conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  conexao.settimeout(None)

  print("\nFazendo a conexão com o Servidor....")

  try:
    #Tenta conectar com o servidor
    conexao.connect((HOST, porta))
  except Exception as e:
    print("\nConexao com o servidor falhou")
    sleep(2)
    quit()

  cliente.ativo = True

  while cliente.ativo:

    cliente.enviaMensagem(conexao, cliente)
    registro = cliente.recebeMensagem(conexao)

    if not registro:
      print("Erro ao registrar sseu usuário. Verifique se já não foi cadastrado antes.")
      cliente.ativo = False
      break
    
    print("Usuário registrado com sucesso!")
    Utils.menuCliente(conexao, cliente)

