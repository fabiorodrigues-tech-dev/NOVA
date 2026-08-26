# 🛠️ Desafio Prático: [Nome do Desafio]

> **Tópico:** [Ex: Clean Architecture / Streams / Mockito / Spring Data JPA]  
> **Dificuldade:** [Fácil / Médio / Desafiador]  
> **Tempo Estimado:** [15 a 30 minutos]

---

## 📋 1. Contexto & Requisitos de Negócio

Descreva o problema real que o código precisa resolver:
1. **Requisito 1:** ...
2. **Requisito 2:** ...
3. **Requisitos Não-Funcionais:** Usar Java 21, DTOs em `record`, validação de parâmetros, lançar exceção de domínio em caso de inconsistência.

---

## 🎯 2. Assinatura da Interface / Contrato

```java
package com.nova.estudos.desafio;

public interface ProcessadorOperacao {
    ResultadoOperacao processar(RequisicaoOperacao requisicao);
}
```

---

## 🧪 3. Suíte de Testes JUnit 5 (Comece por aqui!)

O objetivo do exercício é implementar o código de produção até que todos os testes abaixo passem:

```java
package com.nova.estudos.desafio;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ProcessadorOperacaoTest {

    @Test
    @DisplayName("Deve processar operação com sucesso quando parâmetros forem válidos")
    void deveProcessarComSucesso() {
        // Arrange
        // Act
        // Assert
    }

    @Test
    @DisplayName("Deve lançar RegraDeNegocioException quando valor for inválido")
    void deveLancarExcecaoQuandoInvalido() {
        // Arrange & Act & Assert
    }
}
```

---

## 💡 4. Dicas de Implementação (Opcional)

<details>
<summary>🔍 Ver Dicas (Clique para expandir se travar)</summary>

- **Dica 1:** Lembre-se de utilizar `Optional` para evitar retornos nulos.
- **Dica 2:** DTOs podem validar pré-condições no próprio construtor compacto do `record`.
</details>

---

## ✅ 5. Gabarito Comentado (Consulte após tentar resolver)

<details>
<summary>🏆 Ver Solução Recomendada</summary>

```java
// Solução ideal com boas práticas de Clean Code e Java 21
```
</details>
