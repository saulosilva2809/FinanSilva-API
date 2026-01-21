def message_transfer_completed(first_name, value, from_account, to_account, date):
    """
    Gera o conteúdo de e-mail informando que uma transferência entre contas foi realizada.
    """
    email_subject = f"💸 Transferência Realizada: {from_account} ➔ {to_account}"
    
    # Formatação de moeda R$
    value_fmt = f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    email_body = f"""
    Olá, {first_name}!

    Uma transferência entre suas contas foi processada com sucesso no FinanSilva.

    Resumo da Movimentação:
    ---------------------------------------------------------
    💰 Valor: {value_fmt}
    📤 Origem: {from_account}
    📥 Destino: {to_account}
    📅 Data/hora: {date}
    ---------------------------------------------------------

    O que isso significa?
    1. O saldo da conta "{from_account}" foi reduzido.
    2. O saldo da conta "{to_account}" foi aumentado.
    3. Duas transações automáticas (uma despesa e uma receita) foram 
       geradas no seu extrato para manter o histórico correto.

    Dica: Você pode visualizar os detalhes desta transferência na aba 
    de "Transferências" ou no extrato de cada conta envolvida.

    Se você não realizou esta operação, acesse sua conta agora e verifique suas atividades.

    Atenciosamente,
    Equipe FinanSilva
    """

    return {
        'email_subject': email_subject,
        'email_body': email_body,
    }
