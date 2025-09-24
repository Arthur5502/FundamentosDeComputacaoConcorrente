import socket
import threading
import json
import time
import sys
from concurrent.futures import ThreadPoolExecutor
import math

def eh_primo(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def processar_tarefa(dados_tarefa):
    tipo = dados_tarefa.get('tipo')
    
    if tipo == 'primo':
        numero = dados_tarefa['numero']
        resultado = eh_primo(numero)
        return {
            'numero': numero,
            'eh_primo': resultado,
            'tempo_processamento': time.time()
        }
    
    elif tipo == 'fibonacci':
        n = dados_tarefa['n']
        if n <= 1:
            fib = n
        else:
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            fib = b
        return {
            'n': n,
            'fibonacci': fib,
            'tempo_processamento': time.time()
        }
    
    return {'erro': 'Tipo de tarefa desconhecido'}

class ServidorDistribuido:
    def __init__(self, porta):
        self.porta = porta
        self.clientes = []
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    def iniciar(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind(('0.0.0.0', self.porta))
            servidor.listen(5)
            
            print(f"Servidor iniciado na porta {self.porta}")
            print("Aguardando clientes...")
            
            while True:
                try:
                    cliente, endereco = servidor.accept()
                    print(f"Cliente conectado: {endereco}")
                    
                    thread_cliente = threading.Thread(
                        target=self.atender_cliente,
                        args=(cliente, endereco),
                        daemon=True
                    )
                    thread_cliente.start()
                    
                except KeyboardInterrupt:
                    print("Encerrando servidor...")
                    break
                    
    def atender_cliente(self, cliente, endereco):
        with self.lock:
            self.clientes.append(cliente)
            
        try:
            while True:
                dados = cliente.recv(4096)
                if not dados:
                    break
                    
                try:
                    requisicao = json.loads(dados.decode())
                    print(f"Processando tarefa de {endereco}: {requisicao}")
                    
                    future = self.executor.submit(processar_tarefa, requisicao)
                    resultado = future.result()
                    
                    resposta = {
                        'status': 'sucesso',
                        'resultado': resultado,
                        'servidor': f"localhost:{self.porta}",
                        'timestamp': time.time()
                    }
                    
                    cliente.send(json.dumps(resposta).encode())
                    print(f"Resposta enviada para {endereco}")
                    
                except json.JSONDecodeError:
                    erro = {'status': 'erro', 'mensagem': 'JSON inválido'}
                    cliente.send(json.dumps(erro).encode())
                    
        except Exception as e:
            print(f"Erro com cliente {endereco}: {e}")
        finally:
            with self.lock:
                if cliente in self.clientes:
                    self.clientes.remove(cliente)
            cliente.close()
            print(f"Cliente {endereco} desconectado")

class ClienteDistribuido:
    def __init__(self, host, porta):
        self.host = host
        self.porta = porta
        
    def conectar(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((self.host, self.porta))
            print(f"Conectado ao servidor {self.host}:{self.porta}")
            print("Digite 'primo <numero>' ou 'fibonacci <numero>' ou 'sair'")
            
            while True:
                try:
                    entrada = input("Cliente> ").strip()
                    if entrada.lower() == 'sair':
                        break
                        
                    partes = entrada.split()
                    if len(partes) < 2:
                        print("Use: primo <numero> ou fibonacci <numero>")
                        continue
                        
                    comando, valor = partes[0], int(partes[1])
                    
                    tarefa = {
                        'tipo': comando,
                        'numero' if comando == 'primo' else 'n': valor,
                        'timestamp_envio': time.time()
                    }
                    
                    inicio = time.time()
                    cliente.send(json.dumps(tarefa).encode())
                    
                    resposta = cliente.recv(4096)
                    fim = time.time()
                    
                    resultado = json.loads(resposta.decode())
                    
                    if resultado['status'] == 'sucesso':
                        dados = resultado['resultado']
                        if comando == 'primo':
                            print(f"{dados['numero']} é primo: {dados['eh_primo']}")
                        else:
                            print(f"Fibonacci({dados['n']}) = {dados['fibonacci']}")
                        print(f"Tempo: {fim-inicio:.3f}s")
                    else:
                        print(f"Erro: {resultado.get('mensagem', 'Desconhecido')}")
                        
                except ValueError:
                    print("Digite um número válido")
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Erro: {e}")
                    
            print("Cliente desconectado")

def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  Servidor: python sistema_distribuido_completo.py servidor <porta>")
        print("  Cliente:  python sistema_distribuido_completo.py cliente <host> <porta>")
        sys.exit(1)
        
    modo = sys.argv[1]
    
    if modo == 'servidor' and len(sys.argv) == 3:
        porta = int(sys.argv[2])
        servidor = ServidorDistribuido(porta)
        servidor.iniciar()
        
    elif modo == 'cliente' and len(sys.argv) == 4:
        host = sys.argv[2]
        porta = int(sys.argv[3])
        cliente = ClienteDistribuido(host, porta)
        cliente.conectar()
        
    else:
        print("Argumentos inválidos")
        sys.exit(1)

if __name__ == "__main__":
    main()