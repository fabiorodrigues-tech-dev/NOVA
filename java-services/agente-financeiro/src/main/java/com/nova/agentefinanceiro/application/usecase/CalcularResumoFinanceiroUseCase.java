package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.ResumoFinanceiroResponse;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.ResumoFinanceiro;
import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.temporal.TemporalAdjusters;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Caso de Uso: Calcular resumo financeiro consolidado por período e por categoria.
 */
@Service
public class CalcularResumoFinanceiroUseCase {

    private final TransacaoRepository transacaoRepository;

    public CalcularResumoFinanceiroUseCase(TransacaoRepository transacaoRepository) {
        this.transacaoRepository = transacaoRepository;
    }

    @Transactional(readOnly = true)
    public ResumoFinanceiroResponse executar(LocalDate inicio, LocalDate fim) {
        LocalDate dataInicio = inicio != null
                ? inicio
                : LocalDate.now().with(TemporalAdjusters.firstDayOfMonth());

        LocalDate dataFim = fim != null
                ? fim
                : LocalDate.now().with(TemporalAdjusters.lastDayOfMonth());

        if (dataInicio.isAfter(dataFim)) {
            throw new IllegalArgumentException("A data de início não pode ser posterior à data de fim.");
        }

        List<Transacao> transacoesNoPeriodo = transacaoRepository.listarPorPeriodo(dataInicio, dataFim);

        ResumoFinanceiro resumo = calcularResumo(transacoesNoPeriodo, dataInicio, dataFim);
        return ResumoFinanceiroResponse.fromDomain(resumo);
    }

    /**
     * Lógica pura de cálculo a partir de uma coleção de transações.
     */
    public ResumoFinanceiro calcularResumo(List<Transacao> transacoes, LocalDate inicio, LocalDate fim) {
        if (transacoes == null || transacoes.isEmpty()) {
            return new ResumoFinanceiro(
                    BigDecimal.ZERO,
                    BigDecimal.ZERO,
                    BigDecimal.ZERO,
                    0,
                    inicio,
                    fim,
                    Map.of()
            );
        }

        BigDecimal totalDespesas = transacoes.stream()
                .filter(Transacao::isDespesa)
                .map(Transacao::getValor)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        BigDecimal totalReceitas = transacoes.stream()
                .filter(Transacao::isReceita)
                .map(Transacao::getValor)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        BigDecimal saldo = totalReceitas.subtract(totalDespesas);

        // Agrupamento de gastos (despesas) por categoria
        Map<CategoriaTransacao, BigDecimal> totalPorCategoria = transacoes.stream()
                .filter(Transacao::isDespesa)
                .collect(Collectors.groupingBy(
                        Transacao::getCategoria,
                        () -> new EnumMap<>(CategoriaTransacao.class),
                        Collectors.reducing(BigDecimal.ZERO, Transacao::getValor, BigDecimal::add)
                ));

        return new ResumoFinanceiro(
                totalDespesas,
                totalReceitas,
                saldo,
                transacoes.size(),
                inicio,
                fim,
                totalPorCategoria
        );
    }
}
