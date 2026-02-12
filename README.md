# 🍽️🛍️ Foodkadeh

A B2B food Market-place.


## 🛠️ Tech Stack

* **Python 3.11+**
* **Django REST Framework (DRF)**
* **PostgreSQL**


## 🚀 How to run the project

⚙️ Create a `.env` file:
```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
REDIS_URL=redis://127.0.0.1:6379/1
CELERY_BROKER_URL=redis://127.0.0.1:6379/0 CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

FARAZ_SMS_API_KEY=key
FARAZ_SMS_LOGIN_OTP_PATTERN_CODE=code
FARAZ_SMS_SENDER_NUMBER=123
FARAZ_SMS_PHONE_BOOK_ID=123
```

📦 Install requirements
```bash
# Create virtual environment
python -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

```
🔥 Run the project
```bash
# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

# Start celery worker
celery -A foodkadeh worker --loglevel=INFO
```

## 🧪 API Documentation

* Swagger: `http://localhost:8000/swagger/`

Developed with ❤️ by **Lords of the Pings👑**
