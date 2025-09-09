import asyncio, random, time

async def tarefa_io(nome: str):
    atraso = random.uniform(0.5, 1.5)
    await asyncio.sleep(atraso)
    print(f"Tarefa {nome} terminou em {atraso:.2f}s")
    return atraso

async def main():
    inicio = time.time()
    tarefas = [asyncio.create_task(tarefa_io(str(i))) for i in range(5)]
    resultados = await asyncio.gather(*tarefas)
    print(f"Resultados: {resultados}")
    print(f"Tempo total: {time.time()-inicio:.2f}s (IO concorrente)")

if __name__ == "__main__":
    asyncio.run(main())
