def message_create_account(first_name, account_name, bank_name, initial_balance, created_at):
    """
    Gera o conteúdo de e-mail de confirmação de nova conta bancária cadastrada.
    """
    email_subject = f"🏦 Nova conta conectada: {account_name}"
    
    # Formata o saldo para o padrão brasileiro R$
    balance_fmt = f"R$ {initial_balance:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    email_body = f"""
    Olá, {first_name}!

    Uma nova conta bancária foi cadastrada com sucesso no seu perfil do FinanSilva-API. 
    Agora você pode começar a registrar suas transações e controlar seus gastos nesta conta.

    Detalhes da Conta:
    ---------------------------------------------------------
    🏷️ Nome da Conta: {account_name}
    🏛️ Instituição/Banco: {bank_name}
    💰 Saldo Inicial: {balance_fmt}
    📅 Cadastrada em: {created_at}
    ---------------------------------------------------------

    Próximos passos:
    1. ✅ Verifique se o saldo inicial está correto.
    2. 💸 Adicione suas receitas e despesas vinculadas a esta conta.
    3. 📊 Acompanhe o gráfico de evolução no seu Dashboard.

    Dica: Mantenha seus registros atualizados para ter uma visão real da sua saúde financeira!

    Se você não reconhece este cadastro, por favor, entre em contato com nosso suporte.

    Atenciosamente,
    Equipe FinanSilva
    """

    return {
        'email_subject': email_subject,
        'email_body': email_body,
    }
