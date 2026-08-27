package com.nova.agentefinanceiro.infrastructure.persistence.repository;

import com.nova.agentefinanceiro.infrastructure.persistence.entity.TransacaoJpaEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

/**
 * Interface Spring Data JPA para acesso direto ao banco de dados.
 */
@Repository
public interface SpringDataTransacaoRepository extends JpaRepository<TransacaoJpaEntity, Long> {

    List<TransacaoJpaEntity> findByDataBetweenOrderByDataDesc(LocalDate inicio, LocalDate fim);

    List<TransacaoJpaEntity> findAllByOrderByDataDesc();

    boolean existsByDataAndValorAndDescricao(LocalDate data, java.math.BigDecimal valor, String descricao);
}
