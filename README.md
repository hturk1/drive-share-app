# DriveShare – Peer-to-Peer Car Rental Platform

DriveShare is a web-based peer-to-peer car rental platform inspired by services like Turo.  
It allows users to list cars, search and book vehicles, communicate with owners, and receive notifications regarding bookings, payments, and car updates.

---

## Features

- User registration and login with security questions  
- Car listing and management for owners  
- Search cars by location  
- Booking system with date conflict prevention  
- Messaging system between users  
- Watch system with notifications (price drop / availability alerts)  
- Payment simulation system  
- Password recovery using Chain of Responsibility pattern  

---

## Tech Stack

- Python (Flask)  
- SQLite (Database)  
- HTML / CSS (Frontend templates)  

---

## How to Run the Project

### 1. Clone the repository  
git clone https://github.com/hturk1/drive-share-app.git  
cd drive-share-app  

### 2. Install dependencies  
pip install flask  

### 3. Run the application  
python app.py  

### 4. Open in browser  
http://127.0.0.1:5000/  

---

## Demo Video

https://www.youtube.com/watch?v=SZxSliEMoSc  

---

## How the System Works

Users register and log in with email and password  
Car owners add vehicles using a structured builder process  
Renters search available cars by location  
Users can book cars (system prevents overlapping bookings)  
Messaging system allows communication between users  
Users can watch cars and receive notifications on updates  
Payment is simulated using a proxy layer  
Password recovery uses security questions in a chain process  

---

## Design Pattern Summary

Builder Pattern  
Used to construct Car objects step-by-step in a clean and flexible way  

Singleton Pattern  
Ensures only one session manager exists across the application  

Observer Pattern  
Notifies users when watched cars change price or availability  

Mediator Pattern  
Centralizes communication between messaging, payment, and system events  

Proxy Pattern  
Adds validation before processing payments  

Chain of Responsibility  
Processes password recovery through multiple security question checks  

---

## Notes

No real payment processing is used (simulation only)  
Database is automatically created using SQLite  
Project is built for educational demonstration of design patterns  

---

Project: DriveShare (Design Patterns Assignment)  
GitHub: https://github.com/hturk1/drive-share-app  
Demo Video: https://www.youtube.com/watch?v=SZxSliEMoSc  
