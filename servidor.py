#!/usr/bin/env python3
"""
Servidor do Sistema de Restaurante Distribuído
Gerencia pedidos, processamento e estado do restaurante
"""

import socket
import threading
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor
import uuid

class RestauranteServidor:
    def __init__(self, host='localhost', port=8888, num_chefs=4):
        self.host = host
        self.port = port
        self.server_socket = None
        self.executando = False
        
        # Estado do restaurante
        self.pedidos_prontos = {}
        self.pedidos_em_andamento = {}
        self.contador_pedidos = 0
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=num_chefs, thread_name_prefix="Chef")
        
        # Cardápio e tempos de preparo
        self.cardapio = ['pizza', 'hamburguer', 'salada', 'sopa', 'lasanha', 'sanduiche']
        self.tempos_preparo = {
            'pizza': 2.0,
            'hamburguer': 1.5,
            'salada': 0.8,
            'sopa': 1.2,
            'lasanha': 3.0,
            'sanduiche': 1.0
        }
    
    def preparar_prato(self, pedido):
        """Simula o preparo de diferentes pratos com tempos variados"""
        tipo_prato = pedido.get('prato')
        quantidade = pedido.get('quantidade', 1)
        
        if tipo_prato not in self.tempos_preparo:
            return {
                'erro': f'Prato "{tipo_prato}" não está no cardápio',
                'cardapio': self.cardapio
            }
        
        # Simula o tempo de preparo
        tempo_base = self.tempos_preparo[tipo_prato]
        tempo_total = tempo_base * quantidade + random.uniform(0.2, 0.8)
        
        print(f"👨‍🍳 Chef {threading.current_thread().name} começou a preparar pedido {pedido['id']}")
        
        inicio = time.time()
        time.sleep(tempo_total)  # Simula o preparo
        fim = time.time()
        
        resultado = {
            'pedido_id': pedido.get('id'),
            'prato': tipo_prato,
            'quantidade': quantidade,
            'tempo_preparo': round(fim - inicio, 2),
            'chef': threading.current_thread().name,
            'status': 'pronto',
            'timestamp': time.strftime('%H:%M:%S')
        }
        
        print(f"✅ Pedido {pedido['id']} finalizado pelo {threading.current_thread().name}")
        return resultado
    
    def processar_comando(self, comando):
        """Processa comandos recebidos do cliente"""
        try:
            acao = comando.get('acao')
            
            if acao == 'fazer_pedido':
                return self.fazer_pedido(comando.get('prato'), comando.get('quantidade', 1))
            
            elif acao == 'verificar_pedido':
                return self.verificar_pedido(comando.get('pedido_id'))
            
            elif acao == 'listar_pendentes':
                return self.listar_pedidos_pendentes()
            
            elif acao == 'obter_cardapio':
                return {'cardapio': self.cardapio}
            
            elif acao == 'aguardar_todos':
                return self.aguardar_todos_pedidos()
            
            else:
                return {'erro': 'Comando não reconhecido'}
                
        except Exception as e:
            return {'erro': f'Erro ao processar comando: {str(e)}'}
    
    def fazer_pedido(self, prato, quantidade=1):
        """Adiciona um novo pedido à fila de processamento"""
        if prato not in self.cardapio:
            return {
                'erro': f'Prato "{prato}" não está no cardápio',
                'cardapio': self.cardapio
            }
        
        with self.lock:
            self.contador_pedidos += 1
            pedido_id = f"P{self.contador_pedidos:03d}"
        
        pedido = {
            'id': pedido_id,
            'prato': prato,
            'quantidade': quantidade,
            'timestamp_pedido': time.strftime('%H:%M:%S')
        }
        
        print(f"🍽️  Novo pedido #{pedido_id}: {quantidade}x {prato}")
        
        # Submete o pedido para processamento assíncrono
        future = self.executor.submit(self.preparar_prato, pedido)
        self.pedidos_em_andamento[pedido_id] = future
        
        return {
            'sucesso': True,
            'pedido_id': pedido_id,
            'mensagem': f'Pedido {pedido_id} adicionado à fila'
        }
    
    def verificar_pedido(self, pedido_id):
        """Verifica o status de um pedido específico"""
        if pedido_id in self.pedidos_prontos:
            return self.pedidos_prontos[pedido_id]
        elif pedido_id in self.pedidos_em_andamento:
            future = self.pedidos_em_andamento[pedido_id]
            if future.done():
                resultado = future.result()
                self.pedidos_prontos[pedido_id] = resultado
                del self.pedidos_em_andamento[pedido_id]
                return resultado
            else:
                return {'status': 'preparando', 'pedido_id': pedido_id}
        else:
            return {'erro': 'Pedido não encontrado'}
    
    def listar_pedidos_pendentes(self):
        """Lista todos os pedidos em andamento"""
        return {
            'pedidos_pendentes': list(self.pedidos_em_andamento.keys()),
            'total': len(self.pedidos_em_andamento)
        }
    
    def aguardar_todos_pedidos(self):
        """Aguarda todos os pedidos serem finalizados"""
        total_pedidos = len(self.pedidos_em_andamento)
        
        for pedido_id, future in list(self.pedidos_em_andamento.items()):
            if not future.done():
                resultado = future.result()  # Bloqueia até completar
                self.pedidos_prontos[pedido_id] = resultado
        
        self.pedidos_em_andamento.clear()
        
        return {
            'sucesso': True,
            'mensagem': f'Todos os {total_pedidos} pedidos foram finalizados'
        }
    
    def handle_client(self, client_socket, client_address):
        """Gerencia a conexão com um cliente específico"""
        print(f"🔗 Cliente conectado: {client_address}")
        
        try:
            while self.executando:
                # Recebe dados do cliente
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                try:
                    comando = json.loads(data)
                    print(f"📨 Comando recebido de {client_address}: {comando.get('acao', 'desconhecido')}")
                    
                    # Processa o comando
                    resposta = self.processar_comando(comando)
                    
                    # Envia resposta
                    resposta_json = json.dumps(resposta, ensure_ascii=False)
                    client_socket.send(resposta_json.encode('utf-8'))
                    
                except json.JSONDecodeError:
                    erro = {'erro': 'Formato JSON inválido'}
                    client_socket.send(json.dumps(erro).encode('utf-8'))
                except Exception as e:
                    erro = {'erro': f'Erro interno: {str(e)}'}
                    client_socket.send(json.dumps(erro).encode('utf-8'))
        
        except Exception as e:
            print(f"❌ Erro na conexão com {client_address}: {e}")
        
        finally:
            client_socket.close()
            print(f"🔌 Cliente desconectado: {client_address}")
    
    def iniciar_servidor(self):
        """Inicia o servidor e aceita conexões"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.executando = True
            
            print(f"🚀 Servidor do restaurante iniciado em {self.host}:{self.port}")
            print(f"👨‍🍳 {self.executor._max_workers} chefs disponíveis")
            print("="*50)
            
            while self.executando:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    
                    # Cria uma thread para cada cliente
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.error as e:
                    if self.executando:
                        print(f"❌ Erro ao aceitar conexão: {e}")
                        
        except Exception as e:
            print(f"❌ Erro ao iniciar servidor: {e}")
        finally:
            self.parar_servidor()
    
    def parar_servidor(self):
        """Para o servidor e fecha todas as conexões"""
        print("\n🛑 Parando servidor...")
        self.executando = False
        
        if self.server_socket:
            self.server_socket.close()
        
        # Aguarda pedidos pendentes serem finalizados
        if self.pedidos_em_andamento:
            print("⏳ Aguardando pedidos pendentes serem finalizados...")
            self.aguardar_todos_pedidos()
        
        self.executor.shutdown(wait=True)
        print("✅ Servidor parado com sucesso!")

def main():
    """Função principal do servidor"""
    servidor = RestauranteServidor()
    
    try:
        servidor.iniciar_servidor()
    except KeyboardInterrupt:
        print("\n🛑 Recebido sinal de interrupção...")
    finally:
        servidor.parar_servidor()

if __name__ == "__main__":
    main()