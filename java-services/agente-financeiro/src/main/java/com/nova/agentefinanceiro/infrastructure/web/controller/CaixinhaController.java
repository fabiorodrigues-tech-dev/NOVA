package com.nova.agentefinanceiro.infrastructure.web.controller;

import com.nova.agentefinanceiro.application.dto.CaixinhaRequest;
import com.nova.agentefinanceiro.application.dto.CaixinhaResponse;
import com.nova.agentefinanceiro.application.dto.PatrimonioLiquidoResponse;
import com.nova.agentefinanceiro.application.usecase.ListarCaixinhasUseCase;
import com.nova.agentefinanceiro.application.usecase.SalvarCaixinhaUseCase;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Controller REST para gerenciamento de Caixinhas e Investimentos Nubank (Reserva de Emergência e Fundo do Casal).
 */
@RestController
@RequestMapping("/api/financeiro/caixinhas")
public class CaixinhaController {

    private final SalvarCaixinhaUseCase salvarCaixinhaUseCase;
    private final ListarCaixinhasUseCase listarCaixinhasUseCase;

    public CaixinhaController(
            SalvarCaixinhaUseCase salvarCaixinhaUseCase,
            ListarCaixinhasUseCase listarCaixinhasUseCase
    ) {
        this.salvarCaixinhaUseCase = salvarCaixinhaUseCase;
        this.listarCaixinhasUseCase = listarCaixinhasUseCase;
    }

    @PostMapping
    public ResponseEntity<CaixinhaResponse> salvar(@RequestBody @Valid CaixinhaRequest request) {
        CaixinhaResponse response = salvarCaixinhaUseCase.executar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping
    public ResponseEntity<PatrimonioLiquidoResponse> obterPatrimonioLiquido() {
        PatrimonioLiquidoResponse response = listarCaixinhasUseCase.executar();
        return ResponseEntity.ok(response);
    }
}
