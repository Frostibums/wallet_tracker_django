# Wallets Tracker
Wallets Tracker is a web application for tracking cryptocurrency wallet transactions. The app allows users to add their crypto wallets and monitor the latest transactions so they don't miss anything.
## Features
- Monitoring several blockchains.
- Track the latest transactions for each wallet.
- User authentication and wallet management.
- Background transaction updates using Celery.
## Technologies
- Django
- Django REST framework
- Celery + Redis
- HTML/CSS/JS
## Installation
1. Clone this repository and navigate to the project directory:
```sh
git clone https://github.com/yourusername/wallets-tracker.git
cd wallets-tracker
```
2. Create a virtual environment and activate it:
```sh
python -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```sh
pip install -r requirements.txt
```
4. Start a Redis container in Docker as a message broker:
```sh
docker run -d -p 6379:6379 redis
```
5. Apply migrations:
```sh
python manage.py makemigrations
python manage.py migrate
```
6. Start Celery for task processing:
```sh
celery -A wallet_tracker worker -l info -n workeruno --pool=solo
celery -A wallet_tracker beat -l info
```
7. Start the server:
```sh
python manage.py runserver
```
## Usage
1. Open a web browser and go to http://localhost:8000.
2. Create an account or log in if you're already registered.
3. Add your crypto wallets and start tracking transactions and balances.
# API Endpoints
Wallets Tracker provides the following API endpoints:

- /api/v1/get_wallets/: Get a list of user wallets.
- /api/v1/add_wallet/: Add a new wallet.
- /api/v1/remove_wallet/: Remove a wallet.
