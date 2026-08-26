package com.nova.agentefinanceiro.application.dto;

/**
 * DTO de resposta estruturada para síntese de voz e interface gráfica.
 */
public record VoiceCommandResponse(
    String mensagemVoz,
    String status,
    Object dados
) {
    public static VoiceCommandResponse sucesso(String mensagemVoz, Object dados) {
        return new VoiceCommandResponse(mensagemVoz, "SUCESSO", dados);
    }

    public static VoiceCommandResponse sucesso(String mensagemVoz) {
        return new VoiceCommandResponse(mensagemVoz, "SUCESSO", null);
    }

    public static VoiceCommandResponse erro(String mensagemVoz) {
        return new VoiceCommandResponse(mensagemVoz, "ERRO", null);
    }
}
