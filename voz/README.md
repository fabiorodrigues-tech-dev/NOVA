# 🎙️ Camada de Voz Neural do Ecossistema NOVA (Voice AI Layer)

Este módulo implementa a interface de comunicação por voz bidirecional do **NOVA**, integrando captura por microfone, processamento semântico no Spring Boot e **síntese neural humana de alta fidelidade** (`edge-tts` + `afplay` nativo do macOS).

---

## 🏛️ 1. Arquitetura do Pipeline de Voz Neural

```text
[ Microfone do Usuário ]
          │ (Áudio PCM / 16kHz)
          ▼
[ Speech-To-Text (STT) ] ──────────► Transcrição em Texto ("NOVA, qual o meu saldo?")
          │
          ▼
[ NOVA Voice Bridge (Python) ] ────► Requisição REST HTTP (POST /api/voice/command)
          │
          ▼
[ Microsserviço Java 21 / Spring Boot 3 ]
  ├── ProcessarComandoVozUseCase (Interpretação Semântica & Intenção)
  ├── Casos de Uso de Domínio (CalcularResumo / CadastrarTransacao)
  └── Banco H2 Persistente (ACID)
          │
          ▼
[ Resposta Estruturada ] ──────────► JSON: { "mensagemVoz": "Seu saldo é...", "status": "SUCESSO" }
          │
          ▼
[ Motor Neural edge-tts ] ─────────► Geração de Áudio MP3 em 24kHz (pt-BR-AntonioNeural / pt-BR-FranciscaNeural)
          │
          ▼
[ Player Nativo afplay (macOS) ] ──► Reprodução com Som Cristalino e Baixa Latência
          │
          ▼
[ Alto-falantes do Mac ]
```

---

## 🎭 2. Vozes Neurais Disponíveis

| Alias | Identificador Oficial | Descrição e Tom |
| :--- | :--- | :--- |
| **`antonio` (Padrão)** | `pt-BR-AntonioNeural` | Voz executiva masculina natural, sóbria e articulada. |
| **`francisca`** | `pt-BR-FranciscaNeural` | Voz executiva feminina natural, fluida e clara. |
| **`thalita`** | `pt-BR-ThalitaNeural` | Voz jovem dinâmica em tom coloquial. |

---

## 🚀 3. Modos de Uso do `nova_voice_bridge.py`

### 🔹 Modo 1: Consulta por Comando de Texto (com resposta falada neural)
```bash
# Voz padrão (Antônio)
python3 voz/scripts/nova_voice_bridge.py --texto "NOVA, qual é o meu saldo atual?"

# Voz feminina (Francisca)
python3 voz/scripts/nova_voice_bridge.py --texto "quanto gastei em alimentação?" --voz francisca
```

### 🔹 Modo 2: Interação Contínua por Microfone
```bash
python3 voz/scripts/nova_voice_bridge.py --escutar
```

### 🔹 Modo 3: Teste de Fala Direta
```bash
python3 voz/scripts/nova_voice_bridge.py --falar "Olá, Fábio! O motor de voz neural humana do NOVA está operacional."
```
