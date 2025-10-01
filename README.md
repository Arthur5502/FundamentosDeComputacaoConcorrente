# Sistema de Restaurante Distribuído

Este projeto demonstra uma arquitetura cliente-servidor para um sistema de restaurante com processamento concorrente de pedidos.

## Arquitetura

### 🔧 **Servidor (`servidor.py`)**
- Gerencia o estado do restaurante (pedidos, cardápio, chefs)
- Processa pedidos de forma concorrente usando ThreadPoolExecutor
- Aceita múltiplas conexões simultâneas de clientes
- API baseada em JSON para comunicação

**Principais características:**
- ✅ Processamento assíncrono de pedidos
- ✅ Thread pool para simular múltiplos chefs
- ✅ Gerenciamento de estado thread-safe
- ✅ Suporte a múltiplos clientes simultâneos

### 📱 **Cliente (`cliente.py`)**
- Interface de linha de comando para interação com usuário
- Comunica com servidor via sockets TCP
- Envia comandos em formato JSON

**Funcionalidades:**
- ✅ Fazer pedidos
- ✅ Verificar status de pedidos
- ✅ Listar pedidos pendentes
- ✅ Aguardar finalização de todos os pedidos

## Como Usar

### Método 1: Manual

1. **Iniciar o servidor:**
   ```bash
   python3 servidor.py
   ```

2. **Iniciar cliente(s) em terminal(s) separado(s):**
   ```bash
   python3 cliente.py
   ```

### Método 2: Script Automatizado

```bash
python3 teste_sistema.py
```

## Comandos do Cliente

Uma vez conectado, você pode usar os seguintes comandos:

- `pedido <prato> [quantidade]` - Fazer um pedido
  - Exemplo: `pedido pizza 2`
  
- `status <id>` - Verificar status do pedido
  - Exemplo: `status P001`
  
- `pendentes` - Listar pedidos em andamento

- `aguardar` - Aguardar todos os pedidos serem finalizados

- `menu` - Mostrar menu de comandos

- `sair` - Encerrar cliente

## Cardápio Disponível

- 🍕 Pizza (2.0s base)
- 🍔 Hambúrguer (1.5s base)
- 🥗 Salada (0.8s base)
- 🍲 Sopa (1.2s base)
- 🍝 Lasanha (3.0s base)
- 🥪 Sanduíche (1.0s base)

*Tempos são simulados e podem variar com quantidade e aleatoriedade*

## Protocolo de Comunicação

### Formato das Mensagens

**Cliente → Servidor:**
```json
{
    "acao": "fazer_pedido",
    "prato": "pizza",
    "quantidade": 2
}
```

**Servidor → Cliente:**
```json
{
    "sucesso": true,
    "pedido_id": "P001",
    "mensagem": "Pedido P001 adicionado à fila"
}
```

### Ações Suportadas

- `fazer_pedido` - Criar novo pedido
- `verificar_pedido` - Consultar status
- `listar_pendentes` - Listar pedidos em andamento
- `obter_cardapio` - Obter cardápio disponível
- `aguardar_todos` - Aguardar conclusão de todos os pedidos

## Benefícios da Arquitetura Cliente-Servidor

### ✅ **Separação de Responsabilidades**
- **Servidor**: Lógica de negócio, processamento, estado
- **Cliente**: Interface do usuário, entrada/saída

### ✅ **Escalabilidade**
- Múltiplos clientes simultâneos
- Processamento paralelo no servidor
- Fácil adição de novos recursos

### ✅ **Manutenibilidade**
- Código modularizado
- Fácil modificação de interface ou lógica
- Testes independentes de componentes

### ✅ **Distribuição**
- Clientes podem estar em máquinas diferentes
- Servidor centralizado para consistência
- Comunicação via rede

## Configuração de Rede

**Padrão:**
- Host: `localhost`
- Porta: `8888`

Para alterar, modifique os parâmetros nos arquivos:
```python
# servidor.py
servidor = RestauranteServidor(host='0.0.0.0', port=9999)

# cliente.py  
cliente = RestauranteCliente(host='192.168.1.100', port=9999)
```

## Comparação com Versão Original

| Aspecto | Original (Monolítico) | Nova (Cliente-Servidor) |
|---------|----------------------|-------------------------|
| **Arquitetura** | Tudo em um processo | Separado em 2 componentes |
| **Usuários** | 1 usuário por vez | Múltiplos usuários simultâneos |
| **Distribuição** | Local apenas | Pode ser distribuído em rede |
| **Escalabilidade** | Limitada | Alta (múltiplos clientes) |
| **Manutenção** | Acoplada | Desacoplada |

## Possíveis Extensões

- 🔒 Autenticação de usuários
- 💾 Persistência de dados (banco de dados)
- 🌐 Interface web (HTTP/REST)
- 📊 Métricas e monitoramento
- 🔄 Balanceamento de carga
- 📱 Cliente mobile