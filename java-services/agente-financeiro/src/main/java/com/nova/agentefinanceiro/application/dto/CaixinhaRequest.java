package com.nova.agentefinanceiro.application.dto;

import com.nova.agentefinanceiro.domain.model.TipoCaixinha;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.math.BigDecimal;

/**
 * DTO para cadastro ou atualização de Caixinhas e Investimentos Nubank.
 */
public record CaixinhaRequest(
        @NotBlank(message = "O nome da caixinha é obrigatório.")
        String nome,

        @NotNull(message = "O saldo é obrigatório.")
        @DecimalMin(value = "0.0", message = "O saldo não pode ser negativo.")
        BigDecimal saldo,

        TipoCaixinha tipo,

        BigDecimal rendimentoMensalEstimado
) {
}
