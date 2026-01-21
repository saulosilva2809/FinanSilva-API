def message_delete_account(first_name, account_name, bank_name, deleted_at):
    """
    Gera o conteúdo de e-mail confirmando a exclusão de uma conta bancária.
    """
    email_subject = f"⚠️ Conta Removida: {account_name}"
    
    email_body = f"""
    Olá, {first_name}!

    Este e-mail é para confirmar que a conta bancária "{account_name}" ({bank_name}) 
    foi removida do seu perfil no FinanSilva.

    Detalhes da exclusão:
    ---------------------------------------------------------
    📅 Data/Hora: {deleted_at}
    🏦 Conta: {account_name}
    🏛️ Instituição: {bank_name}
    ---------------------------------------------------------

    O que acontece agora?
    * As transações vinculadas exclusivamente a esta conta foram removidas ou desvinculadas.
    * O saldo total do seu perfil foi recalculado desconsiderando esta conta.

    Segurança:
    Se você **NÃO** realizou esta exclusão, sua conta pode ter sido acessada por terceiros. 
    Nesse caso, entre em contato com nosso suporte imediatamente e altere sua senha.

    Atenciosamente,
    Equipe FinanSilva
    """

    return {
        'email_subject': email_subject,
        'email_body': email_body,
    }