import textwrap
import datetime

LIMITE_SAQUES = 3


def menu():
    menu = """\n
    ================= MENU =================
    [D]\tDepositar
    [S]\tSacar
    [E]\tExtrato
    [C]\tExtrato Consolidado
    [NC]\tNova conta
    [LC]\tListar contas
    [NU]\tNovo usuário
    [Q]\tSair
    => """
    return input(textwrap.dedent(menu)).upper()


def depositar(saldo, valor, extrato, resumo_extrato, total_depositado, /):
    if valor > 0:
        saldo += valor
        total_depositado += valor
        data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"{data_hora} | Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, total_depositado, resumo_extrato


def sacar(*, saldo, valor, extrato, resumo_extrato, total_sacado, limite, numero_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        total_sacado += valor
        data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"{data_hora} | Saque:\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, resumo_extrato, total_sacado, limite, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ===============")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("========================================")


def exibir_resumo_extrato(saldo, /, *, total_depositado, total_sacado):
    print("\n========= EXTRATO CONSOLIDADO ==========")
    if total_depositado == 0 and total_sacado == 0:
        print("Não foram realizadas movimentações.")
    else:
        print(f"\nTotal Depositado: R$ {total_depositado:.2f}")
        print(f"Total Sacado: R$ {total_sacado:.2f}")
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento,
                    "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [
        usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    resumo_extrato = ""
    numero_saques = 0
    total_depositado = 0
    total_sacado = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "D":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato, total_depositado, resumo_extrato = depositar(
                saldo, valor, extrato, resumo_extrato, total_depositado)

        elif opcao == "S":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato, resumo_extrato, total_sacado, limite, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                total_sacado=total_sacado,
                resumo_extrato=resumo_extrato,
                limite=limite,
                numero_saques=numero_saques,
            )

        elif opcao == "E":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "C":
            exibir_resumo_extrato(
                saldo, total_depositado=total_depositado, total_sacado=total_sacado)

        elif opcao == "NU":
            criar_usuario(usuarios)

        elif opcao == "NC":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "LC":
            listar_contas(contas)

        elif opcao == "Q":
            break

        else:
            print("Opção inválida, por favor selecione novamente as opções do menu.")


main()
