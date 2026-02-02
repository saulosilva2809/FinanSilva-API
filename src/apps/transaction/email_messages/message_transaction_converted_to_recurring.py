def message_transaction_converted_to_recurring(first_name, description, value, frequency, next_run):
    """
    Gera o conteúdo de e-mail informando que uma transação comum foi convertida em recorrente.
    """
    email_subject = f"🔄 Transação Convertida: {description}"
    
    # Formatação de moeda (Padrão Brasileiro)
    balance_fmt = f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    email_body = f"""
    Olá, {first_name}!

    Boas notícias! Aquela transação que você realizou agora se tornou um agendamento recorrente.
    Isso significa que o FinanSilva passará a cuidar desse lançamento para você automaticamente.

    Detalhes da Conversão:
    ---------------------------------------------------------
    📝 Descrição: {description}
    💰 Valor: {balance_fmt}
    🔄 Frequência: {frequency}
    🚀 Próxima Execução: {next_run}
    ---------------------------------------------------------

    O que muda agora?
    Você não precisa mais se preocupar em lançar essa despesa ou receita manualmente. 
    Nas próximas datas, o sistema fará o trabalho pesado e apenas te avisará quando estiver pronto.

    Se precisar ajustar o valor ou a frequência, basta acessar a seção de 
    "Agendamentos" no seu painel.

    Continue no controle das suas finanças!

    Atenciosamente,
    Equipe FinanSilva
    """

    return {
        'email_subject': email_subject,
        'email_body': email_body,
    }