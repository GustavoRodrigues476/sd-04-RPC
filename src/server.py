import socket
import multiprocessing
import os
import json

f1 = multiprocessing.Value('i', 0)
f2 = multiprocessing.Value('i', 0)

def fun1(range1, range2):
    print(f"[Processo 1 - PID: {os.getpid()}] Iniciando...")
    x = 0
    for i in range(range1):
        for j in range(range2):
            x = x + 1
    f1.value = x
    print(f"[Processo 1 - PID: {os.getpid()}] Concluído: {x}")

def fun2(range1, range2):
    print(f"[Processo 2 - PID: {os.getpid()}] Iniciando...")
    x = 0
    for i in range(range1):
        for j in range(range2):
            x = x + 1
    f2.value = x
    print(f"[Processo 2 - PID: {os.getpid()}] Concluído: {x}")

def main():
    HOST = "0.0.0.0"
    PORT = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print("[Servidor] Aguardando conexão do client...")

        conn, addr = s.accept()
        with conn:
            print(f"[Servidor] Client conectado: {addr}")

            dados = json.loads(conn.recv(1024).decode())
            range1 = dados["range1"]
            range2 = dados["range2"]
            print(f"[Servidor] Parâmetros recebidos: range1={range1}, range2={range2}")

            print("[Servidor] Iniciando processos em paralelo...")
            p1 = multiprocessing.Process(target=fun1, args=(range1, range2))
            p2 = multiprocessing.Process(target=fun2, args=(range1, range2))

            p1.start()
            p2.start()
            p1.join()
            p2.join()

            resultado = f1.value + f2.value
            print(f"[Servidor] Resultado final: {resultado}")
            conn.sendall(str(resultado).encode())

if __name__ == "__main__":
    main()