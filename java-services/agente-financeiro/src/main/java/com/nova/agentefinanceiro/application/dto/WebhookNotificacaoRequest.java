package com.nova.agentefinanceiro.application.dto;

import jakarta.validation.constraints.NotBlank;

/**
 * DTO para recebimento de notificações push do Nubank via Webhook.
 */
public record WebhookNotificacaoRequest(
        @NotBlank(message = "O texto da notificação é obrigatório.")
        String textoNotificacao
) {
}
