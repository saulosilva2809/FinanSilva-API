def message_approve_recurring_transaction(rec, old_time_fmt, updated_at, new_time_fmt):
    email_subject = f"✅ Transação Confirmada: {rec.description}"
                
    email_body = f"""
    Olá!

    A sua transação recorrente "{rec.description}" foi processada com sucesso.

    Detalhamento da operação:
    ---------------------------------------------------------
    💰 Valor: R$ {rec.value}
    📝 Descrição: {rec.description}
    ---------------------------------------------------------

    O que mudou no seu agendamento:
    ⏰ Execução do dia: {old_time_fmt} realizada em: {updated_at} (Z)
    📅 Próxima execução agendada para: {new_time_fmt} (Z)

    O seu novo agendamento já foi atualizado no sistema e ocorrerá automaticamente na data informada acima.

    Atenciosamente,
    Sistema FinanSilva
    """

    return {
        'email_subject': email_subject,
        'email_body': email_body,
    }
