package com.nova.agentefinanceiro.infrastructure.persistence.entity;

import com.nova.agentefinanceiro.domain.model.TipoCaixinha;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Entidade JPA para persistência de Caixinhas e Investimentos na tabela tb_caixinhas.
 */
@Entity
@Table(name = "tb_caixinhas")
public class CaixinhaJpaEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 150)
    private String nome;

    @Column(nullable = false, precision = 15, scale = 2)
    private BigDecimal saldo;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 50, columnDefinition = "varchar(50)")
    private TipoCaixinha tipo;

    @Column(nullable = false, precision = 15, scale = 2)
    private BigDecimal rendimentoMensalEstimado;

    @Column(nullable = false)
    private LocalDate dataAtualizacao;

    @Column(nullable = false, updatable = false)
    private LocalDateTime criadoEm;

    public CaixinhaJpaEntity() {
        this.criadoEm = LocalDateTime.now();
    }

    public CaixinhaJpaEntity(Long id, String nome, BigDecimal saldo, TipoCaixinha tipo, BigDecimal rendimentoMensalEstimado, LocalDate dataAtualizacao) {
        this.id = id;
        this.nome = nome;
        this.saldo = saldo;
        this.tipo = tipo;
        this.rendimentoMensalEstimado = (rendimentoMensalEstimado != null) ? rendimentoMensalEstimado : BigDecimal.ZERO;
        this.dataAtualizacao = (dataAtualizacao != null) ? dataAtualizacao : LocalDate.now();
        this.criadoEm = LocalDateTime.now();
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public BigDecimal getSaldo() {
        return saldo;
    }

    public void setSaldo(BigDecimal saldo) {
        this.saldo = saldo;
    }

    public TipoCaixinha getTipo() {
        return tipo;
    }

    public void setTipo(TipoCaixinha tipo) {
        this.tipo = tipo;
    }

    public BigDecimal getRendimentoMensalEstimado() {
        return rendimentoMensalEstimado;
    }

    public void setRendimentoMensalEstimado(BigDecimal rendimentoMensalEstimado) {
        this.rendimentoMensalEstimado = rendimentoMensalEstimado;
    }

    public LocalDate getDataAtualizacao() {
        return dataAtualizacao;
    }

    public void setDataAtualizacao(LocalDate dataAtualizacao) {
        this.dataAtualizacao = dataAtualizacao;
    }

    public LocalDateTime getCriadoEm() {
        return criadoEm;
    }
}
