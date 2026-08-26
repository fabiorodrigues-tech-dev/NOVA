package com.nova.agentefinanceiro.infrastructure.web.controller;

import com.nova.agentefinanceiro.application.dto.VoiceCommandRequest;
import com.nova.agentefinanceiro.application.dto.VoiceCommandResponse;
import com.nova.agentefinanceiro.application.usecase.ProcessarComandoVozUseCase;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Controller REST para processamento de comandos de voz do ecossistema NOVA.
 */
@RestController
@RequestMapping("/api/voice")
public class VoiceCommandController {

    private final ProcessarComandoVozUseCase processarComandoVozUseCase;

    public VoiceCommandController(ProcessarComandoVozUseCase processarComandoVozUseCase) {
        this.processarComandoVozUseCase = processarComandoVozUseCase;
    }

    @PostMapping("/command")
    public ResponseEntity<VoiceCommandResponse> processarComando(@RequestBody VoiceCommandRequest request) {
        VoiceCommandResponse response = processarComandoVozUseCase.executar(request);
        return ResponseEntity.ok(response);
    }
}
