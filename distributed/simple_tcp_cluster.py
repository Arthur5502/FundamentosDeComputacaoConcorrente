import socket
import threading
import sys

# Uso:
# Terminal 1: python simple_tcp_cluster.py server 5000
# Terminal 2: python simple_tcp_cluster.py worker 127.0.0.1 5000
# Envie múltiplos workers.
# Depois digite mensagens no servidor para broadcast.

clientes = []
lock = threading.Lock()


def servidor(porta: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", porta))
        s.listen()
        print(f"Servidor escutando na porta {porta}")

        def aceitar():
            while True:
                conn, addr = s.accept()
                with lock:
                    clientes.append(conn)
                print(f"Worker conectado: {addr}")

        threading.Thread(target=aceitar, daemon=True).start()
        try:
            while True:
                msg = input()
                if msg.strip().lower() == 'sair':
                    break
                with lock:
                    vivos = []
                    for c in clientes:
                        try:
                            c.sendall(msg.encode()+b"\n")
                            vivos.append(c)
                        except OSError:
                            pass
                    clientes[:] = vivos
        except KeyboardInterrupt:
            pass
        print("Encerrando servidor")


def worker(host: str, porta: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, porta))
        print("Conectado ao servidor. Aguardando mensagens...")
        try:
            while True:
                dados = s.recv(1024)
                if not dados:
                    break
                print("[Broadcast]", dados.decode().strip())
        except KeyboardInterrupt:
            pass
        print("Worker finalizado")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python simple_tcp_cluster.py server <porta> | worker <host> <porta>")
        sys.exit(1)
    modo = sys.argv[1]
    if modo == 'server' and len(sys.argv) == 3:
        servidor(int(sys.argv[2]))
    elif modo == 'worker' and len(sys.argv) == 4:
        worker(sys.argv[2], int(sys.argv[3]))
    else:
        print("Argumentos inválidos")
