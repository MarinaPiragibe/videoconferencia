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


  def verificarCliente(self, cliente):

    print(cliente, servidor.listaClientes, cliente not in servidor.listaClientes)
    estaNaLista = list(filter(lambda x: x.nome == cliente.nome and x.ip == cliente.ip, servidor.listaClientes))
    
    if not estaNaLista:
      print(f'Cliente registrado:\n> NOME: {cliente.nome} \n> IP: {cliente.ip} \n> PORTA: ')
      servidor.listaSockets.append(socketCliente)
      servidor.listaClientes.append(cliente)
      return True
    
    else:
      print("Erro no registro. O cliente já está cadastrado no Sistema\n")
      return False

  def registrarNovoCliente(self, socketCliente, cliente):
    conectado = True
    while conectado:
      conectado = Utils.menuServidor(servidor, socketCliente, cliente)

    else:
      return conectado


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

  print("\n################### Servidor Iniciado ###################\n")

  while servidor.ativo:
  
    socketCliente, endereco = conexao.accept()

    cliente = servidor.recebeMensagem(socketCliente)
    print("------------- Iniciando Registro --------------")

    if (servidor.verificarCliente(cliente)):
      print("------------ Finalizando Registro -------------")
      servidor.enviaMensagem(socketCliente, True)
      thread = threading.Thread(target=servidor.registrarNovoCliente, args=[socketCliente, cliente])
      thread.start()
      
    else:
      print("------------ Finalizando Registro -------------")
      servidor.enviaMensagem(socketCliente, False)

    Utils.imprimeListaClientes(servidor.listaClientes)
