import socket
import json

SERVER_IP = "192.168.56.10"
PORT = 5000

def main():
    dados = {
        "range1": 500,
        "range2": 1000
    }

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        print("[Client] Conectado ao servidor.")

        print(f"[Client] Enviando parâmetros: {dados}")
        s.sendall(json.dumps(dados).encode())

        print("[Client] Aguardando resultado...")
        resultado = s.recv(1024).decode()
        print(f"[Client] Resultado recebido: {resultado}")

if __name__ == "__main__":
    main()

    