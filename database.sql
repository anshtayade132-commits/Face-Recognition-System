USE face_recognition_db;

INSERT INTO persons
(person_id, name, age, gender, phone, email, city)
VALUES
('P001', 'Ansh Tayade', 20, 'Male', '9876543210', 'ansh666@gmail.com', 'Bhusawal'),
('P002', 'Kashish Singh', 20, 'Female', '9545854575', 'kashish01@gmail.com', 'Bhusawal'),
('P003', 'Kunal Chandan', 20, 'Male', '9632154728', 'kunal691@gmail.com', 'Bhusawal'),
('P004', 'moin Maniyar', 20, 'Male', '8456312912', 'moin088@gmail.com', 'Bhusawal'),
('P005', 'Aamir Shaik', 20, 'Male', '7845632192', 'aamir55@gmail.com', 'Bhusawal');
SELECT * FROM persons;