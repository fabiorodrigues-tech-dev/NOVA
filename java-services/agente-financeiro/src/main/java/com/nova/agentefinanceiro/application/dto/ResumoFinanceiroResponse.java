package com.nova.agentefinanceiro.application.dto;

import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.ResumoFinanceiro;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Map;

/**
 * DTO de resposta para o resumo consolidado de transações.
 */
public record ResumoFinanceiroResponse(
        BigDecimal totalGasto,
        BigDecimal totalReceitas,
        BigDecimal saldo,
        int quantidadeTransacoes,
        LocalDate periodoInicio,
        LocalDate periodoFim,
        Map<CategoriaTransacao, BigDecimal> totalPorCategoria
) {
    public static ResumoFinanceiroResponse fromDomain(ResumoFinanceiro domain) {
        return new ResumoFinanceiroResponse(
                domain.totalDespesas(),
                domain.totalReceitas(),
                domain.saldo(),
                domain.quantidadeTransacoes(),
                domain.periodoInicio(),
                domain.periodoFim(),
                domain.totalPorCategoria()
        );
    }
}
