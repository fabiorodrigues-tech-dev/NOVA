package com.nova.agentefinanceiro.infrastructure.persistence.repository;

import com.nova.agentefinanceiro.domain.model.TipoCaixinha;
import com.nova.agentefinanceiro.infrastructure.persistence.entity.CaixinhaJpaEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * Interface Spring Data JPA para acesso à tabela tb_caixinhas.
 */
@Repository
public interface SpringDataCaixinhaRepository extends JpaRepository<CaixinhaJpaEntity, Long> {

    Optional<CaixinhaJpaEntity> findByTipo(TipoCaixinha tipo);

    Optional<CaixinhaJpaEntity> findByNomeIgnoreCase(String nome);
}
