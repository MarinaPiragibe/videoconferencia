from time import sleep
import socket
from Cliente import Cliente
import threading
from vidstream import AudioReceiver
from vidstream import AudioSender


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
  print("5 - Iniciar chamada com outro cliente")
  print("6 - Responder a chamado do outro Cliente")
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
      print("Cliente com esse IP não encontrado! Tente novamente\n")

  elif (resposta == 4):
    cliente.enviaMensagem(conexao, "desligar")
    mensagem = cliente.recebeMensagem(conexao)
    print(mensagem)
    conexao.close()
    sleep(2)
    quit()

  #Fazendo ainda
  elif (resposta == 5):
    ipContato = input("Digite o IP que deseja trocar mensagem ?\n")
    portaContato = input("Digite a porta que deseja trocar mensagem ?\n")
    conexaoChamada = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexaoChamada.settimeout(None)
    conexaoChamada.connect((str(ipContato), int(portaContato)))
    cliente.enviaMensagem(conexaoChamada, f"Chamada do cliente {cliente.nome}")
    print("Aguardando resposta do cliente .......\n")
    resposta = cliente.recebeMensagem(conexaoChamada)
    if (resposta == "A"):
      print("Iniciando a  chamada.......\n")
      portaVideoTransmissao = cliente.recebeMensagem(conexaoChamada)
      portaAudioTransmissao = cliente.recebeMensagem(conexaoChamada)
      portaVideo = int(
          input("Qual porta deseja usar para receber o video ?\n"))
      cliente.enviaMensagem(conexaoChamada, portaVideo)
      portaAudio = int(
          input("Qual porta deseja usar para receber o audio ?\n"))
      cliente.enviaMensagem(conexaoChamada, portaAudio)
      reciver = AudioReceiver('192.168.0.71',int(portaAudio) )
      reciver_thread = threading.Thread(target=reciver.start_server)
      sender = AudioSender('192.168.0.71', int(portaAudioTransmissao))
      sender_thread = threading.Thread(target=sender.start_stream)
      reciver_thread.start()
      sender_thread.start()
      #Audio SENDER
      #Audio Reciver
      #video SENDER
    if(resposta == "R"):
      print("Chamada Recusada, tente novamente....... \n")
      cliente.ocupado = False
    # conexaoChamada.close()

  elif (resposta == 6):
    conexaoChamada = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexaoChamada.bind((str(cliente.ip), int(cliente.porta)))
    conexaoChamada.listen()
    socketClienteChamada, endereco = conexaoChamada.accept()

    print(socketClienteChamada)
    msg = cliente.recebeMensagem(socketClienteChamada)
    print(msg)

    cliente.ocupado = True
    resposta = str(input("Deseja aceitar (A) ou recusar (R) a chamada ??\n"))
    cliente.enviaMensagem(socketClienteChamada, resposta)
    if (resposta == "A"):
      print("Iniciando a  chamada.......\n")
      portaVideo = int(
          input("Qual porta deseja usar para receber o video ?\n"))
      cliente.enviaMensagem(socketClienteChamada, portaVideo)
      portaAudio = int(
          input("Qual porta deseja usar para receber o audio ?\n"))
      cliente.enviaMensagem(socketClienteChamada, portaAudio)
      portaVideoTransmissao = cliente.recebeMensagem(socketClienteChamada)
      portaAudioTransmissao = cliente.recebeMensagem(socketClienteChamada)
      reciver = AudioReceiver('192.168.0.71',int(portaAudio) )
      reciver_thread = threading.Thread(target=reciver.start_server)
      sender = AudioSender('192.168.0.71', int(portaAudioTransmissao))
      sender_thread = threading.Thread(target=sender.start_stream)
      reciver_thread.start()
      sender_thread.start()
      #Audio SENDER
      #Audio Reciver
      #video SENDER
      #Thread desses cara
      #Tentar mudar logica do recebimento de chamada..... (Foco nos primeiros itens)
    if(resposta == "R"):
      print("Chamada recusada.......\n")
      cliente.ocupado = False
    # conexaoChamada.close()
    # socketClienteChamada.close()


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
    servidor.enviaMensagem(socketCliente, [])

  elif msg == "buscarIP":

    ipClienteProcurado = servidor.recebeMensagem(socketCliente)
    print("Buscando o cliente ", ipClienteProcurado, "\n")
    for cliente in servidor.listaClientes:
      if (cliente.ip == ipClienteProcurado):
        servidor.enviaMensagem(socketCliente, cliente)
    servidor.enviaMensagem(socketCliente, [])

  elif msg == "desligar":

    try:
      servidor.enviaMensagem(socketCliente,
                             "Sua conexão foi encerrada com sucesso. Adeus!")
      print("Desconectando o cliente ", cliente.nome, "\n")
      socketCliente.close()
      servidor.listaSockets.remove(socketCliente)
      servidor.listaClientes.remove(cliente)
      return False
    except:
      servidor.enviaMensagem(socketCliente,
                             "Erro ao encerrar a conexão. Tente novamente")
      print("Erro ao desconectar o cliente")

  return True
