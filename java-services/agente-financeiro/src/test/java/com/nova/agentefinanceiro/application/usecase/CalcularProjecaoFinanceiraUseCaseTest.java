package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.ProjecaoFinanceiraResponse;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CalcularProjecaoFinanceiraUseCaseTest {

    @Mock
    private TransacaoRepository transacaoRepository;

    private CalcularProjecaoFinanceiraUseCase useCase;

    @BeforeEach
    void setUp() {
        useCase = new CalcularProjecaoFinanceiraUseCase(transacaoRepository);
    }

    @Test
    @DisplayName("Deve calcular projeção financeira saudável com superávit ao fim do mês")
    void deveCalcularProjecaoSaudavelComSuperavit() {
        LocalDate dataRef = LocalDate.of(2026, 8, 15); // Dia 15 de 31 dias

        List<Transacao> transacoes = List.of(
                new Transacao(1L, "Salário", new BigDecimal("3000.00"), TipoTransacao.RECEITA, CategoriaTransacao.SALARIO, LocalDate.of(2026, 8, 5)),
                new Transacao(2L, "Aluguel", new BigDecimal("600.00"), TipoTransacao.DESPESA, CategoriaTransacao.MORADIA, LocalDate.of(2026, 8, 10)),
                new Transacao(3L, "Mercado", new BigDecimal("450.00"), TipoTransacao.DESPESA, CategoriaTransacao.ALIMENTACAO, LocalDate.of(2026, 8, 12))
        );

        when(transacaoRepository.listarPorPeriodo(any(), any())).thenReturn(transacoes);

        ProjecaoFinanceiraResponse response = useCase.executar(dataRef);

        assertNotNull(response);
        assertEquals(15, response.diasDecorridos());
        assertEquals(16, response.diasRestantes());
        assertEquals(31, response.totalDiasMes());

        assertEquals(new BigDecimal("1050.00"), response.totalGastosAtual());
        assertEquals(new BigDecimal("3000.00"), response.totalReceitasAtual());
        assertEquals(new BigDecimal("1950.00"), response.saldoAtual());

        // Burn rate = 1050 / 15 = 70.00/dia
        assertEquals(new BigDecimal("70.00"), response.burnRateDiario());
        // Gasto adicional = 70.00 * 16 = 1120.00
        assertEquals(new BigDecimal("1120.00"), response.gastoAdicionalProjetado());
        // Gasto total = 1050 + 1120 = 2170.00
        assertEquals(new BigDecimal("2170.00"), response.gastoTotalProjetado());
        // Saldo projetado = 3000 - 2170 = 830.00
        assertEquals(new BigDecimal("830.00"), response.saldoFinalProjetado());

        assertEquals("SAUDAVEL", response.statusOrcamentario());
        assertFalse(response.alertas().isEmpty());
    }

    @Test
    @DisplayName("Deve calcular projeção crítica com déficit e gerar alertas de redução")
    void deveCalcularProjecaoCriticaComDeficit() {
        LocalDate dataRef = LocalDate.of(2026, 8, 10); // Dia 10 de 31 dias

        List<Transacao> transacoes = List.of(
                new Transacao(1L, "Salário", new BigDecimal("2000.00"), TipoTransacao.RECEITA, CategoriaTransacao.SALARIO, LocalDate.of(2026, 8, 1)),
                new Transacao(2L, "Compras Diversas", new BigDecimal("1500.00"), TipoTransacao.DESPESA, CategoriaTransacao.COMPRAS, LocalDate.of(2026, 8, 5))
        );

        when(transacaoRepository.listarPorPeriodo(any(), any())).thenReturn(transacoes);

        ProjecaoFinanceiraResponse response = useCase.executar(dataRef);

        assertNotNull(response);
        // Burn rate = 1500 / 10 = 150.00/dia
        assertEquals(new BigDecimal("150.00"), response.burnRateDiario());
        // Gasto adicional = 150.00 * 21 = 3150.00
        // Gasto total = 1500 + 3150 = 4650.00
        // Saldo projetado = 2000 - 4650 = -2650.00
        assertEquals(new BigDecimal("-2650.00"), response.saldoFinalProjetado());
        assertEquals("CRITICO", response.statusOrcamentario());
        assertTrue(response.alertas().get(0).contains("⚠️ Risco de Déficit"));
    }

    @Test
    @DisplayName("Deve calcular projeção em alerta quando margem for apertada")
    void deveCalcularProjecaoAlertaComMargemApertada() {
        LocalDate dataRef = LocalDate.of(2026, 8, 15); // Dia 15 de 31 dias

        List<Transacao> transacoes = List.of(
                new Transacao(1L, "Receita", new BigDecimal("2000.00"), TipoTransacao.RECEITA, CategoriaTransacao.SALARIO, LocalDate.of(2026, 8, 1)),
                new Transacao(2L, "Gastos", new BigDecimal("900.00"), TipoTransacao.DESPESA, CategoriaTransacao.OUTROS, LocalDate.of(2026, 8, 10))
        );

        when(transacaoRepository.listarPorPeriodo(any(), any())).thenReturn(transacoes);

        ProjecaoFinanceiraResponse response = useCase.executar(dataRef);

        assertNotNull(response);
        // Burn rate = 900 / 15 = 60.00/dia
        // Gasto adicional = 60.00 * 16 = 960.00
        // Gasto total = 900 + 960 = 1860.00
        // Saldo projetado = 2000 - 1860 = 140.00 (140 < 300 [15% de 2000])
        assertEquals(new BigDecimal("140.00"), response.saldoFinalProjetado());
        assertEquals("ALERTA", response.statusOrcamentario());
    }
}
