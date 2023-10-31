from time import sleep
from Cliente import Cliente


def recebeCliente():
  print("\n------------- Login --------------")
  nome = input('> Informe seu usuário: ')
  ip = input('> Informe seu IP: ')
  porta = input('> Informe a porta: ')
  cliente = Cliente(nome, ip, porta)
  return cliente


def imprimeListaClientes(listaClientes):
  print("\n--------- Lista de Usuários Cadastrados ---------")
  for cliente in listaClientes:
    print("\n")
    print(f'> NOME: {cliente.nome}')
    print(f'> IP: {cliente.ip}')
    print(f'> PORTA: {cliente.porta}')
    print("---------------")

def menuCliente(conexao, cliente):
  print("\n-------------------- Menu --------------------")
  print("Escolha uma opção: \n")
  print("1 - Lista todas os usuários cadastrados")
  print("2 - Buscar pelo nome de um usuário")
  print("3 - Buscar pelo ip de um usuário")
  print("4 - Desligar conexão com servidor e sair")
  resposta = int(input("\n> "))

  if (resposta == 1):
    cliente.enviaMensagem(conexao, "listagem")
    listaClientes = cliente.recebeMensagem(conexao)
    imprimeListaClientes(listaClientes)

  elif (resposta == 2):
    cliente.enviaMensagem(conexao, "buscarNome")

    nomeProcurado = input("Digite o nome do Cliente que deseja procurar: ")
    print(f'\nProcurando NOME: {nomeProcurado} ...')
    cliente.enviaMensagem(conexao, nomeProcurado)
    clienteProcurado = cliente.recebeMensagem(conexao)
    if (clienteProcurado != []):
      print(
          f"\nCliente encontrado! \n > NOME: {clienteProcurado.nome}\n > IP: {clienteProcurado.ip}\n > PORTA: {cliente.porta}\n"
      )
    else:
      print("\nCliente com esse nome não encontrado! Tente novamente\n")

  elif (resposta == 3):
    cliente.enviaMensagem(conexao, "buscarIP")

    ipProcurado = input("Digite o ip do Cliente que deseja procurar: ")
    print(f'\nProcurando IP: {ipProcurado} ...')
    cliente.enviaMensagem(conexao, ipProcurado)
    clienteProcurado = cliente.recebeMensagem(conexao)
    if (clienteProcurado != []):
      print(
          f"\nCliente encontrado! \n > NOME: {clienteProcurado.nome}\n > IP: {clienteProcurado.ip}\n > PORTA: {cliente.porta}\n"
      )
    else:
      print("Cliente com esse nome não encontrado! Tente novamente\n")

  elif (resposta == 4):
    cliente.enviaMensagem(conexao, "desligar")
    mensagem = cliente.recebeMensagem(conexao)
    print(mensagem)
    sleep(2)
    conexao.close()
    quit()

def menuServidor(servidor, socketCliente, cliente):
  msg = servidor.recebeMensagem(socketCliente)

  if msg == "listagem":
    servidor.enviaMensagem(socketCliente, servidor.listaClientes)
  
  elif msg == "buscarNome":

    nomeClienteProcurado = servidor.recebeMensagem(socketCliente)
    print("Buscando o cliente ", nomeClienteProcurado, "\n")
    for cliente in servidor.listaClientes:
      if (cliente.nome == nomeClienteProcurado):
        servidor.enviaMensagem(socketCliente, cliente)

  elif msg == "buscarIP":

    ipClienteProcurado = servidor.recebeMensagem(socketCliente)
    print("Buscando o cliente ", ipClienteProcurado, "\n")
    for cliente in servidor.listaClientes:
      if (cliente.ip == ipClienteProcurado):
        servidor.enviaMensagem(socketCliente, cliente)
    servidor.enviaMensagem(socketCliente, [])

  elif msg == "desligar":

    try:
      servidor.enviaMensagem(socketCliente, "Sua conexão foi encerrada com sucesso. Adeus!")
      print("Desconectando o cliente ", cliente.nome, "\n")
      socketCliente.close()
      servidor.listaSockets.remove(socketCliente)
      servidor.listaClientes.remove(cliente)
      return False
    except:
      servidor.enviaMensagem(socketCliente, "Erro ao encerrar a conexão. Tente novamente")
      print("Erro ao desconectar o cliente")
  
  return True
  