-- Création de la base de données
CREATE DATABASE IF NOT EXISTS elimu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE elimu;

-- Création de la table des vidéos
CREATE TABLE IF NOT EXISTS videos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    youtube_url VARCHAR(255) NOT NULL UNIQUE,
    mentor_email VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    publication_date DATETIME NOT NULL,
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    stars FLOAT DEFAULT 0.0
);

-- Création de la table de suivi de progression
CREATE TABLE IF NOT EXISTS progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    video_id INT NOT NULL,
    mentee_email VARCHAR(100) NOT NULL,
    watched INT DEFAULT 0,
    FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE
);

-- Création d'un index pour optimiser les requêtes sur les emails
CREATE INDEX idx_mentor_email ON videos(mentor_email);
CREATE INDEX idx_mentee_email ON progress(mentee_email);
