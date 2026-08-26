package com.nova.agentefinanceiro.domain.model;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Objects;

/**
 * Entidade de Domínio representando uma Transação Financeira (Gasto ou Receita).
 * Agnóstica de frameworks e tecnologias de persistência.
 */
public class Transacao {

    private final Long id;
    private final String descricao;
    private final BigDecimal valor;
    private final TipoTransacao tipo;
    private final CategoriaTransacao categoria;
    private final LocalDate data;

    public Transacao(Long id, String descricao, BigDecimal valor, TipoTransacao tipo, CategoriaTransacao categoria, LocalDate data) {
        this.id = id;
        this.descricao = validarDescricao(descricao);
        this.valor = validarValor(valor);
        this.tipo = Objects.requireNonNullElse(tipo, TipoTransacao.DESPESA);
        this.categoria = Objects.requireNonNullElse(categoria, CategoriaTransacao.OUTROS);
        this.data = Objects.requireNonNullElseGet(data, LocalDate::now);
    }

    private static String validarDescricao(String descricao) {
        if (descricao == null || descricao.isBlank()) {
            throw new IllegalArgumentException("A descrição da transação é obrigatória.");
        }
        return descricao.trim();
    }

    private static BigDecimal validarValor(BigDecimal valor) {
        if (valor == null || valor.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("O valor da transação deve ser positivo.");
        }
        return valor;
    }

    public Long getId() {
        return id;
    }

    public String getDescricao() {
        return descricao;
    }

    public BigDecimal getValor() {
        return valor;
    }

    public TipoTransacao getTipo() {
        return tipo;
    }

    public CategoriaTransacao getCategoria() {
        return categoria;
    }

    public LocalDate getData() {
        return data;
    }

    public boolean isDespesa() {
        return this.tipo == TipoTransacao.DESPESA;
    }

    public boolean isReceita() {
        return this.tipo == TipoTransacao.RECEITA;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Transacao that)) return false;
        return Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
