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
import org.springframework.web.bind.annotation.RequestHeader;
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
    private final com.nova.agentefinanceiro.application.usecase.ProcessarNotificacaoNubankUseCase processarNotificacaoNubankUseCase;

    public TransacaoController(
            CadastrarTransacaoUseCase cadastrarTransacaoUseCase,
            ListarTransacoesUseCase listarTransacoesUseCase,
            CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase,
            ImportarExtratoOfxUseCase importarExtratoOfxUseCase,
            CalcularProjecaoFinanceiraUseCase calcularProjecaoFinanceiraUseCase,
            com.nova.agentefinanceiro.application.usecase.ProcessarNotificacaoNubankUseCase processarNotificacaoNubankUseCase
    ) {
        this.cadastrarTransacaoUseCase = cadastrarTransacaoUseCase;
        this.listarTransacoesUseCase = listarTransacoesUseCase;
        this.calcularResumoFinanceiroUseCase = calcularResumoFinanceiroUseCase;
        this.importarExtratoOfxUseCase = importarExtratoOfxUseCase;
        this.calcularProjecaoFinanceiraUseCase = calcularProjecaoFinanceiraUseCase;
        this.processarNotificacaoNubankUseCase = processarNotificacaoNubankUseCase;
    }

    @PostMapping
    public ResponseEntity<TransacaoResponse> cadastrar(@RequestBody @Valid TransacaoRequest request) {
        TransacaoResponse response = cadastrarTransacaoUseCase.executar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PostMapping("/importar-ofx")
    public ResponseEntity<ImportacaoExtratoResponse> importarOfx(
            @RequestBody(required = false) String conteudo,
            @RequestParam(required = false) String arquivo
    ) {
        if (arquivo != null && !arquivo.isBlank()) {
            return ResponseEntity.ok(importarExtratoOfxUseCase.importarArquivo(arquivo));
        }
        if (conteudo == null || conteudo.trim().isBlank()) {
            return ResponseEntity.ok(importarExtratoOfxUseCase.importarDiretorioPadrao());
        }
        ImportacaoExtratoResponse response = importarExtratoOfxUseCase.executar(conteudo);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/reconciliar-estrito")
    public ResponseEntity<ImportacaoExtratoResponse> reconciliarEstrito() {
        ImportacaoExtratoResponse response = importarExtratoOfxUseCase.reconciliarExtratosEstrito();
        return ResponseEntity.ok(response);
    }

    @PostMapping("/webhook-notificacao")
    public ResponseEntity<TransacaoResponse> processarWebhookNotificacao(
            @RequestHeader(value = "X-NOVA-PIN", required = false) String headerPin,
            @RequestBody(required = false) String payload
    ) {
        if (payload == null || payload.isBlank()) {
            return ResponseEntity.badRequest().build();
        }

        String texto = payload.trim();
        String pin = headerPin;

        // Se o payload for JSON, extrai campos notificacao / textoNotificacao / pin
        if (texto.startsWith("{") && texto.endsWith("}")) {
            try {
                if (texto.contains("\"pin\"")) {
                    int pStart = texto.indexOf("\"pin\"") + 5;
                    int colon = texto.indexOf(":", pStart);
                    if (colon > 0) {
                        int q1 = texto.indexOf("\"", colon);
                        if (q1 > 0) {
                            int q2 = texto.indexOf("\"", q1 + 1);
                            if (q2 > q1) pin = texto.substring(q1 + 1, q2).trim();
                        }
                    }
                }
                if (texto.contains("\"notificacao\"")) {
                    int nStart = texto.indexOf("\"notificacao\"") + 13;
                    int colon = texto.indexOf(":", nStart);
                    if (colon > 0) {
                        int q1 = texto.indexOf("\"", colon);
                        if (q1 > 0) {
                            int q2 = texto.indexOf("\"", q1 + 1);
                            if (q2 > q1) texto = texto.substring(q1 + 1, q2);
                        }
                    }
                } else if (texto.contains("\"textoNotificacao\"")) {
                    int nStart = texto.indexOf("\"textoNotificacao\"") + 18;
                    int colon = texto.indexOf(":", nStart);
                    if (colon > 0) {
                        int q1 = texto.indexOf("\"", colon);
                        if (q1 > 0) {
                            int q2 = texto.indexOf("\"", q1 + 1);
                            if (q2 > q1) texto = texto.substring(q1 + 1, q2);
                        }
                    }
                }
            } catch (Exception ignored) {}
        }

        // Validação de PIN de segurança se informado
        if (pin != null && !pin.isBlank() && !"7770".equals(pin.trim())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }

        TransacaoResponse response = processarNotificacaoNubankUseCase.executar(texto);
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
