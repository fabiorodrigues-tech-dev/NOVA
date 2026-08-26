package com.nova.agentefinanceiro.infrastructure.config;

import com.nova.agentefinanceiro.infrastructure.mcp.FinanceiroMcpTools;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Configuração e registro do provedor de ferramentas MCP.
 */
@Configuration
public class McpConfiguration {

    @Bean
    public ToolCallbackProvider financeiroToolCallbackProvider(FinanceiroMcpTools financeiroMcpTools) {
        return MethodToolCallbackProvider.builder()
                .toolObjects(financeiroMcpTools)
                .build();
    }
}
