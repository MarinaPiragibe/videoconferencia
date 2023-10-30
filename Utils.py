from Cliente import Cliente


def recebeUsuario():
  print("\n------------- Login --------------")
  nome = input('> Informe seu usuario: ')
  ip = input('> Informe seu IP: ')
  usuario = Cliente(nome, ip)
  return usuario


def buscarClientePeloNome():
  pass

def imprimeListaUsuarios(listaUsuarios):
  print("\n--------- Lista de Usuários Cadastrados ---------")
  for usuario in listaUsuarios:
    print("\n")
    print(f'> NOME: {usuario.nome}')
    print(f'> IP: {usuario.ip}')
    print("---------------")


def menuUsuario(conexao, usuario):
  print("\n-------------------- Menu --------------------")
  print("Escolha uma opção: \n")
  print("1 - Lista todas os usuários cadastrados")
  print("2 - Buscar pelo nome de um usuário")
  print("3 - Buscar pelo ip de um usuário")
  print("4 - Desligar conexão com servidor e sair")
  resposta = int(input("\n> "))

  if (resposta == 1):
    usuario.enviaMensagem(conexao, "listagem")
    listaUsuarios = usuario.recebeMensagem(conexao)
    imprimeListaUsuarios(listaUsuarios)
  elif (resposta == 2):
    usuario.enviaMensagem(conexao, "buscarNome")

    nomeProcurado = input("Digite o nome do Cliente que deseja procurar:\n")
    print("Procurando", nomeProcurado)
    usuario.enviaMensagem(conexao, nomeProcurado)
    clienteProcurado = usuario.recebeMensagem(conexao)
    if (clienteProcurado != []):
      print(
          f"Cliente encontrado! \n Nome: {clienteProcurado.nome}\n IP: {clienteProcurado.ip}\n"
      )
    else:
      print("Cliente com esse nome não encontrado! Tente novamente\n")
  elif (resposta == 3):
    pass
  elif (resposta == 4):
    usuario.enviaMensagem(conexao, "desligar")
    conexao.close()
    quit()
