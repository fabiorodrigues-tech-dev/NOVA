package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.ResumoFinanceiroResponse;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.ResumoFinanceiro;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CalcularResumoFinanceiroUseCaseTest {

    @Mock
    private TransacaoRepository transacaoRepository;

    @InjectMocks
    private CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase;

    private LocalDate dataInicio;
    private LocalDate dataFim;

    @BeforeEach
    void setUp() {
        dataInicio = LocalDate.of(2026, 8, 1);
        dataFim = LocalDate.of(2026, 8, 31);
    }

    @Test
    @DisplayName("Deve calcular totais de despesas, receitas, saldo e detalhe por categoria com precisão")
    void deveCalcularResumoComSucesso() {
        List<Transacao> transacoes = List.of(
                new Transacao(1L, "Supermercado Semanal", new BigDecimal("350.00"), TipoTransacao.DESPESA, CategoriaTransacao.ALIMENTACAO, LocalDate.of(2026, 8, 5)),
                new Transacao(2L, "Restaurante Fim de Semana", new BigDecimal("150.00"), TipoTransacao.DESPESA, CategoriaTransacao.ALIMENTACAO, LocalDate.of(2026, 8, 10)),
                new Transacao(3L, "Combustível", new BigDecimal("200.00"), TipoTransacao.DESPESA, CategoriaTransacao.TRANSPORTE, LocalDate.of(2026, 8, 12)),
                new Transacao(4L, "Salário Tech", new BigDecimal("5000.00"), TipoTransacao.RECEITA, CategoriaTransacao.SALARIO, LocalDate.of(2026, 8, 5))
        );

        when(transacaoRepository.listarPorPeriodo(dataInicio, dataFim)).thenReturn(transacoes);

        ResumoFinanceiroResponse response = calcularResumoFinanceiroUseCase.executar(dataInicio, dataFim);

        assertThat(response).isNotNull();
        assertThat(response.totalGasto()).isEqualByComparingTo("700.00");
        assertThat(response.totalReceitas()).isEqualByComparingTo("5000.00");
        assertThat(response.saldo()).isEqualByComparingTo("4300.00");
        assertThat(response.quantidadeTransacoes()).isEqualTo(4);

        assertThat(response.totalPorCategoria())
                .containsEntry(CategoriaTransacao.ALIMENTACAO, new BigDecimal("500.00"))
                .containsEntry(CategoriaTransacao.TRANSPORTE, new BigDecimal("200.00"))
                .doesNotContainKey(CategoriaTransacao.SALARIO); // Salário é receita, não entra nas categorias de despesa
    }

    @Test
    @DisplayName("Deve retornar resumo zerado e seguro quando a lista de transações for vazia")
    void deveRetornarResumoZeradoQuandoListaVazia() {
        when(transacaoRepository.listarPorPeriodo(any(), any())).thenReturn(List.of());

        ResumoFinanceiroResponse response = calcularResumoFinanceiroUseCase.executar(dataInicio, dataFim);

        assertThat(response.totalGasto()).isEqualByComparingTo(BigDecimal.ZERO);
        assertThat(response.totalReceitas()).isEqualByComparingTo(BigDecimal.ZERO);
        assertThat(response.saldo()).isEqualByComparingTo(BigDecimal.ZERO);
        assertThat(response.quantidadeTransacoes()).isZero();
        assertThat(response.totalPorCategoria()).isEmpty();
    }

    @Test
    @DisplayName("Deve lançar IllegalArgumentException quando data início for posterior à data fim")
    void deveLancarExcecaoQuandoDatasInvalidas() {
        LocalDate inicioInvalido = LocalDate.of(2026, 8, 31);
        LocalDate fimInvalido = LocalDate.of(2026, 8, 1);

        assertThatThrownBy(() -> calcularResumoFinanceiroUseCase.executar(inicioInvalido, fimInvalido))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("A data de início não pode ser posterior à data de fim");
    }

    @Test
    @DisplayName("Lógica pura do método calcularResumo deve operar isoladamente")
    void deveOperarCalculoPuroIsolado() {
        List<Transacao> lista = List.of(
                new Transacao(1L, "Curso Java", new BigDecimal("120.00"), TipoTransacao.DESPESA, CategoriaTransacao.EDUCACAO, LocalDate.now())
        );

        ResumoFinanceiro resumo = calcularResumoFinanceiroUseCase.calcularResumo(lista, dataInicio, dataFim);

        assertThat(resumo.totalDespesas()).isEqualByComparingTo("120.00");
        assertThat(resumo.totalReceitas()).isEqualByComparingTo("0.00");
        assertThat(resumo.saldo()).isEqualByComparingTo("-120.00");
        assertThat(resumo.totalPorCategoria()).containsEntry(CategoriaTransacao.EDUCACAO, new BigDecimal("120.00"));
    }
}
