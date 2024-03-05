CalculatorBackend
|
|
└───────app/
|     |            
|     │
|     └──────cache/
|     │   │
|     │   └───────__init__.py
|     │   │
|     │   └───────redis_client.py # Configuration and access to Redis for caching
|     |
|     │
|     └──────services/
|     │   │
|     │   └───────__init__.py
|     │   │
|     │   └───────currency_service.py # Handles currency conversion logic and Redis caching
|     |
|     | 
|     └─────utils/
|     │   │
|     │   └───────__init__.py
|     │   │
|     │   └───────constants.py
|     │   │
|     │   └───────errors.py
|     │   │
|     │   └───────rate_limiting.py # Implements rate limiting for the API endpoints
|     |
|     |
|     └──────__init__.py # Initializes Flask app and brings together components
|     |     
|     │
|     └──────routes.py # Defines routes/endpoints for the API
|
|
└───────tests/
|     |
|     |
|     └──────__init__.py
|     |     
|     │
|     └──────test_cache.py # test caching mechanism
|     |     
|     │
|     └──────test_services.py # test currency conversion service
|
|
└───────venv/ # virtual environment
|
|
└───────.env # environment variables e.g. API keys
|
|
└───────.env.example # environment variable examples
|
|
└───────.gitignore # ignore certain files & folders
|
|
└───────folder-structure.md # this file itself
|
|
└───────run.py # Entry point to run the Flask application