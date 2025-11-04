from django.db import models


class BankChoices(models.TextChoices):
    # Bancos tradicionais
    ITAU = "ITAÚ", "Itaú"
    BRADESCO = "BRADESCO", "Bradesco"
    SANTANDER = "SANTANDER", "Santander"
    CAIXA = "CAIXA", "Caixa Econômica Federal"
    BB = "BANCO_DO_BRASIL", "Banco do Brasil"
    SAFRA = "SAFRA", "Banco Safra"
    BTG = "BTG_PACTUAL", "BTG Pactual"
    BANRISUL = "BANRISUL", "Banrisul"
    SICREDI = "SICREDI", "Sicredi"
    SICOOB = "SICOOB", "Sicoob"
    MERCANTIL = "MERCANTIL_DO_BRASIL", "Mercantil do Brasil"
    PAN = "BANCO_PAN", "Banco PAN"
    ORIGINAL = "BANCO_ORIGINAL", "Banco Original"
    C6 = "C6_BANK", "C6 Bank"
    INTER = "INTER", "Banco Inter"

    # Bancos digitais / fintechs
    NUBANK = "NUBANK", "Nubank"
    NEON = "NEON", "Neon"
    PAGBANK = "PAGBANK", "PagBank"
    BS2 = "BS2", "Banco BS2"
    WILLBANK = "WILLBANK", "Will Bank"
    NEXT = "NEXT", "Next"
    MEUBMG = "MEUBMG", "Meu BMG"
    AGIBANK = "AGIBANK", "Agibank"
    XP = "XP", "XP Investimentos"
    CREDICOAMO = "CREDICOAMO", "Credicoamo"

    # Internacionais e outros
    CITI = "CITIBANK", "Citibank"
    HSBC = "HSBC", "HSBC"
    JP_MORGAN = "JP_MORGAN", "J.P. Morgan"
    MORGAN_STANLEY = "MORGAN_STANLEY", "Morgan Stanley"
    DEUTSCHE = "DEUTSCHE_BANK", "Deutsche Bank"
    BARCLAYS = "BARCLAYS", "Barclays"

    # Genérico
    OTHER = "OUTRO", "Outro"
