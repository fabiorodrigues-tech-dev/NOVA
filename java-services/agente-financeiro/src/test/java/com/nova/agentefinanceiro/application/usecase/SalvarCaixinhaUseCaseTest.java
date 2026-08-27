package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.CaixinhaRequest;
import com.nova.agentefinanceiro.application.dto.CaixinhaResponse;
import com.nova.agentefinanceiro.domain.model.Caixinha;
import com.nova.agentefinanceiro.domain.model.TipoCaixinha;
import com.nova.agentefinanceiro.domain.repository.CaixinhaRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("Testes do Caso de Uso: Salvar Caixinha")
class SalvarCaixinhaUseCaseTest {

    @Mock
    private CaixinhaRepository caixinhaRepository;

    private SalvarCaixinhaUseCase useCase;

    @BeforeEach
    void setUp() {
        useCase = new SalvarCaixinhaUseCase(caixinhaRepository);
    }

    @Test
    @DisplayName("Deve cadastrar nova Caixinha com tipo inferido corretamente")
    void deveCadastrarNovaCaixinha() {
        CaixinhaRequest request = new CaixinhaRequest(
                "Reserva de Emergência",
                new BigDecimal("1500.00"),
                null,
                new BigDecimal("15.00")
        );

        when(caixinhaRepository.buscarPorNome("Reserva de Emergência")).thenReturn(Optional.empty());
        when(caixinhaRepository.buscarPorTipo(TipoCaixinha.RESERVA_EMERGENCIA)).thenReturn(Optional.empty());
        when(caixinhaRepository.salvar(any())).thenAnswer(invocation -> {
            Caixinha c = invocation.getArgument(0);
            return new Caixinha(1L, c.getNome(), c.getSaldo(), c.getTipo(), c.getRendimentoMensalEstimado(), LocalDate.now());
        });

        CaixinhaResponse response = useCase.executar(request);

        assertThat(response).isNotNull();
        assertThat(response.id()).isEqualTo(1L);
        assertThat(response.nome()).isEqualTo("Reserva de Emergência");
        assertThat(response.tipo()).isEqualTo(TipoCaixinha.RESERVA_EMERGENCIA);
        assertThat(response.saldo()).isEqualByComparingTo("1500.00");

        ArgumentCaptor<Caixinha> captor = ArgumentCaptor.forClass(Caixinha.class);
        verify(caixinhaRepository).salvar(captor.capture());
        assertThat(captor.getValue().getTipo()).isEqualTo(TipoCaixinha.RESERVA_EMERGENCIA);
    }

    @Test
    @DisplayName("Deve atualizar saldo de Caixinha existente")
    void deveAtualizarSaldoDeCaixinhaExistente() {
        Caixinha existente = new Caixinha(2L, "Fundo do Casal", new BigDecimal("800.00"), TipoCaixinha.FUNDO_CASAL, BigDecimal.ZERO, LocalDate.now());
        when(caixinhaRepository.buscarPorNome("Fundo do Casal")).thenReturn(Optional.of(existente));
        when(caixinhaRepository.salvar(any())).thenAnswer(inv -> inv.getArgument(0));

        CaixinhaRequest request = new CaixinhaRequest("Fundo do Casal", new BigDecimal("1200.00"), TipoCaixinha.FUNDO_CASAL, BigDecimal.ZERO);
        CaixinhaResponse response = useCase.executar(request);

        assertThat(response.saldo()).isEqualByComparingTo("1200.00");
        assertThat(existente.getSaldo()).isEqualByComparingTo("1200.00");
    }

    @Test
    @DisplayName("Deve lançar exceção para payload nulo")
    void deveLancarExcecaoParaPayloadNulo() {
        assertThrows(IllegalArgumentException.class, () -> useCase.executar(null));
    }
}
