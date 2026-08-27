package com.nova.agentefinanceiro.infrastructure.persistence.repository;

import com.nova.agentefinanceiro.domain.model.Caixinha;
import com.nova.agentefinanceiro.domain.model.TipoCaixinha;
import com.nova.agentefinanceiro.domain.repository.CaixinhaRepository;
import com.nova.agentefinanceiro.infrastructure.persistence.entity.CaixinhaJpaEntity;
import com.nova.agentefinanceiro.infrastructure.persistence.mapper.CaixinhaMapper;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Implementação do repositório de domínio CaixinhaRepository utilizando Spring Data JPA.
 */
@Repository
public class CaixinhaRepositoryImpl implements CaixinhaRepository {

    private final SpringDataCaixinhaRepository jpaRepository;
    private final CaixinhaMapper mapper;

    public CaixinhaRepositoryImpl(SpringDataCaixinhaRepository jpaRepository, CaixinhaMapper mapper) {
        this.jpaRepository = jpaRepository;
        this.mapper = mapper;
    }

    @Override
    public Caixinha salvar(Caixinha caixinha) {
        CaixinhaJpaEntity entity = mapper.toEntity(caixinha);
        CaixinhaJpaEntity salva = jpaRepository.save(entity);
        return mapper.toDomain(salva);
    }

    @Override
    public Optional<Caixinha> buscarPorId(Long id) {
        return jpaRepository.findById(id).map(mapper::toDomain);
    }

    @Override
    public Optional<Caixinha> buscarPorTipo(TipoCaixinha tipo) {
        return jpaRepository.findByTipo(tipo).map(mapper::toDomain);
    }

    @Override
    public Optional<Caixinha> buscarPorNome(String nome) {
        return jpaRepository.findByNomeIgnoreCase(nome).map(mapper::toDomain);
    }

    @Override
    public List<Caixinha> listarTodas() {
        return jpaRepository.findAll().stream()
                .map(mapper::toDomain)
                .collect(Collectors.toList());
    }
}
