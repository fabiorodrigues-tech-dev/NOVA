package com.nova.agentefinanceiro.infrastructure.persistence.mapper;

import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.infrastructure.persistence.entity.TransacaoJpaEntity;
import org.springframework.stereotype.Component;

/**
 * Mapper responsável pela conversão entre a Entidade de Domínio e a Entidade JPA.
 */
@Component
public class TransacaoMapper {

    public Transacao toDomain(TransacaoJpaEntity entity) {
        if (entity == null) {
            return null;
        }

        return new Transacao(
                entity.getId(),
                entity.getDescricao(),
                entity.getValor(),
                entity.getTipo(),
                entity.getCategoria(),
                entity.getData()
        );
    }

    public TransacaoJpaEntity toEntity(Transacao domain) {
        if (domain == null) {
            return null;
        }

        return new TransacaoJpaEntity(
                domain.getId(),
                domain.getDescricao(),
                domain.getValor(),
                domain.getTipo(),
                domain.getCategoria(),
                domain.getData()
        );
    }
}
