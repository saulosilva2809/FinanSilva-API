def message_recurring_transaction_success(first_name, description, value, account_name):
    # TODO: melhorar essa message
    """
    Padroniza a mensagem de sucesso para processamento de transação recorrente.
    """
    email_subject = f"✅ Lançamento Realizado: {description}"
    
    email_body = f"""
    Olá, {first_name}!

    A sua transação recorrente "{description}" foi processada com sucesso pelo FinanSilva.

    📊 Detalhes do Lançamento:
    - Valor: R$ {value}
    - Conta: {account_name}
    - Data: Agora

    O saldo da sua conta já foi atualizado e o próximo agendamento já está configurado no nosso sistema.

    Atenciosamente,
    Equipe FinanSilva
    """

    return {
        'email_subject': email_subject,
        'email_body': email_body,
    }