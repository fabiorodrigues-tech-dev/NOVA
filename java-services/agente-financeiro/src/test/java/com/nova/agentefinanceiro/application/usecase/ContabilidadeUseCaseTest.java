package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.BalanceteResponse;
import com.nova.agentefinanceiro.application.dto.BalancoPatrimonialResponse;
import com.nova.agentefinanceiro.application.dto.ComparativoMesesResponse;
import com.nova.agentefinanceiro.application.dto.HistoricoAnualResponse;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.domain.repository.CaixinhaRepository;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
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
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ContabilidadeUseCaseTest {

    @Mock
    private TransacaoRepository transacaoRepository;

    @Mock
    private CaixinhaRepository caixinhaRepository;

    @InjectMocks
    private ContabilidadeUseCase contabilidadeUseCase;

    @Test
    @DisplayName("Deve gerar Balancete de Verificação consistente com créditos, débitos e saldo final")
    void deveGerarBalanceteConsistente() {
        LocalDate inicio = LocalDate.of(2026, 8, 1);
        LocalDate fim = LocalDate.of(2026, 8, 31);

        List<Transacao> doMes = List.of(
                new Transacao(1L, "Salário", new BigDecimal("3000.00"), TipoTransacao.RECEITA, CategoriaTransacao.SALARIO, inicio.plusDays(4)),
                new Transacao(2L, "Aluguel", new BigDecimal("1200.00"), TipoTransacao.DESPESA, CategoriaTransacao.MORADIA, inicio.plusDays(5)),
                new Transacao(3L, "Supermercado", new BigDecimal("500.00"), TipoTransacao.DESPESA, CategoriaTransacao.ALIMENTACAO, inicio.plusDays(10))
        );

        when(transacaoRepository.listarPorPeriodo(LocalDate.of(2020, 1, 1), inicio.minusDays(1)))
                .thenReturn(List.of(new Transacao(0L, "Abertura", new BigDecimal("100.00"), TipoTransacao.RECEITA, CategoriaTransacao.OUTROS, LocalDate.of(2026, 7, 1))));
        when(transacaoRepository.listarPorPeriodo(inicio, fim)).thenReturn(doMes);

        BalanceteResponse resp = contabilidadeUseCase.gerarBalancete("2026-08");

        assertThat(resp).isNotNull();
        assertThat(resp.saldoInicial()).isEqualByComparingTo("100.00");
        assertThat(resp.totalCreditos()).isEqualByComparingTo("3000.00");
        assertThat(resp.totalDebitos()).isEqualByComparingTo("1700.00");
        assertThat(resp.saldoFinal()).isEqualByComparingTo("1400.00");
        assertThat(resp.consistente()).isTrue();
        assertThat(resp.statusContabil()).isEqualTo("EQUILIBRADO_CONCILIADO");
        assertThat(resp.hashAutenticidade()).isNotBlank();
    }

    @Test
    @DisplayName("Deve gerar Balanço Patrimonial & DRE com ativos, passivos e patrimônio líquido")
    void deveGerarBalancoPatrimonial() {
        BalancoPatrimonialResponse resp = contabilidadeUseCase.gerarBalancoPatrimonial();

        assertThat(resp).isNotNull();
        assertThat(resp.totalAtivo()).isGreaterThan(BigDecimal.ZERO);
        assertThat(resp.patrimonioLiquidoTotal()).isGreaterThan(BigDecimal.ZERO);
        assertThat(resp.situacaoPatrimonial()).contains("SUPERAVITARIA");
        assertThat(resp.hashAutenticidade()).isNotBlank();
    }

    @Test
    @DisplayName("Deve gerar Comparativo Horizontal entre meses calculando variações absolutas e relativas")
    void deveGerarComparativoEntreMeses() {
        List<Transacao> tJulho = List.of(
                new Transacao(1L, "Freelance", new BigDecimal("2000.00"), TipoTransacao.RECEITA, CategoriaTransacao.SERVICOS, LocalDate.of(2026, 7, 10)),
                new Transacao(2L, "Mercado", new BigDecimal("400.00"), TipoTransacao.DESPESA, CategoriaTransacao.ALIMENTACAO, LocalDate.of(2026, 7, 12))
        );
        List<Transacao> tAgosto = List.of(
                new Transacao(3L, "Freelance", new BigDecimal("3000.00"), TipoTransacao.RECEITA, CategoriaTransacao.SERVICOS, LocalDate.of(2026, 8, 10)),
                new Transacao(4L, "Mercado", new BigDecimal("600.00"), TipoTransacao.DESPESA, CategoriaTransacao.ALIMENTACAO, LocalDate.of(2026, 8, 12))
        );

        when(transacaoRepository.listarPorPeriodo(LocalDate.of(2026, 7, 1), LocalDate.of(2026, 7, 31))).thenReturn(tJulho);
        when(transacaoRepository.listarPorPeriodo(LocalDate.of(2026, 8, 1), LocalDate.of(2026, 8, 31))).thenReturn(tAgosto);

        ComparativoMesesResponse resp = contabilidadeUseCase.gerarComparativo("2026-07", "2026-08");

        assertThat(resp).isNotNull();
        assertThat(resp.receitasMes1()).isEqualByComparingTo("2000.00");
        assertThat(resp.receitasMes2()).isEqualByComparingTo("3000.00");
        assertThat(resp.variacaoReceitasAbsoluta()).isEqualByComparingTo("1000.00");
        assertThat(resp.variacaoReceitasPercentual()).isEqualByComparingTo("50.00");
        assertThat(resp.despesasMes1()).isEqualByComparingTo("400.00");
        assertThat(resp.despesasMes2()).isEqualByComparingTo("600.00");
        assertThat(resp.diagnosticoContabil()).isNotBlank();
    }

    @Test
    @DisplayName("Deve gerar Histórico Anual Consolidado para 2026")
    void deveGerarHistoricoAnual() {
        when(transacaoRepository.listarPorPeriodo(any(LocalDate.class), any(LocalDate.class))).thenReturn(List.of());

        HistoricoAnualResponse resp = contabilidadeUseCase.gerarHistoricoAnual(2026);

        assertThat(resp).isNotNull();
        assertThat(resp.ano()).isEqualTo(2026);
        assertThat(resp.meses()).hasSize(12);
    }
}
