# Currency Backend Setup Guide

Welcome to the Currency Backend setup guide! This document will walk you through the steps needed to get the backend server running on your local machine.

## Prerequisites

Before you begin, make sure you have Python installed on your system. This project requires Python 3.6 or newer.

## Getting Started

1. **Clone the Repository**

   First, clone the project repository to your local machine. You can do this by running the following command in your terminal:

   ```bash
   git clone <repository_url>
   ```

   Replace `<repository_url>` with the actual URL of the project repository.

2. **Navigate to the Backend Directory**

   Change into the `CalculatorBackend` directory within the cloned project:

   ```bash
   cd path/to/CalculatorBackend
   ```

   Ensure you replace `path/to/CalculatorBackend` with the actual path to the `CalculatorBackend` directory on your system.

3. **Create a Python Virtual Environment**

   It's recommended to create a virtual environment to manage the project's dependencies. Run the following command to create a virtual environment named `venv`:

   ```bash
   python -m venv venv
   ```

4. **Activate the Virtual Environment**

   Before installing dependencies, you need to activate the virtual environment. Use the appropriate command based on your operating system:

   - **On Windows:**

     ```cmd
     venv\Scripts\activate
     ```

   - **On macOS and Linux:**

     ```bash
     source venv/bin/activate
     ```

   You should now see `(venv)` at the beginning of your command line prompt, indicating that the virtual environment is activated.

5. **Install Project Dependencies**

   With the virtual environment activated, install the project dependencies using the following command:

   ```bash
   pip install -r requirements.txt
   ```

   This command reads the `requirements.txt` file and installs all the required Python packages.

6. **Set Environment Variables**

   Before running the application, you need to set the necessary environment variables. Rename the `.env.example` file to `.env` and update it with your actual configuration values:

   - **On Windows:**

     ```cmd
     copy .env.example .env
     ```

   - **On macOS and Linux:**
      ```bash
      cp .env.example .env
      ```

   Then, open the `.env` file in your favorite text editor and set the values for the environment variables defined within.

7. **Run the Flask Application**

   Finally, start the Flask application by running:

   ```bash
   python run.py
   ```

   You should see output indicating that the server is running, and it will tell you on which address and port it's accessible.

Congratulations! You've successfully set up and run the Flask backend locally. You can now access the API endpoints from your web browser or API client at whichever port you configured.

## Next Steps

- Explore the API endpoints defined in `routes.py`.
- Deploying your Flask application to a cloud service like Heroku for wider accessibility.

## Troubleshooting

If you encounter any issues during setup, ensure that:

- You're running the commands in the project's root directory.
- The virtual environment is activated when installing dependencies and running the application.
- All environment variables in the `.env` file are correctly set.

For more specific errors, consulting the Flask and Python documentation or searching for the error message online can provide solutions.