# SD-04 — RPC Distribuído com Python

Exemplo de sistema distribuído utilizando **RPC (Remote Procedure Call)** com a biblioteca `rpyc` do Python, comunicando-se entre duas máquinas virtuais Linux.

---

## Descritivo do Programa

**O que é?**
Uma calculadora distribuída onde o client chama funções no server remotamente como se fossem funções locais, utilizando o padrão RPC (Remote Procedure Call). O server expõe métodos através de uma classe de serviço e o client os invoca diretamente pelo nome.

**Como funciona?**
O server define uma classe `CalculadoraService` que herda de `rpyc.Service`. Cada método prefixado com `exposed_` fica disponível remotamente. O `ThreadedServer` gerencia múltiplos clients simultaneamente. O client conecta ao server via `rpyc.connect()` e chama os métodos remotos através de `c.root.metodo()`, exatamente como chamaria uma função local.

**Por que isso é distribuído?**
O cálculo é executado no server (VM 1), mas o client (VM 2) chama os métodos como se fossem locais — sem precisar conhecer a implementação. Essa transparência de localização é a essência do modelo RPC, onde a complexidade da comunicação em rede fica oculta para o programador.

**Diferença para Sockets puro**
No exemplo de Sockets (SD-03), o client precisa montar manualmente o protocolo `X;Y;operacao` e interpretar a resposta. Com RPC, o client simplesmente chama `c.root.soma(10, 5)` e recebe `15` — a serialização e comunicação são feitas automaticamente pela biblioteca.

**Operações disponíveis**
- `soma` — adição entre dois números
- `subtracao` — subtração entre dois números
- `multiplicacao` — multiplicação entre dois números
- `divisao` — divisão com tratamento de erro para divisão por zero
- `potencia` — x elevado a y
- `modulo` — resto da divisão de x por y

**Tecnologias utilizadas**
- `rpyc` — biblioteca de RPC para Python
- `rpyc.Service` — classe base para expor métodos remotamente
- `ThreadedServer` — servidor com suporte a múltiplos clients
- `Vagrant + VirtualBox` — provisionamento das VMs Linux

---

## Arquitetura

```
┌─────────────────────┐          rpyc RPC          ┌──────────────────────────────┐
│   CLIENT VM         │ ────────────────────────> │   SERVER VM                  │
│   192.168.56.11     │   c.root.soma(10, 5)      │   192.168.56.10              │
│                     │ <──────────────────────── │                              │
│   client.py         │   retorna: 15             │   server.py                  │
└─────────────────────┘                           │   CalculadoraService         │
                                                  │   ├── exposed_soma           │
                                                  │   ├── exposed_subtracao      │
                                                  │   ├── exposed_multiplicacao  │
                                                  │   ├── exposed_divisao        │
                                                  │   ├── exposed_potencia       │
                                                  │   └── exposed_modulo         │
                                                  └──────────────────────────────┘
```

---

## Pré-requisitos

- [VirtualBox 7.0.x](https://www.virtualbox.org/wiki/Download_Old_Builds_7_0)
- [Vagrant](https://developer.hashicorp.com/vagrant/downloads)

> **Atenção:** VirtualBox 7.1.x pode apresentar problemas de compatibilidade com o Vagrant no Windows. Recomenda-se a versão **7.0.x**.

---

## Estrutura do projeto

```
sd-04-rpc/
├── Vagrantfile
├── README.md
├── .gitignore
├── setup/
│   ├── setup-server.sh
│   └── setup-client.sh
└── src/
    ├── server.py
    └── client.py
```

---

## Como rodar

### 1. Clone o repositório

```bash
git clone https://github.com/GustavoRodrigues476/sd-04-rpc
cd sd-04-rpc
```

### 2. Suba as VMs

```bash
vagrant up
```

> Na primeira execução o Vagrant baixa a imagem do Ubuntu (~500MB) e instala o `rpyc` automaticamente via script de setup. Aguarde as duas VMs aparecerem como `ready`.

Se apenas uma VM subir, suba a outra manualmente:

```bash
vagrant up client
```

### 3. Abra dois terminais

**Terminal 1 — inicie o servidor:**

```bash
vagrant ssh server
python3 /vagrant/src/server.py
```

**Terminal 2 — execute o client:**

```bash
vagrant ssh client
python3 /vagrant/src/client.py
```

---

## Saída esperada

**Terminal do server:**
```
[Servidor] RPC escutando na porta 18861...
[Servidor] Operações: soma, subtracao, multiplicacao, divisao, potencia, modulo
[Servidor] Client conectado: ('192.168.56.11', 54320)
[Servidor] soma(10, 5) = 15
[Servidor] subtracao(10, 5) = 5
[Servidor] multiplicacao(10, 5) = 50
[Servidor] divisao(10, 5) = 2.0
[Servidor] potencia(2, 8) = 256
[Servidor] modulo(10, 3) = 1
[Servidor] Client desconectado
```

**Terminal do client:**
```
[Client] Conectando ao servidor 192.168.56.10:18861...

=== Calculadora Distribuída via RPC ===

soma(10, 5)          = 15
subtracao(10, 5)     = 5
multiplicacao(10, 5) = 50
divisao(10, 5)       = 2.0
potencia(2, 8)       = 256
modulo(10, 3)        = 1

--- Teste de erro ---
Erro capturado: divisao por zero!

[Client] Conexão encerrada.
```

---

## Solução de problemas

### Erro: `ModuleNotFoundError: No module named 'rpyc'`

Execute manualmente dentro da VM:

```bash
vagrant ssh server
pip3 install rpyc

vagrant ssh client
pip3 install rpyc
```

Ou force o provisionamento novamente:

```bash
vagrant reload --provision
```

### Erro: `timeout during server version negotiating`

Adicione as linhas abaixo no bloco `provider` de cada VM no `Vagrantfile`:

```ruby
vb.customize ["modifyvm", :id, "--usb", "off"]
vb.customize ["modifyvm", :id, "--usbehci", "off"]
```

Depois execute:

```bash
vagrant destroy -f
vagrant up
```

### Erro: `VM not created. Moving on...`

Suba a VM individualmente:

```bash
vagrant up client
```

### Erro de SSH agent

Adicione ao `Vagrantfile` logo após `Vagrant.configure("2") do |config|`:

```ruby
config.ssh.forward_agent = false
```

---

## Comandos úteis do Vagrant

```bash
vagrant up              # sobe as duas VMs
vagrant up server       # sobe só o server
vagrant up client       # sobe só o client
vagrant ssh server      # acessa o server via SSH
vagrant ssh client      # acessa o client via SSH
vagrant halt            # desliga as VMs (sem apagar)
vagrant destroy -f      # apaga as VMs
vagrant reload          # reinicia as VMs
vagrant reload --provision  # reinicia e roda os scripts de setup novamente
vagrant status          # exibe o status das VMs
```

---

## Disciplina

Sistemas Distribuídos
