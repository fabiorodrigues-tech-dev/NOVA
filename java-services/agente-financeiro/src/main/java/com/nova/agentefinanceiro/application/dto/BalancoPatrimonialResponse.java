package com.nova.agentefinanceiro.application.dto;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

/**
 * DTO de resposta para o Balanço Patrimonial & DRE Consolidada.
 */
public record BalancoPatrimonialResponse(
        LocalDate dataPosicao,
        BigDecimal ativoCirculanteDisponivel,
        BigDecimal ativoCirculanteInvestido,
        BigDecimal totalAtivoCirculante,
        BigDecimal totalAtivoNaoCirculante,
        BigDecimal totalAtivo,
        BigDecimal totalPassivoCirculante,
        BigDecimal totalPassivoNaoCirculante,
        BigDecimal totalPassivo,
        BigDecimal patrimonioLiquidoTotal,
        BigDecimal rendimentoAcumuladoCaixinhas,
        String situacaoPatrimonial,
        List<CaixinhaResponse> caixinhas,
        String hashAutenticidade
) {}
