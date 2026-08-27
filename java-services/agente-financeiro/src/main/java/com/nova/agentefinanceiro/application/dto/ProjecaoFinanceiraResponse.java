package com.nova.agentefinanceiro.application.dto;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

/**
 * DTO com a inteligência preditiva e projeção financeira orçamentária.
 */
public record ProjecaoFinanceiraResponse(
        LocalDate dataReferencia,
        int diasDecorridos,
        int diasRestantes,
        int totalDiasMes,
        BigDecimal totalGastosAtual,
        BigDecimal totalReceitasAtual,
        BigDecimal saldoAtual,
        BigDecimal burnRateDiario,
        BigDecimal gastoAdicionalProjetado,
        BigDecimal gastoTotalProjetado,
        BigDecimal saldoFinalProjetado,
        String statusOrcamentario, // "SAUDAVEL", "ALERTA", "CRITICO"
        List<String> alertas,
        String recomendacaoEstrategica
) {
}
