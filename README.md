# SD-01 — Processos Distribuídos com Python

Exemplo de sistema distribuído utilizando **processos paralelos** com `multiprocessing` do Python, comunicando-se entre duas máquinas virtuais Linux via **sockets TCP**.

---

## Descrição

Este exemplo demonstra o uso de **processos** como unidade de paralelismo em sistemas distribuídos.

O **client** envia parâmetros de processamento ao **server** via socket. O server cria dois processos independentes (`Process`) que executam contagens em paralelo, armazenam os resultados em memória compartilhada (`multiprocessing.Value`) e, ao final, somam os valores e devolvem o resultado ao client.

Cada processo exibe seu **PID** no terminal, evidenciando que são processos distintos rodando em paralelo no sistema operacional.

### Conceitos abordados

- `multiprocessing.Process` — criação de processos filhos
- `multiprocessing.Value` — memória compartilhada entre processos
- `p.start()` / `p.join()` — ciclo de vida de processos
- Comunicação entre máquinas via **socket TCP**
- Ambientes isolados com **Vagrant + VirtualBox**

---

## Arquitetura

```
┌─────────────────────┐        socket TCP         ┌─────────────────────────┐
│   CLIENT VM         │ ────────────────────────> │   SERVER VM             │
│   192.168.56.11     │   envia range1, range2    │   192.168.56.10         │
│                     │ <──────────────────────── │                         │
│   client.py         │   recebe resultado        │   server.py             │
└─────────────────────┘                           │   ├── Processo 1 (PID X)│
                                                  │   └── Processo 2 (PID Y)│
                                                  └─────────────────────────┘
```

---

## Pré-requisitos

- [VirtualBox 7.0.x](https://www.virtualbox.org/wiki/Download_Old_Builds_7_0)
- [Vagrant](https://developer.hashicorp.com/vagrant/downloads)

> **Atenção:** VirtualBox 7.1.x pode apresentar problemas de compatibilidade com o Vagrant no Windows. Recomenda-se a versão **7.0.x**.

---

## Estrutura do projeto

```
sd-01-processos/
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
git clone https://github.com/seu-user/sd-01-processos
cd sd-01-processos
```

### 2. Suba as VMs

```bash
vagrant up
```

> Na primeira execução o Vagrant baixa a imagem do Ubuntu (~500MB). Aguarde as duas VMs aparecerem como `ready`.

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
[Servidor] Aguardando conexão do client...
[Servidor] Client conectado: ('192.168.56.11', 54321)
[Servidor] Parâmetros recebidos: range1=500, range2=1000
[Servidor] Iniciando processos em paralelo...
[Processo 1 - PID: 1234] Iniciando...
[Processo 2 - PID: 1235] Iniciando...
[Processo 1 - PID: 1234] Concluído: 500000
[Processo 2 - PID: 1235] Concluído: 500000
[Servidor] Resultado final: 1000000
```

**Terminal do client:**
```
[Client] Conectado ao servidor.
[Client] Enviando parâmetros: {'range1': 500, 'range2': 1000}
[Client] Aguardando resultado...
[Client] Resultado recebido: 1000000
```

---

## Solução de problemas

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