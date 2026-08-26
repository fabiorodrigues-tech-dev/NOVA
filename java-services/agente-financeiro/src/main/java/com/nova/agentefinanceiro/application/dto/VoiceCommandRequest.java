package com.nova.agentefinanceiro.application.dto;

/**
 * DTO para recebimento de comandos de voz transcritos.
 */
public record VoiceCommandRequest(
    String comando,
    String contexto
) {
    public VoiceCommandRequest(String comando) {
        this(comando, null);
    }
}
