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
        // 1. NuPay
        if (textoLower.contains("nupay")) {
            Pattern nuPattern1 = Pattern.compile("(?i)via\\s+nupay\\s+(?:no|na|em)\\s+([^.,\\n]+?)(?:\\s+de\\s+r\\$|\\s+no\\s+valor|$)");
            Matcher m1 = nuPattern1.matcher(texto);
            if (m1.find()) {
                return m1.group(1).trim() + " (NuPay)";
            }
            Pattern nuPattern2 = Pattern.compile("(?i)(?:no|na|em)\\s+([^.,\\n]+?)(?:\\s+via\\s+nupay|\\s+no\\s+valor|\\s+de\\s+r\\$|$)");
            Matcher m2 = nuPattern2.matcher(texto);
            if (m2.find()) {
                String loja = m2.group(1).trim();
                if (!loja.equalsIgnoreCase("débito") && !loja.equalsIgnoreCase("debito") && !loja.equalsIgnoreCase("crédito") && !loja.equalsIgnoreCase("credito")) {
                    return loja + " (NuPay)";
                }
            }
            return "Compra Débito via NuPay";
        }

        // 2. Compras no/na/em [LOJA] aprovadas
        // Ex: "Compra de R$ 45,90 no Restaurante Fogão de Lenha aprovada"
        Pattern compraPattern = Pattern.compile("(?i)compra(?:\\s+de\\s+r\\$\\s*[\\d\\.,]+)?\\s+(?:no|na|em)\\s+([^.,\\n]+?)(?:\\s+aprovad|\\s+no\\s+valor|$)");
        Matcher cm = compraPattern.matcher(texto);
        if (cm.find()) {
            return cm.group(1).trim();
        }

        // 3. Pix enviado / Transferência enviada
        // Ex: "Você enviou um Pix de R$ 150,00 para João da Silva" ou "Você transferiu R$ 150,00 para João"
        Pattern pixEnvPattern = Pattern.compile("(?i)(?:enviou\\s+um\\s+pix|transferiu)(?:\\s+de\\s+r\\$\\s*[\\d\\.,]+)?\\s+para\\s+([^.,\\n]+)");
        Matcher pem = pixEnvPattern.matcher(texto);
        if (pem.find()) {
            return "Pix para " + pem.group(1).trim();
        }
        if (textoLower.contains("para ")) {
            int start = textoLower.indexOf("para ") + 5;
            return "Transferência para " + texto.substring(start).trim();
        }

        // 4. Pix recebido / Transferência recebida
        // Ex: "Você recebeu uma transferência Pix de R$ 500,00 de Maria" ou "Você recebeu um Pix de..."
        Pattern pixRecPattern = Pattern.compile("(?i)(?:recebeu\\s+(?:uma\\s+transferência(?:\\s+pix)?|um\\s+pix)|transferência\\s+recebida)(?:\\s+de\\s+r\\$\\s*[\\d\\.,]+)?\\s+de\\s+([^.,\\n]+)");
        Matcher prm = pixRecPattern.matcher(texto);
        if (prm.find()) {
            return "Transferência de " + prm.group(1).trim();
        }
        if (textoLower.contains(" de ") && (textoLower.contains("recebeu") || textoLower.contains("transferência") || textoLower.contains("transferencia"))) {
            int lastDe = textoLower.lastIndexOf(" de ") + 4;
            return "Transferência de " + texto.substring(lastDe).trim();
        }

        // 5. Pagamento de fatura
        if (textoLower.contains("fatura")) {
            return "Pagamento de Fatura Nubank";
        }

        return "Transação Nubank: " + texto;
    }

    private CategoriaTransacao inferirCategoria(String descricao, TipoTransacao tipo) {
        String d = descricao.toLowerCase();

        // 1. Investimentos (RDB, CDB, NuInvest, etc.)
        if (d.contains("aplicação rdb") || d.contains("aplicacao rdb") || d.contains("resgate rdb") ||
                d.contains(" rdb") || d.startsWith("rdb") || d.contains("investimento") || d.contains("nuinvest") ||
                d.contains("tesouro") || d.contains("b3") || d.contains("poupanca") || d.contains("poupança") ||
                d.contains("cdb") || d.contains("rendimento")) {
            return CategoriaTransacao.INVESTIMENTO;
        }

        // 2. Transferências entre pessoas físicas / Pix
        if (d.contains("iza correia") || d.contains("gildeth") || d.contains("mariana") ||
                d.contains("cleiton") || d.contains("lucas") || d.contains("cicero") ||
                d.contains("transferência") || d.contains("transferencia") || d.contains("pix")) {
            return (tipo == TipoTransacao.RECEITA) ? CategoriaTransacao.SALARIO : CategoriaTransacao.TRANSFERENCIAS;
        }

        if (tipo == TipoTransacao.RECEITA) {
            return CategoriaTransacao.SALARIO;
        }

        // 3. Alimentação
        if (d.contains("outback") || d.contains("conselho burguer") || d.contains("betinho") ||
                d.contains("santos alimentos") || d.contains("melo costa") || d.contains("gamella") ||
                d.contains("ifood") || d.contains("restaurante") || d.contains("almoço") || d.contains("lanche") ||
                d.contains("mercado") || d.contains("supermercado") || d.contains("padaria") || d.contains("açougue") ||
                d.contains("café") || d.contains("comida") || d.contains("gildo") || d.contains("fogão de lenha")) {
            return CategoriaTransacao.ALIMENTACAO;
        }

        // 4. Transporte
        if (d.contains("uber") || d.contains("99") || d.contains("combustivel") || d.contains("gasolina") ||
                d.contains("posto") || d.contains("estacionamento") || d.contains("passagem") || d.contains("metro")) {
            return CategoriaTransacao.TRANSPORTE;
        }

        // 5. Saúde & Farmácia
        if (d.contains("diskfarma") || d.contains("farmacia") || d.contains("farmácia") || d.contains("drogaria") ||
                d.contains("drogasil") || d.contains("pague menos") || d.contains("medico") || d.contains("médico") ||
                d.contains("consulta") || d.contains("hospital") || d.contains("remedio") || d.contains("dentista") ||
                d.contains("saude") || d.contains("saúde")) {
            return CategoriaTransacao.SAUDE;
        }

        // 6. Compras
        if (d.contains("cosmeticos") || d.contains("cosméticos") || d.contains("tarcila ferreira") ||
                d.contains("amazon") || d.contains("mercado livre") || d.contains("magalu") ||
                d.contains("shopee") || d.contains("shopping") || d.contains("roupa") || d.contains("loja") ||
                d.contains("calcado") || d.contains("calçado")) {
            return CategoriaTransacao.COMPRAS;
        }

        // 7. Moradia
        if (d.contains("aluguel") || d.contains("condominio") || d.contains("energia") || d.contains("celpe") ||
                d.contains("neoenergia") || d.contains("compesa") || d.contains("agua") || d.contains("internet") ||
                d.contains("claro") || d.contains("vivo")) {
            return CategoriaTransacao.MORADIA;
        }

        // 8. Educação
        if (d.contains("curso") || d.contains("dio") || d.contains("livro") || d.contains("faculdade") || d.contains("udemy")) {
            return CategoriaTransacao.EDUCACAO;
        }

        // 9. Lazer
        if (d.contains("cinema") || d.contains("show") || d.contains("jogo") || d.contains("steam") || d.contains("netflix") || d.contains("spotify")) {
            return CategoriaTransacao.LAZER;
        }

        return CategoriaTransacao.COMPRAS;
    }
}
