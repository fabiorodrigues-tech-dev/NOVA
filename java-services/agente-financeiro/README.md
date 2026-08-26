# 💰 Agente Financeiro - Serviço Back-end

Serviço central de gestão financeira pessoal e controle orçamentário do ecossistema **NOVA**, desenvolvido com foco em Clean Architecture, Java 21 e Spring Boot 3.

---

## 🛠️ Tecnologias Utilizadas
- **Java 21 LTS** (Records, Streams, Pattern Matching)
- **Spring Boot 3.3.3** (Spring Web, Spring Data JPA, Bean Validation)
- **H2 Database** (Em memória)
- **JUnit 5, Mockito & AssertJ** (Testes unitários e de integração)

---

## 🏛️ Arquitetura (Clean Architecture)

```
com.nova.agentefinanceiro/
├── domain/                  # Entidades, Enums, Value Objects e Portas de Repositório (Puro)
│   ├── model/               # Transacao, CategoriaTransacao, TipoTransacao, ResumoFinanceiro
│   └── repository/          # TransacaoRepository (Output Port)
├── application/             # Casos de Uso e DTOs
│   ├── dto/                 # TransacaoRequest, TransacaoResponse, ResumoFinanceiroResponse
│   └── usecase/             # CadastrarTransacao, ListarTransacoes, CalcularResumoFinanceiro
└── infrastructure/          # Adaptadores Tecnológicos (Spring, Web, JPA)
    ├── persistence/         # TransacaoJpaEntity, SpringDataTransacaoRepository, TransacaoMapper
    └── web/                 # TransacaoController, GlobalExceptionHandler (RFC 7807)
```

---

## 🚀 Como Executar

### 1. Pré-requisitos
- JDK 21+ instalado.
- Maven 3.9+ instalado (ou abra a pasta na sua IDE favorita: IntelliJ IDEA, VS Code, Eclipse).

### 2. Executando a Aplicação
```bash
mvn spring-boot:run
```
A aplicação iniciará na porta **8081**: `http://localhost:8081`.

### 3. Console do Banco H2
- URL: `http://localhost:8081/h2-console`
- JDBC URL: `jdbc:h2:file:./data/financiadb`
- User: `sa`
- Password: *(em branco)*
- Arquivo local: `data/financiadb.mv.db`

---

## 🧪 Executando os Testes
```bash
mvn test
```

## 🤖 Model Context Protocol (MCP Server)

O microsserviço inclui suporte nativo ao **Model Context Protocol (MCP)** via **Spring AI**, permitindo que o **Antigravity (ou qualquer cliente MCP)** conecte e invoque ferramentas inteligentes automaticamente.

### 🛠️ Ferramentas MCP Expostas

1. **`cadastrar_transacao`**
   - **Descrição:** *"Cadastra um novo gasto ou receita financeira pessoal no sistema. Use esta ferramenta sempre que o usuário informar um novo gasto realizado, uma compra, pagamento ou recebimento."*
   - **Parâmetros:** `descricao` (obrigatório), `valor` (obrigatório), `tipo` (opcional: DESPESA/RECEITA), `categoria` (opcional: ALIMENTACAO, TRANSPORTE, etc.), `data` (opcional: AAAA-MM-DD).

2. **`listar_transacoes`**
   - **Descrição:** *"Lista o histórico de transações e movimentações financeiras cadastradas, com suporte a filtro opcional por período de datas. Use para consultar os últimos gastos ou listar o extrato."*
   - **Parâmetros:** `inicio` (opcional: AAAA-MM-DD), `fim` (opcional: AAAA-MM-DD).

3. **`resumo_financeiro`**
   - **Descrição:** *"Calcula o resumo e balanço financeiro consolidado de um período, totalizando despesas, receitas, saldo e detalhamento dos gastos agrupados por categoria. Use quando o usuário perguntar quanto gastou no mês/período ou pedir uma análise/balanço do orçamento."*
   - **Parâmetros:** `inicio` (opcional: AAAA-MM-DD), `fim` (opcional: AAAA-MM-DD).

### 🔌 Conexão no Antigravity (`mcp_config.json`)

Para registrar o servidor MCP no Antigravity ou em outros clientes MCP compatíveis:

```json
{
  "mcpServers": {
    "agente-financeiro": {
      "url": "http://localhost:8081/sse"
    }
  }
}
```

---

## 📡 Endpoints REST

### 1. Cadastrar Transação
- **POST** `/api/transacoes`
- **Request Body:**
```json
{
  "descricao": "Curso Santander AI Java",
  "valor": 150.00,
  "tipo": "DESPESA",
  "categoria": "EDUCACAO",
  "data": "2026-08-25"
}
```

### 2. Listar Transações
- **GET** `/api/transacoes`
- **Filtros opcionais:** `/api/transacoes?inicio=2026-08-01&fim=2026-08-31`

### 3. Obter Resumo Financeiro
- **GET** `/api/transacoes/resumo`
- **Filtros opcionais:** `/api/transacoes/resumo?inicio=2026-08-01&fim=2026-08-31`
- **Exemplo de Resposta:**
```json
{
  "totalGasto": 150.00,
  "totalReceitas": 5000.00,
  "saldo": 4850.00,
  "quantidadeTransacoes": 1,
  "periodoInicio": "2026-08-01",
  "periodoFim": "2026-08-31",
  "totalPorCategoria": {
    "EDUCACAO": 150.00
  }
}
```
