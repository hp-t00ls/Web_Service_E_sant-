-- Recreate the database
CREATE DATABASE IF NOT EXISTS `pascalh_SEV5206E`;
USE `pascalh_SEV5206E`;

-- Table des catégories d'utilisateur
CREATE TABLE `Categorie_Utilisateur` (
  `Id_Categorie_Utilisateur` INT(11) NOT NULL AUTO_INCREMENT,
  `Libelle_Categorie_Utilisateur` VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (`Id_Categorie_Utilisateur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `Categorie_Utilisateur` (`Id_Categorie_Utilisateur`, `Libelle_Categorie_Utilisateur`) VALUES
(1, 'Patient'),
(2, 'Médecin'),
(3, 'Administrateur');

-- Table des droits utilisateur
CREATE TABLE `Droit_Utilisateur` (
  `Id_Droit` VARCHAR(50) NOT NULL,
  `Libelle_Droit` VARCHAR(50) DEFAULT NULL,
  `Methode_HTTP` VARCHAR(6) NOT NULL,
  PRIMARY KEY (`Id_Droit`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `Droit_Utilisateur` (`Id_Droit`, `Libelle_Droit`, `Methode_HTTP`) VALUES
('C', 'Création', 'POST'),
('R', 'Lecture', 'GET'),
('U', 'Mise à jour', 'PUT'),
('D', 'Suppression', 'DELETE');

-- Table des droits associés aux catégories utilisateur
CREATE TABLE `Droit_Categorie_Utilisateur` (
  `Id_Categorie_Utilisateur` INT(11) NOT NULL,
  `Id_Droit` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`Id_Categorie_Utilisateur`, `Id_Droit`),
  FOREIGN KEY (`Id_Categorie_Utilisateur`) REFERENCES `Categorie_Utilisateur` (`Id_Categorie_Utilisateur`),
  FOREIGN KEY (`Id_Droit`) REFERENCES `Droit_Utilisateur` (`Id_Droit`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `Droit_Categorie_Utilisateur` (`Id_Categorie_Utilisateur`, `Id_Droit`) VALUES
(1, 'R'),
(2, 'R'),
(2, 'U'),
(3, 'C'),
(3, 'D'),
(3, 'R'),
(3, 'U');

-- Table des utilisateurs
CREATE TABLE `Utilisateur` (
  `Id_Utilisateur` INT(11) NOT NULL AUTO_INCREMENT,
  `Nom_Utilisateur` VARCHAR(50) NOT NULL,
  `Mot_de_passe` VARCHAR(255) NOT NULL,
  `Login_Utilisateur` VARCHAR(50) NOT NULL,
  `INS` VARCHAR(50) DEFAULT NULL,
  `Id_Categorie_Utilisateur` INT(11) NOT NULL,
  PRIMARY KEY (`Id_Utilisateur`),
  UNIQUE (`Login_Utilisateur`),
  FOREIGN KEY (`Id_Categorie_Utilisateur`) REFERENCES `Categorie_Utilisateur` (`Id_Categorie_Utilisateur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `Utilisateur` (`Id_Utilisateur`, `Nom_Utilisateur`, `Mot_de_passe`, `Login_Utilisateur`, `INS`, `Id_Categorie_Utilisateur`) VALUES
(1, 'Dupont', PASSWORD('password1'), 'jdupont', '1111111111', 1),
(2, 'Martin', PASSWORD('password2'), 'mmartin', NULL, 2),
(3, 'Durand', PASSWORD('password3'), 'pdurand', NULL, 2),
(4, 'Admin', PASSWORD('password4'), 'admin', NULL, 3),
(5, 'Lefevre', PASSWORD('password5'), 'slefevre', '2222222222', 1);

-- Table des médecins
CREATE TABLE `Medecin` (
  `Id_Utilisateur` INT(11) NOT NULL,
  `RPPS` VARCHAR(50) NOT NULL,
  `Prenom_Medecin` VARCHAR(50) DEFAULT NULL,
  `Sexe` VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (`Id_Utilisateur`),
  FOREIGN KEY (`Id_Utilisateur`) REFERENCES `Utilisateur` (`Id_Utilisateur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `Medecin` (`Id_Utilisateur`, `RPPS`, `Prenom_Medecin`, `Sexe`) VALUES
(2, '123456789', 'Marie', 'F'),
(3, '987654321', 'Pierre', 'M');

-- Table des patients
CREATE TABLE `Patient` (
  `Id_Utilisateur` INT(11) NOT NULL,
  `INS` VARCHAR(50) NOT NULL,
  `Sexe_Patient` VARCHAR(50) DEFAULT NULL,
  `Prenom_Patient` VARCHAR(50) DEFAULT NULL,
  `Date_Naissance_Patient` DATE DEFAULT NULL,
  `Id_Medecin` INT(11) DEFAULT NULL,
  PRIMARY KEY (`Id_Utilisateur`),
  FOREIGN KEY (`Id_Utilisateur`) REFERENCES `Utilisateur` (`Id_Utilisateur`),
  FOREIGN KEY (`Id_Medecin`) REFERENCES `Medecin` (`Id_Utilisateur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `Patient` (`Id_Utilisateur`, `INS`, `Sexe_Patient`, `Prenom_Patient`, `Date_Naissance_Patient`, `Id_Medecin`) VALUES
(1, '1111111111', 'M', 'Jean', '1980-01-01', 2),
(5, '2222222222', 'F', 'Sophie', '1990-02-02', 3);

-- Table des codes LOINC
CREATE TABLE `Examen_Biologie` (
  `LOINC_Code` VARCHAR(50) NOT NULL,
  `Libelle_Examen_Biologie` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`LOINC_Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `Examen_Biologie` (`LOINC_Code`, `Libelle_Examen_Biologie`) VALUES
('718-7', 'Hémogramme - Numération des globules rouges'),
('4544-3', 'Hémogramme - Taux d’hématocrite'),
('2339-0', 'Glycémie - Taux de glucose sanguin'),
('2093-3', 'Cholestérol - Taux de cholestérol total');

-- Table des résultats des examens
CREATE TABLE `Resultat_Examen` (
  `Id_Utilisateur` INT(11) NOT NULL,
  `LOINC_Code` VARCHAR(50) NOT NULL,
  `Valeur` DOUBLE DEFAULT NULL,
  `Date_Examen` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`Id_Utilisateur`, `LOINC_Code`, `Date_Examen`),
  FOREIGN KEY (`Id_Utilisateur`) REFERENCES `Patient` (`Id_Utilisateur`),
  FOREIGN KEY (`LOINC_Code`) REFERENCES `Examen_Biologie` (`LOINC_Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `Resultat_Examen` (`Id_Utilisateur`, `LOINC_Code`, `Valeur`, `Date_Examen`) VALUES
(1, '718-7', 4.5, '2024-02-01'),    
(1, '4544-3', 40.2, '2024-02-01'),   
(5, '2339-0', 5.2, '2024-02-01'),    
(5, '2093-3', 180.5, '2024-02-01');
