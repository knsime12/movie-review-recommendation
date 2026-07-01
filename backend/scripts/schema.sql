CREATE DATABASE IF NOT EXISTS cinefeel
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE cinefeel;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    genre VARCHAR(100),
    director VARCHAR(100),
    actors TEXT,
    release_date VARCHAR(50),
    overview TEXT,
    poster_url TEXT,
    rating DECIMAL(3,1) DEFAULT 0.0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uq_movies_title (title),
    INDEX idx_movies_title (title)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    content TEXT NOT NULL,
    sentiment VARCHAR(20),
    positive_prob FLOAT,
    expected_rating FLOAT,
    keywords TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uq_reviews_user_movie (user_id, movie_id),
    INDEX idx_reviews_user_id (user_id),
    INDEX idx_reviews_movie_id (movie_id),

    CONSTRAINT fk_reviews_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_reviews_movie
        FOREIGN KEY (movie_id)
        REFERENCES movies(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS recommendation_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    base_movie_id INT NOT NULL,
    recommended_movie_id INT NOT NULL,
    similarity FLOAT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uq_recommendation_history_user_movies (
        user_id,
        base_movie_id,
        recommended_movie_id
    ),
    INDEX idx_recommendation_history_user_id (user_id),
    INDEX idx_recommendation_history_base_movie_id (base_movie_id),
    INDEX idx_recommendation_history_recommended_movie_id (recommended_movie_id),

    CONSTRAINT fk_recommendation_history_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_recommendation_history_base_movie
        FOREIGN KEY (base_movie_id)
        REFERENCES movies(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_recommendation_history_recommended_movie
        FOREIGN KEY (recommended_movie_id)
        REFERENCES movies(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;