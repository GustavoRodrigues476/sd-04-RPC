import rpyc

HOST = "192.168.56.10"
PORT = 18861

def main():
    print(f"[Client] Conectando ao servidor {HOST}:{PORT}...")
    c = rpyc.connect(HOST, PORT)

    print("\n=== Calculadora Distribuída via RPC ===\n")

    print(f"soma(10, 5)          = {c.root.soma(10, 5)}")
    print(f"subtracao(10, 5)     = {c.root.subtracao(10, 5)}")
    print(f"multiplicacao(10, 5) = {c.root.multiplicacao(10, 5)}")
    print(f"divisao(10, 5)       = {c.root.divisao(10, 5)}")
    print(f"potencia(2, 8)       = {c.root.potencia(2, 8)}")
    print(f"modulo(10, 3)        = {c.root.modulo(10, 3)}")

    print("\n--- Teste de erro ---")
    try:
        c.root.divisao(10, 0)
    except Exception as e:
        print(f"Erro capturado: {e}")

    c.close()
    print("\n[Client] Conexão encerrada.")

if __name__ == "__main__":
    main()