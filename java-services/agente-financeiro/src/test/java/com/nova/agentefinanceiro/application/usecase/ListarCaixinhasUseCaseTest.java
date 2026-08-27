package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.PatrimonioLiquidoResponse;
import com.nova.agentefinanceiro.application.dto.ResumoFinanceiroResponse;
import com.nova.agentefinanceiro.domain.model.Caixinha;
import com.nova.agentefinanceiro.domain.model.TipoCaixinha;
import com.nova.agentefinanceiro.domain.repository.CaixinhaRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("Testes do Caso de Uso: Listar Caixinhas e Patrimônio Líquido")
class ListarCaixinhasUseCaseTest {

    @Mock
    private CaixinhaRepository caixinhaRepository;

    @Mock
    private CalcularResumoFinanceiroUseCase calcularResumoFinanceiroUseCase;

    private ListarCaixinhasUseCase useCase;

    @BeforeEach
    void setUp() {
        useCase = new ListarCaixinhasUseCase(caixinhaRepository, calcularResumoFinanceiroUseCase);
    }

    @Test
    @DisplayName("Deve calcular patrimônio líquido total somando saldo em conta e caixinhas")
    void deveCalcularPatrimonioLiquidoTotal() {
        List<Caixinha> caixinhas = List.of(
                new Caixinha(1L, "Reserva de Emergência", new BigDecimal("1500.00"), TipoCaixinha.RESERVA_EMERGENCIA, new BigDecimal("15.00"), LocalDate.now()),
                new Caixinha(2L, "Fundo do Casal", new BigDecimal("1000.00"), TipoCaixinha.FUNDO_CASAL, new BigDecimal("10.00"), LocalDate.now())
        );
        when(caixinhaRepository.listarTodas()).thenReturn(caixinhas);

        ResumoFinanceiroResponse resumoMock = new ResumoFinanceiroResponse(
                new BigDecimal("1700.00"),
                new BigDecimal("2200.00"),
                new BigDecimal("500.00"), // saldo em conta = R$ 500,00
                20,
                LocalDate.of(2026, 8, 1),
                LocalDate.of(2026, 8, 31),
                Map.of()
        );
        when(calcularResumoFinanceiroUseCase.executar(null, null)).thenReturn(resumoMock);

        PatrimonioLiquidoResponse response = useCase.executar();

        assertThat(response).isNotNull();
        assertThat(response.saldoContaCorrente()).isEqualByComparingTo("500.00");
        assertThat(response.totalInvestidoCaixinhas()).isEqualByComparingTo("2500.00");
        assertThat(response.patrimonioLiquidoTotal()).isEqualByComparingTo("3000.00");
        assertThat(response.caixinhas()).hasSize(2);
    }
}
