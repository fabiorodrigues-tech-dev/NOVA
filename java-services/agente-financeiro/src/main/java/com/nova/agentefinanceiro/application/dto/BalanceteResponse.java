package com.nova.agentefinanceiro.application.dto;

import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Map;

/**
 * DTO de resposta para o Balancete de Verificação Contábil Mensal.
 */
public record BalanceteResponse(
        String mesReferencia,
        LocalDate periodoInicio,
        LocalDate periodoFim,
        BigDecimal saldoInicial,
        BigDecimal totalCreditos,
        BigDecimal totalDebitos,
        BigDecimal saldoFinal,
        boolean consistente,
        String statusContabil,
        Map<CategoriaTransacao, BigDecimal> debitosPorCategoria,
        Map<CategoriaTransacao, BigDecimal> creditosPorCategoria,
        String hashAutenticidade
) {}
