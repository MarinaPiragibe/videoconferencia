
def buscaClienteServidor(parametroBusca, servidor, socketCliente):

  encontrado = False
  valorProcurado = servidor.recebeMensagem(socketCliente)
  print(f"Buscando o cliente com {parametroBusca} igual a {valorProcurado}\n")
  for cliente in servidor.listaClientes:
    if (hasattr(cliente, parametroBusca)):
      if (getattr(cliente, parametroBusca) == valorProcurado):
        encontrado = True
        servidor.enviaMensagem(socketCliente, cliente)
  if(not encontrado):
    servidor.enviaMensagem(socketCliente, [])


def menuServidor(servidor, socketCliente, cliente):

  escolhaDoCliente = servidor.recebeMensagem(socketCliente)

  if escolhaDoCliente == "listagem":
    servidor.enviaMensagem(socketCliente, servidor.listaClientes)

  elif escolhaDoCliente == "nome" or escolhaDoCliente == "ip":

    buscaClienteServidor(escolhaDoCliente, servidor, socketCliente)

  elif escolhaDoCliente == "desligar":

    try:
      servidor.enviaMensagem(socketCliente, "Sua conexão foi encerrada com sucesso. Adeus!")
      print("Desconectando o cliente ", cliente.nome, "\n")
      socketCliente.close()
      servidor.listaSockets.remove(socketCliente)
      servidor.listaClientes.remove(cliente)
      return False
    
    except:
      servidor.enviaMensagem(socketCliente,"Erro ao encerrar a conexão. Tente novamente")
      print("Erro ao desconectar o cliente")

  return True
