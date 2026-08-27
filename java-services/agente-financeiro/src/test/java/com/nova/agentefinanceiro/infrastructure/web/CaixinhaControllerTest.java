package com.nova.agentefinanceiro.infrastructure.web;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.nova.agentefinanceiro.application.dto.CaixinhaRequest;
import com.nova.agentefinanceiro.application.dto.CaixinhaResponse;
import com.nova.agentefinanceiro.application.dto.PatrimonioLiquidoResponse;
import com.nova.agentefinanceiro.application.usecase.ListarCaixinhasUseCase;
import com.nova.agentefinanceiro.application.usecase.SalvarCaixinhaUseCase;
import com.nova.agentefinanceiro.domain.model.TipoCaixinha;
import com.nova.agentefinanceiro.infrastructure.web.controller.CaixinhaController;
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

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(CaixinhaController.class)
@DisplayName("Testes de Integração Web: CaixinhaController")
class CaixinhaControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private SalvarCaixinhaUseCase salvarCaixinhaUseCase;

    @MockBean
    private ListarCaixinhasUseCase listarCaixinhasUseCase;

    @Test
    @DisplayName("POST /api/financeiro/caixinhas - Deve retornar 201 Created ao salvar caixinha")
    void deveSalvarCaixinhaComSucesso() throws Exception {
        CaixinhaRequest request = new CaixinhaRequest(
                "Reserva de Emergência",
                new BigDecimal("2000.00"),
                TipoCaixinha.RESERVA_EMERGENCIA,
                new BigDecimal("20.00")
        );

        CaixinhaResponse response = new CaixinhaResponse(
                1L,
                "Reserva de Emergência",
                new BigDecimal("2000.00"),
                TipoCaixinha.RESERVA_EMERGENCIA,
                new BigDecimal("20.00"),
                LocalDate.now()
        );

        when(salvarCaixinhaUseCase.executar(any())).thenReturn(response);

        mockMvc.perform(post("/api/financeiro/caixinhas")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.nome").value("Reserva de Emergência"))
                .andExpect(jsonPath("$.saldo").value(2000.00));
    }

    @Test
    @DisplayName("GET /api/financeiro/caixinhas - Deve retornar 200 OK com patrimônio líquido consolidado")
    void deveObterPatrimonioLiquido() throws Exception {
        PatrimonioLiquidoResponse response = new PatrimonioLiquidoResponse(
                new BigDecimal("589.23"),
                new BigDecimal("2500.00"),
                new BigDecimal("3089.23"),
                List.of(
                        new CaixinhaResponse(1L, "Reserva de Emergência", new BigDecimal("1500.00"), TipoCaixinha.RESERVA_EMERGENCIA, BigDecimal.ZERO, LocalDate.now()),
                        new CaixinhaResponse(2L, "Fundo do Casal", new BigDecimal("1000.00"), TipoCaixinha.FUNDO_CASAL, BigDecimal.ZERO, LocalDate.now())
                )
        );

        when(listarCaixinhasUseCase.executar()).thenReturn(response);

        mockMvc.perform(get("/api/financeiro/caixinhas"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.saldoContaCorrente").value(589.23))
                .andExpect(jsonPath("$.totalInvestidoCaixinhas").value(2500.00))
                .andExpect(jsonPath("$.patrimonioLiquidoTotal").value(3089.23))
                .andExpect(jsonPath("$.caixinhas.length()").value(2));
    }
}
