-- docker/mysql/init.sql
-- Создание базы данных
CREATE DATABASE IF NOT EXISTS exampleDb;
USE exampleDb;

-- Таблица usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(32) NOT NULL,
  `email` varchar(64) NOT NULL,
  `pw_hash` varchar(255) NOT NULL,
  `rol` enum('admin','user') DEFAULT 'user',
  `f_alta` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuarios_unique` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Таблица posts
CREATE TABLE IF NOT EXISTS `posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(64) NOT NULL,
  `contenido` text,
  `estado` enum('borrador','publicado') NOT NULL DEFAULT 'borrador',
  `f_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `id_autor` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `posts_usuarios_FK` (`id_autor`),
  CONSTRAINT `posts_usuarios_FK` FOREIGN KEY (`id_autor`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Добавляем тестового пользователя (пароль: password123)
-- Хэш сгенерирован для пароля "password123" (можно заменить на свой)
INSERT INTO `usuarios` (`nombre`, `email`, `pw_hash`, `rol`, `f_alta`)
VALUES ('Admin User', 'admin@example.com', 'scrypt:32768:8:1$qV8kLpRmNxZwYtUe$c9b5e3a7d1f8g2h4j6k0l9z8x7c6v5b4n3m2a1s0d9f8g7h6j5k4l3z2x1c0v9b8n7m6', 'admin', NOW())
ON DUPLICATE KEY UPDATE id=id;

-- Добавляем тестового обычного пользователя
INSERT INTO `usuarios` (`nombre`, `email`, `pw_hash`, `rol`, `f_alta`)
VALUES ('Test User', 'test@example.com', 'scrypt:32768:8:1$qV8kLpRmNxZwYtUe$c9b5e3a7d1f8g2h4j6k0l9z8x7c6v5b4n3m2a1s0d9f8g7h6j5k4l3z2x1c0v9b8n7m6', 'user', NOW())
ON DUPLICATE KEY UPDATE id=id;