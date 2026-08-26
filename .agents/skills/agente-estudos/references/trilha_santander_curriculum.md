# 🗺️ Trilha Santander 2026 — AI Java Back-end (DIO)

Este currículo técnico mapeia as competências fundamentais do **Bootcamp Santander 2026**, servindo como guia para o **Agente Estudos (NOVA)** direcionar mentorias, resumos conceituais e desafios práticos.

---

## 📚 Módulos & Competências Principais

### 1. ☕ Java 21 LTS & Fundamentos Modernos
- **Sintaxe & Tipagem:** Tipos primitivos, Wrappers, operadores, controle de fluxo e escopo.
- **Java Moderno (17 a 21):**
  - `Records` (imutabilidade nativa de dados).
  - `Pattern Matching` para `instanceof` e `switch expressions`.
  - `Sealed Classes` & `Sealed Interfaces` (hierarquias restritas).
  - `Text Blocks` (`"""`) e `Sequenced Collections`.
  - `Optional` idiomático e manipulação avançada da `Stream API`.
  - Gerenciamento de memória JVM (Stack, Heap, Garbage Collection básico).

### 2. 🧱 Programação Orientada a Objetos (POO) & SOLID
- **4 Pilares:** Abstração, Encapsulamento, Herança e Polimorfismo.
- **Interfaces & Classes Abstratas:** Composição sobre herança, contratos e desacoplamento.
- **Princípios SOLID:**
  - **S**ingle Responsibility Principle (SRP).
  - **O**pen/Closed Principle (OCP).
  - **L**iskov Substitution Principle (LSP).
  - **I**nterface Segregation Principle (ISP).
  - **D**ependency Inversion Principle (DIP).

### 3. 📦 Estruturas de Dados, Coleções & Tratamento de Erros
- **Collections Framework:** `List` (ArrayList, LinkedList), `Set` (HashSet, TreeSet), `Map` (HashMap, LinkedHashMap, TreeMap).
- **Generics & Comparators:** `Comparable` e `Comparator` com lambdas.
- **Hierarquia de Exceções:** `Throwable`, `Error`, `Exception` (Checked) vs. `RuntimeException` (Unchecked).
- **Tratamento Seguro:** `try-with-resources`, `AutoCloseable` e criação de exceções de domínio personalizadas.

### 4. 🍃 Spring Boot 3 & Persistência Relacional
- **Spring Core:** Inversão de Controle (IoC), Injeção de Dependências (DI), Ciclo de vida dos Beans (`@Component`, `@Service`, `@Repository`, `@Configuration`).
- **Spring Web (REST APIs):** `@RestController`, `@RequestMapping`, `@PathVariable`, `@RequestParam`, `@RequestBody`, status HTTP semânticos.
- **Spring Data JPA & Hibernate:**
  - Mapeamento objeto-relacional (`@Entity`, `@Table`, `@Id`, `@Column`, `@Enumerated`).
  - Relacionamentos (`@OneToMany`, `@ManyToOne`, `@ManyToMany`, estratégias de `FetchType` Lazy/Eager).
  - Consultas com Derived Query Methods, JPQL e `@Query`.
  - Transacionalidade com `@Transactional`.
- **Bean Validation:** `@Valid`, `@NotBlank`, `@NotNull`, `@Positive`, `@Size`, `@Email`.
- **Padronização de Erros:** `@RestControllerAdvice` e RFC 7807 (`ProblemDetails`).

### 5. 🏛️ Arquitetura de Software & Design Patterns
- **Clean Architecture & Arquitetura Hexagonal:** Separação estrita de camadas (`domain`, `application`, `infrastructure`), Ports & Adapters.
- **GoF Design Patterns:**
  - **Criacionais:** Factory Method, Builder, Singleton.
  - **Estruturais:** Adapter, Decorator, Facade.
  - **Comportamentais:** Strategy, Observer, Template Method.

### 6. 🧪 Qualidade de Código & Testes Automatizados
- **JUnit 5:** Anotações essenciais (`@Test`, `@DisplayName`, `@BeforeEach`, `@ParameterizedTest`), asserções com `Assertions` e `AssertJ`.
- **Mockito:** `@Mock`, `@InjectMocks`, `@ExtendWith(MockitoExtension.class)`, `when().thenReturn()`, `verify()`, `doThrow()`.
- **Testes de Integração:** `@WebMvcTest`, `MockMvc`, `@SpringBootTest`, isolamento de datasource com H2 em memória.

### 7. 🤖 Spring AI & Integração com Modelos de Linguagem (LLMs)
- **Conceitos de IA no Back-end:** Prompts estruturados, Function Calling, Embeddings, RAG (*Retrieval-Augmented Generation*).
- **Spring AI:** Clientes de chat, integração com Gemini / OpenAI.
- **Model Context Protocol (MCP):** Criação de servidores MCP no Spring Boot, anotações `@Tool` e `@ToolParam` para execução autônoma de ferramentas por agentes de IA.
