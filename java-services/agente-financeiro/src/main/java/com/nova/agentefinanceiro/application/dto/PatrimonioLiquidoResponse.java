package com.nova.agentefinanceiro.application.dto;

import java.math.BigDecimal;
import java.util.List;

/**
 * DTO consolidando o Patrimônio Líquido Total (Saldo H2 Conta Corrente + Caixinhas Nubank).
 */
public record PatrimonioLiquidoResponse(
        BigDecimal saldoContaCorrente,
        BigDecimal totalInvestidoCaixinhas,
        BigDecimal patrimonioLiquidoTotal,
        List<CaixinhaResponse> caixinhas
) {
}
