package com.nova.agentefinanceiro.application.dto;

import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;

import java.math.BigDecimal;
import java.util.Map;

/**
 * DTO de resposta para Comparativo Horizontal entre dois meses.
 */
public record ComparativoMesesResponse(
        String mes1,
        String mes2,
        BigDecimal receitasMes1,
        BigDecimal receitasMes2,
        BigDecimal variacaoReceitasAbsoluta,
        BigDecimal variacaoReceitasPercentual,
        BigDecimal despesasMes1,
        BigDecimal despesasMes2,
        BigDecimal variacaoDespesasAbsoluta,
        BigDecimal variacaoDespesasPercentual,
        BigDecimal saldoMes1,
        BigDecimal saldoMes2,
        BigDecimal variacaoSaldoAbsoluta,
        Map<CategoriaTransacao, VariacaoCategoria> variacaoPorCategoria,
        String diagnosticoContabil
) {
    public record VariacaoCategoria(
            BigDecimal valorMes1,
            BigDecimal valorMes2,
            BigDecimal variacaoAbsoluta,
            BigDecimal variacaoPercentual
    ) {}
}
