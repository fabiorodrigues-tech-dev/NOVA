package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.ImportacaoExtratoResponse;
import com.nova.agentefinanceiro.application.dto.TransacaoResponse;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.File;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Caso de Uso para importação e processamento de extratos bancários (OFX / CSV),
 * com foco no padrão Nubank, busca na pasta oficial financeiro/extratos_ofx/,
 * categorização automática inteligente e deduplicação no banco H2.
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

    public ImportacaoExtratoResponse importarDiretorioPadrao() {
        File dir = new File("financeiro");
        if (!dir.exists()) {
            dir = new File("../../financeiro");
        }
        if (!dir.exists()) {
            dir = new File("../financeiro");
        }
        if (!dir.exists() || !dir.isDirectory()) {
            dir = new File("financeiro/extratos_ofx");
            if (!dir.exists()) dir = new File("../../financeiro/extratos_ofx");
            if (!dir.exists()) dir = new File("../financeiro/extratos_ofx");
        }
        if (!dir.exists() || !dir.isDirectory()) {
            return ImportacaoExtratoResponse.erro("Diretório 'financeiro' não encontrado.");
        }

        List<File> files = listarArquivosRecursivos(dir);
        if (files.isEmpty()) {
            return ImportacaoExtratoResponse.sucesso(0, 0, 0, List.of());
        }

        int totalLidos = 0;
        int totalImportados = 0;
        int totalDuplicados = 0;
        List<TransacaoResponse> todasImportadas = new ArrayList<>();

        for (File file : files) {
            try {
                String content = Files.readString(file.toPath(), StandardCharsets.UTF_8);
                ImportacaoExtratoResponse res = executar(content);
                totalLidos += res.totalLidos();
                totalImportados += res.totalImportados();
                totalDuplicados += res.totalDuplicados();
                todasImportadas.addAll(res.transacoesImportadas());
            } catch (Exception e) {
                try {
                    String content = Files.readString(file.toPath(), StandardCharsets.ISO_8859_1);
                    ImportacaoExtratoResponse res = executar(content);
                    totalLidos += res.totalLidos();
                    totalImportados += res.totalImportados();
                    totalDuplicados += res.totalDuplicados();
                    todasImportadas.addAll(res.transacoesImportadas());
                } catch (Exception ignored) {}
            }
        }
        return ImportacaoExtratoResponse.sucesso(totalLidos, totalImportados, totalDuplicados, todasImportadas);
    }

    private List<File> listarArquivosRecursivos(File dir) {
        List<File> result = new ArrayList<>();
        if (dir == null || !dir.exists()) return result;
        File[] entries = dir.listFiles();
        if (entries == null) return result;
        for (File f : entries) {
            if (f.isDirectory()) {
                result.addAll(listarArquivosRecursivos(f));
            } else {
                String name = f.getName().toLowerCase();
                if (name.endsWith(".ofx") || name.endsWith(".csv")) {
                    result.add(f);
                }
            }
        }
        return result;
    }

    public ImportacaoExtratoResponse importarArquivo(String caminho) {
        if (caminho == null || caminho.isBlank()) {
            return importarDiretorioPadrao();
        }
        File file = new File(caminho);
        if (!file.exists()) {
            file = new File("financeiro/extratos_ofx/" + caminho);
        }
        if (!file.exists()) {
            file = new File("../../financeiro/extratos_ofx/" + caminho);
        }
        if (!file.exists()) {
            return ImportacaoExtratoResponse.erro("Arquivo não encontrado: " + caminho);
        }
        try {
            String content = Files.readString(file.toPath(), StandardCharsets.UTF_8);
            return executar(content);
        } catch (Exception e) {
            try {
                String content = Files.readString(file.toPath(), StandardCharsets.ISO_8859_1);
                return executar(content);
            } catch (Exception ex) {
                return ImportacaoExtratoResponse.erro("Erro ao ler arquivo: " + ex.getMessage());
            }
        }
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

            String fitid = item.fitid() != null ? item.fitid().trim() : "";
            String hash = calcularHashSha256(item.data(), valorAbsoluto, fitid, item.descricao());

            // Deduplicação estrita por hash SHA-256: se já existir no H2, descarta silenciosamente
            if ((!hash.isBlank() && transacaoRepository.existePorHash(hash)) ||
                    transacaoRepository.existe(item.data(), valorAbsoluto, item.descricao())) {
                totalDuplicados++;
                continue;
            }

            Transacao nova = new Transacao(null, item.descricao(), valorAbsoluto, tipo, categoria, item.data(), hash);
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

    public static String calcularHashSha256(LocalDate data, BigDecimal valor, String fitid, String descricaoLimpa) {
        try {
            String dt = data != null ? data.toString() : "";
            String val = valor != null ? valor.setScale(2, java.math.RoundingMode.HALF_UP).toPlainString() : "0.00";
            String fit = fitid != null ? fitid.trim() : "";
            String desc = descricaoLimpa != null ? descricaoLimpa.trim() : "";
            String payload = dt + val + fit + desc;
            java.security.MessageDigest md = java.security.MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(payload.getBytes(StandardCharsets.UTF_8));
            StringBuilder sb = new StringBuilder();
            for (byte b : hash) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (Exception e) {
            return java.util.UUID.randomUUID().toString();
        }
    }

    @Transactional
    public ImportacaoExtratoResponse reconciliarExtratosEstrito() {
        // Limpa meses de Agosto e Setembro para reingestão limpa e deduplicação estrita
        try {
            transacaoRepository.deletarPorPeriodo(LocalDate.of(2026, 8, 1), LocalDate.of(2026, 8, 31));
            transacaoRepository.deletarPorPeriodo(LocalDate.of(2026, 9, 1), LocalDate.of(2026, 9, 30));
        } catch (Exception ignored) {}

        File dir = new File("financeiro/extratos_ofx");
        if (!dir.exists()) dir = new File("../../financeiro/extratos_ofx");
        if (!dir.exists()) dir = new File("../financeiro/extratos_ofx");
        if (!dir.exists()) dir = new File("financeiro");

        List<File> files = listarArquivosRecursivos(dir);
        // Ordena para processar o arquivo completo de Agosto antes do parcial
        files.sort((f1, f2) -> {
            String n1 = f1.getName().toLowerCase();
            String n2 = f2.getName().toLowerCase();
            if (n1.contains("31ago") && n2.contains("26ago")) return -1;
            if (n1.contains("26ago") && n2.contains("31ago")) return 1;
            return n1.compareTo(n2);
        });

        int totalLidos = 0;
        int totalImportados = 0;
        int totalDuplicados = 0;
        List<TransacaoResponse> todas = new ArrayList<>();

        for (File f : files) {
            try {
                String content = Files.readString(f.toPath(), StandardCharsets.UTF_8);
                ImportacaoExtratoResponse res = executar(content);
                totalLidos += res.totalLidos();
                totalImportados += res.totalImportados();
                totalDuplicados += res.totalDuplicados();
                todas.addAll(res.transacoesImportadas());
            } catch (Exception e) {
                try {
                    String content = Files.readString(f.toPath(), StandardCharsets.ISO_8859_1);
                    ImportacaoExtratoResponse res = executar(content);
                    totalLidos += res.totalLidos();
                    totalImportados += res.totalImportados();
                    totalDuplicados += res.totalDuplicados();
                    todas.addAll(res.transacoesImportadas());
                } catch (Exception ignored) {}
            }
        }
        return ImportacaoExtratoResponse.sucesso(totalLidos, totalImportados, totalDuplicados, todas);
    }

    private List<TransacaoItemParsed> parseOfx(String ofxContent) {
        List<TransacaoItemParsed> items = new ArrayList<>();
        Matcher matcher = OFX_TRANSACTION_PATTERN.matcher(ofxContent);

        while (matcher.find()) {
            String block = matcher.group(1);

            LocalDate data = extrairDataOfx(block);
            BigDecimal valor = extrairValorOfx(block);
            String descricao = extrairDescricaoOfx(block);
            String fitid = extrairFitidOfx(block);

            if (data != null && valor != null && descricao != null && !descricao.isBlank()) {
                items.add(new TransacaoItemParsed(data, valor, descricao, fitid));
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

    private String extrairFitidOfx(String block) {
        Pattern pattern = Pattern.compile("<FITID>\\s*([^<\\r\\n]+)", Pattern.CASE_INSENSITIVE);
        Matcher matcher = pattern.matcher(block);
        if (matcher.find()) {
            return matcher.group(1).trim();
        }
        return null;
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
        String d = descricao.toLowerCase();

        // 1. Investimentos (RDB, Aplicação, Resgate, CDB, Poupança)
        if (d.contains("aplicação rdb") || d.contains("aplicacao rdb") || d.contains("resgate rdb") ||
                d.contains(" rdb") || d.startsWith("rdb") || d.contains("investimento") || d.contains("nuinvest") ||
                d.contains("tesouro") || d.contains("b3") || d.contains("poupanca") || d.contains("poupança") ||
                d.contains("cdb") || d.contains("rendimento") || d.contains("dividendo")) {
            return CategoriaTransacao.INVESTIMENTO;
        }

        // 2. Compras
        if (d.contains("cosmeticos") || d.contains("cosméticos") || d.contains("tarcila ferreira") ||
                d.contains("amazon") || d.contains("mercado livre") || d.contains("magalu") ||
                d.contains("shopee") || d.contains("shopping") || d.contains("roupa") || d.contains("loja") ||
                d.contains("calcado") || d.contains("calçado")) {
            return CategoriaTransacao.COMPRAS;
        }

        // 3. Saúde & Farmácia
        if (d.contains("diskfarma") || d.contains("farmacia") || d.contains("farmácia") || d.contains("drogaria") ||
                d.contains("drogasil") || d.contains("pague menos") || d.contains("medico") || d.contains("médico") ||
                d.contains("consulta") || d.contains("hospital") || d.contains("dentista") || d.contains("saude") ||
                d.contains("saúde") || d.contains("laboratorio") || d.contains("laboratório")) {
            return CategoriaTransacao.SAUDE;
        }

        // 4. Alimentação
        if (d.contains("outback") || d.contains("conselho burguer") || d.contains("conselho") ||
                d.contains("betinho") || d.contains("santos alimentos") || d.contains("melo costa") ||
                d.contains("melocostasorvetes") || d.contains("gamella") || d.contains("ifood") ||
                d.contains("barteco") || d.contains("restaurante") || d.contains("padaria") ||
                d.contains("mercado") || d.contains("supermercado") || d.contains("lanchonete") ||
                d.contains("alimentacao") || d.contains("alimentação") || d.contains("cafe") ||
                d.contains("café") || d.contains("burger") || d.contains("burguer") || d.contains("pizza") ||
                d.contains("acai") || d.contains("açaí") || d.contains("acaichefcela") || d.contains("sorvete") || d.contains("comedoria")) {
            return CategoriaTransacao.ALIMENTACAO;
        }

        // 5. Transferências para Pessoas Físicas (PIX para PF nunca é Alimentação ou Transporte)
        String[] pessoasFisicas = {
            "iza correia", "gildeth", "mariana", "cleiton", "lucas", "cicero",
            "manoel elias", "noemia", "rosangela", "abinadar", "kaua carlos",
            "livia maria", "tatiana keci", "isabela alme", "leones arrud",
            "mariahelena", "hermirio", "sublimix", "ramon", "washington luiz", "fabio andre"
        };
        for (String pf : pessoasFisicas) {
            if (d.contains(pf)) {
                return CategoriaTransacao.TRANSFERENCIAS;
            }
        }

        if (d.contains("transferência") || d.contains("transferencia") || d.contains("pix")) {
            if (d.contains("uber") || d.contains("99")) {
                return CategoriaTransacao.TRANSPORTE;
            }
            return CategoriaTransacao.TRANSFERENCIAS;
        }

        // 6. Transporte
        if (d.contains("uber") || d.contains("99") || d.contains("combustivel") || d.contains("combustível") ||
                d.contains("posto") || d.contains("gasolina") || d.contains("estacionamento") || d.contains("pedagio") || d.contains("pedágio")) {
            return CategoriaTransacao.TRANSPORTE;
        }

        // 7. Moradia
        if (d.contains("aluguel") || d.contains("condominio") || d.contains("condomínio") || d.contains("energia") ||
                d.contains("celpe") || d.contains("neoenergia") || d.contains("agua") || d.contains("água") || d.contains("compesa") ||
                d.contains("internet") || d.contains("claro") || d.contains("vivo") || d.contains("tim") || d.contains("gas") || d.contains("gás")) {
            return CategoriaTransacao.MORADIA;
        }

        // 8. Lazer
        if (d.contains("cinema") || d.contains("show") || d.contains("bar") || d.contains("viagem") || d.contains("hotel") ||
                d.contains("airbnb") || d.contains("streaming") || d.contains("netflix") || d.contains("spotify") || d.contains("prime") || d.contains("disney")) {
            return CategoriaTransacao.LAZER;
        }

        // 9. Educação
        if (d.contains("curso") || d.contains("livro") || d.contains("faculdade") || d.contains("dio") || d.contains("udemy") ||
                d.contains("escola") || d.contains("educacao") || d.contains("educação") || d.contains("treinamento")) {
            return CategoriaTransacao.EDUCACAO;
        }

        // 10. Receita geral / Salário
        if (tipo == TipoTransacao.RECEITA) {
            if (d.contains("salario") || d.contains("salário") || d.contains("remuneracao") || d.contains("pro-labore")) {
                return CategoriaTransacao.SALARIO;
            }
            return CategoriaTransacao.TRANSFERENCIAS;
        }

        return CategoriaTransacao.OUTROS;
    }

    public record TransacaoItemParsed(LocalDate data, BigDecimal valor, String descricao, String fitid) {
        public TransacaoItemParsed(LocalDate data, BigDecimal valor, String descricao) {
            this(data, valor, descricao, null);
        }
    }
}
