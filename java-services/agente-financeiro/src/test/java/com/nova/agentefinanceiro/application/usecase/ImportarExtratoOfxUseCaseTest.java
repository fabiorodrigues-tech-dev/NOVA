package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.ImportacaoExtratoResponse;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import com.nova.agentefinanceiro.domain.model.Transacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ImportarExtratoOfxUseCaseTest {

    @Mock
    private TransacaoRepository transacaoRepository;

    private ImportarExtratoOfxUseCase useCase;

    @BeforeEach
    void setUp() {
        useCase = new ImportarExtratoOfxUseCase(transacaoRepository);
    }

    @Test
    @DisplayName("Deve importar e categorizar transações de extrato OFX com sucesso")
    void deveImportarExtratoOfxComSucessoECategorizar() {
        String ofx = """
                <OFX>
                <BANKMSGSRSV1>
                <STMTTRNRS>
                <STMTRS>
                <BANKTRANLIST>
                <STMTTRN>
                  <TRNTYPE>DEBIT
                  <DTPOSTED>20260810120000
                  <TRNAMT>-32.50
                  <FITID>1001
                  <MEMO>Uber Viagem Centro
                </STMTTRN>
                <STMTTRN>
                  <TRNTYPE>DEBIT
                  <DTPOSTED>20260811120000
                  <TRNAMT>-85.90
                  <FITID>1002
                  <MEMO>Supermercado Pao de Acucar
                </STMTTRN>
                <STMTTRN>
                  <TRNTYPE>CREDIT
                  <DTPOSTED>20260812120000
                  <TRNAMT>2500.00
                  <FITID>1003
                  <MEMO>Salario Mensal
                </STMTTRN>
                </BANKTRANLIST>
                </STMTRS>
                </STMTTRNRS>
                </BANKMSGSRSV1>
                </OFX>
                """;

        when(transacaoRepository.existe(any(), any(), any())).thenReturn(false);
        when(transacaoRepository.salvar(any())).thenAnswer(invocation -> {
            Transacao t = invocation.getArgument(0);
            return new Transacao(1L, t.getDescricao(), t.getValor(), t.getTipo(), t.getCategoria(), t.getData());
        });

        ImportacaoExtratoResponse response = useCase.executar(ofx);

        assertNotNull(response);
        assertEquals(3, response.totalLidos());
        assertEquals(3, response.totalImportados());
        assertEquals(0, response.totalDuplicados());
        assertEquals(3, response.transacoesImportadas().size());

        // Valida primeira transação (Uber -> TRANSPORTE, DESPESA)
        assertEquals(new BigDecimal("32.50"), response.transacoesImportadas().get(0).valor());
        assertEquals(TipoTransacao.DESPESA, response.transacoesImportadas().get(0).tipo());
        assertEquals(CategoriaTransacao.TRANSPORTE, response.transacoesImportadas().get(0).categoria());

        // Valida segunda transação (Mercado -> ALIMENTACAO, DESPESA)
        assertEquals(new BigDecimal("85.90"), response.transacoesImportadas().get(1).valor());
        assertEquals(CategoriaTransacao.ALIMENTACAO, response.transacoesImportadas().get(1).categoria());

        // Valida terceira transação (Salario -> SALARIO, RECEITA)
        assertEquals(new BigDecimal("2500.00"), response.transacoesImportadas().get(2).valor());
        assertEquals(TipoTransacao.RECEITA, response.transacoesImportadas().get(2).tipo());
        assertEquals(CategoriaTransacao.SALARIO, response.transacoesImportadas().get(2).categoria());

        verify(transacaoRepository, times(3)).salvar(any());
    }

    @Test
    @DisplayName("Deve importar e processar extrato CSV no padrão Nubank")
    void deveImportarExtratoCsvNubankComSucesso() {
        String csv = """
                Data,Valor,Identificador,Descrição
                15/08/2026,-45.00,uuid-1,Farmacia Drogasil
                16/08/2026,-120.00,uuid-2,Neoenergia Celpe
                17/08/2026,300.00,uuid-3,Pix Recebido de Cliente
                """;

        when(transacaoRepository.existe(any(), any(), any())).thenReturn(false);
        when(transacaoRepository.salvar(any())).thenAnswer(invocation -> {
            Transacao t = invocation.getArgument(0);
            return new Transacao(10L, t.getDescricao(), t.getValor(), t.getTipo(), t.getCategoria(), t.getData());
        });

        ImportacaoExtratoResponse response = useCase.executar(csv);

        assertNotNull(response);
        assertEquals(3, response.totalLidos());
        assertEquals(3, response.totalImportados());
        assertEquals(0, response.totalDuplicados());

        assertEquals(CategoriaTransacao.SAUDE, response.transacoesImportadas().get(0).categoria());
        assertEquals(CategoriaTransacao.MORADIA, response.transacoesImportadas().get(1).categoria());
        assertEquals(CategoriaTransacao.TRANSFERENCIAS, response.transacoesImportadas().get(2).categoria());
        assertEquals(TipoTransacao.RECEITA, response.transacoesImportadas().get(2).tipo());
    }

    @Test
    @DisplayName("Deve identificar e ignorar transações duplicadas no banco H2")
    void deveIgnorarTransacoesDuplicadas() {
        String csv = """
                Data,Valor,Identificador,Descrição
                20/08/2026,-50.00,uuid-1,Posto Shell Gasolina
                """;

        // Simula que a transação já existe
        when(transacaoRepository.existe(LocalDate.of(2026, 8, 20), new BigDecimal("50.00"), "Posto Shell Gasolina"))
                .thenReturn(true);

        ImportacaoExtratoResponse response = useCase.executar(csv);

        assertNotNull(response);
        assertEquals(1, response.totalLidos());
        assertEquals(0, response.totalImportados());
        assertEquals(1, response.totalDuplicados());
        assertTrue(response.transacoesImportadas().isEmpty());

        verify(transacaoRepository, never()).salvar(any());
    }

    @Test
    @DisplayName("Deve retornar resposta vazia quando conteúdo for nulo ou em branco")
    void deveRetornarVazioQuandoConteudoForNuloOuEmBranco() {
        ImportacaoExtratoResponse r1 = useCase.executar(null);
        assertEquals(0, r1.totalLidos());
        assertEquals(0, r1.totalImportados());

        ImportacaoExtratoResponse r2 = useCase.executar("   ");
        assertEquals(0, r2.totalLidos());
        assertEquals(0, r2.totalImportados());
    }
}
