-- Run: mysql -u root -p < schema.sql
CREATE DATABASE IF NOT EXISTS covid_awareness_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE covid_awareness_db;

CREATE TABLE IF NOT EXISTS feedback (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  name       VARCHAR(100) NULL,
  email      VARCHAR(150) NULL,
  category   VARCHAR(50)  NOT NULL,
  message    TEXT         NOT NULL,
  created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;
