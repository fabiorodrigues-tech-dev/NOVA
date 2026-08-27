package com.nova.agentefinanceiro.infrastructure.web;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.nova.agentefinanceiro.application.dto.ResumoFinanceiroResponse;
import com.nova.agentefinanceiro.application.dto.TransacaoRequest;
import com.nova.agentefinanceiro.application.dto.TransacaoResponse;
import com.nova.agentefinanceiro.application.usecase.CadastrarTransacaoUseCase;
import com.nova.agentefinanceiro.application.usecase.CalcularResumoFinanceiroUseCase;
import com.nova.agentefinanceiro.application.usecase.ListarTransacoesUseCase;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import com.nova.agentefinanceiro.infrastructure.web.controller.TransacaoController;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(TransacaoController.class)
class TransacaoControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private CadastrarTransacaoUseCase cadastrarTransacaoUseCase;

    @MockBean
    private ListarTransacoesUseCase listarTransacoesUseCase;

    @MockBean
    private CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase;

    @MockBean
    private com.nova.agentefinanceiro.application.usecase.ImportarExtratoOfxUseCase importarExtratoOfxUseCase;

    @MockBean
    private com.nova.agentefinanceiro.application.usecase.CalcularProjecaoFinanceiraUseCase calcularProjecaoFinanceiraUseCase;

    @MockBean
    private com.nova.agentefinanceiro.application.usecase.ProcessarNotificacaoNubankUseCase processarNotificacaoNubankUseCase;

    @Test
    @DisplayName("POST /api/transacoes - Deve retornar 201 Created quando payload for válido")
    void deveCadastrarTransacaoComSucesso() throws Exception {
        TransacaoRequest request = new TransacaoRequest(
                "Almoço Executivo",
                new BigDecimal("45.90"),
                TipoTransacao.DESPESA,
                CategoriaTransacao.ALIMENTACAO,
                LocalDate.now()
        );

        TransacaoResponse response = new TransacaoResponse(
                1L,
                "Almoço Executivo",
                new BigDecimal("45.90"),
                TipoTransacao.DESPESA,
                CategoriaTransacao.ALIMENTACAO,
                LocalDate.now()
        );

        when(cadastrarTransacaoUseCase.executar(any())).thenReturn(response);

        mockMvc.perform(post("/api/transacoes")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.descricao").value("Almoço Executivo"))
                .andExpect(jsonPath("$.valor").value(45.90))
                .andExpect(jsonPath("$.tipo").value("DESPESA"))
                .andExpect(jsonPath("$.categoria").value("ALIMENTACAO"));
    }

    @Test
    @DisplayName("POST /api/transacoes/webhook-notificacao - Deve retornar 200 OK ao processar notificação Nubank")
    void deveProcessarWebhookNotificacaoComSucesso() throws Exception {
        TransacaoResponse response = new TransacaoResponse(
                10L,
                "Restaurante Fogão de Lenha",
                new BigDecimal("45.90"),
                TipoTransacao.DESPESA,
                CategoriaTransacao.ALIMENTACAO,
                LocalDate.now()
        );

        when(processarNotificacaoNubankUseCase.executar(any())).thenReturn(response);

        mockMvc.perform(post("/api/transacoes/webhook-notificacao")
                        .contentType(MediaType.TEXT_PLAIN)
                        .content("Compra de R$ 45,90 no Restaurante Fogão de Lenha aprovada"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.descricao").value("Restaurante Fogão de Lenha"))
                .andExpect(jsonPath("$.valor").value(45.90));
    }

    @Test
    @DisplayName("POST /api/transacoes - Deve retornar 400 Bad Request quando payload for inválido")
    void deveRetornar400QuandoPayloadInvalido() throws Exception {
        TransacaoRequest requestInvalido = new TransacaoRequest(
                "", // Descrição em branco
                new BigDecimal("-10.00"), // Valor negativo
                TipoTransacao.DESPESA,
                CategoriaTransacao.ALIMENTACAO,
                LocalDate.now()
        );

        mockMvc.perform(post("/api/transacoes")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(requestInvalido)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.title").value("Requisição Inválida"));
    }

    @Test
    @DisplayName("GET /api/transacoes - Deve retornar 200 OK com a lista de transações")
    void deveListarTransacoesComSucesso() throws Exception {
        List<TransacaoResponse> lista = List.of(
                new TransacaoResponse(1L, "Academia", new BigDecimal("120.00"), TipoTransacao.DESPESA, CategoriaTransacao.SAUDE, LocalDate.now())
        );

        when(listarTransacoesUseCase.executar(any(), any())).thenReturn(lista);

        mockMvc.perform(get("/api/transacoes"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.size()").value(1))
                .andExpect(jsonPath("$[0].descricao").value("Academia"));
    }

    @Test
    @DisplayName("GET /api/transacoes/resumo - Deve retornar 200 OK com resumo consolidado")
    void deveRetornarResumoComSucesso() throws Exception {
        ResumoFinanceiroResponse resumo = new ResumoFinanceiroResponse(
                new BigDecimal("600.00"),
                new BigDecimal("3000.00"),
                new BigDecimal("2400.00"),
                2,
                LocalDate.of(2026, 8, 1),
                LocalDate.of(2026, 8, 31),
                Map.of(CategoriaTransacao.ALIMENTACAO, new BigDecimal("600.00"))
        );

        when(calcularResumoFinanceiroUseCase.executar(any(), any())).thenReturn(resumo);

        mockMvc.perform(get("/api/transacoes/resumo"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalGasto").value(600.00))
                .andExpect(jsonPath("$.totalReceitas").value(3000.00))
                .andExpect(jsonPath("$.saldo").value(2400.00))
                .andExpect(jsonPath("$.quantidadeTransacoes").value(2))
                .andExpect(jsonPath("$.totalPorCategoria.ALIMENTACAO").value(600.00));
    }

    @Test
    @DisplayName("POST /api/transacoes/importar-ofx - Deve retornar 200 OK com resumo da importação")
    void deveImportarExtratoOfxComSucesso() throws Exception {
        com.nova.agentefinanceiro.application.dto.ImportacaoExtratoResponse response =
                com.nova.agentefinanceiro.application.dto.ImportacaoExtratoResponse.sucesso(2, 2, 0, List.of());

        when(importarExtratoOfxUseCase.executar(any())).thenReturn(response);

        mockMvc.perform(post("/api/transacoes/importar-ofx")
                        .contentType(MediaType.TEXT_PLAIN)
                        .content("conteudo fake ofx"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalLidos").value(2))
                .andExpect(jsonPath("$.totalImportados").value(2))
                .andExpect(jsonPath("$.totalDuplicados").value(0));
    }

    @Test
    @DisplayName("GET /api/transacoes/projecao - Deve retornar 200 OK com projeção financeira")
    void deveRetornarProjecaoComSucesso() throws Exception {
        com.nova.agentefinanceiro.application.dto.ProjecaoFinanceiraResponse projecao =
                new com.nova.agentefinanceiro.application.dto.ProjecaoFinanceiraResponse(
                        LocalDate.of(2026, 8, 15), 15, 16, 31,
                        new BigDecimal("1000.00"), new BigDecimal("3000.00"), new BigDecimal("2000.00"),
                        new BigDecimal("66.67"), new BigDecimal("1066.72"), new BigDecimal("2066.72"),
                        new BigDecimal("933.28"), "SAUDAVEL", List.of("Alerta OK"), "Recomendação OK"
                );

        when(calcularProjecaoFinanceiraUseCase.executar(any())).thenReturn(projecao);

        mockMvc.perform(get("/api/transacoes/projecao"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.statusOrcamentario").value("SAUDAVEL"))
                .andExpect(jsonPath("$.burnRateDiario").value(66.67))
                .andExpect(jsonPath("$.saldoFinalProjetado").value(933.28));
    }
}
