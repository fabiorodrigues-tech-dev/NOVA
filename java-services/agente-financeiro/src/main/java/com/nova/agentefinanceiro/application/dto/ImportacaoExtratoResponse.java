package com.nova.agentefinanceiro.application.dto;

import java.util.List;

/**
 * DTO de resposta para operações de importação de extrato bancário (OFX / CSV).
 */
public record ImportacaoExtratoResponse(
        int totalLidos,
        int totalImportados,
        int totalDuplicados,
        List<TransacaoResponse> transacoesImportadas,
        String mensagem
) {
    public static ImportacaoExtratoResponse sucesso(int lidos, int importados, int duplicados, List<TransacaoResponse> transacoes) {
        String msg = String.format("Extrato processado com sucesso: %d lidos, %d importados, %d duplicados ignorados.",
                lidos, importados, duplicados);
        return new ImportacaoExtratoResponse(lidos, importados, duplicados, transacoes, msg);
    }
}
