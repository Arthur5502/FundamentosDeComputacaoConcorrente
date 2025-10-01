#!/usr/bin/env python3
"""
Cliente do Sistema de Restaurante Distribuído
Interface para interação com o usuário
"""

import socket
import json
import time

class RestauranteCliente:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.socket = None
        self.conectado = False
        self.cardapio = []
    
    def conectar(self):
        """Estabelece conexão com o servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.conectado = True
            print(f"🔗 Conectado ao servidor {self.host}:{self.port}")
            
            # Obtém o cardápio do servidor
            self.obter_cardapio()
            return True
            
        except Exception as e:
            print(f"❌ Erro ao conectar ao servidor: {e}")
            return False
    
    def desconectar(self):
        """Fecha a conexão com o servidor"""
        if self.socket:
            self.socket.close()
            self.conectado = False
            print("🔌 Desconectado do servidor")
    
    def enviar_comando(self, comando):
        """Envia um comando para o servidor e retorna a resposta"""
        if not self.conectado:
            return {'erro': 'Não conectado ao servidor'}
        
        try:
            # Envia comando
            comando_json = json.dumps(comando, ensure_ascii=False)
            self.socket.send(comando_json.encode('utf-8'))
            
            # Recebe resposta
            resposta = self.socket.recv(4096).decode('utf-8')
            return json.loads(resposta)
            
        except Exception as e:
            return {'erro': f'Erro de comunicação: {str(e)}'}
    
    def obter_cardapio(self):
        """Obtém o cardápio do servidor"""
        comando = {'acao': 'obter_cardapio'}
        resposta = self.enviar_comando(comando)
        
        if 'cardapio' in resposta:
            self.cardapio = resposta['cardapio']
        
        return resposta
    
    def fazer_pedido(self, prato, quantidade=1):
        """Faz um pedido ao servidor"""
        comando = {
            'acao': 'fazer_pedido',
            'prato': prato,
            'quantidade': quantidade
        }
        return self.enviar_comando(comando)
    
    def verificar_pedido(self, pedido_id):
        """Verifica o status de um pedido"""
        comando = {
            'acao': 'verificar_pedido',
            'pedido_id': pedido_id
        }
        return self.enviar_comando(comando)
    
    def listar_pendentes(self):
        """Lista pedidos pendentes no servidor"""
        comando = {'acao': 'listar_pendentes'}
        return self.enviar_comando(comando)
    
    def aguardar_todos_pedidos(self):
        """Solicita ao servidor aguardar todos os pedidos"""
        comando = {'acao': 'aguardar_todos'}
        return self.enviar_comando(comando)
    
    def mostrar_menu(self):
        """Exibe o menu de opções para o usuário"""
        print("\n" + "="*50)
        print("🍴 BEM-VINDO AO RESTAURANTE DISTRIBUÍDO 🍴")
        print("="*50)
        
        if self.cardapio:
            print("CARDÁPIO:")
            for i, prato in enumerate(self.cardapio, 1):
                print(f"  {i}. {prato.title()}")
        else:
            print("❌ Cardápio não disponível")
        
        print("\nCOMANDOS:")
        print("  pedido <prato> [quantidade]  - Fazer um pedido")
        print("  status <id>                  - Verificar status do pedido")
        print("  pendentes                    - Listar pedidos em andamento")
        print("  aguardar                     - Aguardar todos os pedidos")
        print("  menu                         - Mostrar este menu")
        print("  sair                         - Encerrar")
        print("="*50)
    
    def processar_pedido(self, entrada):
        """Processa um comando de pedido do usuário"""
        partes = entrada.split()
        if len(partes) < 2:
            print("❌ Use: pedido <prato> [quantidade]")
            return
        
        prato = partes[1].lower()
        quantidade = 1
        
        if len(partes) > 2:
            try:
                quantidade = int(partes[2])
                if quantidade <= 0:
                    print("❌ Quantidade deve ser maior que zero")
                    return
            except ValueError:
                print("❌ Quantidade deve ser um número válido")
                return
        
        if prato not in self.cardapio:
            print(f"❌ Prato '{prato}' não está no cardápio")
            print(f"Pratos disponíveis: {', '.join(self.cardapio)}")
            return
        
        print(f"📡 Enviando pedido: {quantidade}x {prato}...")
        resposta = self.fazer_pedido(prato, quantidade)
        
        if 'sucesso' in resposta and resposta['sucesso']:
            print(f"✅ {resposta['mensagem']}")
            print(f"🆔 ID do pedido: {resposta['pedido_id']}")
        elif 'erro' in resposta:
            print(f"❌ {resposta['erro']}")
        else:
            print(f"📋 Resposta: {resposta}")
    
    def verificar_status(self, entrada):
        """Verifica o status de um pedido"""
        partes = entrada.split()
        if len(partes) != 2:
            print("❌ Use: status <id_do_pedido>")
            return
        
        pedido_id = partes[1].upper()
        print(f"📡 Verificando status do pedido {pedido_id}...")
        
        resposta = self.verificar_pedido(pedido_id)
        
        if 'erro' in resposta:
            print(f"❌ {resposta['erro']}")
        elif resposta.get('status') == 'preparando':
            print(f"👨‍🍳 Pedido {pedido_id} ainda está sendo preparado...")
        elif resposta.get('status') == 'pronto':
            print(f"🎉 Pedido {pedido_id} está PRONTO!")
            print(f"   📋 {resposta['quantidade']}x {resposta['prato'].title()}")
            print(f"   👨‍🍳 Preparado pelo: {resposta['chef']}")
            print(f"   ⏱️  Tempo de preparo: {resposta['tempo_preparo']}s")
            print(f"   🕐 Finalizado às: {resposta['timestamp']}")
        else:
            print(f"📋 Status: {resposta}")
    
    def listar_pedidos_pendentes(self):
        """Lista pedidos pendentes no servidor"""
        print("📡 Consultando pedidos pendentes...")
        resposta = self.listar_pendentes()
        
        if 'erro' in resposta:
            print(f"❌ {resposta['erro']}")
        elif 'pedidos_pendentes' in resposta:
            pedidos = resposta['pedidos_pendentes']
            total = resposta.get('total', len(pedidos))
            
            if pedidos:
                print(f"📋 {total} pedidos em andamento: {', '.join(pedidos)}")
            else:
                print("✅ Nenhum pedido pendente")
        else:
            print(f"📋 Resposta: {resposta}")
    
    def aguardar_todos(self):
        """Aguarda todos os pedidos serem finalizados"""
        print("📡 Solicitando aguardar todos os pedidos...")
        resposta = self.aguardar_todos_pedidos()
        
        if 'erro' in resposta:
            print(f"❌ {resposta['erro']}")
        elif 'sucesso' in resposta and resposta['sucesso']:
            print(f"✅ {resposta['mensagem']}")
        else:
            print(f"📋 Resposta: {resposta}")
    
    def executar(self):
        """Loop principal de interação com o usuário"""
        if not self.conectar():
            return
        
        self.mostrar_menu()
        
        try:
            while self.conectado:
                try:
                    entrada = input("\n🍽️  Comando> ").strip().lower()
                    
                    if entrada == 'sair':
                        print("👋 Obrigado por visitar nosso restaurante!")
                        break
                    elif entrada == 'menu':
                        self.mostrar_menu()
                    elif entrada == 'pendentes':
                        self.listar_pedidos_pendentes()
                    elif entrada == 'aguardar':
                        self.aguardar_todos()
                    elif entrada.startswith('pedido '):
                        self.processar_pedido(entrada)
                    elif entrada.startswith('status '):
                        self.verificar_status(entrada)
                    else:
                        print("❌ Comando não reconhecido. Digite 'menu' para ver os comandos.")
                
                except KeyboardInterrupt:
                    print("\n👋 Encerrando cliente...")
                    break
                except Exception as e:
                    print(f"❌ Erro: {e}")
        
        finally:
            self.desconectar()

def main():
    """Função principal do cliente"""
    print("🔧 Iniciando cliente do restaurante...")
    
    try:
        cliente = RestauranteCliente()
        cliente.executar()
    except Exception as e:
        print(f"❌ Erro ao iniciar cliente: {e}")

if __name__ == "__main__":
    main()