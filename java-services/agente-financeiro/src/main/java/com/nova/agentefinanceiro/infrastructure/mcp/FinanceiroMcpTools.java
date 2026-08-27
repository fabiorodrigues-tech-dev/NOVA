package com.nova.agentefinanceiro.infrastructure.mcp;

import com.nova.agentefinanceiro.application.dto.CaixinhaRequest;
import com.nova.agentefinanceiro.application.dto.CaixinhaResponse;
import com.nova.agentefinanceiro.application.dto.ImportacaoExtratoResponse;
import com.nova.agentefinanceiro.application.dto.PatrimonioLiquidoResponse;
import com.nova.agentefinanceiro.application.dto.ProjecaoFinanceiraResponse;
import com.nova.agentefinanceiro.application.dto.ResumoFinanceiroResponse;
import com.nova.agentefinanceiro.application.dto.TransacaoRequest;
import com.nova.agentefinanceiro.application.dto.TransacaoResponse;
import com.nova.agentefinanceiro.application.usecase.CadastrarTransacaoUseCase;
import com.nova.agentefinanceiro.application.usecase.CalcularProjecaoFinanceiraUseCase;
import com.nova.agentefinanceiro.application.usecase.CalcularResumoFinanceiroUseCase;
import com.nova.agentefinanceiro.application.usecase.ImportarExtratoOfxUseCase;
import com.nova.agentefinanceiro.application.usecase.ListarCaixinhasUseCase;
import com.nova.agentefinanceiro.application.usecase.ListarTransacoesUseCase;
import com.nova.agentefinanceiro.application.usecase.SalvarCaixinhaUseCase;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoCaixinha;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

/**
 * Ferramentas MCP (Model Context Protocol) para interação do agente de IA com o domínio financeiro,
 * incluindo extratos Nubank OFX/CSV, Caixinhas de Investimento e Projeção Orçamentária.
 */
@Component
public class FinanceiroMcpTools {

    private final CadastrarTransacaoUseCase cadastrarTransacaoUseCase;
    private final ListarTransacoesUseCase listarTransacoesUseCase;
    private final CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase;
    private final ImportarExtratoOfxUseCase importarExtratoOfxUseCase;
    private final CalcularProjecaoFinanceiraUseCase calcularProjecaoFinanceiraUseCase;
    private final SalvarCaixinhaUseCase salvarCaixinhaUseCase;
    private final ListarCaixinhasUseCase listarCaixinhasUseCase;

    public FinanceiroMcpTools(
            CadastrarTransacaoUseCase cadastrarTransacaoUseCase,
            ListarTransacoesUseCase listarTransacoesUseCase,
            CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase,
            ImportarExtratoOfxUseCase importarExtratoOfxUseCase,
            CalcularProjecaoFinanceiraUseCase calcularProjecaoFinanceiraUseCase,
            SalvarCaixinhaUseCase salvarCaixinhaUseCase,
            ListarCaixinhasUseCase listarCaixinhasUseCase
    ) {
        this.cadastrarTransacaoUseCase = cadastrarTransacaoUseCase;
        this.listarTransacoesUseCase = listarTransacoesUseCase;
        this.calcularResumoFinanceiroUseCase = calcularResumoFinanceiroUseCase;
        this.importarExtratoOfxUseCase = importarExtratoOfxUseCase;
        this.calcularProjecaoFinanceiraUseCase = calcularProjecaoFinanceiraUseCase;
        this.salvarCaixinhaUseCase = salvarCaixinhaUseCase;
        this.listarCaixinhasUseCase = listarCaixinhasUseCase;
    }

    @Tool(
            name = "atualizar_caixinha",
            description = "Cadastra ou atualiza o saldo de uma Caixinha / Fundo de Investimento Nubank (ex: Reserva de Emergência, Fundo do Casal, Metas). Use sempre que o usuário informar um novo saldo investido ou aporte."
    )
    public CaixinhaResponse atualizarCaixinha(
            @ToolParam(description = "Nome da caixinha (ex: 'Reserva de Emergência', 'Fundo do Casal', 'Viagem')")
            String nome,

            @ToolParam(description = "Saldo total atualizado na caixinha em reais (ex: 1500.00)")
            BigDecimal saldo,

            @ToolParam(required = false, description = "Tipo da caixinha: 'RESERVA_EMERGENCIA', 'FUNDO_CASAL', 'METAS', 'OUTROS'. Padrão: inferido pelo nome.")
            TipoCaixinha tipo,

            @ToolParam(required = false, description = "Rendimento mensal estimado em reais. Padrão: 0.00")
            BigDecimal rendimentoMensalEstimado
    ) {
        return salvarCaixinhaUseCase.executar(new CaixinhaRequest(nome, saldo, tipo, rendimentoMensalEstimado));
    }

    @Tool(
            name = "consultar_caixinhas",
            description = "Consulta todos os investimentos e Caixinhas Nubank cadastrados, calculando o Patrimônio Líquido Total (Saldo em Conta + Caixinhas)."
    )
    public PatrimonioLiquidoResponse consultarCaixinhas() {
        return listarCaixinhasUseCase.executar();
    }

    @Tool(
            name = "projecao_financeira",
            description = "Calcula a inteligência preditiva e projeção financeira orçamentária do mês corrente, estimando o burn rate diário (ritmo de gastos), projeção de saldo final ao fechar o mês e alertas de risco."
    )
    public ProjecaoFinanceiraResponse projecaoFinanceira(
            @ToolParam(required = false, description = "Data de referência para o cálculo no formato 'AAAA-MM-DD'. Se omitida, assume a data de hoje.")
            LocalDate dataReferencia
    ) {
        return calcularProjecaoFinanceiraUseCase.executar(dataReferencia);
    }

    @Tool(
            name = "importar_extrato_ofx",
            description = "Importa e processa extratos bancários em formato OFX ou CSV (padrão Nubank). Se o conteúdo não for informado, processa automaticamente todos os arquivos da pasta oficial 'financeiro/extratos_ofx/'."
    )
    public ImportacaoExtratoResponse importarExtratoOfx(
            @ToolParam(required = false, description = "Conteúdo textual completo do arquivo OFX ou CSV do extrato bancário. Se omitido, lê os arquivos em financeiro/extratos_ofx/.")
            String conteudoExtrato,

            @ToolParam(required = false, description = "Nome ou caminho do arquivo específico dentro de financeiro/extratos_ofx/.")
            String nomeArquivo
    ) {
        if (nomeArquivo != null && !nomeArquivo.isBlank()) {
            return importarExtratoOfxUseCase.importarArquivo(nomeArquivo);
        }
        if (conteudoExtrato == null || conteudoExtrato.trim().isBlank()) {
            return importarExtratoOfxUseCase.importarDiretorioPadrao();
        }
        return importarExtratoOfxUseCase.executar(conteudoExtrato);
    }

    @Tool(
            name = "cadastrar_transacao",
            description = "Cadastra um novo gasto ou receita financeira pessoal no sistema. Use esta ferramenta sempre que o usuário informar um novo gasto realizado, uma compra, pagamento ou recebimento."
    )
    public TransacaoResponse cadastrarTransacao(
            @ToolParam(description = "Descrição clara do gasto ou receita (ex: 'Almoço no restaurante', 'Supermercado Mensal', 'Gasolina')")
            String descricao,

            @ToolParam(description = "Valor numérico positivo da transação em reais (ex: 35.00, 150.90)")
            BigDecimal valor,

            @ToolParam(required = false, description = "Tipo da transação: 'DESPESA' para gastos e saídas, ou 'RECEITA' para entradas financeiras. Padrão: DESPESA")
            TipoTransacao tipo,

            @ToolParam(required = false, description = "Categoria do gasto/receita: 'ALIMENTACAO', 'TRANSPORTE', 'MORADIA', 'EDUCACAO', 'SAUDE', 'LAZER', 'COMPRAS', 'TRANSFERENCIAS', 'SERVICOS', 'SALARIO', 'INVESTIMENTO', 'OUTROS'. Padrão: OUTROS")
            CategoriaTransacao categoria,

            @ToolParam(required = false, description = "Data da transação no formato 'AAAA-MM-DD' (ex: '2026-08-25'). Se não informada, assume a data de hoje.")
            LocalDate data
    ) {
        TransacaoRequest request = new TransacaoRequest(
                descricao,
                valor,
                tipo != null ? tipo : TipoTransacao.DESPESA,
                categoria != null ? categoria : CategoriaTransacao.OUTROS,
                data != null ? data : LocalDate.now()
        );
        return cadastrarTransacaoUseCase.executar(request);
    }

    @Tool(
            name = "listar_transacoes",
            description = "Lista o histórico de transações e movimentações financeiras cadastradas, com suporte a filtro opcional por período de datas. Use para consultar os últimos gastos ou listar o extrato."
    )
    public List<TransacaoResponse> listarTransacoes(
            @ToolParam(required = false, description = "Data inicial para o filtro no formato 'AAAA-MM-DD' (ex: '2026-08-01'). Opcional.")
            LocalDate inicio,

            @ToolParam(required = false, description = "Data final para o filtro no formato 'AAAA-MM-DD' (ex: '2026-08-31'). Opcional.")
            LocalDate fim
    ) {
        return listarTransacoesUseCase.executar(inicio, fim);
    }

    @Tool(
            name = "resumo_financeiro",
            description = "Calcula o resumo e balanço financeiro consolidado de um período, totalizando despesas, receitas, saldo e detalhamento dos gastos agrupados por categoria. Use quando o usuário perguntar quanto gastou no mês/período ou pedir uma análise/balanço do orçamento."
    )
    public ResumoFinanceiroResponse resumoFinanceiro(
            @ToolParam(required = false, description = "Data de início do período para cálculo no formato 'AAAA-MM-DD'. Se omitida, considera o 1º dia do mês corrente.")
            LocalDate inicio,

            @ToolParam(required = false, description = "Data de fim do período para cálculo no formato 'AAAA-MM-DD'. Se omitida, considera o último dia do mês corrente.")
            LocalDate fim
    ) {
        return calcularResumoFinanceiroUseCase.executar(inicio, fim);
    }
}
