package com.nova.agentefinanceiro.application.dto;

import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

/**
 * DTO de resposta para o Histórico Anual Consolidado.
 */
public record HistoricoAnualResponse(
        int ano,
        BigDecimal totalReceitasAnual,
        BigDecimal totalDespesasAnual,
        BigDecimal saldoAnualConsolidado,
        BigDecimal taxaPoupancaMedia,
        String mesMaiorReceita,
        BigDecimal valorMaiorReceita,
        List<MesConsolidado> meses,
        Map<CategoriaTransacao, BigDecimal> rankingDespesasAnual
) {
    public record MesConsolidado(
            String mes,
            int numeroMes,
            BigDecimal receitas,
            BigDecimal despesas,
            BigDecimal saldo,
            BigDecimal taxaPoupanca,
            int quantidadeTransacoes
    ) {}
}
