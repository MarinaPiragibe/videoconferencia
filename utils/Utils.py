def imprimeListaClientes(listaClientes):

  print("\n--------- Lista de Usuários Cadastrados ---------")
  for cliente in listaClientes:
    print("\n")
    print(f'> NOME: {cliente.nome}')
    print(f'> IP: {cliente.ip}')
    print(f'> PORTA: {cliente.porta}')
    print("---------------")
