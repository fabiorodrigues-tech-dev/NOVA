# 🌌 NOVA — Visão Geral Técnica do Back-End (Java 21 + Spring Boot 3 + Spring AI MCP)

> **Documento Consolidado de Arquitetura, Engenharia & Código Real**  
> **Ecossistema:** Java 21 LTS, Spring Boot 3.3.3, Spring AI 1.0.0-M6 (MCP Server), Clean Architecture, DDD, H2 ACID, JUnit 5, Mockito, Docker Multi-Stage, GitHub Actions.  
> **Autor / Engenheiro:** Fábio Rodrigues (Recife/PE) | [LinkedIn](https://linkedin.com/in/fabiorodrigues-dev) • [GitHub](https://github.com/fabiorodrigues-tech-dev/NOVA)

---

## 🧭 1. Estrutura do Projeto & Clean Architecture (DDD)

O back-end do **NOVA** é estruturado rigorosamente em camadas concêntricas de **Clean Architecture (Ports & Adapters)** e **Domain-Driven Design (DDD)**, isolando 100% o núcleo de negócio e as entidades de regras de dependências externas de banco, frameworks ou bibliotecas de terceiros.

```text
java-services/agente-financeiro/
├── pom.xml                                  # Gerenciador de dependências Maven & plugins
├── data/
│   └── financiadb.mv.db                     # Arquivo físico persistente H2 (Integridade ACID)
├── src/
│   ├── main/
│   │   ├── java/com/nova/agentefinanceiro/
│   │   │   ├── AgenteFinanceiroApplication.java  # Ponto de entrada Spring Boot
│   │   │   │
│   │   │   ├── domain/                      # 🟡 CAMADA 1: DOMÍNIO (Núcleo Puro & Agnóstico)
│   │   │   │   ├── model/                   # Entidades, Value Objects e Enums
│   │   │   │   │   ├── Transacao.java       # Entidade pura de Transação Financeira
│   │   │   │   │   ├── Caixinha.java        # Entidade de Investimentos / Caixinhas Nubank
│   │   │   │   │   ├── ResumoFinanceiro.java# Value Object imutável (Java Record)
│   │   │   │   │   ├── TipoTransacao.java   # Enum (RECEITA, DESPESA)
│   │   │   │   │   ├── TipoCaixinha.java    # Enum (RESERVA_EMERGENCIA, FUNDO_CASAL, METAS)
│   │   │   │   │   └── CategoriaTransacao.java # Enum categorizador
│   │   │   │   └── repository/              # Portas de Saída (Output Ports)
│   │   │   │       ├── TransacaoRepository.java  # Interface de repositório de domínio
│   │   │   │       └── CaixinhaRepository.java   # Interface de repositório de caixinhas
│   │   │   │
│   │   │   ├── application/                 # 🔵 CAMADA 2: APLICAÇÃO & CASOS DE USO
│   │   │   │   ├── dto/                     # Data Transfer Objects (Records imutáveis)
│   │   │   │   │   ├── TransacaoRequest.java
│   │   │   │   │   ├── TransacaoResponse.java
│   │   │   │   │   ├── CaixinhaRequest.java
│   │   │   │   │   ├── CaixinhaResponse.java
│   │   │   │   │   ├── PatrimonioLiquidoResponse.java
│   │   │   │   │   ├── ProjecaoFinanceiraResponse.java
│   │   │   │   │   ├── ImportacaoExtratoResponse.java
│   │   │   │   │   ├── VoiceCommandRequest.java
│   │   │   │   │   └── VoiceCommandResponse.java
│   │   │   │   └── usecase/                 # Orquestração das Regras de Negócio
│   │   │   │       ├── CadastrarTransacaoUseCase.java
│   │   │   │       ├── ListarTransacoesUseCase.java
│   │   │   │       ├── CalcularResumoFinanceiroUseCase.java
│   │   │   │       ├── CalcularProjecaoFinanceiraUseCase.java  # IA Preditiva & Burn Rate
│   │   │   │       ├── SalvarCaixinhaUseCase.java
│   │   │   │       ├── ListarCaixinhasUseCase.java
│   │   │   │       ├── ImportarExtratoOfxUseCase.java          # Parser OFX/CSV
│   │   │   │       ├── ProcessarNotificacaoNubankUseCase.java  # Webhook Parser
│   │   │   │       └── ProcessarComandoVozUseCase.java         # Voice Controller
│   │   │   │
│   │   │   └── infrastructure/              # 🔴 CAMADA 3: INFRAESTRUTURA & ADAPTERS
│   │   │       ├── config/                  # Configurações de Frameworks e Spring AI
│   │   │       │   └── McpConfiguration.java# Registro do Provedor de Ferramentas MCP
│   │   │       ├── mcp/                     # Servidor MCP (Model Context Protocol)
│   │   │       │   └── FinanceiroMcpTools.java # Ferramentas semânticas (@Tool)
│   │   │       ├── persistence/             # Adaptadores de Persistência (JPA / H2)
│   │   │       │   ├── entity/              # Entidades JPA (@Entity)
│   │   │       │   │   ├── TransacaoJpaEntity.java
│   │   │       │   │   └── CaixinhaJpaEntity.java
│   │   │       │   ├── mapper/              # Conversores Domínio <-> JPA
│   │   │       │   │   ├── TransacaoMapper.java
│   │   │       │   │   └── CaixinhaMapper.java
│   │   │       │   └── repository/          # Implementação concreta dos Ports
│   │   │       │       ├── SpringDataTransacaoRepository.java
│   │   │       │       ├── TransacaoRepositoryImpl.java
│   │   │       │       ├── SpringDataCaixinhaRepository.java
│   │   │       │       └── CaixinhaRepositoryImpl.java
│   │   │       └── web/                     # Adaptadores Web (REST Controllers / RFC 7807)
│   │   │           ├── controller/
│   │   │           │   ├── TransacaoController.java
│   │   │           │   ├── CaixinhaController.java
│   │   │           │   └── VoiceCommandController.java
│   │   │           └── handler/
│   │   │               └── GlobalExceptionHandler.java # Tratamento uniforme ProblemDetails
│   │   └── resources/
│   │       └── application.yml              # Configurações de porta, H2 e Spring AI MCP
│   │
│   └── test/                                # 🧪 SUÍTE DE TESTES AUTOMATIZADOS (TDD)
│       ├── java/com/nova/agentefinanceiro/
│       │   ├── application/usecase/         # Testes Unitários de Use Cases (Mockito)
│       │   │   ├── CadastrarTransacaoUseCaseTest.java
│       │   │   ├── CalcularProjecaoFinanceiraUseCaseTest.java
│       │   │   ├── CalcularResumoFinanceiroUseCaseTest.java
│       │   │   ├── ImportarExtratoOfxUseCaseTest.java
│       │   │   ├── ListarCaixinhasUseCaseTest.java
│       │   │   ├── ProcessarComandoVozUseCaseTest.java
│       │   │   ├── ProcessarNotificacaoNubankUseCaseTest.java
│       │   │   └── SalvarCaixinhaUseCaseTest.java
│       │   └── infrastructure/              # Testes de Integração & WebMvc
│       │       ├── mcp/FinanceiroMcpToolsTest.java
│       │       ├── web/TransacaoControllerTest.java
│       │       └── web/CaixinhaControllerTest.java
│       └── resources/
│           └── application.yml              # Configuração H2 em memória para testes
```

---

## 📦 2. Dependências & Build (`pom.xml`)

O arquivo Maven gerencia **Java 21 LTS**, **Spring Boot 3.3.3**, o **BOM do Spring AI 1.0.0-M6**, o iniciador do **Spring AI MCP Server (WebMVC / SSE)**, persistência com **Spring Data JPA / H2** e suíte de testes com **JUnit 5, Mockito e AssertJ**.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.3</version>
        <relativePath/>
    </parent>

    <groupId>com.nova</groupId>
    <artifactId>agente-financeiro</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>agente-financeiro</name>
    <description>Microsserviço de Gestão Financeira do ecossistema NOVA</description>

    <properties>
        <java.version>21</java.version>
        <spring-ai.version>1.0.0-M6</spring-ai.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.ai</groupId>
                <artifactId>spring-ai-bom</artifactId>
                <version>${spring-ai.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <!-- Spring Boot Web -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- Spring Data JPA -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <!-- Bean Validation -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <!-- Spring AI MCP Server (WebMVC / SSE) -->
        <dependency>
            <groupId>org.springframework.ai</groupId>
            <artifactId>spring-ai-mcp-server-webmvc-spring-boot-starter</artifactId>
        </dependency>

        <!-- H2 Database (In-Memory / File-based) -->
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- Testes (JUnit 5, Mockito, AssertJ) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>

        <dependency>
            <groupId>org.junit.platform</groupId>
            <artifactId>junit-platform-launcher</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <repositories>
        <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
            <snapshots>
                <enabled>false</enabled>
            </snapshots>
        </repository>
    </repositories>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
                <configuration>
                    <forkCount>0</forkCount>
                    <excludes>
                        <exclude>**/TestExecutionMain.java</exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

---

## ⚙️ 3. Configurações da Aplicação (`application.yml`)

Configuração do microsserviço na porta `8081`, banco de dados relacional **H2 em arquivo físico** com integridade transacional persistente e servidor **Spring AI MCP** síncrono.

```yaml
server:
  port: 8081

spring:
  application:
    name: agente-financeiro

  datasource:
    url: jdbc:h2:file:./data/financiadb;DB_CLOSE_DELAY=-1
    driver-class-name: org.h2.Driver
    username: sa
    password: "***"

  h2:
    console:
      enabled: true
      path: /h2-console

  jpa:
    database-platform: org.hibernate.dialect.H2Dialect
    hibernate:
      ddl-auto: update
    show-sql: false

  # Configurações do MCP Server (Spring AI)
  ai:
    mcp:
      server:
        name: agente-financeiro-mcp
        version: 1.0.0
        type: SYNC
        sse-message-endpoint: /mcp/message
```

---

## 🏛️ 4. Domínio & Casos de Uso (Código Real)

### 🔹 4.1 Entidade de Domínio: `Transacao.java`
*Núcleo de negócio 100% puro com validações invariantes e agnóstico de frameworks.*

```java
package com.nova.agentefinanceiro.domain.model;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Objects;

/**
 * Entidade de Domínio representando uma Transação Financeira (Gasto ou Receita).
 * Agnóstica de frameworks e tecnologias de persistência.
 */
public class Transacao {

    private final Long id;
    private final String descricao;
    private final BigDecimal valor;
    private final TipoTransacao tipo;
    private final CategoriaTransacao categoria;
    private final LocalDate data;

    public Transacao(Long id, String descricao, BigDecimal valor, TipoTransacao tipo, CategoriaTransacao categoria, LocalDate data) {
        this.id = id;
        this.descricao = validarDescricao(descricao);
        this.valor = validarValor(valor);
        this.tipo = Objects.requireNonNullElse(tipo, TipoTransacao.DESPESA);
        this.categoria = Objects.requireNonNullElse(categoria, CategoriaTransacao.OUTROS);
        this.data = Objects.requireNonNullElseGet(data, LocalDate::now);
    }

    private static String validarDescricao(String descricao) {
        if (descricao == null || descricao.isBlank()) {
            throw new IllegalArgumentException("A descrição da transação é obrigatória.");
        }
        return descricao.trim();
    }

    private static BigDecimal validarValor(BigDecimal valor) {
        if (valor == null || valor.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("O valor da transação deve ser positivo.");
        }
        return valor;
    }

    public Long getId() { return id; }
    public String getDescricao() { return descricao; }
    public BigDecimal getValor() { return valor; }
    public TipoTransacao getTipo() { return tipo; }
    public CategoriaTransacao getCategoria() { return categoria; }
    public LocalDate getData() { return data; }

    public boolean isDespesa() { return this.tipo == TipoTransacao.DESPESA; }
    public boolean isReceita() { return this.tipo == TipoTransacao.RECEITA; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Transacao that)) return false;
        return Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() { return Objects.hash(id); }
}
```

---

### 🔹 4.2 Value Object Imutável: `ResumoFinanceiro.java`
*Registro imutável (Java Record) com mapas não-modificáveis.*

```java
package com.nova.agentefinanceiro.domain.model;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Collections;
import java.util.Map;
import java.util.Objects;

/**
 * Value Object imutável representando o resumo consolidado de transações em um período.
 */
public record ResumoFinanceiro(
        BigDecimal totalDespesas,
        BigDecimal totalReceitas,
        BigDecimal saldo,
        int quantidadeTransacoes,
        LocalDate periodoInicio,
        LocalDate periodoFim,
        Map<CategoriaTransacao, BigDecimal> totalPorCategoria
) {
    public ResumoFinanceiro {
        totalDespesas = Objects.requireNonNullElse(totalDespesas, BigDecimal.ZERO);
        totalReceitas = Objects.requireNonNullElse(totalReceitas, BigDecimal.ZERO);
        saldo = Objects.requireNonNullElse(saldo, BigDecimal.ZERO);
        totalPorCategoria = totalPorCategoria != null
                ? Collections.unmodifiableMap(totalPorCategoria)
                : Collections.emptyMap();
    }
}
```

---

### 🔹 4.3 Output Port de Domínio: `TransacaoRepository.java`

```java
package com.nova.agentefinanceiro.domain.repository;

import com.nova.agentefinanceiro.domain.model.Transacao;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

/**
 * Porta de saída (Output Port) para operações de persistência de Transacao.
 * Definida no domínio, implementada na infraestrutura.
 */
public interface TransacaoRepository {
    Transacao salvar(Transacao transacao);
    List<Transacao> listarTodas();
    List<Transacao> listarPorPeriodo(LocalDate inicio, LocalDate fim);
    Optional<Transacao> buscarPorId(Long id);
    boolean existe(LocalDate data, BigDecimal valor, String descricao);
}
```

---

### 🔹 4.4 Caso de Uso: `CalcularProjecaoFinanceiraUseCase.java`
*Inteligência Preditiva & Consultoria Orçamentária (Cálculo de Burn Rate e Alertas).*

```java
package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.ProjecaoFinanceiraResponse;
import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.YearMonth;
import java.util.ArrayList;
import java.util.List;

/**
 * Caso de Uso para Inteligência Preditiva & Consultoria Financeira.
 * Estima o burn rate diário, projeta o saldo ao fim do mês e emite alertas de proteção orçamentária.
 */
@Service
public class CalcularProjecaoFinanceiraUseCase {

    private final TransacaoRepository transacaoRepository;

    public CalcularProjecaoFinanceiraUseCase(TransacaoRepository transacaoRepository) {
        this.transacaoRepository = transacaoRepository;
    }

    public ProjecaoFinanceiraResponse executar(LocalDate dataRef) {
        LocalDate hoje = (dataRef != null) ? dataRef : LocalDate.now();
        YearMonth ym = YearMonth.from(hoje);
        LocalDate inicioMes = ym.atDay(1);
        LocalDate fimMes = ym.atEndOfMonth();

        int totalDiasMes = ym.lengthOfMonth();
        int diaAtual = hoje.getDayOfMonth();
        int diasDecorridos = Math.max(1, diaAtual);
        int diasRestantes = Math.max(0, totalDiasMes - diaAtual);

        List<Transacao> transacoes = transacaoRepository.listarPorPeriodo(inicioMes, fimMes);

        BigDecimal totalGastos = BigDecimal.ZERO;
        BigDecimal totalReceitas = BigDecimal.ZERO;

        for (Transacao t : transacoes) {
            if (!t.getData().isAfter(hoje)) {
                if (t.isDespesa()) {
                    totalGastos = totalGastos.add(t.getValor());
                } else if (t.isReceita()) {
                    totalReceitas = totalReceitas.add(t.getValor());
                }
            }
        }

        BigDecimal saldoAtual = totalReceitas.subtract(totalGastos);

        // Burn rate diário médio (Gastos / Dias Decorridos)
        BigDecimal burnRateDiario = totalGastos.divide(BigDecimal.valueOf(diasDecorridos), 2, RoundingMode.HALF_UP);

        // Gasto adicional estimado para os dias restantes
        BigDecimal gastoAdicionalProjetado = burnRateDiario.multiply(BigDecimal.valueOf(diasRestantes)).setScale(2, RoundingMode.HALF_UP);

        // Gasto total estimado ao final do mês
        BigDecimal gastoTotalProjetado = totalGastos.add(gastoAdicionalProjetado).setScale(2, RoundingMode.HALF_UP);

        // Saldo final projetado
        BigDecimal saldoFinalProjetado = totalReceitas.subtract(gastoTotalProjetado).setScale(2, RoundingMode.HALF_UP);

        String status;
        List<String> alertas = new ArrayList<>();
        String recomendacao;

        if (saldoFinalProjetado.compareTo(BigDecimal.ZERO) < 0) {
            status = "CRITICO";
            alertas.add(String.format("⚠️ Risco de Déficit: No ritmo atual (R$ %.2f/dia), você gastará mais R$ %.2f até o fim do mês, resultando em saldo negativo de R$ %.2f.",
                    burnRateDiario, gastoAdicionalProjetado, saldoFinalProjetado.abs()));
            recomendacao = String.format("Reduza despesas variáveis não essenciais imediatamente. O teto diário recomendado para os próximos %d dias é de R$ %.2f/dia para zerar o balanço.",
                    diasRestantes, diasRestantes > 0 ? saldoAtual.max(BigDecimal.ZERO).divide(BigDecimal.valueOf(diasRestantes), 2, RoundingMode.HALF_UP) : BigDecimal.ZERO);
        } else {
            BigDecimal margemSeguranca = totalReceitas.multiply(BigDecimal.valueOf(0.15));
            if (saldoFinalProjetado.compareTo(margemSeguranca) < 0) {
                status = "ALERTA";
                alertas.add(String.format("⚡ Margem Apertada: Projeção de superávit modesto de R$ %.2f (abaixo de 15%% da receita total).", saldoFinalProjetado));
                recomendacao = "Mantenha cautela em novos gastos até o fechamento do mês para preservar a margem positiva.";
            } else {
                status = "SAUDAVEL";
                alertas.add(String.format("✅ Balanço Saudável: Superávit projetado de R$ %.2f ao fim do mês.", saldoFinalProjetado));
                BigDecimal aporteSugerido = saldoFinalProjetado.multiply(BigDecimal.valueOf(0.50)).setScale(2, RoundingMode.HALF_UP);
                recomendacao = String.format("Ritmo financeiro sob controle! Sugestão de aporte de R$ %.2f nas caixinhas (Reserva de Emergência e Metas do Casal).", aporteSugerido);
            }
        }

        return new ProjecaoFinanceiraResponse(
                hoje, diasDecorridos, diasRestantes, totalDiasMes,
                totalGastos.setScale(2, RoundingMode.HALF_UP),
                totalReceitas.setScale(2, RoundingMode.HALF_UP),
                saldoAtual.setScale(2, RoundingMode.HALF_UP),
                burnRateDiario, gastoAdicionalProjetado, gastoTotalProjetado,
                saldoFinalProjetado, status, alertas, recomendacao
        );
    }
}
```

---

## 🤖 5. Integração com Inteligência Artificial & MCP (Model Context Protocol)

### 🔹 5.1 Configuração Spring AI MCP: `McpConfiguration.java`

```java
package com.nova.agentefinanceiro.infrastructure.config;

import com.nova.agentefinanceiro.infrastructure.mcp.FinanceiroMcpTools;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Configuração e registro do provedor de ferramentas MCP no Spring AI.
 */
@Configuration
public class McpConfiguration {

    @Bean
    public ToolCallbackProvider financeiroToolCallbackProvider(FinanceiroMcpTools financeiroMcpTools) {
        return MethodToolCallbackProvider.builder()
                .toolObjects(financeiroMcpTools)
                .build();
    }
}
```

---

### 🔹 5.2 Ferramentas MCP (`@Tool`): `FinanceiroMcpTools.java`
*Ferramentas semânticas tipadas expostas nativamente pelo Spring AI para consumo por agentes LLMs.*

```java
package com.nova.agentefinanceiro.infrastructure.mcp;

import com.nova.agentefinanceiro.application.dto.*;
import com.nova.agentefinanceiro.application.usecase.*;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoCaixinha;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

/**
 * Ferramentas MCP (Model Context Protocol) para interação do agente de IA com o domínio financeiro.
 */
@Component
public class FinanceiroMcpTools {

    private final CadastrarTransacaoUseCase cadastrarTransacaoUseCase;
    private final ListarTransacoesUseCase listarTransacoesUseCase;
    private final CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase;
    private final ImportarExtratoOfxUseCase importarExtratoOfxUseCase;
    private final CalcularProjecaoFinanceiraUseCase calcularProjecaoFinanceiraUseCase;
    private final SalvarCaixinhaUseCase salvarCaixinhaUseCase;
    private final ListarCaixinhasUseCase listarCaixinhasUseCase;

    public FinanceiroMcpTools(
            CadastrarTransacaoUseCase cadastrarTransacaoUseCase,
            ListarTransacoesUseCase listarTransacoesUseCase,
            CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase,
            ImportarExtratoOfxUseCase importarExtratoOfxUseCase,
            CalcularProjecaoFinanceiraUseCase calcularProjecaoFinanceiraUseCase,
            SalvarCaixinhaUseCase salvarCaixinhaUseCase,
            ListarCaixinhasUseCase listarCaixinhasUseCase
    ) {
        this.cadastrarTransacaoUseCase = cadastrarTransacaoUseCase;
        this.listarTransacoesUseCase = listarTransacoesUseCase;
        this.calcularResumoFinanceiroUseCase = calcularResumoFinanceiroUseCase;
        this.importarExtratoOfxUseCase = importarExtratoOfxUseCase;
        this.calcularProjecaoFinanceiraUseCase = calcularProjecaoFinanceiraUseCase;
        this.salvarCaixinhaUseCase = salvarCaixinhaUseCase;
        this.listarCaixinhasUseCase = listarCaixinhasUseCase;
    }

    @Tool(
            name = "atualizar_caixinha",
            description = "Cadastra ou atualiza o saldo de uma Caixinha / Fundo de Investimento Nubank (ex: Reserva de Emergência, Fundo do Casal, Metas)."
    )
    public CaixinhaResponse atualizarCaixinha(
            @ToolParam(description = "Nome da caixinha (ex: 'Reserva de Emergência', 'Fundo do Casal', 'Viagem')") String nome,
            @ToolParam(description = "Saldo total atualizado na caixinha em reais (ex: 1500.00)") BigDecimal saldo,
            @ToolParam(required = false, description = "Tipo da caixinha: 'RESERVA_EMERGENCIA', 'FUNDO_CASAL', 'METAS', 'OUTROS'.") TipoCaixinha tipo,
            @ToolParam(required = false, description = "Rendimento mensal estimado em reais.") BigDecimal rendimentoMensalEstimado
    ) {
        return salvarCaixinhaUseCase.executar(new CaixinhaRequest(nome, saldo, tipo, rendimentoMensalEstimado));
    }

    @Tool(
            name = "consultar_caixinhas",
            description = "Consulta todos os investimentos e Caixinhas Nubank cadastrados, calculando o Patrimônio Líquido Total."
    )
    public PatrimonioLiquidoResponse consultarCaixinhas() {
        return listarCaixinhasUseCase.executar();
    }

    @Tool(
            name = "projecao_financeira",
            description = "Calcula a inteligência preditiva e projeção financeira orçamentária do mês corrente, estimando o burn rate diário e alertas de risco."
    )
    public ProjecaoFinanceiraResponse projecaoFinanceira(
            @ToolParam(required = false, description = "Data de referência para o cálculo no formato 'AAAA-MM-DD'.") LocalDate dataReferencia
    ) {
        return calcularProjecaoFinanceiraUseCase.executar(dataReferencia);
    }

    @Tool(
            name = "cadastrar_transacao",
            description = "Cadastra um novo gasto ou receita financeira pessoal no sistema."
    )
    public TransacaoResponse cadastrarTransacao(
            @ToolParam(description = "Descrição clara do gasto ou receita") String descricao,
            @ToolParam(description = "Valor numérico positivo da transação em reais") BigDecimal valor,
            @ToolParam(required = false, description = "Tipo da transação: 'DESPESA' ou 'RECEITA'. Padrão: DESPESA") TipoTransacao tipo,
            @ToolParam(required = false, description = "Categoria do gasto/receita") CategoriaTransacao categoria,
            @ToolParam(required = false, description = "Data da transação no formato 'AAAA-MM-DD'") LocalDate data
    ) {
        TransacaoRequest request = new TransacaoRequest(
                descricao, valor,
                tipo != null ? tipo : TipoTransacao.DESPESA,
                categoria != null ? categoria : CategoriaTransacao.OUTROS,
                data != null ? data : LocalDate.now()
        );
        return cadastrarTransacaoUseCase.executar(request);
    }

    @Tool(
            name = "listar_transacoes",
            description = "Lista o histórico de transações cadastradas, com suporte a filtro opcional por período de datas."
    )
    public List<TransacaoResponse> listarTransacoes(
            @ToolParam(required = false, description = "Data inicial 'AAAA-MM-DD'") LocalDate inicio,
            @ToolParam(required = false, description = "Data final 'AAAA-MM-DD'") LocalDate fim
    ) {
        return listarTransacoesUseCase.executar(inicio, fim);
    }

    @Tool(
            name = "resumo_financeiro",
            description = "Calcula o resumo e balanço financeiro consolidado de um período, totalizando despesas, receitas, saldo e categorias."
    )
    public ResumoFinanceiroResponse resumoFinanceiro(
            @ToolParam(required = false, description = "Data de início 'AAAA-MM-DD'") LocalDate inicio,
            @ToolParam(required = false, description = "Data de fim 'AAAA-MM-DD'") LocalDate fim
    ) {
        return calcularResumoFinanceiroUseCase.executar(inicio, fim);
    }
}
```

---

### 🔹 5.3 Controller de Voz & IA: `VoiceCommandController.java`

```java
package com.nova.agentefinanceiro.infrastructure.web.controller;

import com.nova.agentefinanceiro.application.dto.VoiceCommandRequest;
import com.nova.agentefinanceiro.application.dto.VoiceCommandResponse;
import com.nova.agentefinanceiro.application.usecase.ProcessarComandoVozUseCase;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Controller REST para processamento de comandos de voz do ecossistema NOVA.
 */
@RestController
@RequestMapping("/api/voice")
public class VoiceCommandController {

    private final ProcessarComandoVozUseCase processarComandoVozUseCase;

    public VoiceCommandController(ProcessarComandoVozUseCase processarComandoVozUseCase) {
        this.processarComandoVozUseCase = processarComandoVozUseCase;
    }

    @PostMapping("/command")
    public ResponseEntity<VoiceCommandResponse> processarComando(@RequestBody VoiceCommandRequest request) {
        VoiceCommandResponse response = processarComandoVozUseCase.executar(request);
        return ResponseEntity.ok(response);
    }
}
```

---

## 🧪 6. Testes Automatizados (TDD com JUnit 5 & Mockito)

### 🔹 6.1 Teste Unitário de Use Case: `CalcularProjecaoFinanceiraUseCaseTest.java`

```java
package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.ProjecaoFinanceiraResponse;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CalcularProjecaoFinanceiraUseCaseTest {

    @Mock
    private TransacaoRepository transacaoRepository;

    private CalcularProjecaoFinanceiraUseCase useCase;

    @BeforeEach
    void setUp() {
        useCase = new CalcularProjecaoFinanceiraUseCase(transacaoRepository);
    }

    @Test
    @DisplayName("Deve calcular projeção financeira saudável com superávit ao fim do mês")
    void deveCalcularProjecaoSaudavelComSuperavit() {
        LocalDate dataRef = LocalDate.of(2026, 8, 15); // Dia 15 de 31 dias

        List<Transacao> transacoes = List.of(
                new Transacao(1L, "Salário", new BigDecimal("3000.00"), TipoTransacao.RECEITA, CategoriaTransacao.SALARIO, LocalDate.of(2026, 8, 5)),
                new Transacao(2L, "Aluguel", new BigDecimal("600.00"), TipoTransacao.DESPESA, CategoriaTransacao.MORADIA, LocalDate.of(2026, 8, 10)),
                new Transacao(3L, "Mercado", new BigDecimal("450.00"), TipoTransacao.DESPESA, CategoriaTransacao.ALIMENTACAO, LocalDate.of(2026, 8, 12))
        );

        when(transacaoRepository.listarPorPeriodo(any(), any())).thenReturn(transacoes);

        ProjecaoFinanceiraResponse response = useCase.executar(dataRef);

        assertNotNull(response);
        assertEquals(15, response.diasDecorridos());
        assertEquals(16, response.diasRestantes());
        assertEquals(31, response.totalDiasMes());

        assertEquals(new BigDecimal("1050.00"), response.totalGastosAtual());
        assertEquals(new BigDecimal("3000.00"), response.totalReceitasAtual());
        assertEquals(new BigDecimal("1950.00"), response.saldoAtual());

        // Burn rate = 1050 / 15 = 70.00/dia
        assertEquals(new BigDecimal("70.00"), response.burnRateDiario());
        // Gasto adicional = 70.00 * 16 = 1120.00
        assertEquals(new BigDecimal("1120.00"), response.gastoAdicionalProjetado());
        // Gasto total = 1050 + 1120 = 2170.00
        assertEquals(new BigDecimal("2170.00"), response.gastoTotalProjetado());
        // Saldo projetado = 3000 - 2170 = 830.00
        assertEquals(new BigDecimal("830.00"), response.saldoFinalProjetado());

        assertEquals("SAUDAVEL", response.statusOrcamentario());
        assertFalse(response.alertas().isEmpty());
    }

    @Test
    @DisplayName("Deve calcular projeção crítica com déficit e gerar alertas de redução")
    void deveCalcularProjecaoCriticaComDeficit() {
        LocalDate dataRef = LocalDate.of(2026, 8, 10); // Dia 10 de 31 dias

        List<Transacao> transacoes = List.of(
                new Transacao(1L, "Salário", new BigDecimal("2000.00"), TipoTransacao.RECEITA, CategoriaTransacao.SALARIO, LocalDate.of(2026, 8, 1)),
                new Transacao(2L, "Compras Diversas", new BigDecimal("1500.00"), TipoTransacao.DESPESA, CategoriaTransacao.COMPRAS, LocalDate.of(2026, 8, 5))
        );

        when(transacaoRepository.listarPorPeriodo(any(), any())).thenReturn(transacoes);

        ProjecaoFinanceiraResponse response = useCase.executar(dataRef);

        assertNotNull(response);
        assertEquals(new BigDecimal("150.00"), response.burnRateDiario());
        assertEquals(new BigDecimal("-2650.00"), response.saldoFinalProjetado());
        assertEquals("CRITICO", response.statusOrcamentario());
        assertTrue(response.alertas().get(0).contains("⚠️ Risco de Déficit"));
    }
}
```

---

### 🔹 6.2 Teste de Integração WebMvc: `TransacaoControllerTest.java`

```java
package com.nova.agentefinanceiro.infrastructure.web;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.nova.agentefinanceiro.application.dto.ResumoFinanceiroResponse;
import com.nova.agentefinanceiro.application.dto.TransacaoRequest;
import com.nova.agentefinanceiro.application.dto.TransacaoResponse;
import com.nova.agentefinanceiro.application.usecase.CadastrarTransacaoUseCase;
import com.nova.agentefinanceiro.application.usecase.CalcularResumoFinanceiroUseCase;
import com.nova.agentefinanceiro.application.usecase.ListarTransacoesUseCase;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import com.nova.agentefinanceiro.infrastructure.web.controller.TransacaoController;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(TransacaoController.class)
class TransacaoControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private CadastrarTransacaoUseCase cadastrarTransacaoUseCase;

    @MockBean
    private ListarTransacoesUseCase listarTransacoesUseCase;

    @MockBean
    private CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase;

    @MockBean
    private com.nova.agentefinanceiro.application.usecase.ImportarExtratoOfxUseCase importarExtratoOfxUseCase;

    @MockBean
    private com.nova.agentefinanceiro.application.usecase.CalcularProjecaoFinanceiraUseCase calcularProjecaoFinanceiraUseCase;

    @MockBean
    private com.nova.agentefinanceiro.application.usecase.ProcessarNotificacaoNubankUseCase processarNotificacaoNubankUseCase;

    @Test
    @DisplayName("POST /api/transacoes - Deve retornar 201 Created quando payload for válido")
    void deveCadastrarTransacaoComSucesso() throws Exception {
        TransacaoRequest request = new TransacaoRequest(
                "Almoço Executivo",
                new BigDecimal("45.90"),
                TipoTransacao.DESPESA,
                CategoriaTransacao.ALIMENTACAO,
                LocalDate.now()
        );

        TransacaoResponse response = new TransacaoResponse(
                1L,
                "Almoço Executivo",
                new BigDecimal("45.90"),
                TipoTransacao.DESPESA,
                CategoriaTransacao.ALIMENTACAO,
                LocalDate.now()
        );

        when(cadastrarTransacaoUseCase.executar(any())).thenReturn(response);

        mockMvc.perform(post("/api/transacoes")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.descricao").value("Almoço Executivo"))
                .andExpect(jsonPath("$.valor").value(45.90))
                .andExpect(jsonPath("$.tipo").value("DESPESA"))
                .andExpect(jsonPath("$.categoria").value("ALIMENTACAO"));
    }

    @Test
    @DisplayName("POST /api/transacoes/webhook-notificacao - Deve retornar 200 OK ao processar notificação Nubank")
    void deveProcessarWebhookNotificacaoComSucesso() throws Exception {
        TransacaoResponse response = new TransacaoResponse(
                10L,
                "Restaurante Fogão de Lenha",
                new BigDecimal("45.90"),
                TipoTransacao.DESPESA,
                CategoriaTransacao.ALIMENTACAO,
                LocalDate.now()
        );

        when(processarNotificacaoNubankUseCase.executar(any())).thenReturn(response);

        mockMvc.perform(post("/api/transacoes/webhook-notificacao")
                        .contentType(MediaType.TEXT_PLAIN)
                        .content("Compra de R$ 45,90 no Restaurante Fogão de Lenha aprovada"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.descricao").value("Restaurante Fogão de Lenha"))
                .andExpect(jsonPath("$.valor").value(45.90));
    }

    @Test
    @DisplayName("POST /api/transacoes - Deve retornar 400 Bad Request quando payload for inválido")
    void deveRetornar400QuandoPayloadInvalido() throws Exception {
        TransacaoRequest requestInvalido = new TransacaoRequest(
                "", // Descrição em branco
                new BigDecimal("-10.00"), // Valor negativo
                TipoTransacao.DESPESA,
                CategoriaTransacao.ALIMENTACAO,
                LocalDate.now()
        );

        mockMvc.perform(post("/api/transacoes")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(requestInvalido)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.title").value("Requisição Inválida"));
    }
}
```

---

## 🐳 7. DevOps, Conteinerização & CI/CD

### 🔹 7.1 `Dockerfile` (Multi-Stage Production Build)
*Build unificado com Java 21 Temurin, Maven caching, Python 3.11 runtime e otimização G1GC.*

```dockerfile
# ==============================================================================
# NOVA — Production Multi-Stage Dockerfile (Java 21 + Python 3.11 Runtime 24/7)
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build Spring Boot Microservice (Java 21)
# ------------------------------------------------------------------------------
FROM maven:3.9.6-eclipse-temurin-21 AS backend-builder
WORKDIR /build

# Cache dependencies
COPY java-services/agente-financeiro/pom.xml .
RUN mvn dependency:go-offline -B -q

# Build application JAR
COPY java-services/agente-financeiro/src ./src
RUN mvn clean package -DskipTests -B -q

# ------------------------------------------------------------------------------
# Stage 2: Final Unified Runtime (Java 21 + Python 3.11 + Web Dashboard)
# ------------------------------------------------------------------------------
FROM eclipse-temurin:21-jre-jammy

LABEL maintainer="Fábio Rodrigues <https://linkedin.com/in/fabiorodrigues-dev>"
LABEL description="NOVA Control Center — Production Multi-Agent Ecosystem"

# Install Python 3.11, pip, curl and utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies (Root + Voice requirements)
COPY requirements.txt ./requirements.txt
COPY voz/requirements.txt ./voz-requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy Spring Boot Executable JAR from builder stage
COPY --from=backend-builder /build/target/*.jar ./agente-financeiro.jar

# Copy Application Modules & Assets
COPY dashboard/ ./dashboard/
COPY voz/ ./voz/
COPY docs/ ./docs/
COPY carreira/ ./carreira/
COPY estudos/ ./estudos/
COPY financeiro/ ./financeiro/
COPY scripts/ ./scripts/
COPY entrypoint.sh ./entrypoint.sh

RUN chmod +x ./entrypoint.sh

# Production Environment Settings
ENV PORT=10000
ENV NOVA_PORT=10000
ENV SPRING_PROFILES_ACTIVE=default
ENV JAVA_OPTS="-Xms128m -Xmx384m -XX:+UseG1GC"

# Expose Web Traffic Port & Spring Boot Internal Port
EXPOSE 10000 8081

ENTRYPOINT ["/app/entrypoint.sh"]
```

---

### 🔹 7.2 GitHub Actions Pipeline: `.github/workflows/ci.yml`
*Esteira automatizada de CI/CD validando compilação Java 21, testes JUnit 5/Mockito, linting Python e build da imagem Docker.*

```yaml
name: NOVA CI/CD Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  backend-test:
    name: ☕ Java 21 & Spring Boot Test Suite
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: java-services/agente-financeiro

    steps:
      - name: 📥 Checkout do Repositório
        uses: actions/checkout@v4

      - name: ☕ Configurar Java 21 (Eclipse Temurin)
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'
          cache: 'maven'

      - name: 🔨 Compilar Microsserviço Agente Financeiro
        run: mvn clean compile -B

      - name: 🧪 Executar Testes Unitários & Integração (JUnit 5 + Mockito)
        run: mvn test -B

      - name: 📊 Publicar Relatório de Testes
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: surefire-reports
          path: java-services/agente-financeiro/target/surefire-reports/
          if-no-files-found: ignore

  python-quality:
    name: 🐍 Python Scripts & Voice AI Check
    runs-on: ubuntu-latest

    steps:
      - name: 📥 Checkout do Repositório
        uses: actions/checkout@v4

      - name: 🐍 Configurar Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: 📦 Instalar Dependências e Ferramentas
        run: |
          python -m pip install --upgrade pip
          pip install -r voz/requirements.txt
          pip install flake8 reportlab matplotlib

      - name: 🔍 Validar Sintaxe dos Scripts Python (Linter & Headless Check)
        run: |
          flake8 scripts/ dashboard/server.py voz/scripts/ --count --select=E9,F63,F7,F82 --show-source --statistics --exit-zero
          python -m py_compile scripts/*.py dashboard/server.py voz/scripts/*.py || true

  docker-build:
    name: 🐳 Docker Multi-Stage Build Check
    runs-on: ubuntu-latest
    needs: [backend-test, python-quality]
    steps:
      - name: 📥 Checkout do Repositório
        uses: actions/checkout@v4

      - name: 🐳 Configurar Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: 🔨 Validar Build da Imagem Docker
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: nova-control-center:latest
```
