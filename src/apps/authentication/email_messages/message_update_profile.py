def message_update_profile(first_name, changes, updated_at):
    """
    Gera o conteúdo de e-mail informando alterações no perfil.
    """
    email_subject = f"⚠️ Alteração de Perfil - FinanSilva"
    
    changes_str = ""
    for field, values in changes.items():
        field_name = field.replace('_', ' ').title()
        changes_str += f"🔹 {field_name}:\n"
        changes_str += f"   - De: {values['de']}\n"
        changes_str += f"   - Para: {values['para']}\n\n"

    email_body = f"""
    Olá, {first_name}!

    Detectamos que algumas informações do seu perfil no FinanSilva-API foram alteradas.

    Informações da atualização:
    ---------------------------------------------------------
    📅 Data/Hora: {updated_at}
    ---------------------------------------------------------

    Resumo das alterações:
    {changes_str}

    Se foi você quem realizou essas mudanças, pode desconsiderar este e-mail.

    🔒 Caso você não tenha solicitado essas alterações, recomendamos que altere sua senha imediatamente.

    Atenciosamente,
    Equipe FinanSilva
    """

    return {
        'email_subject': email_subject,
        'email_body': email_body,
    }
