# Real-Time London Underground Arrival Time Aggregator

## Description

This project aims to develop a live feed aggregator in collaboration with Transport for London (TfL) to collect real-time updates from the London Underground. The aggregator serves as a valuable resource for dispatchers, operators, passengers, and city planners by providing reliable and up-to-date information on various parameters such as vehicle ID, current location, destination name, expected arrival time, platform name, station name, time left for the arrival, and direction. By accessing this comprehensive data, stakeholders can make informed decisions quickly and effectively, improving the overall efficiency and reliability of the London Underground system. The system leverages modern technologies to obtain, process, store, and present the collected data in a user-friendly and interactive manner.

## Table of Contents

- [Installation](#installation)
- [System Architecture](#system-architecture)
- [Usage](#usage)
- [License](#license)

## Installation

Provide step-by-step instructions on how to install and set up the project locally. Include any dependencies, prerequisites, or environment setup required. For example:

1. Clone the repository: `git clone https://github.com/EnricoZanetti/Real-Time-London-Underground-Arrival-Time-Aggregator`
2. Navigate to the project directory: `cd project`
3. Install dependencies: `pip install -r requirements.txt`

## System Architecture

![2023-06-10 14 07 37](https://github.com/EnricoZanetti/Real-Time-London-Underground-Arrival-Time-Aggregator/assets/98333026/97b9abc2-8d2c-467f-bd9d-3f48bc4f817f)

## Usage

To use the project and access its main functionalities, follow these instructions:

1. **Environment Setup:**
   - Make sure you have Docker installed on your machine.
   - Open a terminal or command prompt and navigate to the project directory.
   - Run the command `docker-compose up -d` to create and execute the Docker containers for Redis and PostgreSQL. Keep these containers active throughout the process.

2. **Database Configuration:**
   - Access the "my-postgres-container" using a database management tool or command line.
   - Connect to the "tubedb" database.
   - Create a table named "lines" in the "tubedb" database. This table will serve as a persistent storage entity for the relevant data.

3. **Python Environment and Dependencies:**
   - Create a virtual environment for Python using a tool like `virtualenv` or `conda`.
   - Activate the virtual environment.
   
4. **Executing the Workflow:**
   - Run the `main.py` file to initiate the workflow, which includes data ingestion, validation, cleaning, storage, and transmission to the webpage.
   - This process will be repeated every 30 seconds to provide updated data.

5. **Launching the Web Application:**
   - Open a new terminal or command prompt.
   - Set the environment variable for Flask by executing the command `export FLASK_APP=webpage.py` (for Unix/Linux) or `set FLASK_APP=webpage.py` (for Windows).
   - Run the command `flask run` to launch the Flask application.
   - Open your web browser and enter `http://127.0.0.1:5000` to access the webpage.
   - The webpage will display a drop-down list allowing you to select a specific London Underground line to view updated data.
   - The webpage will also feature a map of the underground network.
   - Upon selecting a line from the drop-down list, the corresponding data will be displayed in tabular form on the webpage.

Example code snippet for running the project:
```bash
# Terminal 1
docker-compose up -d
# Keep this terminal open and the Docker containers running

# Terminal 2
# Set up Python environment
virtualenv myenv
source myenv/bin/activate
pip install -r requirements.txt

# Execute the workflow
python main.py

# Terminal 3
# Launch Flask application
export FLASK_APP=webpage.py
flask run
```

Once the project is running and the webpage is accessible, you can interact with it to view updated data for different London Underground lines.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
