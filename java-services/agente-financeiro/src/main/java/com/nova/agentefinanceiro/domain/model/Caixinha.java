package com.nova.agentefinanceiro.domain.model;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Objects;

/**
 * Entidade de Domínio representando uma Caixinha / Fundo de Investimento (Nubank).
 */
public class Caixinha {

    private Long id;
    private String nome;
    private BigDecimal saldo;
    private TipoCaixinha tipo;
    private BigDecimal rendimentoMensalEstimado;
    private LocalDate dataAtualizacao;

    public Caixinha(Long id, String nome, BigDecimal saldo, TipoCaixinha tipo, BigDecimal rendimentoMensalEstimado, LocalDate dataAtualizacao) {
        if (nome == null || nome.isBlank()) {
            throw new IllegalArgumentException("O nome da caixinha não pode ser vazio.");
        }
        if (saldo == null || saldo.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("O saldo da caixinha não pode ser nulo ou negativo.");
        }
        this.id = id;
        this.nome = nome.trim();
        this.saldo = saldo;
        this.tipo = (tipo != null) ? tipo : TipoCaixinha.METAS;
        this.rendimentoMensalEstimado = (rendimentoMensalEstimado != null) ? rendimentoMensalEstimado : BigDecimal.ZERO;
        this.dataAtualizacao = (dataAtualizacao != null) ? dataAtualizacao : LocalDate.now();
    }

    public Caixinha(String nome, BigDecimal saldo, TipoCaixinha tipo, BigDecimal rendimentoMensalEstimado) {
        this(null, nome, saldo, tipo, rendimentoMensalEstimado, LocalDate.now());
    }

    public Long getId() {
        return id;
    }

    public String getNome() {
        return nome;
    }

    public BigDecimal getSaldo() {
        return saldo;
    }

    public TipoCaixinha getTipo() {
        return tipo;
    }

    public BigDecimal getRendimentoMensalEstimado() {
        return rendimentoMensalEstimado;
    }

    public LocalDate getDataAtualizacao() {
        return dataAtualizacao;
    }

    public void atualizarSaldo(BigDecimal novoSaldo) {
        if (novoSaldo == null || novoSaldo.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("O saldo da caixinha não pode ser nulo ou negativo.");
        }
        this.saldo = novoSaldo;
        this.dataAtualizacao = LocalDate.now();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Caixinha caixinha = (Caixinha) o;
        return Objects.equals(id, caixinha.id) || (Objects.equals(nome, caixinha.nome) && tipo == caixinha.tipo);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, nome, tipo);
    }
}
