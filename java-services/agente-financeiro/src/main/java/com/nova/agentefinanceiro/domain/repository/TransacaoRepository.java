package com.nova.agentefinanceiro.domain.repository;

import com.nova.agentefinanceiro.domain.model.Transacao;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

/**
 * Porta de saída (Output Port) para operações de persistência de Transacao.
 * Definida no domínio, implementada na infraestrutura.
 */
public interface TransacaoRepository {

    Transacao salvar(Transacao transacao);

    List<Transacao> listarTodas();

    List<Transacao> listarPorPeriodo(LocalDate inicio, LocalDate fim);

    Optional<Transacao> buscarPorId(Long id);
}
