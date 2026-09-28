# Face Recognition System

A Python-based real-time face recognition system using OpenCV, face_recognition, and MySQL.

## Features

- Real-time face recognition
- Webcam-based face registration
- MySQL database integration
- Person information retrieval
- Secure `.env` configuration

## Technologies

- Python 3.14
- OpenCV
- face_recognition
- MySQL
- python-dotenv

## Project Structure

```text
Face-Recognition-System/
├── face_system.py
├── database.py
├── database.sql
├── face_recognition_DB.sql
├── .gitignore
└── README.md

The faces/ folder and .env file are stored locally and excluded from GitHub.

Installation
pip install opencv-python face-recognition mysql-connector-python python-dotenv

pip install -r requirements.txt

Run
python face_system.py

The system can register faces and recognize registered people through the webcam.

Security

Database credentials are stored in .env and are not uploaded to GitHub.

Author

Ansh Tayade

GitHub: https://github.com/anshtayade132-commits

Repository

https://github.com/anshtayade132-commits/Face-Recognition-System


Then save it and run:

```powershell
git add README.md
git commit -m "Add README"
git push







