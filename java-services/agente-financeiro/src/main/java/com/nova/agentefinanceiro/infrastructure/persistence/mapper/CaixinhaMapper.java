package com.nova.agentefinanceiro.infrastructure.persistence.mapper;

import com.nova.agentefinanceiro.domain.model.Caixinha;
import com.nova.agentefinanceiro.infrastructure.persistence.entity.CaixinhaJpaEntity;
import org.springframework.stereotype.Component;

/**
 * Mapper responsável pela conversão entre a Entidade de Domínio Caixinha e a Entidade JPA.
 */
@Component
public class CaixinhaMapper {

    public Caixinha toDomain(CaixinhaJpaEntity entity) {
        if (entity == null) {
            return null;
        }

        return new Caixinha(
                entity.getId(),
                entity.getNome(),
                entity.getSaldo(),
                entity.getTipo(),
                entity.getRendimentoMensalEstimado(),
                entity.getDataAtualizacao()
        );
    }

    public CaixinhaJpaEntity toEntity(Caixinha domain) {
        if (domain == null) {
            return null;
        }

        return new CaixinhaJpaEntity(
                domain.getId(),
                domain.getNome(),
                domain.getSaldo(),
                domain.getTipo(),
                domain.getRendimentoMensalEstimado(),
                domain.getDataAtualizacao()
        );
    }
}
