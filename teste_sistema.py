#!/bin/bash
"""
Script de teste para o sistema distribuído do restaurante
Inicia o servidor e múltiplos clientes para demonstrar a arquitetura
"""

import subprocess
import time
import sys
import os
import signal

def iniciar_servidor():
    """Inicia o servidor em um processo separado"""
    print("🚀 Iniciando servidor...")
    return subprocess.Popen([sys.executable, "servidor.py"])

def iniciar_cliente(numero=1):
    """Inicia um cliente em um processo separado"""
    print(f"🔧 Iniciando cliente {numero}...")
    return subprocess.Popen([sys.executable, "cliente.py"])

def main():
    print("="*60)
    print("🍴 TESTE DO SISTEMA DISTRIBUÍDO DO RESTAURANTE 🍴")
    print("="*60)
    
    processos = []
    
    try:
        # Inicia o servidor
        servidor = iniciar_servidor()
        processos.append(servidor)
        
        # Aguarda um pouco para o servidor inicializar
        print("⏳ Aguardando servidor inicializar...")
        time.sleep(2)
        
        # Pergunta quantos clientes iniciar
        try:
            num_clientes = int(input("Quantos clientes deseja iniciar? (1-5): "))
            num_clientes = max(1, min(5, num_clientes))
        except ValueError:
            num_clientes = 1
        
        # Inicia os clientes
        for i in range(num_clientes):
            cliente = iniciar_cliente(i + 1)
            processos.append(cliente)
            time.sleep(0.5)  # Pequena pausa entre clientes
        
        print(f"\n✅ Sistema iniciado com sucesso!")
        print(f"   - 1 servidor")
        print(f"   - {num_clientes} cliente(s)")
        print("\n💡 Dica: Use Ctrl+C para parar todos os processos")
        print("="*60)
        
        # Aguarda até que o usuário pare o sistema
        while True:
            time.sleep(1)
            
            # Verifica se algum processo morreu
            for processo in processos[:]:
                if processo.poll() is not None:
                    print(f"⚠️  Um processo terminou inesperadamente")
                    processos.remove(processo)
            
            if not processos:
                print("❌ Todos os processos terminaram")
                break
    
    except KeyboardInterrupt:
        print(f"\n🛑 Parando sistema...")
    
    finally:
        # Termina todos os processos
        for processo in processos:
            try:
                processo.terminate()
                processo.wait(timeout=5)
            except subprocess.TimeoutExpired:
                processo.kill()
        
        print("✅ Sistema parado com sucesso!")

if __name__ == "__main__":
    # Verifica se os arquivos existem
    if not os.path.exists("servidor.py"):
        print("❌ Arquivo servidor.py não encontrado!")
        sys.exit(1)
    
    if not os.path.exists("cliente.py"):
        print("❌ Arquivo cliente.py não encontrado!")
        sys.exit(1)
    
    main()