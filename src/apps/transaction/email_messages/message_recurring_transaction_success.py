def message_recurring_transaction_success(first_name, description, value, account_name):
    """
    Mensagem profissional para confirmação de execução de transação recorrente.
    """
    email_subject = f"💰 Lançamento Confirmado: {description}"
    
    # Formatando o valor para garantir que apareça como dinheiro (opcional, se já não vier formatado)
    # Ex: 1500.0 -> 1.500,00
    
    email_body = f"""
    Olá, {first_name},

    Passando para avisar que processamos o lançamento automático da sua transação recorrente. Tudo certo com o seu financeiro!

    📌 Resumo do Lançamento:
    --------------------------------------------------
    🔹 Descrição: {description}
    🔹 Valor: R$ {value}
    🔹 Conta de Destino: {account_name}
    🔹 Status: Processado com Sucesso
    --------------------------------------------------

    ✅ O que aconteceu agora?
    1. O saldo da conta "{account_name}" foi atualizado automaticamente.
    2. O próximo agendamento já foi programado para manter sua organização em dia.

    Você pode conferir os detalhes completos acessando o painel do FinanSilva.

    Atenciosamente,
    Equipe FinanSilva
    """

    return {
        'email_subject': email_subject,
        'email_body': email_body,
    }