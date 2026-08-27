package com.nova.agentefinanceiro.application.dto;

import com.nova.agentefinanceiro.domain.model.Caixinha;
import com.nova.agentefinanceiro.domain.model.TipoCaixinha;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * DTO de resposta para Caixinhas.
 */
public record CaixinhaResponse(
        Long id,
        String nome,
        BigDecimal saldo,
        TipoCaixinha tipo,
        BigDecimal rendimentoMensalEstimado,
        LocalDate dataAtualizacao
) {
    public static CaixinhaResponse deDominio(Caixinha c) {
        if (c == null) return null;
        return new CaixinhaResponse(
                c.getId(),
                c.getNome(),
                c.getSaldo(),
                c.getTipo(),
                c.getRendimentoMensalEstimado(),
                c.getDataAtualizacao()
        );
    }
}
