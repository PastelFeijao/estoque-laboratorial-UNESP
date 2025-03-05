-- Estrutura do banco de dados para estoque laboratorial.
DROP DATABASE IF EXISTS `estoque_laboratorio_db`;
CREATE DATABASE IF NOT EXISTS `estoque_laboratorio_db`;
USE `estoque_laboratorio_db`;

-- Estrutura para tabela de usuários.
DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) DEFAULT NULL,
  `email` VARCHAR(100) DEFAULT NULL,
  `senha` VARCHAR(255) DEFAULT NULL,
  `telefone` VARCHAR(11) DEFAULT NULL,
  `cpf` VARCHAR(11) NOT NULL,
  `cidade` VARCHAR(100) DEFAULT NULL,
  `nome_mae` VARCHAR(100) DEFAULT NULL,
  `nome_professor` VARCHAR(100) DEFAULT NULL,
  `ativo` INT(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_cpf` (`cpf`),
  UNIQUE KEY `UK_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Estrutura para tabela estoque.
DROP TABLE IF EXISTS `estoque`;
CREATE TABLE IF NOT EXISTS `estoque` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `produto` VARCHAR(100) DEFAULT NULL,
  `categoria` VARCHAR(100) DEFAULT NULL,
  `chegada` DATE DEFAULT NULL,
  `teste` INT(100) DEFAULT NULL,
  `lote` VARCHAR(100) DEFAULT NULL,
  `validade` DATE DEFAULT NULL,
  `estoque_final` INT(5) DEFAULT NULL,
  `obs` VARCHAR(500) DEFAULT NULL,
  `ativo` INT(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- Estrutura para tabela exames.
DROP TABLE IF EXISTS `exames`;
CREATE TABLE IF NOT EXISTS `exames` (
  `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nome_exame` VARCHAR(255) NOT NULL,
  `fitc` VARCHAR(255) NOT NULL,
  `quantidade1` INT(11) DEFAULT NULL,
  `pe` VARCHAR(255) NOT NULL,
  `quantidade2` INT(11) DEFAULT NULL,
  `ecd` VARCHAR(255) NOT NULL,
  `quantidade3` INT(11) DEFAULT NULL,
  `pc55` VARCHAR(255) NOT NULL,
  `quantidade4` INT(11) DEFAULT NULL,
  `pc7` VARCHAR(255) NOT NULL,
  `quantidade5` INT(11) DEFAULT NULL,
  `apc` VARCHAR(255) NOT NULL,
  `quantidade6` INT(11) DEFAULT NULL,
  `a700` VARCHAR(255) NOT NULL,
  `quantidade7` INT(11) DEFAULT NULL,
  `a750` VARCHAR(255) NOT NULL,
  `quantidade8` INT(11) DEFAULT NULL,
  `pb` VARCHAR(255) NOT NULL,
  `quantidade9` INT(11) DEFAULT NULL,
  `ko` VARCHAR(255) NOT NULL,
  `quantidade10` INT(11) DEFAULT NULL,
  `dupli_pe` VARCHAR(255) NOT NULL,
  `dupli1` INT(11) DEFAULT NULL,
  `dupli_a750` VARCHAR(255) NOT NULL,
  `dupli2` INT(11) DEFAULT NULL,
  `dupli_pb` VARCHAR(255) NOT NULL,
  `dupli3` INT(11) DEFAULT NULL,

  `ativo` INT(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

-- Estrutura para tabela pacientes.
DROP TABLE IF EXISTS `pacientes`;
CREATE TABLE IF NOT EXISTS `pacientes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nome` VARCHAR(100) DEFAULT NULL,
  `prontuario` INT(5) DEFAULT NULL,
  `id_laboratorio` VARCHAR(100) DEFAULT NULL,
  `quantia_teste` INT(5) DEFAULT NULL,
  `hip_diagnostica` VARCHAR(200) DEFAULT NULL,
  `obs` VARCHAR(500) DEFAULT NULL,
  `procedencia` VARCHAR(20) DEFAULT NULL,
  `exames` VARCHAR(250) DEFAULT NULL,
  `ativo` INT(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=UTF8MB4;

-- Estrutura para tabela despesas.
DROP TABLE IF EXISTS `despesas`;
CREATE TABLE IF NOT EXISTS `despesas` (
  `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `data` DATE DEFAULT NULL,
  `produtos` VARCHAR(100) DEFAULT NULL,
  `testes` INT(100) DEFAULT NULL,
  `lote` VARCHAR(100) DEFAULT NULL,
  `validade` DATE DEFAULT NULL,
  `quantia_frascos` INT(100) DEFAULT NULL,
  `quantia_final` INT(100) DEFAULT NULL,
  `comprador` VARCHAR(100) DEFAULT NULL,
  `faturamento` INT(100) DEFAULT NULL,
  `fonte_pagadora` VARCHAR(100) DEFAULT NULL,
  `valor_unitario` INT(100) DEFAULT NULL,
  `valor_total` INT(100) DEFAULT NULL,
  `numero_nota` VARCHAR(100) DEFAULT NULL,
  `data_nota` DATE DEFAULT NULL,
  `ativo` INT(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=UTF8MB4;

-- Estrutura para tabela configuracoes.
DROP TABLE IF EXISTS `configuracoes`;
CREATE TABLE configuracoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_acesso VARCHAR(10) NOT NULL
);

INSERT INTO configuracoes (codigo_acesso) VALUES ('0000'); -- Valor inicial
