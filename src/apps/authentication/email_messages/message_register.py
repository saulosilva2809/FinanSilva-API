def message_register(first_name, email, created_at):
    """
    Gera o conteúdo de e-mail de boas-vindas para novos usuários.
    :param user: Instância do modelo de usuário (Django User model)
    """
    email_subject = f"🚀 Bem-vindo(a) ao FinanSilva, {first_name}!"
                
    email_body = f"""
    Olá, {first_name}!

    É um prazer ter você conosco no FinanSilva-API. Sua conta foi criada com sucesso e agora você tem controle total sobre suas finanças.

    Informações da sua conta:
    ---------------------------------------------------------
    👤 Usuário: {first_name}
    📧 E-mail cadastrado: {email}
    📅 Data de adesão: {created_at}
    ---------------------------------------------------------

    O que você pode fazer agora:
    1. 🏦 Cadastre suas Contas Bancárias.
    2. 💸 Registre suas primeiras Transações.
    3. 📅 Agende Transações Recorrentes para não esquecer as contas.
    4. 📊 Acompanhe tudo pelo seu Dashboard em tempo real.

    Se precisar de qualquer ajuda para começar, basta responder a este e-mail.

    Atenciosamente,
    Equipe FinanSilva
    """

    return {
        'email_subject': email_subject,
        'email_body': email_body,
    }
