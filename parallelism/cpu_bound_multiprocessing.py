from multiprocessing import Pool, cpu_count
import math, time

def eh_primo(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    limite = int(math.sqrt(n)) + 1
    for i in range(3, limite, 2):
        if n % i == 0:
            return False
    return True


def contar_primos(intervalo):
    inicio, fim = intervalo
    return sum(1 for n in range(inicio, fim) if eh_primo(n))

if __name__ == "__main__":
    N = 300_000
    blocos = 8
    tamanho = N // blocos
    intervalos = [(i*tamanho, (i+1)*tamanho) for i in range(blocos)]

    inicio = time.time()
    with Pool(processes=min(cpu_count(), blocos)) as p:
        resultados = p.map(contar_primos, intervalos)
    total = sum(resultados)
    duracao = time.time() - inicio
    print(f"Total de primos < {N}: {total} em {duracao:.2f}s usando multiprocessing")
