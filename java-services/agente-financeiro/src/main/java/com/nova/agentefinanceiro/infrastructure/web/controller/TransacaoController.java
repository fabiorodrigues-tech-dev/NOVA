package com.nova.agentefinanceiro.infrastructure.web.controller;

import com.nova.agentefinanceiro.application.dto.ImportacaoExtratoResponse;
import com.nova.agentefinanceiro.application.dto.ProjecaoFinanceiraResponse;
import com.nova.agentefinanceiro.application.dto.ResumoFinanceiroResponse;
import com.nova.agentefinanceiro.application.dto.TransacaoRequest;
import com.nova.agentefinanceiro.application.dto.TransacaoResponse;
import com.nova.agentefinanceiro.application.usecase.CadastrarTransacaoUseCase;
import com.nova.agentefinanceiro.application.usecase.CalcularProjecaoFinanceiraUseCase;
import com.nova.agentefinanceiro.application.usecase.CalcularResumoFinanceiroUseCase;
import com.nova.agentefinanceiro.application.usecase.ImportarExtratoOfxUseCase;
import com.nova.agentefinanceiro.application.usecase.ListarTransacoesUseCase;
import jakarta.validation.Valid;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;
import java.util.List;

/**
 * Controller REST expondo os endpoints para gerenciamento de transações financeiras.
 */
@RestController
@RequestMapping("/api/transacoes")
public class TransacaoController {

    private final CadastrarTransacaoUseCase cadastrarTransacaoUseCase;
    private final ListarTransacoesUseCase listarTransacoesUseCase;
    private final CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase;
    private final ImportarExtratoOfxUseCase importarExtratoOfxUseCase;
    private final CalcularProjecaoFinanceiraUseCase calcularProjecaoFinanceiraUseCase;

    public TransacaoController(
            CadastrarTransacaoUseCase cadastrarTransacaoUseCase,
            ListarTransacoesUseCase listarTransacoesUseCase,
            CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase,
            ImportarExtratoOfxUseCase importarExtratoOfxUseCase,
            CalcularProjecaoFinanceiraUseCase calcularProjecaoFinanceiraUseCase
    ) {
        this.cadastrarTransacaoUseCase = cadastrarTransacaoUseCase;
        this.listarTransacoesUseCase = listarTransacoesUseCase;
        this.calcularResumoFinanceiroUseCase = calcularResumoFinanceiroUseCase;
        this.importarExtratoOfxUseCase = importarExtratoOfxUseCase;
        this.calcularProjecaoFinanceiraUseCase = calcularProjecaoFinanceiraUseCase;
    }

    @PostMapping
    public ResponseEntity<TransacaoResponse> cadastrar(@RequestBody @Valid TransacaoRequest request) {
        TransacaoResponse response = cadastrarTransacaoUseCase.executar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PostMapping("/importar-ofx")
    public ResponseEntity<ImportacaoExtratoResponse> importarOfx(@RequestBody String conteudo) {
        ImportacaoExtratoResponse response = importarExtratoOfxUseCase.executar(conteudo);
        return ResponseEntity.ok(response);
    }

    @GetMapping
    public ResponseEntity<List<TransacaoResponse>> listar(
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate inicio,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate fim
    ) {
        List<TransacaoResponse> lista = listarTransacoesUseCase.executar(inicio, fim);
        return ResponseEntity.ok(lista);
    }

    @GetMapping("/resumo")
    public ResponseEntity<ResumoFinanceiroResponse> obterResumo(
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate inicio,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate fim
    ) {
        ResumoFinanceiroResponse resumo = calcularResumoFinanceiroUseCase.executar(inicio, fim);
        return ResponseEntity.ok(resumo);
    }

    @GetMapping("/projecao")
    public ResponseEntity<ProjecaoFinanceiraResponse> obterProjecao(
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate dataReferencia
    ) {
        ProjecaoFinanceiraResponse projecao = calcularProjecaoFinanceiraUseCase.executar(dataReferencia);
        return ResponseEntity.ok(projecao);
    }
}
