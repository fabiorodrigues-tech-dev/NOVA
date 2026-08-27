package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.ImportacaoExtratoResponse;
import com.nova.agentefinanceiro.application.dto.TransacaoResponse;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Caso de Uso para importação e processamento de extratos bancários (OFX / CSV),
 * com foco no padrão Nubank, categorização automática inteligente e deduplicação no banco H2.
 */
@Service
public class ImportarExtratoOfxUseCase {

    private final TransacaoRepository transacaoRepository;

    private static final Pattern OFX_TRANSACTION_PATTERN = Pattern.compile(
            "<STMTTRN>([\\s\\S]*?)</STMTTRN>", Pattern.CASE_INSENSITIVE
    );

    private static final DateTimeFormatter OFX_DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyyMMdd");
    private static final DateTimeFormatter BR_DATE_FORMATTER = DateTimeFormatter.ofPattern("dd/MM/yyyy");
    private static final DateTimeFormatter ISO_DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd");

    public ImportarExtratoOfxUseCase(TransacaoRepository transacaoRepository) {
        this.transacaoRepository = transacaoRepository;
    }

    @Transactional
    public ImportacaoExtratoResponse executar(String conteudo) {
        if (conteudo == null || conteudo.trim().isBlank()) {
            return ImportacaoExtratoResponse.sucesso(0, 0, 0, List.of());
        }

        String texto = conteudo.trim();
        List<TransacaoItemParsed> parsedItems;

        if (texto.toUpperCase().contains("<OFX>") || texto.toUpperCase().contains("<STMTTRN>")) {
            parsedItems = parseOfx(texto);
        } else {
            parsedItems = parseCsv(texto);
        }

        int totalLidos = parsedItems.size();
        int totalImportados = 0;
        int totalDuplicados = 0;
        List<TransacaoResponse> importadas = new ArrayList<>();

        for (TransacaoItemParsed item : parsedItems) {
            BigDecimal valorAbsoluto = item.valor().abs();
            TipoTransacao tipo = item.valor().compareTo(BigDecimal.ZERO) < 0 ? TipoTransacao.DESPESA : TipoTransacao.RECEITA;
            CategoriaTransacao categoria = inferirCategoria(item.descricao(), tipo);

            // Deduplicação automática: verifica se já existe registro idêntico (data, valor, descrição)
            if (transacaoRepository.existe(item.data(), valorAbsoluto, item.descricao())) {
                totalDuplicados++;
                continue;
            }

            Transacao nova = new Transacao(null, item.descricao(), valorAbsoluto, tipo, categoria, item.data());
            Transacao salva = transacaoRepository.salvar(nova);

            importadas.add(new TransacaoResponse(
                    salva.getId(),
                    salva.getDescricao(),
                    salva.getValor(),
                    salva.getTipo(),
                    salva.getCategoria(),
                    salva.getData()
            ));
            totalImportados++;
        }

        return ImportacaoExtratoResponse.sucesso(totalLidos, totalImportados, totalDuplicados, importadas);
    }

    private List<TransacaoItemParsed> parseOfx(String ofxContent) {
        List<TransacaoItemParsed> items = new ArrayList<>();
        Matcher matcher = OFX_TRANSACTION_PATTERN.matcher(ofxContent);

        while (matcher.find()) {
            String block = matcher.group(1);

            LocalDate data = extrairDataOfx(block);
            BigDecimal valor = extrairValorOfx(block);
            String descricao = extrairDescricaoOfx(block);

            if (data != null && valor != null && descricao != null && !descricao.isBlank()) {
                items.add(new TransacaoItemParsed(data, valor, descricao));
            }
        }
        return items;
    }

    private LocalDate extrairDataOfx(String block) {
        Pattern pattern = Pattern.compile("<DTPOSTED>\\s*(\\d{8})", Pattern.CASE_INSENSITIVE);
        Matcher matcher = pattern.matcher(block);
        if (matcher.find()) {
            try {
                return LocalDate.parse(matcher.group(1), OFX_DATE_FORMATTER);
            } catch (DateTimeParseException ignored) {
            }
        }
        return null;
    }

    private BigDecimal extrairValorOfx(String block) {
        Pattern pattern = Pattern.compile("<TRNAMT>\\s*([+-]?\\d+(?:[.,]\\d+)?)", Pattern.CASE_INSENSITIVE);
        Matcher matcher = pattern.matcher(block);
        if (matcher.find()) {
            try {
                String valStr = matcher.group(1).replace(",", ".");
                return new BigDecimal(valStr);
            } catch (NumberFormatException ignored) {
            }
        }
        return null;
    }

    private String extrairDescricaoOfx(String block) {
        Pattern memoPattern = Pattern.compile("<MEMO>\\s*([^<\\r\\n]+)", Pattern.CASE_INSENSITIVE);
        Matcher memoMatcher = memoPattern.matcher(block);
        if (memoMatcher.find()) {
            return memoMatcher.group(1).trim();
        }

        Pattern namePattern = Pattern.compile("<NAME>\\s*([^<\\r\\n]+)", Pattern.CASE_INSENSITIVE);
        Matcher nameMatcher = namePattern.matcher(block);
        if (nameMatcher.find()) {
            return nameMatcher.group(1).trim();
        }

        return "Transação OFX";
    }

    private List<TransacaoItemParsed> parseCsv(String csvContent) {
        List<TransacaoItemParsed> items = new ArrayList<>();
        String[] lines = csvContent.split("\\r?\\n");

        for (String line : lines) {
            String trimmed = line.trim();
            if (trimmed.isEmpty()) continue;

            // Ignora cabeçalhos comuns
            String lower = trimmed.toLowerCase();
            if (lower.startsWith("data,") || lower.startsWith("data;") || lower.startsWith("date,") || lower.startsWith("data do lançamento")) {
                continue;
            }

            String delimiter = trimmed.contains(";") ? ";" : ",";
            String[] cols = trimmed.split(delimiter);
            if (cols.length < 2) continue;

            LocalDate data = parseDataFlexivel(cols[0].trim().replaceAll("^\"|\"$", ""));
            if (data == null) continue;

            // Suporta formatos:
            // 1. Data, Valor, Identificador, Descrição (Nubank Padrão)
            // 2. Data, Descrição, Valor
            // 3. Data, Valor, Descrição
            BigDecimal valor = null;
            String descricao = "Transação CSV";

            if (cols.length >= 4) {
                // Padrão Nubank: Data (0), Valor (1), Identificador (2), Descrição (3)
                valor = parseValorFlexivel(cols[1]);
                descricao = cols[3].trim().replaceAll("^\"|\"$", "");
            } else if (cols.length == 3) {
                BigDecimal valCol1 = parseValorFlexivel(cols[1]);
                if (valCol1 != null) {
                    valor = valCol1;
                    descricao = cols[2].trim().replaceAll("^\"|\"$", "");
                } else {
                    valor = parseValorFlexivel(cols[2]);
                    descricao = cols[1].trim().replaceAll("^\"|\"$", "");
                }
            } else {
                valor = parseValorFlexivel(cols[1]);
            }

            if (valor != null && !descricao.isBlank()) {
                items.add(new TransacaoItemParsed(data, valor, descricao));
            }
        }
        return items;
    }

    private LocalDate parseDataFlexivel(String str) {
        if (str == null || str.isBlank()) return null;
        try {
            if (str.contains("/")) {
                return LocalDate.parse(str, BR_DATE_FORMATTER);
            } else if (str.contains("-")) {
                return LocalDate.parse(str, ISO_DATE_FORMATTER);
            }
        } catch (DateTimeParseException ignored) {
        }
        return null;
    }

    private BigDecimal parseValorFlexivel(String str) {
        if (str == null || str.isBlank()) return null;
        try {
            String clean = str.trim().replaceAll("^\"|\"$", "")
                    .replace("R$", "")
                    .replace(" ", "");
            if (clean.contains(",") && clean.contains(".")) {
                clean = clean.replace(".", "").replace(",", ".");
            } else if (clean.contains(",")) {
                clean = clean.replace(",", ".");
            }
            return new BigDecimal(clean);
        } catch (NumberFormatException ignored) {
            return null;
        }
    }

    public CategoriaTransacao inferirCategoria(String descricao, TipoTransacao tipo) {
        if (tipo == TipoTransacao.RECEITA) {
            String d = descricao.toLowerCase();
            if (d.contains("salario") || d.contains("salário") || d.contains("remuneracao") || d.contains("pro-labore")) {
                return CategoriaTransacao.SALARIO;
            }
            if (d.contains("rendimento") || d.contains("cdb") || d.contains("dividendo") || d.contains("juros")) {
                return CategoriaTransacao.INVESTIMENTO;
            }
            return CategoriaTransacao.TRANSFERENCIAS;
        }

        String d = descricao.toLowerCase();
        if (d.contains("uber") || d.contains("99") || d.contains("combustivel") || d.contains("combustível") ||
                d.contains("posto") || d.contains("gasolina") || d.contains("estacionamento") || d.contains("pedagio") || d.contains("pedágio")) {
            return CategoriaTransacao.TRANSPORTE;
        }
        if (d.contains("ifood") || d.contains("restaurante") || d.contains("padaria") || d.contains("mercado") ||
                d.contains("supermercado") || d.contains("lanchonete") || d.contains("alimentacao") || d.contains("alimentação") ||
                d.contains("cafe") || d.contains("café") || d.contains("burger") || d.contains("pizza") || d.contains("acai") || d.contains("açaí")) {
            return CategoriaTransacao.ALIMENTACAO;
        }
        if (d.contains("farmacia") || d.contains("farmácia") || d.contains("drogaria") || d.contains("drogasil") ||
                d.contains("pague menos") || d.contains("medico") || d.contains("médico") || d.contains("consulta") ||
                d.contains("hospital") || d.contains("dentista") || d.contains("saude") || d.contains("saúde") || d.contains("laboratorio") || d.contains("laboratório")) {
            return CategoriaTransacao.SAUDE;
        }
        if (d.contains("aluguel") || d.contains("condominio") || d.contains("condomínio") || d.contains("energia") ||
                d.contains("celpe") || d.contains("neoenergia") || d.contains("agua") || d.contains("água") || d.contains("compesa") ||
                d.contains("internet") || d.contains("claro") || d.contains("vivo") || d.contains("tim") || d.contains("gas") || d.contains("gás")) {
            return CategoriaTransacao.MORADIA;
        }
        if (d.contains("cinema") || d.contains("show") || d.contains("bar") || d.contains("viagem") || d.contains("hotel") ||
                d.contains("airbnb") || d.contains("streaming") || d.contains("netflix") || d.contains("spotify") || d.contains("prime") || d.contains("disney")) {
            return CategoriaTransacao.LAZER;
        }
        if (d.contains("curso") || d.contains("livro") || d.contains("faculdade") || d.contains("dio") || d.contains("udemy") ||
                d.contains("escola") || d.contains("educacao") || d.contains("educação") || d.contains("treinamento")) {
            return CategoriaTransacao.EDUCACAO;
        }
        if (d.contains("investimento") || d.contains("nuinvest") || d.contains("tesouro") || d.contains("b3")) {
            return CategoriaTransacao.INVESTIMENTO;
        }
        if (d.contains("shopping") || d.contains("amazon") || d.contains("mercado livre") || d.contains("magalu") ||
                d.contains("roupa") || d.contains("loja") || d.contains("calcado") || d.contains("calçado")) {
            return CategoriaTransacao.COMPRAS;
        }

        return CategoriaTransacao.OUTROS;
    }

    public record TransacaoItemParsed(LocalDate data, BigDecimal valor, String descricao) {
    }
}
