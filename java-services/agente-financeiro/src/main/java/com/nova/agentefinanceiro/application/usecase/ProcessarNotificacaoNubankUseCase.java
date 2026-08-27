package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.TransacaoRequest;
import com.nova.agentefinanceiro.application.dto.TransacaoResponse;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Caso de Uso para processar notificações push do Nubank via Webhook.
 * Extrai valores, tipo, estabelecimento e categoria, realizando cadastro e deduplicação no banco H2.
 */
@Service
public class ProcessarNotificacaoNubankUseCase {

    private final CadastrarTransacaoUseCase cadastrarTransacaoUseCase;
    private final TransacaoRepository transacaoRepository;

    private static final Pattern VALOR_PATTERN = Pattern.compile("R\\$\\s*([\\d\\.]+([.,]\\d{2}))");

    public ProcessarNotificacaoNubankUseCase(
            CadastrarTransacaoUseCase cadastrarTransacaoUseCase,
            TransacaoRepository transacaoRepository
    ) {
        this.cadastrarTransacaoUseCase = cadastrarTransacaoUseCase;
        this.transacaoRepository = transacaoRepository;
    }

    public TransacaoResponse executar(String textoNotificacao) {
        if (textoNotificacao == null || textoNotificacao.isBlank()) {
            throw new IllegalArgumentException("O texto da notificação não pode ser vazio.");
        }

        String texto = textoNotificacao.trim();
        String textoLower = texto.toLowerCase();

        // 1. Extração do Valor Monetário
        BigDecimal valor = extrairValor(texto);

        // 2. Determinação de Tipo (Receita vs Despesa)
        TipoTransacao tipo = TipoTransacao.DESPESA;
        if (textoLower.contains("recebeu") || textoLower.contains("recebida") || textoLower.contains("depósito") || textoLower.contains("reembolso")) {
            tipo = TipoTransacao.RECEITA;
        }

        // 3. Extração da Descrição / Estabelecimento
        String descricao = extrairDescricao(texto, textoLower);

        // 4. Inferência da Categoria
        CategoriaTransacao categoria = inferirCategoria(descricao, tipo);

        LocalDate data = LocalDate.now();

        // 5. Deduplicação: se já existir hoje com mesmo valor e descrição, retorna a transação existente
        if (transacaoRepository.existe(data, valor, descricao)) {
            var existentes = transacaoRepository.listarPorPeriodo(data, data);
            for (var t : existentes) {
                if (t.getValor().compareTo(valor) == 0 && t.getDescricao().equalsIgnoreCase(descricao)) {
                    return TransacaoResponse.deDominio(t);
                }
            }
        }

        TransacaoRequest request = new TransacaoRequest(
                descricao,
                valor,
                tipo,
                categoria,
                data
        );

        return cadastrarTransacaoUseCase.executar(request);
    }

    private BigDecimal extrairValor(String texto) {
        Matcher m = VALOR_PATTERN.matcher(texto);
        if (m.find()) {
            String valStr = m.group(1).replace(".", "").replace(",", ".");
            return new BigDecimal(valStr);
        }
        // Fallback para qualquer número no texto
        Pattern fallbackPattern = Pattern.compile("(\\d+([.,]\\d{1,2})?)");
        Matcher fm = fallbackPattern.matcher(texto);
        if (fm.find()) {
            String valStr = fm.group(1).replace(",", ".");
            return new BigDecimal(valStr);
        }
        throw new IllegalArgumentException("Não foi possível identificar o valor monetário na notificação.");
    }

    private String extrairDescricao(String texto, String textoLower) {
        // Ex: "Compra de R$ 45,90 no Restaurante Fogão de Lenha aprovada"
        if (textoLower.contains(" no ") && textoLower.contains(" aprovad")) {
            int start = textoLower.indexOf(" no ") + 4;
            int end = textoLower.indexOf(" aprovad");
            if (end > start) return texto.substring(start, end).trim();
        }
        if (textoLower.contains(" na ") && textoLower.contains(" aprovad")) {
            int start = textoLower.indexOf(" na ") + 4;
            int end = textoLower.indexOf(" aprovad");
            if (end > start) return texto.substring(start, end).trim();
        }
        if (textoLower.contains(" em ") && textoLower.contains(" aprovad")) {
            int start = textoLower.indexOf(" em ") + 4;
            int end = textoLower.indexOf(" aprovad");
            if (end > start) return texto.substring(start, end).trim();
        }
        // Ex: "Você transferiu R$ 150,00 para João da Silva"
        if (textoLower.contains("para ")) {
            int start = textoLower.indexOf("para ") + 5;
            return "Transferência para " + texto.substring(start).trim();
        }
        // Ex: "Você recebeu uma transferência de R$ 500,00 de Maria Souza"
        if (textoLower.contains(" de ") && (textoLower.contains("recebeu") || textoLower.contains("transferência"))) {
            int lastDe = textoLower.lastIndexOf(" de ") + 4;
            return "Transferência de " + texto.substring(lastDe).trim();
        }
        return "Transação Nubank: " + texto;
    }

    private CategoriaTransacao inferirCategoria(String descricao, TipoTransacao tipo) {
        if (tipo == TipoTransacao.RECEITA) {
            return CategoriaTransacao.SALARIO;
        }
        String d = descricao.toLowerCase();
        if (d.contains("restaurante") || d.contains("almoço") || d.contains("lanche") || d.contains("mercado") ||
                d.contains("supermercado") || d.contains("ifood") || d.contains("padaria") || d.contains("açougue") ||
                d.contains("café") || d.contains("comida") || d.contains("gildo")) {
            return CategoriaTransacao.ALIMENTACAO;
        }
        if (d.contains("uber") || d.contains("99") || d.contains("combustivel") || d.contains("gasolina") ||
                d.contains("posto") || d.contains("estacionamento") || d.contains("passagem") || d.contains("metro")) {
            return CategoriaTransacao.TRANSPORTE;
        }
        if (d.contains("farmacia") || d.contains("drogaria") || d.contains("medico") || d.contains("consulta") ||
                d.contains("hospital") || d.contains("remedio") || d.contains("dentista")) {
            return CategoriaTransacao.SAUDE;
        }
        if (d.contains("aluguel") || d.contains("condominio") || d.contains("energia") || d.contains("celpe") ||
                d.contains("neoenergia") || d.contains("compesa") || d.contains("agua") || d.contains("internet") ||
                d.contains("claro") || d.contains("vivo")) {
            return CategoriaTransacao.MORADIA;
        }
        if (d.contains("curso") || d.contains("dio") || d.contains("livro") || d.contains("faculdade") || d.contains("udemy")) {
            return CategoriaTransacao.EDUCACAO;
        }
        if (d.contains("cinema") || d.contains("show") || d.contains("jogo") || d.contains("steam") || d.contains("netflix") || d.contains("spotify")) {
            return CategoriaTransacao.LAZER;
        }
        if (d.contains("transferência") || d.contains("pix")) {
            return CategoriaTransacao.OUTROS;
        }
        return CategoriaTransacao.COMPRAS;
    }
}
