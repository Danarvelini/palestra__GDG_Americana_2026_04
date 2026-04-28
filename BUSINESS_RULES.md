# User Service — Regras de Negócio

Este documento define o **comportamento esperado** da API.  
Todo contribuidor **deve** ler este documento antes de abrir ou revisar um PR.

---

## BR-01 · Unicidade de E-mail

O e-mail de cada usuário deve ser **único** no sistema.  
Tentar cadastrar um e-mail já existente deve retornar **HTTP 409 Conflict**.

---

## BR-02 · Papéis de Usuário (Roles)

O campo `role` aceita apenas os valores: `viewer`, `editor`, `admin`.  
O **valor padrão para todo novo usuário é `viewer`**.  
Qualquer valor fora desse conjunto deve ser rejeitado com **HTTP 422 Unprocessable Entity**.

---

## BR-03 · Soft Delete

Usuários **nunca são removidos permanentemente** do banco de dados.  
Uma operação `DELETE` deve setar `active = False` no registro.  
Usuários inativos (`active = False`) devem ser tratados como inexistentes em **todos os endpoints de leitura**.

---

## BR-04 · Audit Log

Toda **operação de escrita** (create, update, delete) deve adicionar um registro à lista
`audit_log` antes de retornar a resposta.

Cada registro deve conter:

| Campo       | Descrição                              |
|-------------|----------------------------------------|
| `action`    | `"create"`, `"update"` ou `"delete"`  |
| `user_id`   | O ID do usuário afetado                |
| `timestamp` | Timestamp UTC no formato ISO-8601      |

---

## BR-05 · Geração de ID

O ID de novos usuários deve ser gerado incrementando o **maior ID existente** em `users_db`:

```python
new_id = max(users_db.keys()) + 1
```

Usar `len(users_db) + 1` é **proibido** — gera IDs duplicados após qualquer deleção.
