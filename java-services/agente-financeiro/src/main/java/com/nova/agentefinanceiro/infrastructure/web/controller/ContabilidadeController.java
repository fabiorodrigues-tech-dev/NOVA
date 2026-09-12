package com.nova.agentefinanceiro.infrastructure.web.controller;

import com.nova.agentefinanceiro.application.dto.BalanceteResponse;
import com.nova.agentefinanceiro.application.dto.BalancoPatrimonialResponse;
import com.nova.agentefinanceiro.application.dto.ComparativoMesesResponse;
import com.nova.agentefinanceiro.application.dto.HistoricoAnualResponse;
import com.nova.agentefinanceiro.application.usecase.ContabilidadeUseCase;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * Controller REST para Operações Contábeis Sênior do Ecossistema NOVA:
 * - Balancete de Verificação Mensal
 * - Balanço Patrimonial & DRE
 * - Comparativo Horizontal entre Meses
 * - Histórico Anual Consolidado
 */
@RestController
@RequestMapping("/api/financeiro")
public class ContabilidadeController {

    private final ContabilidadeUseCase contabilidadeUseCase;

    public ContabilidadeController(ContabilidadeUseCase contabilidadeUseCase) {
        this.contabilidadeUseCase = contabilidadeUseCase;
    }

    @GetMapping("/balancete")
    public ResponseEntity<BalanceteResponse> obterBalancete(
            @RequestParam(name = "mes", required = false) String mes
    ) {
        BalanceteResponse response = contabilidadeUseCase.gerarBalancete(mes);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/balanco-patrimonial")
    public ResponseEntity<BalancoPatrimonialResponse> obterBalancoPatrimonial() {
        BalancoPatrimonialResponse response = contabilidadeUseCase.gerarBalancoPatrimonial();
        return ResponseEntity.ok(response);
    }

    @GetMapping("/comparativo")
    public ResponseEntity<ComparativoMesesResponse> obterComparativo(
            @RequestParam(name = "mes1", required = false, defaultValue = "2026-07") String mes1,
            @RequestParam(name = "mes2", required = false, defaultValue = "2026-08") String mes2
    ) {
        ComparativoMesesResponse response = contabilidadeUseCase.gerarComparativo(mes1, mes2);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/anual")
    public ResponseEntity<HistoricoAnualResponse> obterHistoricoAnual(
            @RequestParam(name = "ano", required = false, defaultValue = "2026") int ano
    ) {
        HistoricoAnualResponse response = contabilidadeUseCase.gerarHistoricoAnual(ano);
        return ResponseEntity.ok(response);
    }
}
