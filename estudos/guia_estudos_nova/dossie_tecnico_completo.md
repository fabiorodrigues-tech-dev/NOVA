# 📚 MANUAL DE ENGENHARIA & ARQUITETURA DE SOFTWARE — ECOSSISTEMA NOVA
**Dossiê Técnico, Arquitetural e Didático de Consolidação Profissional**  
*Autor: Fábio Rodrigues | Ecossistema NOVA | Trilha Santander 2026 AI Java Back-end (DIO)*

---

## 📑 Sumário Executivo

Este compêndio consolida os fundamentos teóricos, padrões arquiteturais, código de produção e tecnologias emergentes implementadas no ecossistema **NOVA**. Ele serve como fonte definitiva de consulta para entrevistas técnicas, design de microsserviços e aceleração de estudos em **Java 21 LTS**, **Spring Boot 3**, **Clean Architecture**, **TDD**, **Bancos Relacionais** e **Agentes de Inteligência Artificial (MCP / Voice AI)**.

---

# ☕ 1. Java 21 LTS Moderno & Recursos Avançados

O Java 21 é uma versão de suporte de longo prazo (LTS) que consolida a transição do Java para uma linguagem mais expressiva, imutável e eficiente.

### 1.1. Records: Imutabilidade e Dados Puros
Records são classes imutáveis transparentes cujo propósito exclusivo é carregar dados. O compilador gera automaticamente os campos `private final`, construtor canônico, `getters` (sem o prefixo `get`), `equals()`, `hashCode()` e `toString()`.

```java
// DTO imutável e conciso
public record TransacaoRequest(
    String descricao,
    BigDecimal valor,
    TipoTransacao tipo,
    CategoriaTransacao categoria,
    LocalDate data
) {
    // Compact Constructor para validações de domínio
    public TransacaoRequest {
        if (valor == null || valor.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("O valor da transação deve ser positivo.");
        }
        if (data == null) {
            data = LocalDate.now();
        }
    }
}
```

### 1.2. Pattern Matching (instanceof & Switch Expressions)
Elimina o casting manual redundante e torna a tomada de decisão tipada e exaustiva.

```java
// Pattern Matching com Switch Expression
public String formatarRelatorio(Object obj) {
    return switch (obj) {
        case Transacao t when t.getValor().compareTo(new BigDecimal("1000")) > 0 -> 
            "Transação de Alto Valor: " + t.getDescricao();
        case Transacao t -> 
            "Transação Regular: " + t.getDescricao() + " | R$ " + t.getValor();
        case ResumoFinanceiro r -> 
            "Balanço Consolidado: Saldo R$ " + r.saldo();
        case null -> "Dado nulo fornecido";
        default -> "Objeto não mapeado: " + obj.getClass().getSimpleName();
    };
}
```

### 1.3. Sealed Classes e Interfaces
Permitem restringir quais classes ou records podem estender ou implementar uma interface, criando hierarquias fechadas e controladas pelo compilador.

```java
public sealed interface EventoFinanceiro permits TransacaoCriada, TransacaoCancelada, BalancoCalculado {}

public record TransacaoCriada(Long id, BigDecimal valor) implements EventoFinanceiro {}
public record TransacaoCancelada(Long id, String motivo) implements EventoFinanceiro {}
public record BalancoCalculado(BigDecimal saldo) implements EventoFinanceiro {}
```

### 1.4. Streams API & Processamento Funcional
A Streams API permite operações declarativas sobre coleções de dados, com filtros, transformações e agregações matemáticas de alta performance.

```java
// Cálculo do total de despesas por categoria usando Streams
Map<CategoriaTransacao, BigDecimal> totalPorCategoria = transacoes.stream()
    .filter(t -> t.getTipo() == TipoTransacao.DESPESA)
    .collect(Collectors.groupingBy(
        Transacao::getCategoria,
        Collectors.reducing(BigDecimal.ZERO, Transacao::getValor, BigDecimal::add)
    ));
```

### 1.5. Concorrência Moderna & Virtual Threads (Project Loom)
O Java 21 introduziu as **Virtual Threads** (threads leves gerenciadas pela JVM e não pelo Sistema Operacional). Enquanto uma thread de plataforma do SO consome ~1MB de memória e tem criação cara, milhões de Virtual Threads podem coexistir consumindo poucos bytes, ideal para microsserviços I/O-bound com requisições HTTP e chamadas a bancos de dados.

---

# 🍃 2. Spring Boot 3.3+ & Frameworks Corporativos

### 2.1. Inversão de Controle (IoC) & Injeção de Dependências (DI)
O Spring gerencia o ciclo de vida dos componentes através do seu **ApplicationContext**. A melhor prática moderna é a injeção via construtor com campos `final`, garantindo imutabilidade e facilidade de teste unitário sem necessidade de subir o contexto Spring.

```java
@Service
public class CadastrarTransacaoUseCase {
    
    private final TransacaoRepository repository; // Porta de Domínio

    // Injeção de dependência via construtor (sem @Autowired explícito)
    public CadastrarTransacaoUseCase(TransacaoRepository repository) {
        this.repository = repository;
    }

    public TransacaoResponse executar(TransacaoRequest request) {
        Transacao transacao = new Transacao(
            request.descricao(),
            request.valor(),
            request.tipo(),
            request.categoria(),
            request.data()
        );
        Transacao salva = repository.salvar(transacao);
        return TransacaoResponse.fromDomain(salva);
    }
}
```

### 2.2. Spring Data JPA & Derived Queries
Abstrai operações de banco de dados eliminando código boilerplate de JDBC ou EntityManager.

```java
public interface SpringDataTransacaoRepository extends JpaRepository<TransacaoEntity, Long> {
    List<TransacaoEntity> findByDataBetween(LocalDate inicio, LocalDate fim);
    List<TransacaoEntity> findByTipo(TipoTransacao tipo);
}
```

### 2.3. APIs RESTful & RFC 7807 ProblemDetails
O padrão moderno de resposta de erro HTTP exige estrutura semântica detalhada para que clientes e agentes inteligentes entendam exatamente a falha.

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public ProblemDetail handleBusinessException(BusinessException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.UNPROCESSABLE_ENTITY, ex.getMessage()
        );
        problem.setTitle("Regra de Negócio Violada");
        problem.setProperty("timestamp", Instant.now());
        return problem;
    }
}
```

### 2.4. Spring AI & Model Context Protocol (MCP)
O **Model Context Protocol (MCP)** é o padrão aberto que permite que Modelos de Linguagem (LLMs) executem ferramentas corporativas de forma autônoma e segura. No Spring Boot, anotamos métodos com `@Tool`:

```java
@Component
public class FinanceiroMcpTools {

    private final CadastrarTransacaoUseCase cadastrarUseCase;
    private final CalcularResumoFinanceiroUseCase resumoUseCase;

    public FinanceiroMcpTools(CadastrarTransacaoUseCase c, CalcularResumoFinanceiroUseCase r) {
        this.cadastrarUseCase = c;
        this.resumoUseCase = r;
    }

    @Tool(description = "Registra uma nova transação financeira no banco de dados persistente.")
    public TransacaoResponse cadastrarTransacao(
            @ToolParam(description = "Descrição da despesa ou receita") String descricao,
            @ToolParam(description = "Valor monetário positivo") double valor,
            @ToolParam(description = "Tipo: RECEITA ou DESPESA") String tipo,
            @ToolParam(description = "Categoria contábil") String categoria,
            @ToolParam(description = "Data no formato AAAA-MM-DD") String data) {
        
        TransacaoRequest request = new TransacaoRequest(
            descricao,
            BigDecimal.valueOf(valor),
            TipoTransacao.valueOf(tipo.toUpperCase()),
            CategoriaTransacao.valueOf(categoria.toUpperCase()),
            LocalDate.parse(data)
        );
        return cadastrarUseCase.executar(request);
    }
}
```

---

# 🏛️ 3. Clean Architecture & Arquitetura Hexagonal (Ports & Adapters)

O objetivo central da Clean Architecture (Robert C. Martin) e da Arquitetura Hexagonal (Alistair Cockburn) é o **isolamento total das regras de negócio em relação a detalhes tecnológicos externos** (bancos de dados, frameworks web, UI, bibliotecas de terceiros).

### 3.1. A Estrutura em 3 Camadas no NOVA

```text
+-------------------------------------------------------------+
|  INFRASTRUCTURE (Adaptadores Externos)                       |
|  - Web Controllers (REST Endpoints)                         |
|  - Persistence Entities (JPA / Hibernate)                   |
|  - Spring Data Repositories & H2 Database                   |
|  - Spring AI MCP Server (@Tool)                             |
|                                                             |
|  +-------------------------------------------------------+  |
|  |  APPLICATION (Casos de Uso & Orquestracao)            |  |
|  |  - Use Cases (CadastrarTransacao, ListarTransacoes)   |  |
|  |  - DTOs (Records de Request/Response)                 |  |
|  |                                                       |  |
|  |  +-------------------------------------------------+  |  |
|  |  |  DOMAIN (Nucleo Puro de Negocio)                |  |  |
|  |  |  - Entidades de Dominio (Transacao, Balanco)    |  |  |
|  |  |  - Value Objects & Enums                        |  |  |
|  |  |  - Interfaces de Repositorio (Ports)            |  |  |
|  |  |  - Regras e Invariantes de Negocio              |  |  |
|  |  +-------------------------------------------------+  |  |
|  +-------------------------------------------------------+  |
+-------------------------------------------------------------+
```

### 3.2. A Regra de Ouro da Dependência
- As dependências de código-fonte apontam **SEMPRE DE FORA PARA DENTRO**.
- O **Domínio** não importa nenhuma classe do Spring, Hibernate, JPA ou Jackson.
- A **Aplicação** depende apenas do Domínio.
- A **Infraestrutura** implementa as interfaces do Domínio (Inversão de Dependência - DIP).

---

# 🧪 4. Testes Automatizados & Test-Driven Development (TDD)

### 4.1. O Ciclo TDD (Red-Green-Refactor)
1. **🔴 Red:** Escrever um teste que define o comportamento esperado antes de escrever o código. O teste falha.
2. **🟢 Green:** Escrever a menor quantidade de código possível para fazer o teste passar.
3. **🔵 Refactor:** Melhorar a estrutura do código, remover duplicações e aplicar padrões, garantindo que o teste continue verde.

### 4.2. JUnit 5 + Mockito + AssertJ na Prática

```java
@ExtendWith(MockitoExtension.class)
@DisplayName("Testes do Caso de Uso: Cadastrar Transação")
class CadastrarTransacaoUseCaseTest {

    @Mock
    private TransacaoRepository repository; // Mock da porta de saída

    @InjectMocks
    private CadastrarTransacaoUseCase useCase;

    @Test
    @DisplayName("Deve cadastrar uma transação válida com sucesso")
    void deveCadastrarTransacaoValida() {
        // 1. Arrange (Preparação)
        TransacaoRequest request = new TransacaoRequest(
            "Aluguel",
            new BigDecimal("600.00"),
            TipoTransacao.DESPESA,
            CategoriaTransacao.MORADIA,
            LocalDate.of(2026, 8, 1)
        );

        when(repository.salvar(any(Transacao.class)))
            .thenAnswer(invocation -> {
                Transacao t = invocation.getArgument(0);
                t.setId(1L);
                return t;
            });

        // 2. Act (Execução)
        TransacaoResponse response = useCase.executar(request);

        // 3. Assert (Verificação com AssertJ)
        assertThat(response).isNotNull();
        assertThat(response.id()).isEqualTo(1L);
        assertThat(response.descricao()).isEqualTo("Aluguel");
        assertThat(response.valor()).isEqualByComparingTo("600.00");
        assertThat(response.tipo()).isEqualTo(TipoTransacao.DESPESA);

        // Verificação de comportamento com Mockito
        verify(repository, times(1)).salvar(any(Transacao.class));
    }
}
```

---

# 💾 5. Bancos de Dados Relacionais & Persistência ACID

### 5.1. O que são Garantias ACID?
- **A — Atomicidade:** Uma transação é tratada como uma unidade indivisível. Todas as operações são confirmadas (`commit`) ou revertidas (`rollback`).
- **C — Consistência:** A transação leva o banco de um estado válido a outro estado válido, respeitando chaves primárias, constraints e regras de integridade.
- **I — Isolamento:** Transações concorrentes executam sem interferir no estado intermediário umas das outras.
- **D — Durabilidade:** Uma vez confirmada a transação, os dados permanecem gravados no disco mesmo diante de falhas de energia ou reinicialização.

### 5.2. Persistência em Arquivo Físico com H2
Ao contrário de bancos em memória (`jdbc:h2:mem:...`) que perdem dados ao encerrar o processo, o **NOVA** utiliza persistência em arquivo binário (`.mv.db`):

```yaml
spring:
  datasource:
    url: jdbc:h2:file:./data/financiadb;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE;AUTO_SERVER=TRUE
    driverClassName: org.h2.Driver
    username: sa
    password: 
  jpa:
    database-platform: org.hibernate.dialect.H2Dialect
    hibernate:
      ddl-auto: update
```

---

# 🤖 6. Inteligência Artificial & Agentes Autônomos

### 6.1. Model Context Protocol (MCP)
Criado para padronizar como LLMs acessam bases de dados e ferramentas computacionais. Ele opera sobre transporte **SSE (Server-Sent Events)** ou **stdio**:
1. O Cliente MCP (ex: Antigravity / Claude) inicia o handshake e descobre as ferramentas (`tools/list`).
2. O Servidor MCP (Spring Boot) responde com o esquema JSON de parâmetros de cada `@Tool`.
3. O LLM decide chamar a ferramenta e emite um `tools/call`.
4. O servidor executa a regra de negócio no banco H2 e devolve o resultado estruturado.

### 6.2. Arquitetura de Agentes de Voz em Tempo Real (Sofia Voice AI)
O pipeline de voz de baixa latência conecta múltiplos serviços assíncronos:

```text
[Usuario / Telefone]
       | (Audio PCM / WebRTC)
       v
[Vapi Platform] ----> [STT: Whisper / Deepgram] (Audio -> Texto ~120ms)
       |
       v
[Orquestrador de IA] ----> [LLM: OpenAI GPT-4o-Mini + RAG] (Inferencia ~250ms)
       |
       v
[TTS: Cartesia / Clara V2] (Texto -> Audio Neural com Pausas ~150ms)
       |
       v
[Webhook Assincrono] ----> [WhatsApp API / CRM / NOVA Backend] (Acao & Persistencia)
```

---

# 🐍 7. Python, Automação & Geração Documental

### 7.1. Matplotlib e o Motor de Gráficos (`chart_engine.py`)
- Utiliza o backend sem interface gráfica `matplotlib.use('Agg')` para execução segura em servidores.
- Renderiza gráficos com densidade de 300 DPI, paletas de cores corporativas (Navy `#1A2530`, Azul `#2980B9`, Verde `#27AE60`) e layout proporcional (`tight_layout()`).

### 7.2. ReportLab e `python-docx`
- **ReportLab:** Constrói árvores de elementos visuais (**Flowables**) calculando quebras de página automáticas, margens de precisão milimétrica e estilos tipográficos imutáveis para garantir PDFs 100% legíveis por ATS.
- **python-docx:** Manipula a estrutura XML padrão OpenXML da Microsoft (`w:pBdr`, `w:r`, `w:p`), injetando cabeçalhos timbrados e tabelas formais para exportação profissional.

# 💳 8. Casos de Uso Avançados, Parser OFX & Inteligência Preditiva (Fase 9)

### 8.1. Ingestão Bancária: `ImportarExtratoOfxUseCase`
O caso de uso de importação bancária processa extratos nos formatos `.ofx` e `.csv` do Nubank salvos em `financeiro/extratos_ofx/`:
- **Parser SGML/XML Nativo:** Extração precisa das tags financeiras padrão Open Financial Exchange (`<STMTTRN>`, `<TRNAMT>`, `<MEMO>`, `<DTPOSTED>`, `<FITID>`).
- **Classificação Categórica Semântica:** Mapeamento inteligente de descrições em categorias de despesas e receitas (`ALIMENTACAO`, `MORADIA`, `TRANSPORTE`, `SAUDE`, `LAZER`, `INVESTIMENTO`, `OUTROS`).
- **Deduplicação Transacional no H2:** Validação por identificador único e data/valor para garantir que nenhuma transação seja inserida em duplicidade.

### 8.2. CFO Algorítmico & Fórmulas Preditivas: `CalcularProjecaoFinanceiraUseCase`
O módulo preditivo realiza projeção matemática de fluxo de caixa em tempo real:
- **Burn Rate Diário:**
  $$\text{Burn Rate} = \frac{\text{Total de Despesas Acumuladas}}{\text{Dias Decorridos no Ciclo}}$$
- **Despesa Total Projetada:**
  $$\text{Despesa Projetada} = \text{Despesas Atuais} + (\text{Burn Rate} \times \text{Dias Restantes})$$
- **Saldo Final Projetado:**
  $$\text{Saldo Final} = \text{Receitas Atuais} - \text{Despesa Projetada}$$
- **Classificação de Risco:** `SAUDÁVEL` (margem > 20%), `ALERTA` (margem < 10%) e `CRÍTICO` (saldo projetado negativo).

### 8.3. Caixinhas Nubank & Patrimônio Líquido Total
- Módulo de alocação de ativos em reservas estratégicas (Reserva de Emergência e Reserva Casal).
- Endpoint REST `/api/caixinhas` integrado ao cálculo automático de **Patrimônio Líquido Total** somando saldo em conta H2 e aportes das caixinhas.

---

# 🧪 9. Qualidade de Software, Cobertura & CI/CD (40 Testes JUnit 5)

### 9.1. Suíte de 40 Testes Automatizados (100% Green)
A integridade de todas as camadas é validada por **40 testes automatizados** executados via `./run-tests.sh`:
- **Casos de Uso Unitários (Isolados com Mockito):**
  - `ImportarExtratoOfxUseCaseTest`: Validação de parsing de tags OFX e regras de deduplicação.
  - `CalcularProjecaoFinanceiraUseCaseTest`: Verificação dos cálculos de Burn Rate e cenários de risco.
  - `CalcularResumoFinanceiroUseCaseTest`: Validação de saldo, total de receitas e despesas.
  - `SalvarCaixinhaUseCaseTest` e `ListarCaixinhasUseCaseTest`: Gestão de depósitos e saldo das caixinhas.
  - `ProcessarNotificacaoNubankUseCaseTest`: Simulação de webhooks de compra e conciliação.
  - `ProcessarComandoVozUseCaseTest`: Validação do roteamento de comandos de voz para a API.
- **Testes de Integração WebMvc:**
  - `TransacaoControllerTest`: MockMvc testando contratos REST, paginação e RFC 7807 ProblemDetail.
  - `CaixinhaControllerTest`: MockMvc testando endpoints de caixinhas e atualização de valores.
- **Testes Spring AI MCP Tools:**
  - `FinanceiroMcpToolsTest`: Chamadas determinísticas das anotações `@Tool`.

### 9.2. Esteira de Integração Contínua (`.github/workflows/ci.yml`)
- **Job Java 21:** Compilação Maven, execução de todos os 40 testes e publicação de relatórios Surefire a cada push na branch `main`.
- **Job Python:** Verificação estática de sintaxe e dependências via Flake8.

---

# ☁️ 10. Infraestrutura DevOps, Docker & Deploy em Nuvem (Render)

### 10.1. Docker Multi-Stage Build (`Dockerfile`)
- **Stage 1 (Builder):** `maven:3.9-eclipse-temurin-21` compilando e empacotando o JAR Spring Boot.
- **Stage 2 (Runner):** Imagem enxuta baseada em Debian com OpenJDK 21 JRE e Python 3.11, permitindo execução paralela e segura dos microsserviços.
- **Healthcheck Ativo:** Monitoramento no endpoint `/api/status?demo=true`.

### 10.2. Blueprint do Render (`render.yaml`) & Nuvem 24/7
- Deploy contínuo na nuvem conectado ao repositório GitHub.
- URL Oficial de Produção: **`https://nova-control-center-alsl.onrender.com`**.

---

# 🧭 11. Frontend SPA com 7 Abas em Material 3 Expressive & DevSecOps

### 11.1. Matriz de 7 Abas Dedicadas (SPA View Switcher)
1. **Cockpit Dashboard:** Visão geral, Voice Assistant interativo, KPIs corporativos e Living Shader WebGL.
2. **Finanças & Preditivo H2:** Balanço, auditoria de despesas, burn rate diário, projeção de fechamento e caixinhas.
3. **Candidaturas 360°:** Rastreamento de vagas ativas, índices de aderência técnica (Match %) e exportação de dossiês.
4. **Estudos & Certificações:** Monitoramento de trilhas ativas (Santander DIO 26/26 com Certificado e Full Stack 5/5).
5. **Voice Studio Pro:** Laboratório de síntese vocal neural, catálogo de vozes PT-BR/globais e testes executivos.
6. **Engenharia & Testes:** Telemetria dos serviços, Clean Architecture 4 Camadas, persistência H2 ACID e 40 testes 100% OK.
7. **Spring Boot API Explorer:** Documentação interativa de contratos REST, 5 endpoints mapeados e esquemas JSON.

### 11.2. DevSecOps: Controle de Acesso por PIN & Modo Demonstração (LGPD Safe)
- O painel inicializa por padrão servindo apenas dados simulados, sem risco de vazamento de dados bancários ou confidenciais.
- A alternância para dados reais exige autenticação via modal validada por chave segura (`ADMIN_PIN`).
- Motor de voz (`/api/voice/interact`) sincronizado com o PIN: transita dinamicamente entre dados reais e fictícios.

---

# 💼 12. Esteira de Carreira 360° em 3 Trilhas Especializadas

- 💻 **Trilha Tech & Dev:** Currículos Harvard Tech ATS (`Curriculo_Fabio_Rodrigues_Java_Backend.pdf`), cartas timbradas em PDF/DOCX, LinkedIn oficial e GitHub do projeto.
- 🎬 **Trilha Marketing & Audiovisual:** Dossiê de portfólio visual com 6 cases reais (DER-PE, Gildo Lanches, Quintal dos Primos), Google Drive exclusivo e setup Apple Silicon M1 (**Sem LinkedIn**).
- 📋 **Trilha Suporte, Operações & Administrativo:** Suporte a sistemas SaaS/ERP, validação documental ICP-Brasil, Customer Experience (CX), CRM e currículos dedicados (`Curriculo_Fabio_Rodrigues_Suporte_TI.pdf`).

---

## 🎯 Conclusão & Próximos Passos
Este compêndio consolida a excelência de engenharia de software do ecossistema **NOVA**. A integração harmônica entre Java 21, Spring Boot 3, Clean Architecture, Spring AI MCP, infraestrutura Docker/Render, segurança DevSecOps (LGPD Safe) e testes automatizados demonstra prontidão técnica sênior para entrega de software em nível corporativo de alta performance.

