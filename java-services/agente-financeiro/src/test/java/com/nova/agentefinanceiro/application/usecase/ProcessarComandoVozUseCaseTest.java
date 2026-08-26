package com.nova.agentefinanceiro.application.usecase;

import com.nova.agentefinanceiro.application.dto.ResumoFinanceiroResponse;
import com.nova.agentefinanceiro.application.dto.TransacaoRequest;
import com.nova.agentefinanceiro.application.dto.TransacaoResponse;
import com.nova.agentefinanceiro.application.dto.VoiceCommandRequest;
import com.nova.agentefinanceiro.application.dto.VoiceCommandResponse;
import com.nova.agentefinanceiro.domain.model.CategoriaTransacao;
import com.nova.agentefinanceiro.domain.model.TipoTransacao;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("Testes do Caso de Uso: Processar Comando de Voz")
class ProcessarComandoVozUseCaseTest {

    @Mock
    private CalcularResumoFinanceiroUseCase calcularResumoUseCase;

    @Mock
    private CadastrarTransacaoUseCase cadastrarTransacaoUseCase;

    @InjectMocks
    private ProcessarComandoVozUseCase useCase;

    @Test
    @DisplayName("Deve processar consulta de saldo por voz com resposta natural")
    void deveProcessarConsultaDeSaldo() {
        ResumoFinanceiroResponse resumoMock = new ResumoFinanceiroResponse(
            new BigDecimal("1709.77"),
            new BigDecimal("2299.00"),
            new BigDecimal("589.23"),
            43,
            LocalDate.of(2026, 8, 1),
            LocalDate.of(2026, 8, 31),
            Map.of(CategoriaTransacao.ALIMENTACAO, new BigDecimal("645.00"))
        );

        when(calcularResumoUseCase.executar(null, null)).thenReturn(resumoMock);

        VoiceCommandRequest request = new VoiceCommandRequest("NOVA, qual é o meu saldo atual?");
        VoiceCommandResponse response = useCase.executar(request);

        assertThat(response).isNotNull();
        assertThat(response.status()).isEqualTo("SUCESSO");
        assertThat(response.mensagemVoz()).contains("R$ 589,23").contains("43 lançamentos");
    }

    @Test
    @DisplayName("Deve processar consulta de gastos por categoria")
    void deveProcessarConsultaGastosCategoria() {
        ResumoFinanceiroResponse resumoMock = new ResumoFinanceiroResponse(
            new BigDecimal("1709.77"),
            new BigDecimal("2299.00"),
            new BigDecimal("589.23"),
            43,
            LocalDate.of(2026, 8, 1),
            LocalDate.of(2026, 8, 31),
            Map.of(CategoriaTransacao.ALIMENTACAO, new BigDecimal("645.00"))
        );

        when(calcularResumoUseCase.executar(null, null)).thenReturn(resumoMock);

        VoiceCommandRequest request = new VoiceCommandRequest("quanto gastei em alimentacao?");
        VoiceCommandResponse response = useCase.executar(request);

        assertThat(response).isNotNull();
        assertThat(response.status()).isEqualTo("SUCESSO");
        assertThat(response.mensagemVoz()).contains("R$ 645,00").contains("alimentacao");
    }

    @Test
    @DisplayName("Deve processar comando de ajuda e identidade do NOVA")
    void deveProcessarComandoIdentidade() {
        VoiceCommandRequest request = new VoiceCommandRequest("NOVA, quem é você?");
        VoiceCommandResponse response = useCase.executar(request);

        assertThat(response).isNotNull();
        assertThat(response.status()).isEqualTo("SUCESSO");
        assertThat(response.mensagemVoz()).contains("Sou o NOVA");
    }

    @Test
    @DisplayName("Deve retornar erro amigável para comando vazio")
    void deveTratarComandoVazio() {
        VoiceCommandRequest request = new VoiceCommandRequest("   ");
        VoiceCommandResponse response = useCase.executar(request);

        assertThat(response).isNotNull();
        assertThat(response.status()).isEqualTo("ERRO");
        assertThat(response.mensagemVoz()).contains("Não entendi");
    }
}
