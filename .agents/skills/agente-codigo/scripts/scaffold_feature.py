#!/usr/bin/env python3
"""
Scaffolding Generator para Clean Architecture (Java 21 + Spring Boot 3)
Ecossistema NOVA - Agente Código

Gera a estrutura completa de uma feature seguindo Clean Architecture:
- Domain (Model, Repository Port, Exceptions)
- Application (DTOs records, UseCases)
- Infrastructure (JPA Entity, Spring Data, Mapper, REST Controller)
- Tests (JUnit 5 + Mockito)
"""

import os
import sys
import argparse
from pathlib import Path

def generate_feature(feature_name: str, base_package: str, output_dir: str):
    cap_feature = feature_name[0].upper() + feature_name[1:]
    lower_feature = feature_name.lower()
    plural_lower = lower_feature + "s"
    
    package_path = base_package.replace(".", "/")
    src_main_java = Path(output_dir) / "src" / "main" / "java" / package_path
    src_test_java = Path(output_dir) / "src" / "test" / "java" / package_path

    # Directories
    dirs = [
        src_main_java / "domain" / "model",
        src_main_java / "domain" / "repository",
        src_main_java / "domain" / "exception",
        src_main_java / "application" / "dto",
        src_main_java / "application" / "usecase",
        src_main_java / "infrastructure" / "persistence" / "entity",
        src_main_java / "infrastructure" / "persistence" / "repository",
        src_main_java / "infrastructure" / "persistence" / "mapper",
        src_main_java / "infrastructure" / "web" / "controller",
        src_test_java / "application" / "usecase"
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    files = {}

    # 1. Domain Model
    files[src_main_java / "domain" / "model" / f"{cap_feature}.java"] = f"""package {base_package}.domain.model;

import java.time.LocalDateTime;

/**
 * Modelo de domínio puro para {cap_feature}.
 * 100% isolado de dependências de persistência ou web.
 */
public class {cap_feature} {{

    private Long id;
    private String nome;
    private String descricao;
    private LocalDateTime criadoEm;

    public {cap_feature}() {{
        this.criadoEm = LocalDateTime.now();
    }}

    public {cap_feature}(Long id, String nome, String descricao) {{
        this.id = id;
        this.nome = nome;
        this.descricao = descricao;
        this.criadoEm = LocalDateTime.now();
    }}

    public Long getId() {{
        return id;
    }}

    public void setId(Long id) {{
        this.id = id;
    }}

    public String getNome() {{
        return nome;
    }}

    public void setNome(String nome) {{
        this.nome = nome;
    }}

    public String getDescricao() {{
        return descricao;
    }}

    public void setDescricao(String descricao) {{
        this.descricao = descricao;
    }}

    public LocalDateTime getCriadoEm() {{
        return criadoEm;
    }}
}}
"""

    # 2. Domain Repository (Port)
    files[src_main_java / "domain" / "repository" / f"{cap_feature}Repository.java"] = f"""package {base_package}.domain.repository;

import {base_package}.domain.model.{cap_feature};
import java.util.List;
import java.util.Optional;

/**
 * Porta de saída (Port) do domínio para persistência de {cap_feature}.
 */
public interface {cap_feature}Repository {{
    {cap_feature} salvar({cap_feature} {lower_feature});
    Optional<{cap_feature}> buscarPorId(Long id);
    List<{cap_feature}> listarTodos();
    void deletarPorId(Long id);
}}
"""

    # 3. Domain Exception
    files[src_main_java / "domain" / "exception" / f"{cap_feature}NaoEncontradoException.java"] = f"""package {base_package}.domain.exception;

public class {cap_feature}NaoEncontradoException extends RuntimeException {{
    public {cap_feature}NaoEncontradoException(Long id) {{
        super("{cap_feature} com ID " + id + " não foi encontrado.");
    }}
}}
"""

    # 4. Application DTOs (Records Java 21)
    files[src_main_java / "application" / "dto" / f"{cap_feature}Request.java"] = f"""package {base_package}.application.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/**
 * DTO imutável (Java 21 record) para criação/atualização de {cap_feature}.
 */
public record {cap_feature}Request(
    @NotBlank(message = "O nome é obrigatório")
    @Size(min = 3, max = 100, message = "O nome deve ter entre 3 e 100 caracteres")
    String nome,

    @Size(max = 255, message = "A descrição não pode exceder 255 caracteres")
    String descricao
) {{}}
"""

    files[src_main_java / "application" / "dto" / f"{cap_feature}Response.java"] = f"""package {base_package}.application.dto;

import {base_package}.domain.model.{cap_feature};
import java.time.LocalDateTime;

/**
 * DTO imutável (Java 21 record) de saída para {cap_feature}.
 */
public record {cap_feature}Response(
    Long id,
    String nome,
    String descricao,
    LocalDateTime criadoEm
) {{
    public static {cap_feature}Response fromDomain({cap_feature} {lower_feature}) {{
        return new {cap_feature}Response(
            {lower_feature}.getId(),
            {lower_feature}.getNome(),
            {lower_feature}.getDescricao(),
            {lower_feature}.getCriadoEm()
        );
    }}
}}
"""

    # 5. Application Use Cases
    files[src_main_java / "application" / "usecase" / f"Criar{cap_feature}UseCase.java"] = f"""package {base_package}.application.usecase;

import {base_package}.application.dto.{cap_feature}Request;
import {base_package}.application.dto.{cap_feature}Response;
import {base_package}.domain.model.{cap_feature};
import {base_package}.domain.repository.{cap_feature}Repository;
import org.springframework.stereotype.Service;

/**
 * Caso de uso: Criação de {cap_feature}.
 */
@Service
public class Criar{cap_feature}UseCase {{

    private final {cap_feature}Repository {lower_feature}Repository;

    public Criar{cap_feature}UseCase({cap_feature}Repository {lower_feature}Repository) {{
        this.{lower_feature}Repository = {lower_feature}Repository;
    }}

    public {cap_feature}Response executar({cap_feature}Request request) {{
        {cap_feature} {lower_feature} = new {cap_feature}(null, request.nome(), request.descricao());
        {cap_feature} salvo = {lower_feature}Repository.salvar({lower_feature});
        return {cap_feature}Response.fromDomain(salvo);
    }}
}}
"""

    files[src_main_java / "application" / "usecase" / f"Buscar{cap_feature}UseCase.java"] = f"""package {base_package}.application.usecase;

import {base_package}.application.dto.{cap_feature}Response;
import {base_package}.domain.exception.{cap_feature}NaoEncontradoException;
import {base_package}.domain.repository.{cap_feature}Repository;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Caso de uso: Busca e listagem de {cap_feature}.
 */
@Service
public class Buscar{cap_feature}UseCase {{

    private final {cap_feature}Repository {lower_feature}Repository;

    public Buscar{cap_feature}UseCase({cap_feature}Repository {lower_feature}Repository) {{
        this.{lower_feature}Repository = {lower_feature}Repository;
    }}

    public {cap_feature}Response porId(Long id) {{
        return {lower_feature}Repository.buscarPorId(id)
                .map({cap_feature}Response::fromDomain)
                .orElseThrow(() -> new {cap_feature}NaoEncontradoException(id));
    }}

    public List<{cap_feature}Response> listarTodos() {{
        return {lower_feature}Repository.listarTodos().stream()
                .map({cap_feature}Response::fromDomain)
                .toList();
    }}
}}
"""

    # 6. Infrastructure JPA Entity
    files[src_main_java / "infrastructure" / "persistence" / "entity" / f"{cap_feature}JpaEntity.java"] = f"""package {base_package}.infrastructure.persistence.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "tb_{plural_lower}")
public class {cap_feature}JpaEntity {{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String nome;

    @Column(length = 255)
    private String descricao;

    @Column(nullable = false, updatable = false)
    private LocalDateTime criadoEm;

    public {cap_feature}JpaEntity() {{
        this.criadoEm = LocalDateTime.now();
    }}

    public {cap_feature}JpaEntity(Long id, String nome, String descricao) {{
        this.id = id;
        this.nome = nome;
        this.descricao = descricao;
        this.criadoEm = LocalDateTime.now();
    }}

    public Long getId() {{
        return id;
    }}

    public void setId(Long id) {{
        this.id = id;
    }}

    public String getNome() {{
        return nome;
    }}

    public void setNome(String nome) {{
        this.nome = nome;
    }}

    public String getDescricao() {{
        return descricao;
    }}

    public void setDescricao(String descricao) {{
        this.descricao = descricao;
    }}

    public LocalDateTime getCriadoEm() {{
        return criadoEm;
    }}
}}
"""

    # 7. Infrastructure Mapper
    files[src_main_java / "infrastructure" / "persistence" / "mapper" / f"{cap_feature}Mapper.java"] = f"""package {base_package}.infrastructure.persistence.mapper;

import {base_package}.domain.model.{cap_feature};
import {base_package}.infrastructure.persistence.entity.{cap_feature}JpaEntity;
import org.springframework.stereotype.Component;

@Component
public class {cap_feature}Mapper {{

    public {cap_feature} toDomain({cap_feature}JpaEntity entity) {{
        if (entity == null) return null;
        return new {cap_feature}(entity.getId(), entity.getNome(), entity.getDescricao());
    }}

    public {cap_feature}JpaEntity toEntity({cap_feature} domain) {{
        if (domain == null) return null;
        return new {cap_feature}JpaEntity(domain.getId(), domain.getNome(), domain.getDescricao());
    }}
}}
"""

    # 8. Infrastructure Repository Adapter
    files[src_main_java / "infrastructure" / "persistence" / "repository" / f"SpringData{cap_feature}Repository.java"] = f"""package {base_package}.infrastructure.persistence.repository;

import {base_package}.infrastructure.persistence.entity.{cap_feature}JpaEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SpringData{cap_feature}Repository extends JpaRepository<{cap_feature}JpaEntity, Long> {{
}}
"""

    files[src_main_java / "infrastructure" / "persistence" / "repository" / f"{cap_feature}RepositoryImpl.java"] = f"""package {base_package}.infrastructure.persistence.repository;

import {base_package}.domain.model.{cap_feature};
import {base_package}.domain.repository.{cap_feature}Repository;
import {base_package}.infrastructure.persistence.entity.{cap_feature}JpaEntity;
import {base_package}.infrastructure.persistence.mapper.{cap_feature}Mapper;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public class {cap_feature}RepositoryImpl implements {cap_feature}Repository {{

    private final SpringData{cap_feature}Repository springDataRepository;
    private final {cap_feature}Mapper mapper;

    public {cap_feature}RepositoryImpl(SpringData{cap_feature}Repository springDataRepository, {cap_feature}Mapper mapper) {{
        this.springDataRepository = springDataRepository;
        this.mapper = mapper;
    }}

    @Override
    public {cap_feature} salvar({cap_feature} {lower_feature}) {{
        {cap_feature}JpaEntity entity = mapper.toEntity({lower_feature});
        {cap_feature}JpaEntity salva = springDataRepository.save(entity);
        return mapper.toDomain(salva);
    }}

    @Override
    public Optional<{cap_feature}> buscarPorId(Long id) {{
        return springDataRepository.findById(id).map(mapper::toDomain);
    }}

    @Override
    public List<{cap_feature}> listarTodos() {{
        return springDataRepository.findAll().stream().map(mapper::toDomain).toList();
    }}

    @Override
    public void deletarPorId(Long id) {{
        springDataRepository.deleteById(id);
    }}
}}
"""

    # 9. Infrastructure Web Controller
    files[src_main_java / "infrastructure" / "web" / "controller" / f"{cap_feature}Controller.java"] = f"""package {base_package}.infrastructure.web.controller;

import {base_package}.application.dto.{cap_feature}Request;
import {base_package}.application.dto.{cap_feature}Response;
import {base_package}.application.usecase.Buscar{cap_feature}UseCase;
import {base_package}.application.usecase.Criar{cap_feature}UseCase;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/{plural_lower}")
public class {cap_feature}Controller {{

    private final Criar{cap_feature}UseCase criarUseCase;
    private final Buscar{cap_feature}UseCase buscarUseCase;

    public {cap_feature}Controller(Criar{cap_feature}UseCase criarUseCase, Buscar{cap_feature}UseCase buscarUseCase) {{
        this.criarUseCase = criarUseCase;
        this.buscarUseCase = buscarUseCase;
    }}

    @PostMapping
    public ResponseEntity<{cap_feature}Response> criar(@Valid @RequestBody {cap_feature}Request request) {{
        {cap_feature}Response response = criarUseCase.executar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }}

    @GetMapping("/{{id}}")
    public ResponseEntity<{cap_feature}Response> buscarPorId(@PathVariable Long id) {{
        return ResponseEntity.ok(buscarUseCase.porId(id));
    }}

    @GetMapping
    public ResponseEntity<List<{cap_feature}Response>> listarTodos() {{
        return ResponseEntity.ok(buscarUseCase.listarTodos());
    }}
}}
"""

    # 10. Unit Test (JUnit 5 + Mockito)
    files[src_test_java / "application" / "usecase" / f"Criar{cap_feature}UseCaseTest.java"] = f"""package {base_package}.application.usecase;

import {base_package}.application.dto.{cap_feature}Request;
import {base_package}.application.dto.{cap_feature}Response;
import {base_package}.domain.model.{cap_feature};
import {base_package}.domain.repository.{cap_feature}Repository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class Criar{cap_feature}UseCaseTest {{

    @Mock
    private {cap_feature}Repository {lower_feature}Repository;

    @InjectMocks
    private Criar{cap_feature}UseCase criarUseCase;

    @Test
    @DisplayName("Deve criar {cap_feature} com sucesso a partir de um request válido")
    void deveCriar{cap_feature}ComSucesso() {{
        // Arrange
        {cap_feature}Request request = new {cap_feature}Request("Exemplo {cap_feature}", "Descrição detalhada");
        {cap_feature} {lower_feature}Salvo = new {cap_feature}(1L, request.nome(), request.descricao());

        when({lower_feature}Repository.salvar(any({cap_feature}.class))).thenReturn({lower_feature}Salvo);

        // Act
        {cap_feature}Response response = criarUseCase.executar(request);

        // Assert
        assertNotNull(response);
        assertEquals(1L, response.id());
        assertEquals("Exemplo {cap_feature}", response.nome());
        verify({lower_feature}Repository, times(1)).salvar(any({cap_feature}.class));
    }}
}}
"""

    # Write files
    created_files = []
    for file_path, content in files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        created_files.append(str(file_path))

    print(f"✨ Feature '{cap_feature}' gerada com sucesso em '{output_dir}'!")
    print(f"📁 Total de arquivos gerados: {len(created_files)}")
    for cf in created_files:
        print(f"  ├── {cf}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean Architecture Scaffolding Generator (Java 21 + Spring Boot 3)")
    parser.add_argument("--feature", required=True, help="Nome da entidade/feature (ex: Cliente, Produto, Meta)")
    parser.add_argument("--base-package", default="com.nova", help="Pacote base (ex: com.nova.catalogo)")
    parser.add_argument("--output-dir", default=".", help="Diretório raiz de destino")

    args = parser.parse_args()
    generate_feature(args.feature, args.base_package, args.output_dir)
