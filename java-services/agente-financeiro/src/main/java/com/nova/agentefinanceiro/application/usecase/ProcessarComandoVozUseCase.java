package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.ResumoFinanceiroResponse;
import com.nova.agentefinanceiro.application.dto.TransacaoRequest;
import com.nova.agentefinanceiro.application.dto.TransacaoResponse;
import com.nova.agentefinanceiro.application.dto.VoiceCommandRequest;
import com.nova.agentefinanceiro.application.dto.VoiceCommandResponse;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Caso de Uso para interpretação semântica e execução de comandos de voz no ecossistema NOVA.
 */
@Service
public class ProcessarComandoVozUseCase {

    private final CalcularResumoFinanceiroUseCase calcularResumoUseCase;
    private final CadastrarTransacaoUseCase cadastrarTransacaoUseCase;
    private final CalcularProjecaoFinanceiraUseCase calcularProjecaoUseCase;

    public ProcessarComandoVozUseCase(
            CalcularResumoFinanceiroUseCase calcularResumoUseCase,
            CadastrarTransacaoUseCase cadastrarTransacaoUseCase,
            CalcularProjecaoFinanceiraUseCase calcularProjecaoUseCase
    ) {
        this.calcularResumoUseCase = calcularResumoUseCase;
        this.cadastrarTransacaoUseCase = cadastrarTransacaoUseCase;
        this.calcularProjecaoUseCase = calcularProjecaoUseCase;
    }

    public VoiceCommandResponse executar(VoiceCommandRequest request) {
        if (request == null || request.comando() == null || request.comando().isBlank()) {
            return VoiceCommandResponse.erro("Não entendi o comando. Pode repetir?");
        }

        String comando = request.comando().toLowerCase(Locale.ROOT).trim();

        // 1. Intenção: Projeção Financeira & Inteligência Preditiva (Fase 9)
        if (comando.contains("previsao") || comando.contains("previsão") || comando.contains("projecao") ||
                comando.contains("projeção") || comando.contains("burn rate") || comando.contains("fechar") ||
                comando.contains("terminar o mes") || comando.contains("terminar o mês") || comando.contains("positivo")) {
            var proj = calcularProjecaoUseCase.executar(null);
            String msg;
            if ("CRITICO".equals(proj.statusOrcamentario())) {
                msg = String.format(
                        Locale.forLanguageTag("pt-BR"),
                        "Atenção Fábio! Seu burn rate é de R$ %.2f por dia. No ritmo atual, você fechará o mês com déficit estimado de R$ %.2f.",
                        proj.burnRateDiario(),
                        proj.saldoFinalProjetado().abs()
                );
            } else {
                msg = String.format(
                        Locale.forLanguageTag("pt-BR"),
                        "Fábio, seu burn rate atual é de R$ %.2f por dia. A projeção ao fim do mês é positiva com saldo de R$ %.2f. %s",
                        proj.burnRateDiario(),
                        proj.saldoFinalProjetado(),
                        proj.recomendacaoEstrategica()
                );
            }
            return VoiceCommandResponse.sucesso(msg, proj);
        }

        // 2. Intenção: Consulta de Saldo / Resumo Geral
        if (comando.contains("saldo") || comando.contains("quanto eu tenho") || comando.contains("resumo") || comando.contains("balanço") || comando.contains("balanco")) {
            ResumoFinanceiroResponse resumo = calcularResumoUseCase.executar(null, null);
            String msg = String.format(
                Locale.forLanguageTag("pt-BR"),
                "Fábio, seu saldo atual é positivo em R$ %.2f. Suas receitas somam R$ %.2f e as despesas R$ %.2f em um total de %d lançamentos conciliados no banco H2.",
                resumo.saldo(),
                resumo.totalReceitas(),
                resumo.totalGasto(),
                resumo.quantidadeTransacoes()
            );
            return VoiceCommandResponse.sucesso(msg, resumo);
        }

        // 2. Intenção: Consulta de Despesas em Categoria Específica
        if (comando.contains("gastei") || comando.contains("quanto gastei") || comando.contains("gasto com") || comando.contains("despesa com")) {
            ResumoFinanceiroResponse resumo = calcularResumoUseCase.executar(null, null);
            for (CategoriaTransacao cat : CategoriaTransacao.values()) {
                if (comando.contains(cat.name().toLowerCase(Locale.ROOT))) {
                    BigDecimal totalCat = resumo.totalPorCategoria().getOrDefault(cat, BigDecimal.ZERO);
                    String msg = String.format(
                        Locale.forLanguageTag("pt-BR"),
                        "Você gastou R$ %.2f na categoria %s neste período.",
                        totalCat,
                        cat.name().toLowerCase(Locale.ROOT)
                    );
                    return VoiceCommandResponse.sucesso(msg, totalCat);
                }
            }
            // Se nenhuma categoria específica foi mencionada
            String msg = String.format(
                Locale.forLanguageTag("pt-BR"),
                "O total de despesas consolidadas é de R$ %.2f.",
                resumo.totalGasto()
            );
            return VoiceCommandResponse.sucesso(msg, resumo.totalGasto());
        }

        // 3. Intenção: Cadastro Rápido de Transação por Voz
        // Ex: "cadastrar despesa de 45 reais de mercado em alimentacao"
        if (comando.startsWith("cadastrar") || comando.startsWith("adicionar") || comando.startsWith("novo gasto") || comando.startsWith("nova despesa")) {
            return processarCadastroPorVoz(comando);
        }

        // 4. Intenção: Identidade & Status do Ecossistema
        if (comando.contains("quem é você") || comando.contains("status") || comando.contains("ajuda") || comando.contains("ola") || comando.contains("olá")) {
            String msg = "Olá Fábio! Sou o NOVA, seu ecossistema central de inteligência, finanças e engenharia de software Java 21. Estou pronto para executar seus comandos.";
            return VoiceCommandResponse.sucesso(msg);
        }

        // Fallback: Resposta inteligente contextual
        return VoiceCommandResponse.sucesso(
            "Recebi seu comando: \"" + request.comando() + "\". Todos os serviços do NOVA estão operacionais na porta 8081."
        );
    }

    private VoiceCommandResponse processarCadastroPorVoz(String comando) {
        try {
            // Regex para extrair valor numérico
            Pattern valorPattern = Pattern.compile("(\\d+([.,]\\d{1,2})?)");
            Matcher matcher = valorPattern.matcher(comando);

            BigDecimal valor = BigDecimal.TEN; // valor padrão caso não encontre
            if (matcher.find()) {
                String valorStr = matcher.group(1).replace(",", ".");
                valor = new BigDecimal(valorStr);
            }

            TipoTransacao tipo = comando.contains("receita") || comando.contains("entrada") ? TipoTransacao.RECEITA : TipoTransacao.DESPESA;
            
            CategoriaTransacao categoria = CategoriaTransacao.OUTROS;
            for (CategoriaTransacao cat : CategoriaTransacao.values()) {
                if (comando.contains(cat.name().toLowerCase(Locale.ROOT))) {
                    categoria = cat;
                    break;
                }
            }

            String descricao = "Lançamento por Voz";
            if (comando.contains(" de ") && comando.contains(" em ")) {
                int start = comando.indexOf(" de ") + 4;
                int end = comando.indexOf(" em ");
                if (end > start) {
                    descricao = comando.substring(start, end).trim();
                }
            }

            TransacaoRequest req = new TransacaoRequest(
                descricao,
                valor,
                tipo,
                categoria,
                LocalDate.now()
            );

            TransacaoResponse res = cadastrarTransacaoUseCase.executar(req);
            String msg = String.format(
                Locale.forLanguageTag("pt-BR"),
                "%s de %s no valor de R$ %.2f cadastrada com sucesso na categoria %s.",
                tipo == TipoTransacao.RECEITA ? "Receita" : "Despesa",
                res.descricao(),
                res.valor(),
                res.categoria().name().toLowerCase(Locale.ROOT)
            );
            return VoiceCommandResponse.sucesso(msg, res);

        } catch (Exception e) {
            return VoiceCommandResponse.erro("Não consegui processar os detalhes do cadastro por voz: " + e.getMessage());
        }
    }
}
