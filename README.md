# Nexus – A Software Authentication Checker Tool for Computer Networks

## Introduction
Nexus is a versatile software authentication checker tool designed specifically for computer networks. It addresses the critical need for software authentication and data collection in networked environments. Nexus empowers users to authenticate software, gather essential data from computer systems, store the collected information securely, and perform various operations based on their respective roles within the network.

## Features
- User registration and login
- Authentication of software on Windows and Unix machines
- Data collection from computer systems, including software details and system information
- Role-based access control
- Email notifications for untrusted software
- Intuitive graphical user interfaces (GUI)
- Secure data storage in a database
- API for programmatic interaction

## Usage
1. **Register a new user or log in with existing credentials.**
2. **Navigate through the GUI to authenticate software and collect data from the networked machines.**
3. **Use the admin panel to manage users and monitor the authentication status of software.**
4. **Receive email notifications for any untrusted software detected.**

## Project Structure
- `nexus/`: Main Django project directory
- `api/`: Django app containing the API endpoints
- `gui/`: Directory containing PyQt5 GUI files
- `scripts/`: Python scripts for data collection and other functionalities
- `requirements.txt`: List of dependencies
- `README.md`: Project documentation

## Technologies Used
- **Python 3**: Core programming language
- **Django**: Web framework for building the API
- **Django REST Framework**: Toolkit for building Web APIs
- **PyQt5**: Toolkit for creating graphical user interfaces
- **SQLite3**: Database for storing collected data
- **Heroku**: Platform for deploying the application
- **GitHub**: Version control and collaboration platform
