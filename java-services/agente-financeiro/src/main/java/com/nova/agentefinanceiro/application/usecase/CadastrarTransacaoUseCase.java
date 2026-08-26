package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.TransacaoRequest;
import com.nova.agentefinanceiro.application.dto.TransacaoResponse;
import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Caso de Uso: Cadastrar uma nova transação financeira.
 */
@Service
public class CadastrarTransacaoUseCase {

    private final TransacaoRepository transacaoRepository;

    public CadastrarTransacaoUseCase(TransacaoRepository transacaoRepository) {
        this.transacaoRepository = transacaoRepository;
    }

    @Transactional
    public TransacaoResponse executar(TransacaoRequest request) {
        Transacao novaTransacao = new Transacao(
                null,
                request.descricao(),
                request.valor(),
                request.tipo(),
                request.categoria(),
                request.data()
        );

        Transacao transacaoSalva = transacaoRepository.salvar(novaTransacao);
        return TransacaoResponse.fromDomain(transacaoSalva);
    }
}
