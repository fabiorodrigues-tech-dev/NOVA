# 🔍 Checklist de Code Review — Trilha Santander 2026 (AI Java Back-end)

Este checklist serve como base para revisão estática de código realizada pelo **Agente Código (NOVA)** em projetos, desafios de código da DIO e entregas de microsserviços.

---

## 1. ☕ Java 21 & Sintaxe Moderna

- [ ] **DTOs Imutáveis:** DTOs de entrada e saída utilizam `record` em vez de classes com getters/setters manuais ou Lombok boilerplate excessivo.
- [ ] **Pattern Matching:** Uso de `instanceof` com pattern matching e `switch expressions` quando houver múltiplos tipos ou enums.
- [ ] **Coleções Imutáveis:** Uso de `List.of()`, `Set.of()` ou `Map.of()` para coleções estáticas; evitar mutação desnecessária.
- [ ] **Optional Seguro:** Evitar chamadas diretas a `.get()`. Utilizar `.orElseThrow()`, `.map()`, `.flatMap()` ou `.ifPresent()`.
- [ ] **Tratamento de Strings & Text Blocks:** Uso de Text Blocks `"""` para queries SQL complexas, prompts LLM ou templates JSON em testes.

---

## 2. 🍃 Spring Boot 3 & Clean Code

- [ ] **Injeção por Construtor:** Todas as dependências injetadas via construtor (preferencialmente com `final` fields), sem anotação `@Autowired` em campos privados.
- [ ] **Isolamento de Entidades JPA:** Entidades de persistência (`@Entity`) **nunca** são expostas diretamente nos endpoints de `@RestController`; a conversão para DTO record é obrigatória.
- [ ] **Validação com Bean Validation:** Todos os DTOs de entrada possuem anotações como `@NotBlank`, `@NotNull`, `@PositiveOrZero`, `@Size` e os métodos do controller usam `@Valid`.
- [ ] **Transacionalidade Correta:** Anotação `@Transactional` utilizada apenas em operações que alteram estado no banco ou necessitam de atomicidade; leitura pura não deve abrir transações de escrita.
- [ ] **Padronização REST & HTTP:**
  - `POST` retorna `201 Created` (com header `Location` quando aplicável).
  - `GET` retorna `200 OK` ou lança exceção resultando em `404 Not Found`.
  - `DELETE` retorna `204 No Content`.
  - Erros de negócio retornam `400 Bad Request` ou `422 Unprocessable Entity`.

---

## 3. 🏛️ Arquitetura & SOLID

- [ ] **Single Responsibility Principle (SRP):** Cada UseCase ou serviço executa apenas uma responsabilidade de negócio clara.
- [ ] **Dependency Inversion Principle (DIP):** Casos de uso dependem de interfaces (*Ports*) do pacote `domain.repository`, não de classes concretas de banco de dados.
- [ ] **Domínio Puro:** Classes de modelo de domínio em `domain.model` não contêm anotações de frameworks de persistência ou web.
- [ ] **Tratamento Centralizado de Erros:** Ausência de blocos `try/catch` vazios ou com `e.printStackTrace()`. Erros são capturados pelo `@RestControllerAdvice` e convertidos em `ProblemDetails` (RFC 7807).

---

## 4. 🧪 Testes Automatizados & Confiabilidade

- [ ] **Testes de Casos de Uso:** UseCases testados com JUnit 5 + Mockito (`@ExtendWith(MockitoExtension.class)`), mockando os repositórios/ports.
- [ ] **Testes de Controller:** Endpoints REST validados com `@WebMvcTest` ou `MockMvc`, verificando status HTTP, headers e corpo JSON.
- [ ] **Isolamento de Dados em Testes:** Testes nunca alteram nem dependem de dados do banco de dados em disco local.
- [ ] **Cobertura de Cenários Negativos:** Testes verificam explicitamente o lançamento de exceções esperadas (`assertThrows`).

---

## 5. 🤖 Integração com Modelos de IA / MCP

- [ ] **Documentação de Ferramentas:** Toda ferramenta `@Tool` do MCP possui descrições claras no `@Tool` e em cada `@ToolParam` para o LLM entender quando e como utilizá-la.
- [ ] **Tratamento Resiliente:** Chamadas externas a LLMs (Gemini API / Spring AI) tratam timeouts e retornos nulos graciosamente.
