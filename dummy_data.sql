USE airline_db;

-- Insert Admin and Passenger (Password for both is 'password123')
INSERT INTO users (name, email, password, role) VALUES 
('Admin Account', 'admin@airline.com', 'Admin', 'admin'),
('User Account', 'user@gmail.com', 'User', 'passenger');

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