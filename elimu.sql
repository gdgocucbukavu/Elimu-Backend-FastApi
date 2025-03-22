-- Création de la base de données "elimu" avec le jeu de caractères UTF8MB4 pour un support complet d'Unicode
CREATE DATABASE IF NOT EXISTS elimu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE elimu;

-- ======================================================================
-- Création de la table "videos"
-- Cette table stocke les informations sur chaque vidéo.
-- Le champ `order` est entouré de backticks car "order" est un mot réservé SQL.
-- La colonne "stars" est conservée ici si vous souhaitez éventuellement stocker la note moyenne,
-- mais elle pourra être recalculée dynamiquement à partir des reviews.
-- ======================================================================
CREATE TABLE IF NOT EXISTS videos (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Identifiant unique de la vidéo
    youtube_url VARCHAR(255) NOT NULL UNIQUE,       -- URL YouTube (stocke uniquement l'ID dans le code) ; doit être unique
    mentor_email VARCHAR(100) NOT NULL,             -- Email du mentor associé à la vidéo
    category VARCHAR(100) NOT NULL,                 -- Catégorie de la vidéo (ex : tutoriel, entretien, etc.)
    title VARCHAR(255) NOT NULL,                    -- Titre de la vidéo
    description TEXT,                               -- Description de la vidéo
    publication_date DATETIME NOT NULL,             -- Date et heure de publication de la vidéo
    views INT DEFAULT 0,                            -- Nombre de vues
    likes INT DEFAULT 0,                            -- Nombre de likes
    stars FLOAT DEFAULT 0.0,                        -- Évaluation en étoiles (optionnelle si calculée dynamiquement)
    `order` INT NOT NULL                           -- Ordre d'affichage ; important pour le tri
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ======================================================================
-- Création de la table "progress"
-- Cette table suit la progression de visionnage pour chaque vidéo.
-- La clé étrangère (video_id) référence la table "videos" et est configurée avec ON DELETE CASCADE.
-- ======================================================================
CREATE TABLE IF NOT EXISTS progress (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Identifiant unique de la progression
    video_id INT NOT NULL,                          -- Référence à l'ID de la vidéo dans la table "videos"
    mentee_email VARCHAR(100) NOT NULL,             -- Email du mentee (utilisateur) suivant la vidéo
    watched INT DEFAULT 0,                          -- Quantité de vidéo visionnée (par exemple, en secondes ou en pourcentage)
    CONSTRAINT fk_video_progress FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ======================================================================
-- Création de la table "reviews"
-- Cette table stocke les avis laissés par les utilisateurs sur une vidéo.
-- Chaque avis contient une notation (stars), un commentaire, et une date de création.
-- La clé étrangère (video_id) référence la table "videos" et est configurée avec ON DELETE CASCADE.
-- ======================================================================
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Identifiant unique de la review
    video_id INT NOT NULL,                          -- Référence à l'ID de la vidéo dans la table "videos"
    mentee_email VARCHAR(100) NOT NULL,             -- Email du mentee (utilisateur) ayant laissé l'avis
    stars TINYINT NOT NULL,                         -- Note donnée à la vidéo (entre 1 et 5)
    comment TEXT,                                   -- Commentaire laissé par l'utilisateur (optionnel)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Date de création de l'avis
    CONSTRAINT fk_video_review FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ======================================================================
-- Création d'index pour optimiser les requêtes sur les emails
-- ======================================================================
CREATE INDEX idx_mentor_email ON videos(mentor_email);
CREATE INDEX idx_mentee_email_progress ON progress(mentee_email);
CREATE INDEX idx_mentee_email_reviews ON reviews(mentee_email);
