import time
from tqdm import tqdm

def cronometro():
    input("Pressione Enter para iniciar o cronômetro.")
    inicio = time.time()

    try:
        for _ in tqdm(iterable=range(int(1e10)), unit="seg",  bar_format=" "):
            tempo_passado = time.time() - inicio
            horas, minutos = divmod(tempo_passado, 3600)
            minutos, segundos = divmod(minutos, 60)
            horas = int(horas)
            minutos = int(minutos)
            segundos = int(segundos)

            print(f"\rChamada em andamento... {horas:02d}:{minutos:02d}:{segundos:02d}", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCronômetro interrompido.")

if __name__ == "__main__":
    cronometro()
