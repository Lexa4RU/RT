-- Création de la table des semestres
CREATE TABLE Semestres (
	code_semestre VARCHAR(10) PRIMARY KEY,
	nom_semestre VARCHAR(50) NOT NULL
);

-- Insertion des semestres
INSERT INTO Semestres (code_semestre, nom_semestre)
VALUES
('S1', 'Semestre 1'),
('S2', 'Semestre 2');

-- Création de la table des blocs de compétences
CREATE TABLE BlocsCompetences (
	code_bloc VARCHAR(10) PRIMARY KEY,
	nom_bloc VARCHAR(100) NOT NULL,
	code_semestre VARCHAR(10),
	FOREIGN KEY (code_semestre) REFERENCES Semestres(code_semestre)
);

-- Insertion des blocs de compétences
INSERT INTO BlocsCompetences (code_bloc, nom_bloc, code_semestre)
VALUES
('B1', 'Administrer', 'S1'),
('B2', 'Connecter', 'S1'),
('B3', 'Programmer', 'S1'),
('B4', 'Administrer', 'S2'),
('B5', 'Connecter', 'S2'),
('B6', 'Programmer', 'S2');

-- Création de la table des compétences
CREATE TABLE Competences (
	code_competence VARCHAR(15) PRIMARY KEY,
	nom_competence VARCHAR(200) NOT NULL,
	code_bloc VARCHAR(10),
	FOREIGN KEY (code_bloc) REFERENCES BlocsCompetences(code_bloc)
);

-- Insertion des compétences
INSERT INTO Competences (code_competence, nom_competence, code_bloc) 
VALUES
('AC11.01', 'Maitriser les lois fondamentales de l''électricité afin d''intervenir sur des équipements de réseaux et télécommunications', 'B1'),
('AC11.02', 'Comprendre l''architecture et les fondements des systèmes numériques, les principes du codage de l''information, des communications et de l''internet', 'B1'),
('AC11.03', 'Configurer les fonctions de base du réseau local', 'B1'),
('AC11.04', 'Maîtriser les rôles et les principes fondamentaux des systèmes d''exploitation afin d''interagir avec ceux-ci pour la configuration et l''administration des réseaux et services fournis', 'B1'),
('AC11.05', 'Identifier les dysfonctionnements du réseau local et savoir les signaler', 'B4'),
('AC11.06', 'Installer un poste client, expliquer la procédure mise en place', 'B4'),
('AC12.01', 'Mesurer, analyser et commenter les signaux', 'B2'),
('AC12.02', 'Caractériser des systèmes de transmissions élémentaires et découvrir la modélisation mathématique de leur fonctionnement', 'B2'),
('AC12.03', 'Déployer des supports de transmission', 'B5'),
('AC12.04', 'Connecter les systèmes de ToIP', 'B5'),
('AC12.05', 'Communiquer avec un tiers (client, collaborateur...) et adapter son discours et sa langue à son interlocuteur', 'B5'),
('AC13.01', 'Utiliser un système informatique et ses outils', 'B3'),
('AC13.02', 'Lire, exécuter, corriger et modifier un programme', 'B3'),
('AC13.03', 'Traduire un algorithme, dans un langage et pour un environnement donné', 'B3'),
('AC13.04', 'Connaître l''architecture et les technologies d''un site Web', 'B6'),
('AC13.05', 'Choisir les mécanismes de gestion de données adaptés au développement de l''outil et argumenter ses choix', 'B6'),
('AC13.06', 'S''intégrer dans un environnement propice au développement et au travail collaboratif', 'B6');

-- Création de la table des niveaux d'acquisition
CREATE TABLE NiveauxAcquisition (
	code_acquisition SERIAL PRIMARY KEY,
	code_competence VARCHAR(10),
	niveau_acquisition VARCHAR(50) NOT NULL,
	FOREIGN KEY (code_competence) REFERENCES Competences(code_competence)
);

-- Insertion des niveaux d'acquisition
INSERT INTO NiveauxAcquisition (code_competence, niveau_acquisition)
VALUES
('AC11.01', 'En cours d''acquisition'),
('AC11.02', 'Acquis'),
('AC11.03', 'Presque acquis'),
('AC11.04', 'Acquis'),
('AC11.05', 'Acquis'),
('AC11.06', 'Acquis'),
('AC12.01', 'Acquis'),
('AC12.02', 'Presque acquis'),
('AC12.03', 'Acquis'),
('AC12.04', 'En cours d''acquisition'),
('AC12.05', 'Acquis'),
('AC13.01', 'Expert'),
('AC13.02', 'Expert'),
('AC13.03', 'Acquis'),
('AC13.04', 'Acquis'),
('AC13.05', 'En cours d''acquisition'),
('AC13.06', 'Expert');

-- Création de la table des utilisateurs
CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(50) NOT NULL,
	password VARCHAR(100) NOT NULL
);

-- Insertion des utilisateurs
INSERT INTO users (username, password) VALUES ('lev', SHA2('progtr00', 256));