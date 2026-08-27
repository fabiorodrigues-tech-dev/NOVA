package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.ProjecaoFinanceiraResponse;
import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.YearMonth;
import java.util.ArrayList;
import java.util.List;

/**
 * Caso de Uso para Inteligência Preditiva & Consultoria Financeira (Fase 9).
 * Estima o burn rate diário, projeta o saldo ao fim do mês e emite alertas de proteção orçamentária.
 */
@Service
public class CalcularProjecaoFinanceiraUseCase {

    private final TransacaoRepository transacaoRepository;

    public CalcularProjecaoFinanceiraUseCase(TransacaoRepository transacaoRepository) {
        this.transacaoRepository = transacaoRepository;
    }

    public ProjecaoFinanceiraResponse executar(LocalDate dataRef) {
        LocalDate hoje = (dataRef != null) ? dataRef : LocalDate.now();
        YearMonth ym = YearMonth.from(hoje);
        LocalDate inicioMes = ym.atDay(1);
        LocalDate fimMes = ym.atEndOfMonth();

        int totalDiasMes = ym.lengthOfMonth();
        int diaAtual = hoje.getDayOfMonth();
        int diasDecorridos = Math.max(1, diaAtual);
        int diasRestantes = Math.max(0, totalDiasMes - diaAtual);

        List<Transacao> transacoes = transacaoRepository.listarPorPeriodo(inicioMes, fimMes);

        BigDecimal totalGastos = BigDecimal.ZERO;
        BigDecimal totalReceitas = BigDecimal.ZERO;

        for (Transacao t : transacoes) {
            // Considera apenas transações ocorridas até a data de referência para cálculo de histórico
            if (!t.getData().isAfter(hoje)) {
                if (t.isDespesa()) {
                    totalGastos = totalGastos.add(t.getValor());
                } else if (t.isReceita()) {
                    totalReceitas = totalReceitas.add(t.getValor());
                }
            }
        }

        BigDecimal saldoAtual = totalReceitas.subtract(totalGastos);

        // Burn rate diário médio (Gastos / Dias Decorridos)
        BigDecimal burnRateDiario = totalGastos.divide(BigDecimal.valueOf(diasDecorridos), 2, RoundingMode.HALF_UP);

        // Gasto adicional estimado para os dias restantes
        BigDecimal gastoAdicionalProjetado = burnRateDiario.multiply(BigDecimal.valueOf(diasRestantes)).setScale(2, RoundingMode.HALF_UP);

        // Gasto total estimado ao final do mês
        BigDecimal gastoTotalProjetado = totalGastos.add(gastoAdicionalProjetado).setScale(2, RoundingMode.HALF_UP);

        // Saldo final projetado
        BigDecimal saldoFinalProjetado = totalReceitas.subtract(gastoTotalProjetado).setScale(2, RoundingMode.HALF_UP);

        // Diagnóstico e Alertas Preditivos
        String status;
        List<String> alertas = new ArrayList<>();
        String recomendacao;

        if (saldoFinalProjetado.compareTo(BigDecimal.ZERO) < 0) {
            status = "CRITICO";
            alertas.add(String.format("⚠️ Risco de Déficit: No ritmo atual (R$ %.2f/dia), você gastará mais R$ %.2f até o fim do mês, resultando em saldo negativo de R$ %.2f.",
                    burnRateDiario, gastoAdicionalProjetado, saldoFinalProjetado.abs()));
            recomendacao = String.format("Reduza despesas variáveis não essenciais imediatamente. O teto diário recomendado para os próximos %d dias é de R$ %.2f/dia para zerar o balanço.",
                    diasRestantes, diasRestantes > 0 ? saldoAtual.max(BigDecimal.ZERO).divide(BigDecimal.valueOf(diasRestantes), 2, RoundingMode.HALF_UP) : BigDecimal.ZERO);
        } else {
            BigDecimal margemSeguranca = totalReceitas.multiply(BigDecimal.valueOf(0.15));
            if (saldoFinalProjetado.compareTo(margemSeguranca) < 0) {
                status = "ALERTA";
                alertas.add(String.format("⚡ Margem Apertada: Projeção de superávit modesto de R$ %.2f (abaixo de 15%% da receita total).", saldoFinalProjetado));
                recomendacao = "Mantenha cautela em novos gastos até o fechamento do mês para preservar a margem positiva.";
            } else {
                status = "SAUDAVEL";
                alertas.add(String.format("✅ Balanço Saudável: Superávit projetado de R$ %.2f ao fim do mês.", saldoFinalProjetado));
                BigDecimal aporteSugerido = saldoFinalProjetado.multiply(BigDecimal.valueOf(0.50)).setScale(2, RoundingMode.HALF_UP);
                recomendacao = String.format("Ritmo financeiro sob controle! Sugestão de aporte de R$ %.2f nas caixinhas (Reserva de Emergência e Metas do Casal).", aporteSugerido);
            }
        }

        return new ProjecaoFinanceiraResponse(
                hoje,
                diasDecorridos,
                diasRestantes,
                totalDiasMes,
                totalGastos.setScale(2, RoundingMode.HALF_UP),
                totalReceitas.setScale(2, RoundingMode.HALF_UP),
                saldoAtual.setScale(2, RoundingMode.HALF_UP),
                burnRateDiario,
                gastoAdicionalProjetado,
                gastoTotalProjetado,
                saldoFinalProjetado,
                status,
                alertas,
                recomendacao
        );
    }
}
