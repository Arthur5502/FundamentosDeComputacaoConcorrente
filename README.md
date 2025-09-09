# Fundamentos de Computação Concorrente, Paralela e Distribuída

Coleção de exemplos simples em Python para ilustrar conceitos fundamentais:

1. Condição de Corrida e Exclusão Mútua (threads + Lock)
2. Produtor / Consumidor com fila segura (`queue.Queue`)
3. Paralelismo CPU-Bound com `multiprocessing`
4. Concorrência IO-Bound com `asyncio`
5. Comunicação em Cluster simples via sockets (modelo distribuído)

## Estrutura

```
concurrency/
	threads_race_condition.py
	producer_consumer_queue.py
parallelism/
	cpu_bound_multiprocessing.py
	async_io_example.py
distributed/
	simple_tcp_cluster.py
```

## 1. Condição de corrida vs Lock

Mostra resultado incorreto sem sincronização e correto com `Lock`.

Executar:
```bash
python concurrency/threads_race_condition.py
```

Observe que sem lock geralmente o contador < 200.

## 2. Produtor / Consumidor

Usa `queue.Queue` para coordenação segura entre threads.

```bash
python concurrency/producer_consumer_queue.py
```

## 3. Paralelismo CPU-Bound

Conta números primos em blocos usando vários processos (aproveita múltiplos núcleos).

```bash
python parallelism/cpu_bound_multiprocessing.py
```

Adapte `N` e blocos para experimentar impacto de granularidade.

## 4. IO Concorrente com asyncio

Simula operações de IO concorrentes sem múltiplas threads pesadas.

```bash
python parallelism/async_io_example.py
```

## 5. Exemplo Distribuído (Broadcast simples)

Servidor aceita múltiplos workers e retransmite mensagens digitadas.

Terminal 1 (servidor):
```bash
python distributed/simple_tcp_cluster.py server 5000
```

Terminal 2..N (workers):
```bash
python distributed/simple_tcp_cluster.py worker 127.0.0.1 5000
```

Digite mensagens no servidor para broadcast. Digite `sair` para encerrar.

## Conceitos Relacionados

- Condição de corrida: acesso concorrente não controlado levando a estado inconsistente.
- Exclusão mútua: uso de locks / monitores para proteger região crítica.
- Espera bloqueante vs não bloqueante.
- Paralelismo x Concorrência: paralelismo = execução simultânea física; concorrência = progressão intercalada ou simultânea.
- CPU-bound x IO-bound.
- Overhead de criação de threads vs reutilização (asyncio/event loop).
- Comunicação entre processos vs threads (memória compartilhada vs mensagem).

## Próximos Passos (Sugestões)

- Adicionar exemplo de deadlock e prevenção.
- Implementar pool de threads manual.
- Exemplo com `asyncio.Queue` e produtor/consumidor assíncrono.
- Exemplo distribuído com troca estruturada (JSON) e heartbeats.

---
Sinta-se livre para expandir os exemplos e adicionar medições de tempo para análise de desempenho.