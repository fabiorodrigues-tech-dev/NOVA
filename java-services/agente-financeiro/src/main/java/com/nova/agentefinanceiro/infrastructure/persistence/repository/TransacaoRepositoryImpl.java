package com.nova.agentefinanceiro.infrastructure.persistence.repository;

import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import com.nova.agentefinanceiro.infrastructure.persistence.entity.TransacaoJpaEntity;
import com.nova.agentefinanceiro.infrastructure.persistence.mapper.TransacaoMapper;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

/**
 * Adaptador de persistência (Secondary Adapter) que implementa a porta TransacaoRepository.
 */
@Repository
public class TransacaoRepositoryImpl implements TransacaoRepository {

    private final SpringDataTransacaoRepository springDataRepository;
    private final TransacaoMapper mapper;

    public TransacaoRepositoryImpl(SpringDataTransacaoRepository springDataRepository, TransacaoMapper mapper) {
        this.springDataRepository = springDataRepository;
        this.mapper = mapper;
    }

    @Override
    public Transacao salvar(Transacao transacao) {
        TransacaoJpaEntity entity = mapper.toEntity(transacao);
        TransacaoJpaEntity salva = springDataRepository.save(entity);
        return mapper.toDomain(salva);
    }

    @Override
    public List<Transacao> listarTodas() {
        return springDataRepository.findAllByOrderByDataDesc().stream()
                .map(mapper::toDomain)
                .toList();
    }

    @Override
    public List<Transacao> listarPorPeriodo(LocalDate inicio, LocalDate fim) {
        return springDataRepository.findByDataBetweenOrderByDataDesc(inicio, fim).stream()
                .map(mapper::toDomain)
                .toList();
    }

    @Override
    public Optional<Transacao> buscarPorId(Long id) {
        return springDataRepository.findById(id)
                .map(mapper::toDomain);
    }

    @Override
    public boolean existe(LocalDate data, java.math.BigDecimal valor, String descricao) {
        return springDataRepository.existsByDataAndValorAndDescricao(data, valor, descricao);
    }
}
