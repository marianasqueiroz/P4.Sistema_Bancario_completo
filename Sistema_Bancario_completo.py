from abc import ABC, abstractmethod
from datetime import date

# Variáveis globais para gerenciar o estado do sistema
AGENCIA = "0001"
clientes = [] # Lista para armazenar objetos Cliente
contas = []   # Lista para armazenar objetos Conta

menu = '''

==========================================
Este é o Menu do nosso sistema bancário
==========================================
 
Digite a opção desejada:


[1] = Saque
[2] = Depósito
[3] = Extrato
[4] = Realizar Cadastro
[5] = Abrir Conta Corrente
[6] = Sair


'''

# --- CLASSES DO SISTEMA BANCÁRIO (Sem Alterações na Estrutura) ---

class Transacao(ABC):
    """Interface para transações, exige o método registrar."""
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            # Adiciona a transação ao histórico, que agora é uma lista de objetos
            conta.historico.adicionar_transacao(self)
            print(f"\n--- Saque de R$ {self.valor:.2f} realizado com sucesso! ---")
        else:
            print("\n--- Falha ao realizar Saque. ---")

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
        
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            # Adiciona a transação ao histórico, que agora é uma lista de objetos
            conta.historico.adicionar_transacao(self)
            print(f"\n--- Depósito de R$ {self.valor:.2f} realizado com sucesso! ---")
        else:
            print("\n--- Falha ao realizar Depósito. ---")

class Historico:
    def __init__(self):
        self._transacoes = [] # Corrigido para usar o prefixo '_' para a lista

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        # Armazenar o objeto Transacao e o tipo (para extrato/limite de saque)
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": date.today().strftime("%d-%m-%Y")
        })

class Conta:
    # A classe Conta não pode ser criada diretamente, apenas suas subclasses,
    # mas para simplificar, ajustamos o __init__ para aceitar o saldo inicial.
    def __init__(self, numero, cliente, saldo=0): # Ajustado para saldo default 0
        self._saldo = saldo
        self._numero = numero
        self._agencia = AGENCIA # Usando a variável global AGENCIA
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente 
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo

        if valor <= 0:
            print("\n--- O valor informado é inválido. ---")
        elif excedeu_saldo:
            print("\n--- Você não tem saldo o suficiente. ---")
        else:
            self._saldo -= valor
            return True
        return False # Retorna False se a operação falhar
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True 
        else:
            print("\n--- Operação Falhou: valor inválido. ---")
            return False
    
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao (self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)
    
    @property
    def contas(self):
        return self._contas

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nascimento(self):
        return self._data_nascimento
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        # Ajustado para passar numero e cliente para o superclass (Conta)
        super().__init__(numero=numero, cliente=cliente, saldo=0) 
        self._limite = limite
        self._limite_saques = limite_saques
        
    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques
    
    def sacar(self, valor):
        # Conta o número de saques (objetos Saque) no histórico
        numero_saques = len([
            transacao for transacao in self.historico.transacoes 
            if transacao["tipo"] == Saque.__name__
        ])
        
        excedeu_limite = valor > self.limite
        # Corrigido operador de comparação para >=
        excedeu_saques = numero_saques >= self.limite_saques 

        if excedeu_limite:
            print(f"\n--- O valor do saque excede o limite de R$ {self.limite:.2f}. ---")
            return False
        elif excedeu_saques:
            print(f"\n--- Número máximo de {self.limite_saques} saques excedido. ---")
            return False
        else:
            # Chama o método sacar da superclasse (Conta)
            return super().sacar(valor)
        
    def __str__(self):
        return f"""\
    Agência:\t{self.agencia}
    Conta:\t\t{self.numero}
    Titular:\t{self.cliente.nome}
"""

# --- FUNÇÕES DE INTERAÇÃO COM O USUÁRIO ---

def filtrar_cliente(cpf, clientes):
    """Busca um cliente na lista pelo CPF."""
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def filtrar_conta(numero_conta, contas):
    """Busca uma conta na lista pelo número."""
    contas_filtradas = [conta for conta in contas if conta.numero == numero_conta]
    return contas_filtradas[0] if contas_filtradas else None

def recuperar_conta_cliente(cliente):
    """Retorna a primeira conta de um cliente. Para simplificação."""
    if not cliente.contas:
        print("\n--- Cliente não possui conta! ---")
        return None
    # Retorna a primeira conta do cliente (simplificação)
    return cliente.contas[0]

def depositar():
    """Realiza a operação de Depósito."""
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n--- Cliente não encontrado! ---")
        return

    valor = input("Informe o valor do depósito: ")
    try:
        valor = float(valor)
    except ValueError:
        print("\n--- Valor inválido! Use apenas números. ---")
        return

    conta = recuperar_conta_cliente(cliente)
    if conta:
        transacao = Deposito(valor)
        cliente.realizar_transacao(conta, transacao)

def sacar():
    """Realiza a operação de Saque."""
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n--- Cliente não encontrado! ---")
        return

    valor = input("Informe o valor do saque: ")
    try:
        valor = float(valor)
    except ValueError:
        print("\n--- Valor inválido! Use apenas números. ---")
        return

    conta = recuperar_conta_cliente(cliente)
    if conta:
        transacao = Saque(valor)
        cliente.realizar_transacao(conta, transacao)

def exibir_extrato():
    """Exibe o extrato da conta do cliente."""
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n--- Cliente não encontrado! ---")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            tipo = transacao["tipo"]
            valor = transacao["valor"]
            data = transacao["data"]
            print(f"{data} | {tipo}: \t\tR$ {valor:.2f}")

    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente():
    """Cria um novo cliente (PessoaFisica) e o adiciona à lista global."""
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n--- Já existe cliente com esse CPF! ---")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Validação simples da data para evitar erro. O ideal seria usar datetime.strptime
    try:
        # Apenas para usar a data de forma simples no objeto
        dia, mes, ano = map(int, data_nascimento.split('-'))
        data_nascimento_obj = date(ano, mes, dia) 
    except:
        print("\n--- Formato de data inválido. Cadastro cancelado. ---")
        return


    novo_cliente = PessoaFisica(
        cpf=cpf, 
        nome=nome, 
        data_nascimento=data_nascimento_obj, 
        endereco=endereco
    )
    clientes.append(novo_cliente)
    print("\n--- Cliente criado com sucesso! ---")

def criar_conta_corrente():
    """Cria uma nova ContaCorrente para um cliente existente."""
    cpf = input("Informe o CPF do titular (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n--- Cliente não encontrado, fluxo de criação de conta encerrado! ---")
        return

    # Gera o próximo número de conta (baseado no tamanho da lista global de contas)
    numero_conta = len(contas) + 1 
    
    # Cria a instância de ContaCorrente
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta) 

    contas.append(conta) # Adiciona à lista global de contas
    cliente.adicionar_conta(conta) # Associa a conta ao cliente

    print("\n--- Conta criada com sucesso! ---")
    print(conta) # Exibe os detalhes da nova conta

# --- FUNÇÃO PRINCIPAL (Loop de Execução) ---

def main():
    while True:
        print(menu)
        opcao = input().strip()

        if opcao == "1":
            sacar()
        
        elif opcao == "2":
            depositar()
        
        elif opcao == "3":
            exibir_extrato()
        
        elif opcao == "4":
            criar_cliente()
        
        elif opcao == "5":
            criar_conta_corrente()

        elif opcao == "6":
            print("\nObrigado por utilizar nosso sistema bancário. Até mais!")
            break

        else:
            print("\n--- Opção inválida, por favor selecione novamente a opção desejada. ---")

if __name__ == "__main__":
    main()