# 🏦 Projeto Bank do Zé: O Seu Novo Sistema Bancário em Python!

Olá! Dê uma olhada neste projeto de sistema bancário feito em Python. Não é só um monte de código, é uma forma super legal de aprender sobre **Programação Orientada a Objetos (POO)** na prática.

---

## O que torna este projeto especial?

Esqueça os dicionários bagunçados! Aqui, a gente guarda tudo do jeito certo: usando **Classes**. Isso torna o código muito mais organizado e fácil de manter.

| Conceito POO | O que acontece no nosso banco | Exemplo de Classe |
| :---: | :---: | :---: |
| **Abstração (ABC)** | Garante que certas classes sigam regras (como a `Transacao` exigir um método `registrar`). | `Transacao` |
| **Herança** | Clientes e Contas compartilham comportamentos e características. | `PessoaFisica` herda de `Cliente` |
| **Encapsulamento** | Dados internos (como `_saldo`) são protegidos e só acessíveis via `properties`. | `Conta` |
| **Polimorfismo** | `Sacar` e `Depositar` funcionam de formas diferentes dependendo do tipo de conta (`ContaCorrente`). | `ContaCorrente.sacar()` |

---

## 🛠️ As Classes Essenciais (O "Core" do Banco)

* **`Cliente` e `PessoaFisica`:** É quem usa o banco! O `Cliente` básico guarda o endereço, e o `PessoaFisica` adiciona CPF, nome e data de nascimento.
* **`Conta` e `ContaCorrente`:** Onde o dinheiro mora! A `ContaCorrente` é mais esperta, adicionando **limites de saque e um valor máximo** para cada retirada.
* **`Historico`:** O nome já diz! Ele guarda uma lista de todas as transações, para você não se perder.
* **`Transacao`, `Saque`, e `Deposito`:** Essas são as ações. Elas garantem que, antes de qualquer coisa, a operação seja "registrada" no `Historico` da conta.

---

## 💻 Interação com o Usuário (A parte divertida!)

O código não é apenas um monte de classes, ele tem uma **interface simples de Menu** que roda em *loop*. O usuário escolhe a opção, e o sistema chama a função correta.

```python
# O famoso bloco que inicia o menu e a execução
if __name__ == "__main__":
    main()