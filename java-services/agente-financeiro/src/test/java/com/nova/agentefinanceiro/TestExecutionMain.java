package com.nova.agentefinanceiro;

import org.junit.platform.launcher.Launcher;
import org.junit.platform.launcher.LauncherDiscoveryRequest;
import org.junit.platform.launcher.core.LauncherDiscoveryRequestBuilder;
import org.junit.platform.launcher.core.LauncherFactory;
import org.junit.platform.launcher.listeners.SummaryGeneratingListener;
import org.junit.platform.launcher.listeners.TestExecutionSummary;

import java.io.PrintWriter;

import static org.junit.platform.engine.discovery.DiscoverySelectors.selectPackage;

public class TestExecutionMain {

    public static void main(String[] args) {
        LauncherDiscoveryRequest request = LauncherDiscoveryRequestBuilder.request()
                .selectors(selectPackage("com.nova.agentefinanceiro"))
                .build();

        Launcher launcher = LauncherFactory.create();
        SummaryGeneratingListener listener = new SummaryGeneratingListener();
        launcher.registerTestExecutionListeners(listener);

        launcher.execute(request);

        TestExecutionSummary summary = listener.getSummary();
        summary.printTo(new PrintWriter(System.out));

        long total = summary.getTestsFoundCount();
        long passed = summary.getTestsSucceededCount();
        long failed = summary.getTestsFailedCount();
        long skipped = summary.getTestsSkippedCount();

        System.out.println("\n==========================================");
        System.out.println("📊 RELATÓRIO DE EXECUÇÃO DE TESTES (NOVA)");
        System.out.println("==========================================");
        System.out.println("Total de Testes Encontrados: " + total);
        System.out.println("✅ Testes que Passaram:      " + passed);
        System.out.println("❌ Testes que Falharam:      " + failed);
        System.out.println("⏭️ Testes Ignorados:         " + skipped);
        System.out.println("⏱️ Tempo Total de Execução:  " + summary.getTimeFinished() + "ms");
        System.out.println("==========================================");

        if (failed > 0) {
            System.err.println("\nDetalhes das Falhas:");
            summary.getFailures().forEach(failure -> {
                System.err.println("- " + failure.getTestIdentifier().getDisplayName() + ": " + failure.getException().getMessage());
            });
            System.exit(1);
        } else {
            System.out.println("🎉 TODOS OS TESTES PASSARAM COM SUCESSO!");
            System.exit(0);
        }
    }
}
