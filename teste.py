import time

def cronometro():
    input("Pressione Enter para iniciar o cronômetro.")
    inicio = time.time()

    try:
        while True:
            tempo_passado = time.time() - inicio
            horas, minutos = divmod(tempo_passado, 3600)
            minutos, segundos = divmod(minutos, 60)
            horas = int(horas)
            minutos = int(minutos)
            segundos = int(segundos)
            
            # Limpa a tela do console para atualizar o tempo
            print("\033c", end="")

            # Formata e exibe o tempo decorrido
            print("Chamada em andamento... ")
            print(f"{horas:02d}:{minutos:02d}:{segundos:02d}", end="", flush=True)

            print("\n Ctrl+C para encerrar a chamada")

            time.sleep(1)
    except KeyboardInterrupt:
        print("Cronômetro interrompido.")


if __name__ == "__main__":
    cronometro()