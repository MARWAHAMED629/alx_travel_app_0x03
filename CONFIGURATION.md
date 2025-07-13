# Configuration Guide

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Settings
DB_NAME=alx_travel_app
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=3306

# Chapa Payment Settings
CHAPA_SECRET_KEY=your-chapa-secret-key

# Email Settings (Gmail)
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

## Gmail Setup for Email Notifications

To use Gmail for sending emails:

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
3. **Use the App Password** in your `.env` file instead of your regular password

## RabbitMQ Setup

### Windows
1. Download and install RabbitMQ from https://www.rabbitmq.com/download.html
2. Start RabbitMQ server:
   ```bash
   rabbitmq-server
   ```

### macOS
```bash
# Install with Homebrew
brew install rabbitmq

# Start the service
brew services start rabbitmq
```

### Ubuntu/Debian
```bash
# Install
sudo apt-get install rabbitmq-server

# Start the service
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server
```

## Testing the Setup

1. **Test Celery connection**:
   ```bash
   python test_celery.py
   ```

2. **Test with Django management command**:
   ```bash
   python manage.py test_celery
   ```

3. **Test with API**:
   ```bash
   # Create a booking via API
   curl -X POST http://localhost:8000/api/bookings/ \
     -H "Content-Type: application/json" \
     -d '{
       "listing": "listing-uuid-here",
       "user": "test@example.com",
       "start_date": "2024-01-15",
       "end_date": "2024-01-20"
     }'
   ```

## Troubleshooting

### RabbitMQ Issues
- Check if RabbitMQ is running: `rabbitmqctl status`
- Check if port 5672 is accessible
- Restart RabbitMQ service if needed

### Email Issues
- Verify Gmail credentials
- Check if App Password is correct
- Ensure 2FA is enabled on Gmail account
- Check firewall settings

### Celery Issues
- Ensure all dependencies are installed
- Check if Django project can be imported
- Verify Celery configuration in settings.py
- Check worker logs for errors 