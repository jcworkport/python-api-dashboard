# Tech Dash

Welcome to **Tech Dash**!

This is a Python web dashboard that updates every minute, gathering data from a WMS API. It's made user-friendly with Dash after cleaning the data with Pandas. I created it independently while working as an IT Specialist, managing department operations. Despite being new to Python and API integration, I finished it in under a month. Some parts of the code were adjusted/removed for privacy and security reasons.

![Image](https://github.com/jcworkport/python-api-dashboard/raw/main/tech-dash.jpg)

## Running the Project Locally

To run this project in development mode, you'll need to follow these steps:

1. **Clone the Repository**: 
    ```bash
    git clone https://github.com/jcworkport/python-api-dashboard
    ```

2. **Navigate into the Project Directory**: 
    ```bash
    cd tech-dash-2.0
    ```

3. **Create a Virtual Environment**: 
    ```bash
    python -m venv env
    ```

4. **Activate the Virtual Environment**:
    - On **Windows**:
    ```bash
    .\env\Scripts\Activate
    ```
    - On **Unix or MacOS**:
    ```bash
    source env/bin/activate
    ```

5. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

6. **Run the Program**:
    ```bash
    python index.py
    ```

7. **Access the Dashboard**:
    The Dash application will be running on [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

## Requirements

To run this project locally, you'll need the following:

- Python **3.12.2** or higher installed on your operating system.

