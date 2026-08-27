package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.CaixinhaResponse;
import com.nova.agentefinanceiro.application.dto.PatrimonioLiquidoResponse;
import com.nova.agentefinanceiro.application.dto.ResumoFinanceiroResponse;
import com.nova.agentefinanceiro.domain.model.Caixinha;
import com.nova.agentefinanceiro.domain.repository.CaixinhaRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Caso de Uso para listar todas as Caixinhas e calcular o Patrimônio Líquido Total.
 */
@Service
public class ListarCaixinhasUseCase {

    private final CaixinhaRepository caixinhaRepository;
    private final CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase;

    public ListarCaixinhasUseCase(
            CaixinhaRepository caixinhaRepository,
            CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase
    ) {
        this.caixinhaRepository = caixinhaRepository;
        this.calcularResumoFinanceiroUseCase = calcularResumoFinanceiroUseCase;
    }

    public PatrimonioLiquidoResponse executar() {
        List<Caixinha> caixinhas = caixinhaRepository.listarTodas();

        BigDecimal totalCaixinhas = caixinhas.stream()
                .map(Caixinha::getSaldo)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        ResumoFinanceiroResponse resumo = calcularResumoFinanceiroUseCase.executar(null, null);
        BigDecimal saldoConta = (resumo != null && resumo.saldo() != null) ? resumo.saldo() : BigDecimal.ZERO;

        BigDecimal patrimonioLiquidoTotal = saldoConta.add(totalCaixinhas);

        List<CaixinhaResponse> responses = caixinhas.stream()
                .map(CaixinhaResponse::deDominio)
                .collect(Collectors.toList());

        return new PatrimonioLiquidoResponse(
                saldoConta,
                totalCaixinhas,
                patrimonioLiquidoTotal,
                responses
        );
    }
}
