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
