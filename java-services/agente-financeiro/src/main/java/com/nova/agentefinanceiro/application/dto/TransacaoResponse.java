package com.nova.agentefinanceiro.application.dto;

import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import com.nova.agentefinanceiro.domain.model.Transacao;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * DTO imutável de resposta para retorno de dados de uma transação.
 */
public record TransacaoResponse(
        Long id,
        String descricao,
        BigDecimal valor,
        TipoTransacao tipo,
        CategoriaTransacao categoria,
        LocalDate data
) {
    public static TransacaoResponse fromDomain(Transacao domain) {
        return new TransacaoResponse(
                domain.getId(),
                domain.getDescricao(),
                domain.getValor(),
                domain.getTipo(),
                domain.getCategoria(),
                domain.getData()
        );
    }
}
