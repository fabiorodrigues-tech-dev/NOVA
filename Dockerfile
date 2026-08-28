# ==============================================================================
# NOVA — Production Multi-Stage Dockerfile (Java 21 + Python 3.11 Runtime 24/7)
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build Spring Boot Microservice (Java 21)
# ------------------------------------------------------------------------------
FROM maven:3.9.6-eclipse-temurin-21 AS backend-builder
WORKDIR /build

# Cache dependencies
COPY java-services/agente-financeiro/pom.xml .
RUN mvn dependency:go-offline -B -q

# Build application JAR
COPY java-services/agente-financeiro/src ./src
RUN mvn clean package -DskipTests -B -q

# ------------------------------------------------------------------------------
# Stage 2: Final Unified Runtime (Java 21 + Python 3.11 + Web Dashboard)
# ------------------------------------------------------------------------------
FROM eclipse-temurin:21-jre-jammy

LABEL maintainer="Fábio Rodrigues <https://linkedin.com/in/fabiorodrigues-dev>"
LABEL description="NOVA Control Center — Production Multi-Agent Ecosystem"

# Install Python 3.11, pip, curl and utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies (Root + Voice requirements)
COPY requirements.txt ./requirements.txt
COPY voz/requirements.txt ./voz-requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy Spring Boot Executable JAR from builder stage
COPY --from=backend-builder /build/target/*.jar ./agente-financeiro.jar

# Copy Application Modules & Assets
COPY dashboard/ ./dashboard/
COPY voz/ ./voz/
COPY docs/ ./docs/
COPY carreira/ ./carreira/
COPY estudos/ ./estudos/
COPY financeiro/ ./financeiro/
COPY scripts/ ./scripts/
COPY entrypoint.sh ./entrypoint.sh

RUN chmod +x ./entrypoint.sh

# Production Environment Settings
ENV PORT=10000
ENV NOVA_PORT=10000
ENV SPRING_PROFILES_ACTIVE=default
ENV JAVA_OPTS="-Xms128m -Xmx384m -XX:+UseG1GC"

# Expose Web Traffic Port & Spring Boot Internal Port
EXPOSE 10000 8081

ENTRYPOINT ["/app/entrypoint.sh"]
