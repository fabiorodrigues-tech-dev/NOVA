package com.nova.agentefinanceiro.application.dto;

import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * DTO de entrada para cadastro de nova transação financeira.
 */
public record TransacaoRequest(
        @NotBlank(message = "A descrição da transação é obrigatória.")
        @Size(max = 255, message = "A descrição deve ter no máximo 255 caracteres.")
        String descricao,

        @NotNull(message = "O valor é obrigatório.")
        @Positive(message = "O valor da transação deve ser positivo.")
        BigDecimal valor,

        TipoTransacao tipo,

        CategoriaTransacao categoria,

        LocalDate data
) {}
