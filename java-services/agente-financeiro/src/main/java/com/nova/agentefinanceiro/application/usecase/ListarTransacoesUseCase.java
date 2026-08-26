package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.TransacaoResponse;
import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;

/**
 * Caso de Uso: Listar transações com suporte opcional a filtro de período.
 */
@Service
public class ListarTransacoesUseCase {

    private final TransacaoRepository transacaoRepository;

    public ListarTransacoesUseCase(TransacaoRepository transacaoRepository) {
        this.transacaoRepository = transacaoRepository;
    }

    @Transactional(readOnly = true)
    public List<TransacaoResponse> executar(LocalDate inicio, LocalDate fim) {
        List<Transacao> transacoes;

        if (inicio != null && fim != null) {
            transacoes = transacaoRepository.listarPorPeriodo(inicio, fim);
        } else {
            transacoes = transacaoRepository.listarTodas();
        }

        return transacoes.stream()
                .map(TransacaoResponse::fromDomain)
                .toList();
    }
}
