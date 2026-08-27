package com.nova.agentefinanceiro.domain.repository;

import com.nova.agentefinanceiro.domain.model.Caixinha;
import com.nova.agentefinanceiro.domain.model.TipoCaixinha;

import java.util.List;
import java.util.Optional;

/**
 * Contrato de repositório de domínio para persistência de Caixinhas e Investimentos.
 */
public interface CaixinhaRepository {

    Caixinha salvar(Caixinha caixinha);

    Optional<Caixinha> buscarPorId(Long id);

    Optional<Caixinha> buscarPorTipo(TipoCaixinha tipo);

    Optional<Caixinha> buscarPorNome(String nome);

    List<Caixinha> listarTodas();
}
