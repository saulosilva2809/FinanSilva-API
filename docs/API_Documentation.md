# 💰 FinanSilva API Documentation

API RESTful para o sistema financeiro pessoal **FinanSilva**, construída com **Django REST Framework**.  
Esta documentação lista todos os endpoints principais, seus exemplos de uso e respostas esperadas em JSON.  

---

## 🔐 AUTENTICAÇÃO / USUÁRIOS

### 1️⃣ `POST /api/v1/auth/register/`
Cria um novo usuário.

#### Request:
```json
{
  "first_name": "Saulo",
  "last_name": "Silva",
  "email": "saulo@gmail.com",
  "password": "senha123"
}
```

#### Response (201 Created):
```json
{
  "id": 1,
  "first_name": "Saulo",
  "last_name": "Silva",
  "email": "saulo@gmail.com"
}
```

---

### 2️⃣ `POST /api/v1/auth/login/`
Gera tokens de acesso (JWT).

#### Request:
```json
{
  "email": "saulo@gmail.com",
  "password": "senha123"
}
```

#### Response (200 OK):
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUz..."
}
```

---

### 3️⃣ `POST /api/v1/auth/refresh/`
Atualiza o access token.

#### Request:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUz..."
}
```

---

### 4️⃣ `GET /api/v1/auth/profile/`
Retorna dados do usuário logado.

#### Header:
```
Authorization: Bearer <access_token>
```

#### Response:
```json
{
  "id": 1,
  "first_name": "Saulo",
  "last_name": "Silva",
  "email": "saulo@gmail.com",
  "date_joined": "2025-11-01T14:22:12Z"
}
```

---

### 5️⃣ `PATCH /api/v1/auth/profile/`
Atualiza os dados do usuário.

#### Request:
```json
{
  "first_name": "Saulo Henrique",
  "last_name": "Silva"
}
```

#### Response:
```json
{
  "id": 1,
  "first_name": "Saulo Henrique",
  "last_name": "Silva",
  "email": "saulo@gmail.com"
}
```

---

### 6️⃣ `POST /api/v1/auth/logout/`
Invalida o refresh token (se estiver usando o `token_blacklist`).

#### Request:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### Response:
```json
{
  "detail": "Logout successful."
}
```

---

## 💰 CONTAS (Accounts)

### 7️⃣ `GET /api/v1/accounts/`
Lista as contas do usuário logado.

#### Response:
```json
[
  {
    "id": 1,
    "name": "Nubank",
    "balance": 1250.50,
    "type": "checking",
    "created_at": "2025-10-25T12:00:00Z"
  },
  {
    "id": 2,
    "name": "Carteira",
    "balance": 200.00,
    "type": "cash",
    "created_at": "2025-10-27T10:30:00Z"
  }
]
```

---

### 8️⃣ `POST /api/v1/accounts/`
Cria uma nova conta.

#### Request:
```json
{
  "name": "Inter",
  "balance": 3000.00,
  "type": "savings"
}
```

#### Response:
```json
{
  "id": 3,
  "name": "Inter",
  "balance": 3000.00,
  "type": "savings",
  "created_at": "2025-11-01T12:22:10Z"
}
```

---

### 9️⃣ `GET /api/v1/accounts/{id}/`
Obtém detalhes de uma conta.

#### Response:
```json
{
  "id": 1,
  "name": "Nubank",
  "balance": 1250.50,
  "type": "checking",
  "created_at": "2025-10-25T12:00:00Z"
}
```

---

### 🔟 `PATCH /api/v1/accounts/{id}/`
Atualiza dados da conta.

#### Request:
```json
{
  "name": "Nubank (principal)"
}
```

#### Response:
```json
{
  "id": 1,
  "name": "Nubank (principal)",
  "balance": 1250.50,
  "type": "checking"
}
```

---

### 1️⃣1️⃣ `DELETE /api/v1/accounts/{id}/`
Remove uma conta (e opcionalmente, todas as transações associadas).

#### Response (204 No Content):
```
(nenhum conteúdo)
```

---

## 💸 TRANSAÇÕES (Transactions)

### 1️⃣2️⃣ `GET /api/v1/transactions/`
Lista as transações do usuário (ou filtradas por conta/categoria).

#### Response:
```json
[
  {
    "id": 1,
    "account": 1,
    "type": "expense",
    "amount": 50.00,
    "category": "Alimentação",
    "description": "Lanche",
    "date": "2025-10-29T18:45:00Z"
  },
  {
    "id": 2,
    "account": 1,
    "type": "income",
    "amount": 200.00,
    "category": "Salário",
    "description": "Pagamento mensal",
    "date": "2025-10-28T09:00:00Z"
  }
]
```

---

### 1️⃣3️⃣ `POST /api/v1/transactions/`
Cria uma transação.

#### Request:
```json
{
  "account": 1,
  "type": "expense",
  "amount": 150.00,
  "category": "Transporte",
  "description": "Gasolina"
}
```

#### Response:
```json
{
  "id": 3,
  "account": 1,
  "type": "expense",
  "amount": 150.00,
  "category": "Transporte",
  "description": "Gasolina",
  "date": "2025-11-01T14:00:00Z"
}
```

---

## 🏷️ CATEGORIAS (Categories)

### 1️⃣4️⃣ `GET /api/v1/categories/`
Lista todas as categorias do usuário.

#### Response:
```json
[
  {"id": 1, "name": "Alimentação"},
  {"id": 2, "name": "Transporte"},
  {"id": 3, "name": "Salário"}
]
```

---

### 1️⃣5️⃣ `POST /api/v1/categories/`
Cria uma categoria personalizada.

#### Request:
```json
{
  "name": "Investimentos"
}
```

#### Response:
```json
{
  "id": 4,
  "name": "Investimentos"
}
```

---

## 📊 DASHBOARD / RESUMOS

### 1️⃣6️⃣ `GET /api/v1/summary/`
Retorna um resumo financeiro geral.

#### Response:
```json
{
  "total_income": 5000.00,
  "total_expense": 2750.50,
  "balance": 2249.50,
  "by_category": {
    "Alimentação": 850.00,
    "Transporte": 450.00,
    "Lazer": 600.00
  },
  "last_transactions": [
    {"description": "Cinema", "amount": 60.00, "type": "expense"},
    {"description": "Salário", "amount": 3000.00, "type": "income"}
  ]
}
```

---

## ✅ Conclusão

Com esses **16 endpoints**, o **FinanSilva API** cobre:
- Autenticação segura (JWT)
- Gestão de contas e transações
- Categorias personalizáveis
- Relatórios e dashboards financeiros
- Edição de perfil e logout seguro

---

**Autor:** Saulo 👨‍💻  
**Tech Stack:** Django REST Framework + PostgreSQL + JWT  
**Status:** 🚀 Em desenvolvimento
