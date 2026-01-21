def message_recurring_transaction_created(first_name, description, value, frequency, start_date, next_run):
    """
    Gera o conteúdo de e-mail informando que um agendamento recorrente foi criado.
    """
    email_subject = f"📅 Agendamento Confirmado: {description}"
    
    # Formatação de moeda
    balance_fmt = f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    email_body = f"""
    Olá, {first_name}!

    Você acabou de cadastrar um novo agendamento recorrente no FinanSilva. 
    Isso ajudará você a manter suas contas em dia sem precisar lançar manualmente todo mês!

    Detalhes do Agendamento:
    ---------------------------------------------------------
    📝 Descrição: {description}
    💰 Valor: {balance_fmt}
    🔄 Frequência: {frequency}
    📅 Data de Início: {start_date}
    🚀 Próxima Execução: {next_run}
    ---------------------------------------------------------

    Como funciona?
    Na data de cada execução, o sistema criará automaticamente uma transação 
    no seu extrato e você receberá uma confirmação por e-mail.

    Dica: Certifique-se de ter saldo na conta vinculada na data da execução 
    para manter seus relatórios precisos.

    Você pode editar ou cancelar este agendamento a qualquer momento pelo app.

    Atenciosamente,
    Equipe FinanSilva
    """

    return {
        'email_subject': email_subject,
        'email_body': email_body,
    }
