package com.nova.agentefinanceiro.infrastructure.mcp;

import com.nova.agentefinanceiro.application.dto.ResumoFinanceiroResponse;
import com.nova.agentefinanceiro.application.dto.TransacaoRequest;
import com.nova.agentefinanceiro.application.dto.TransacaoResponse;
import com.nova.agentefinanceiro.application.usecase.CadastrarTransacaoUseCase;
import com.nova.agentefinanceiro.application.usecase.CalcularResumoFinanceiroUseCase;
import com.nova.agentefinanceiro.application.usecase.ListarTransacoesUseCase;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class FinanceiroMcpToolsTest {

    @Mock
    private CadastrarTransacaoUseCase cadastrarTransacaoUseCase;

    @Mock
    private ListarTransacoesUseCase listarTransacoesUseCase;

    @Mock
    private CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase;

    @Mock
    private com.nova.agentefinanceiro.application.usecase.ImportarExtratoOfxUseCase importarExtratoOfxUseCase;

    @Mock
    private com.nova.agentefinanceiro.application.usecase.CalcularProjecaoFinanceiraUseCase calcularProjecaoFinanceiraUseCase;

    @Mock
    private com.nova.agentefinanceiro.application.usecase.SalvarCaixinhaUseCase salvarCaixinhaUseCase;

    @Mock
    private com.nova.agentefinanceiro.application.usecase.ListarCaixinhasUseCase listarCaixinhasUseCase;

    @InjectMocks
    private FinanceiroMcpTools financeiroMcpTools;

    @Test
    @DisplayName("Ferramenta cadastrar_transacao deve converter parâmetros e delegar ao use case")
    void deveCadastrarTransacaoViaMcpTool() {
        TransacaoResponse responseEsperada = new TransacaoResponse(
                1L, "Almoço", new BigDecimal("35.00"), TipoTransacao.DESPESA, CategoriaTransacao.ALIMENTACAO, LocalDate.now()
        );
        when(cadastrarTransacaoUseCase.executar(any())).thenReturn(responseEsperada);

        TransacaoResponse response = financeiroMcpTools.cadastrarTransacao(
                "Almoço", new BigDecimal("35.00"), TipoTransacao.DESPESA, CategoriaTransacao.ALIMENTACAO, LocalDate.now()
        );

        assertThat(response).isEqualTo(responseEsperada);

        ArgumentCaptor<TransacaoRequest> captor = ArgumentCaptor.forClass(TransacaoRequest.class);
        verify(cadastrarTransacaoUseCase).executar(captor.capture());
        assertThat(captor.getValue().descricao()).isEqualTo("Almoço");
        assertThat(captor.getValue().valor()).isEqualByComparingTo("35.00");
    }

    @Test
    @DisplayName("Ferramenta listar_transacoes deve repassar filtros ao use case")
    void deveListarTransacoesViaMcpTool() {
        LocalDate inicio = LocalDate.of(2026, 8, 1);
        LocalDate fim = LocalDate.of(2026, 8, 31);
        when(listarTransacoesUseCase.executar(inicio, fim)).thenReturn(List.of());

        List<TransacaoResponse> lista = financeiroMcpTools.listarTransacoes(inicio, fim);

        assertThat(lista).isEmpty();
        verify(listarTransacoesUseCase).executar(inicio, fim);
    }

    @Test
    @DisplayName("Ferramenta resumo_financeiro deve delegar ao use case de resumo")
    void deveObterResumoViaMcpTool() {
        ResumoFinanceiroResponse resumoEsperado = new ResumoFinanceiroResponse(
                BigDecimal.ZERO, BigDecimal.ZERO, BigDecimal.ZERO, 0, null, null, Map.of()
        );
        when(calcularResumoFinanceiroUseCase.executar(any(), any())).thenReturn(resumoEsperado);

        ResumoFinanceiroResponse response = financeiroMcpTools.resumoFinanceiro(null, null);

        assertThat(response).isEqualTo(resumoEsperado);
        verify(calcularResumoFinanceiroUseCase).executar(null, null);
    }

    @Test
    @DisplayName("Ferramenta importar_extrato_ofx deve delegar ao use case de importação")
    void deveImportarExtratoOfxViaMcpTool() {
        com.nova.agentefinanceiro.application.dto.ImportacaoExtratoResponse responseEsperada =
                com.nova.agentefinanceiro.application.dto.ImportacaoExtratoResponse.sucesso(2, 2, 0, List.of());
        when(importarExtratoOfxUseCase.executar(any())).thenReturn(responseEsperada);

        com.nova.agentefinanceiro.application.dto.ImportacaoExtratoResponse response =
                financeiroMcpTools.importarExtratoOfx("conteudo fake", null);

        assertThat(response).isEqualTo(responseEsperada);
        verify(importarExtratoOfxUseCase).executar("conteudo fake");
    }

    @Test
    @DisplayName("Ferramenta projecao_financeira deve delegar ao use case de projeção")
    void deveObterProjecaoViaMcpTool() {
        com.nova.agentefinanceiro.application.dto.ProjecaoFinanceiraResponse projecaoEsperada =
                new com.nova.agentefinanceiro.application.dto.ProjecaoFinanceiraResponse(
                        LocalDate.now(), 15, 16, 31,
                        BigDecimal.ZERO, BigDecimal.ZERO, BigDecimal.ZERO,
                        BigDecimal.ZERO, BigDecimal.ZERO, BigDecimal.ZERO, BigDecimal.ZERO,
                        "SAUDAVEL", List.of(), "Recomendação OK"
                );
        when(calcularProjecaoFinanceiraUseCase.executar(any())).thenReturn(projecaoEsperada);

        com.nova.agentefinanceiro.application.dto.ProjecaoFinanceiraResponse response =
                financeiroMcpTools.projecaoFinanceira(null);

        assertThat(response).isEqualTo(projecaoEsperada);
        verify(calcularProjecaoFinanceiraUseCase).executar(null);
    }

    @Test
    @DisplayName("Ferramenta atualizar_caixinha deve delegar ao use case de caixinhas")
    void deveAtualizarCaixinhaViaMcpTool() {
        com.nova.agentefinanceiro.application.dto.CaixinhaResponse responseEsperada =
                new com.nova.agentefinanceiro.application.dto.CaixinhaResponse(
                        1L, "Reserva de Emergência", new BigDecimal("1500.00"),
                        com.nova.agentefinanceiro.domain.model.TipoCaixinha.RESERVA_EMERGENCIA,
                        BigDecimal.ZERO, LocalDate.now()
                );
        when(salvarCaixinhaUseCase.executar(any())).thenReturn(responseEsperada);

        com.nova.agentefinanceiro.application.dto.CaixinhaResponse response =
                financeiroMcpTools.atualizarCaixinha("Reserva de Emergência", new BigDecimal("1500.00"), null, null);

        assertThat(response).isEqualTo(responseEsperada);
        verify(salvarCaixinhaUseCase).executar(any());
    }

    @Test
    @DisplayName("Ferramenta consultar_caixinhas deve delegar ao use case de listagem")
    void deveConsultarCaixinhasViaMcpTool() {
        com.nova.agentefinanceiro.application.dto.PatrimonioLiquidoResponse responseEsperada =
                new com.nova.agentefinanceiro.application.dto.PatrimonioLiquidoResponse(
                        new BigDecimal("500.00"), new BigDecimal("1500.00"), new BigDecimal("2000.00"), List.of()
                );
        when(listarCaixinhasUseCase.executar()).thenReturn(responseEsperada);

        com.nova.agentefinanceiro.application.dto.PatrimonioLiquidoResponse response =
                financeiroMcpTools.consultarCaixinhas();

        assertThat(response).isEqualTo(responseEsperada);
        verify(listarCaixinhasUseCase).executar();
    }
}
