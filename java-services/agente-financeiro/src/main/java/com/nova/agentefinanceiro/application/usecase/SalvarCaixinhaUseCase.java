package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.CaixinhaRequest;
import com.nova.agentefinanceiro.application.dto.CaixinhaResponse;
import com.nova.agentefinanceiro.domain.model.Caixinha;
import com.nova.agentefinanceiro.domain.model.TipoCaixinha;
import com.nova.agentefinanceiro.domain.repository.CaixinhaRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.Optional;

/**
 * Caso de Uso para salvar ou atualizar saldos de Caixinhas e Fundos de Investimento Nubank.
 */
@Service
public class SalvarCaixinhaUseCase {

    private final CaixinhaRepository caixinhaRepository;

    public SalvarCaixinhaUseCase(CaixinhaRepository caixinhaRepository) {
        this.caixinhaRepository = caixinhaRepository;
    }

    public CaixinhaResponse executar(CaixinhaRequest request) {
        if (request == null) {
            throw new IllegalArgumentException("O payload da caixinha não pode ser nulo.");
        }

        TipoCaixinha tipo = (request.tipo() != null) ? request.tipo() : inferirTipoPorNome(request.nome());

        Optional<Caixinha> existente = caixinhaRepository.buscarPorNome(request.nome());
        if (existente.isEmpty() && tipo != TipoCaixinha.OUTROS) {
            existente = caixinhaRepository.buscarPorTipo(tipo);
        }

        Caixinha caixinha;
        if (existente.isPresent()) {
            caixinha = existente.get();
            caixinha.atualizarSaldo(request.saldo());
        } else {
            caixinha = new Caixinha(
                    request.nome(),
                    request.saldo(),
                    tipo,
                    request.rendimentoMensalEstimado() != null ? request.rendimentoMensalEstimado() : BigDecimal.ZERO
            );
        }

        Caixinha salva = caixinhaRepository.salvar(caixinha);
        return CaixinhaResponse.deDominio(salva);
    }

    private TipoCaixinha inferirTipoPorNome(String nome) {
        if (nome == null) return TipoCaixinha.METAS;
        String n = nome.toLowerCase();
        if (n.contains("emergencia") || n.contains("emergência") || n.contains("reserva")) {
            return TipoCaixinha.RESERVA_EMERGENCIA;
        }
        if (n.contains("casal") || n.contains("fundo casal") || n.contains("nós") || n.contains("juntos")) {
            return TipoCaixinha.FUNDO_CASAL;
        }
        return TipoCaixinha.METAS;
    }
}
