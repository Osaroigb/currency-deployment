import os
from app import app
from dotenv import load_dotenv

load_dotenv()

# Run the Flask application
if __name__ == "__main__":
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT"), debug=True)