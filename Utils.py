from Cliente import Cliente


def recebeUsuario():
    print("\n------------- Login --------------")
    nome = input('> Informe seu usuario: ')
    ip = input('> Informe seu IP: ')
    usuario = Cliente(nome, ip)
    return usuario

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
    print("4 - Sair")
    resposta = int(input("\n> "))

    if (resposta == 1):
        listaUsuarios = usuario.recebeMensagem(conexao)
        imprimeListaUsuarios(listaUsuarios)
    elif (resposta == 2):
        pass
    elif (resposta == 3):
        pass
    elif (resposta == 4):
        quit()