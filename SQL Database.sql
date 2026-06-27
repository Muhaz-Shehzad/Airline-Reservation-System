CREATE DATABASE IF NOT EXISTS airline_db;
USE airline_db;

-- 1. Users / Passengers Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('passenger', 'admin') DEFAULT 'passenger'
);

-- 2. Aircraft Table
CREATE TABLE IF NOT EXISTS aircraft (
    aircraft_id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(50) NOT NULL,
    total_seats INT NOT NULL
);

-- 3. Flights Table (Routes)
CREATE TABLE IF NOT EXISTS flights (
    flight_number VARCHAR(10) PRIMARY KEY,
    departure_airport VARCHAR(50) NOT NULL,
    arrival_airport VARCHAR(50) NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL
);

-- 4. Flight Schedules Table (Specific Instances of Flights)
CREATE TABLE IF NOT EXISTS schedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(10),
    aircraft_id INT,
    flight_date DATE NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (flight_number) REFERENCES flights(flight_number) ON DELETE CASCADE,
    FOREIGN KEY (aircraft_id) REFERENCES aircraft(aircraft_id) ON DELETE CASCADE
);

-- 5. Bookings Table
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    schedule_id INT,
    seat_number VARCHAR(5) NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (schedule_id) REFERENCES schedules(schedule_id) ON DELETE CASCADE,
    UNIQUE(schedule_id, seat_number) -- Prevents double-booking of the same seat
);

USE airline_db;

-- Insert Admin and Passenger (Password for both is 'password123')
INSERT INTO users (name, email, password, role) VALUES 
('Admin Account', 'admin@airline.com', 'password123', 'admin'),
('User Account', 'user@gmail.com', 'password123', 'passenger');

-- Insert Aircraft
INSERT INTO aircraft (model, total_seats) VALUES 
('Boeing 737', 180),
('Airbus A320', 150);

-- Insert Routes
INSERT INTO flights (flight_number, departure_airport, arrival_airport, departure_time, arrival_time) VALUES 
('PK-301', 'Karachi', 'Islamabad', '08:00:00', '10:00:00'),
('PK-302', 'Islamabad', 'Karachi', '14:00:00', '16:00:00'),
('PK-181', 'Lahore', 'Islamabad', '11:30:00', '12:45:00');

-- Insert Schedules (Adjust dates forward if testing long-term)
INSERT INTO schedules (flight_number, aircraft_id, flight_date, price) VALUES 
('PK-301', 1, '2026-06-15', 15000.00),
('PK-302', 1, '2026-06-16', 15500.00),
('PK-181', 2, '2026-06-15', 12000.00);

-- Set unique password for Admin
UPDATE users SET password = 'Admin' WHERE email = 'admin@airline.com';

-- Set unique password for Passenger
UPDATE users SET password = 'User' WHERE email = 'user@gmail.com';