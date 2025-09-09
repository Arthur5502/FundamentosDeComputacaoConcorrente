import threading
import time

contador = 0

# Exemplo de condição de corrida

def incrementar(n):
    global contador
    for _ in range(n):
        valor = contador  # lê
        # Simula processamento
        time.sleep(0.0001)
        contador = valor + 1  # escreve


def sem_sincronizacao():
    global contador
    contador = 0
    t1 = threading.Thread(target=incrementar, args=(100,))
    t2 = threading.Thread(target=incrementar, args=(100,))
    t1.start(); t2.start()
    t1.join(); t2.join()
    print(f"Sem sincronização contador = {contador} (esperado 200)")

# Corrigindo com Lock
lock = threading.Lock()

def incrementar_com_lock(n):
    global contador
    for _ in range(n):
        with lock:
            valor = contador
            time.sleep(0.0001)
            contador = valor + 1

def com_lock():
    global contador
    contador = 0
    t1 = threading.Thread(target=incrementar_com_lock, args=(100,))
    t2 = threading.Thread(target=incrementar_com_lock, args=(100,))
    t1.start(); t2.start()
    t1.join(); t2.join()
    print(f"Com Lock contador = {contador} (esperado 200)")

if __name__ == "__main__":
    sem_sincronizacao()
    com_lock()
