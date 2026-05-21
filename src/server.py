import rpyc
from rpyc.utils.server import ThreadedServer

class CalculadoraService(rpyc.Service):

    def on_connect(self, conn):
        print(f"[Servidor] Client conectado: {conn._channel.stream.sock.getpeername()}")

    def on_disconnect(self, conn):
        print(f"[Servidor] Client desconectado")

    def exposed_soma(self, x, y):
        resultado = x + y
        print(f"[Servidor] soma({x}, {y}) = {resultado}")
        return resultado

    def exposed_subtracao(self, x, y):
        resultado = x - y
        print(f"[Servidor] subtracao({x}, {y}) = {resultado}")
        return resultado

    def exposed_multiplicacao(self, x, y):
        resultado = x * y
        print(f"[Servidor] multiplicacao({x}, {y}) = {resultado}")
        return resultado

    def exposed_divisao(self, x, y):
        if y == 0:
            raise ValueError("Divisao por zero!")
        resultado = x / y
        print(f"[Servidor] divisao({x}, {y}) = {resultado}")
        return resultado

    def exposed_potencia(self, x, y):
        resultado = x ** y
        print(f"[Servidor] potencia({x}, {y}) = {resultado}")
        return resultado

    def exposed_modulo(self, x, y):
        resultado = x % y
        print(f"[Servidor] modulo({x}, {y}) = {resultado}")
        return resultado

if __name__ == "__main__":
    PORT = 18861
    print(f"[Servidor] RPC escutando na porta {PORT}...")
    print("[Servidor] Operações: soma, subtracao, multiplicacao, divisao, potencia, modulo")
    t = ThreadedServer(CalculadoraService, port=PORT)
    t.start()