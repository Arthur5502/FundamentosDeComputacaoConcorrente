import threading
import queue
import time
import random

fila = queue.Queue(maxsize=5)

TOTAL = 10


def produtor(id_prod):
    for i in range(TOTAL):
        item = (id_prod, i)
        fila.put(item)  # bloqueia se cheia
        print(f"Produtor {id_prod} produziu {item}. Tamanho fila={fila.qsize()}")
        time.sleep(random.uniform(0.05, 0.2))
    fila.put(None)  # sinal de término


def consumidor():
    while True:
        item = fila.get()
        if item is None:  # término
            fila.task_done()
            break
        time.sleep(random.uniform(0.1, 0.3))
        print(f"Consumidor processou {item}. Tamanho fila={fila.qsize()}")
        fila.task_done()

if __name__ == "__main__":
    t_prod1 = threading.Thread(target=produtor, args=(1,))
    t_prod2 = threading.Thread(target=produtor, args=(2,))
    t_cons = threading.Thread(target=consumidor)

    t_prod1.start(); t_prod2.start(); t_cons.start()

    t_prod1.join(); t_prod2.join()
    fila.join()  # aguarda processamento
    # garante que consumidor termine
    t_cons.join()
