# 🏛️ Guia de Clean Architecture — Java 21 & Spring Boot 3

Este guia define a estrutura arquitetural oficial recomendada pelo **Agente Código (NOVA)** para microsserviços e projetos da trilha **Santander 2026**.

---

## 🎯 Princípios Fundamentais

1. **Independência de Frameworks:** A regra de negócio principal (`domain` e `application`) não deve depender de anotações ou bibliotecas de framework (como Spring Web, JPA ou Jackson).
2. **Regra de Dependência:** Dependências apontam sempre de fora para dentro:
   `infrastructure` ➔ `application` ➔ `domain`
3. **Imutabilidade e Tipagem Estrita (Java 21):**
   - Utilização de `record` para todos os DTOs de entrada e saída.
   - `Pattern Matching` e `Sealed Classes` para modelagem de estados de domínio.
   - `Optional` e `Streams` aplicados de forma idiomática e legível.

---

## 📦 Estrutura de Camadas & Pacotes

```text
com.nova.<modulo>/
├── domain/                                  # 1. NÚCLEO DO NEGÓCIO (Puro Java)
│   ├── model/                               # Entidades ricas e Value Objects
│   │   └── Entidade.java
│   ├── repository/                          # Ports (Interfaces de persistência)
│   │   └── EntidadeRepository.java
│   └── exception/                           # Exceções de regras de negócio
│       ├── RegraDeNegocioException.java
│       └── RecursoNaoEncontradoException.java
│
├── application/                             # 2. CASOS DE USO & ORQUESTRAÇÃO
│   ├── dto/                                 # DTOs de transporte (Java 21 records)
│   │   ├── EntidadeRequest.java
│   │   └── EntidadeResponse.java
│   └── usecase/                             # Use Cases de responsabilidade única
│       ├── CriarEntidadeUseCase.java
│       └── BuscarEntidadeUseCase.java
│
└── infrastructure/                          # 3. DETALHES EXTERNOS & ADAPTADORES
    ├── persistence/                         # Adaptadores de Banco de Dados
    │   ├── entity/                          # Entidades JPA (@Entity)
    │   │   └── EntidadeJpaEntity.java
    │   ├── repository/                      # Implementação do Port + Spring Data
    │   │   ├── SpringDataEntidadeRepository.java
    │   │   └── EntidadeRepositoryImpl.java
    │   └── mapper/                          # Conversores Domain <-> JPA Entity
    │       └── EntidadeMapper.java
    ├── web/                                 # Adaptadores HTTP / REST
    │   ├── controller/                      # @RestController
    │   │   └── EntidadeController.java
    │   └── handler/                         # RFC 7807 ProblemDetails Global Handler
    │       └── GlobalExceptionHandler.java
    └── mcp/                                 # Ferramentas expostas ao ecossistema de IA (MCP)
        └── ModuloMcpTools.java
```

---

## 🔄 Fluxo de Execução Típico

```text
[ Cliente HTTP / MCP ]
         │
         ▼
[ EntidadeController ] (Valida @Valid DTO Record)
         │
         ▼
[ CriarEntidadeUseCase ] (Aplica regras de negócio)
         │
         ▼
[ EntidadeRepository ] (Interface / Port)
         │
         ▼
[ EntidadeRepositoryImpl ] (Adapter) ➔ [ SpringDataJpaRepository ] ➔ [ Banco de Dados ]
```

---

## 🛡️ Padrão para Tratamento de Exceções (RFC 7807)

Todos os endpoints REST devem retornar `ProblemDetail` em caso de erro, garantindo respostas ricas e padronizadas:

```java
@ExceptionHandler(RecursoNaoEncontradoException.class)
public ProblemDetail handleRecursoNaoEncontrado(RecursoNaoEncontradoException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
    problem.setTitle("Recurso Não Encontrado");
    problem.setType(URI.create("https://nova.dev/errors/not-found"));
    problem.setProperty("timestamp", Instant.now());
    return problem;
}
```
