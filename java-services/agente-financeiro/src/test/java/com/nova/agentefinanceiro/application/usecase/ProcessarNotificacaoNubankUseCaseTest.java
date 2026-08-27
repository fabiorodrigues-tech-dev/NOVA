package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.TransacaoRequest;
import com.nova.agentefinanceiro.application.dto.TransacaoResponse;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import com.nova.agentefinanceiro.domain.repository.TransacaoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("Testes do Caso de Uso: Processar Notificação Nubank (Webhook)")
class ProcessarNotificacaoNubankUseCaseTest {

    @Mock
    private CadastrarTransacaoUseCase cadastrarTransacaoUseCase;

    @Mock
    private TransacaoRepository transacaoRepository;

    private ProcessarNotificacaoNubankUseCase useCase;

    @BeforeEach
    void setUp() {
        useCase = new ProcessarNotificacaoNubankUseCase(cadastrarTransacaoUseCase, transacaoRepository);
    }

    @Test
    @DisplayName("Deve extrair compra de alimentação e cadastrar despesa")
    void deveProcessarNotificacaoCompraAlimentacao() {
        String texto = "Compra de R$ 45,90 no Restaurante Fogão de Lenha aprovada";

        when(transacaoRepository.existe(any(), any(), any())).thenReturn(false);
        when(cadastrarTransacaoUseCase.executar(any())).thenReturn(
                new TransacaoResponse(1L, "Restaurante Fogão de Lenha", new BigDecimal("45.90"), TipoTransacao.DESPESA, CategoriaTransacao.ALIMENTACAO, LocalDate.now())
        );

        TransacaoResponse response = useCase.executar(texto);

        assertThat(response).isNotNull();
        assertThat(response.valor()).isEqualByComparingTo("45.90");
        assertThat(response.descricao()).isEqualTo("Restaurante Fogão de Lenha");

        ArgumentCaptor<TransacaoRequest> captor = ArgumentCaptor.forClass(TransacaoRequest.class);
        verify(cadastrarTransacaoUseCase).executar(captor.capture());
        assertThat(captor.getValue().valor()).isEqualByComparingTo("45.90");
        assertThat(captor.getValue().tipo()).isEqualTo(TipoTransacao.DESPESA);
        assertThat(captor.getValue().categoria()).isEqualTo(CategoriaTransacao.ALIMENTACAO);
    }

    @Test
    @DisplayName("Deve extrair transferência recebida como receita")
    void deveProcessarNotificacaoTransferenciaRecebida() {
        String texto = "Você recebeu uma transferência de R$ 500,00 de Ramon Rodrigues";

        when(transacaoRepository.existe(any(), any(), any())).thenReturn(false);
        when(cadastrarTransacaoUseCase.executar(any())).thenReturn(
                new TransacaoResponse(2L, "Transferência de Ramon Rodrigues", new BigDecimal("500.00"), TipoTransacao.RECEITA, CategoriaTransacao.SALARIO, LocalDate.now())
        );

        TransacaoResponse response = useCase.executar(texto);

        assertThat(response).isNotNull();
        assertThat(response.valor()).isEqualByComparingTo("500.00");

        ArgumentCaptor<TransacaoRequest> captor = ArgumentCaptor.forClass(TransacaoRequest.class);
        verify(cadastrarTransacaoUseCase).executar(captor.capture());
        assertThat(captor.getValue().valor()).isEqualByComparingTo("500.00");
        assertThat(captor.getValue().tipo()).isEqualTo(TipoTransacao.RECEITA);
    }

    @Test
    @DisplayName("Deve extrair corrida de Uber como transporte")
    void deveProcessarNotificacaoUberTransporte() {
        String texto = "Compra de R$ 18,50 no Uber aprovada";

        when(transacaoRepository.existe(any(), any(), any())).thenReturn(false);
        when(cadastrarTransacaoUseCase.executar(any())).thenReturn(
                new TransacaoResponse(3L, "Uber", new BigDecimal("18.50"), TipoTransacao.DESPESA, CategoriaTransacao.TRANSPORTE, LocalDate.now())
        );

        useCase.executar(texto);

        ArgumentCaptor<TransacaoRequest> captor = ArgumentCaptor.forClass(TransacaoRequest.class);
        verify(cadastrarTransacaoUseCase).executar(captor.capture());
        assertThat(captor.getValue().categoria()).isEqualTo(CategoriaTransacao.TRANSPORTE);
    }

    @Test
    @DisplayName("Deve lançar exceção para notificação vazia")
    void deveLancarExcecaoParaNotificacaoVazia() {
        assertThrows(IllegalArgumentException.class, () -> useCase.executar("   "));
    }
}
