# RescueDB

**RescueDash** is a full-stack web application designed for the interactive visualization and geospatial tracking of rescue animal data. Built using the **Dash** framework and **MongoDB Atlas**, it allows users to filter animal records by rescue type (Water, Mountain, Disaster) and view real-time breed distributions and geographical locations.

## Key Features
* **Secure CRUD Integration**: Implements a custom Python module for Create, Read, Update, and Delete operations with MongoDB.
* **Dynamic Data Filtering**: Interactive radio buttons allow users to toggle between specific rescue categories, updating the dataset in real-time.
* **Geospatial Visualization**: Integrated **Leaflet** maps provide location tracking for individual animals based on their specific coordinates.
* **Interactive Analytics**: Automated **Plotly** pie charts visualize breed distribution across the current filtered dataset.
* **Security Focused**: Fully refactored to utilize system environment variables, ensuring database credentials are never hardcoded in the source code.

## Tech Stack
* **Language**: Python
* **Backend**: MongoDB Atlas (NoSQL)
* **Frontend**: Dash, Plotly, Dash-Leaflet
* **Data Processing**: Pandas, NumPy

## Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.9+ installed and a MongoDB Atlas cluster ready for connection.

### 2. Clone the Repository
```bash
git clone [https://github.com/tyler-eaker/RescueDash.git](https://github.com/tyler-eaker/RescueDash.git)
cd RescueDash
