CREATE DATABASE insurancedb;

-- Use the database
USE insurancedb;

-- Create the Users table for signup/login
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    middleName VARCHAR(50),
    lastName VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL -- Passwords should be hashed in the application layer
);

-- Create the InsuranceForms table for form-filling data
CREATE TABLE InsuranceForms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    middleName VARCHAR(50),
    lastName VARCHAR(50) NOT NULL,
    gender ENUM('Male', 'Female', 'Other'),
    age INT NOT NULL,
    status ENUM('Single', 'Married', 'Student', 'Employed', 'Other'),
    dob DATE NOT NULL,
    streetAddress VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    stateProvince VARCHAR(100) NOT NULL,
    zipCode VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phoneNumber VARCHAR(20) NOT NULL,
    applicantType ENUM('Partner', 'Child'),
    applicantFullName VARCHAR(150),
    applicantGender ENUM('Male', 'Female', 'Other'),
    applicantDob DATE,
    digitalSignature BLOB -- Store signature data as binary
);