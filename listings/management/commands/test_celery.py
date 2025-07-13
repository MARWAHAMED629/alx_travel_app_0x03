from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from listings.models import Listing, Booking
from listings.tasks import send_booking_confirmation_email

class Command(BaseCommand):
    help = 'Test Celery background tasks and email notifications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sync',
            action='store_true',
            help='Run the task synchronously for testing',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== Testing Celery Background Tasks ===')
        )

        # Create test listing
        listing = Listing.objects.create(
            title="Test Vacation Home",
            description="A beautiful vacation home for testing",
            price_per_night=200.00,
            available_from=date.today(),
            available_to=date.today() + timedelta(days=30)
        )

        self.stdout.write(
            self.style.SUCCESS(f'Created test listing: {listing.title}')
        )

        # Create test booking
        booking = Booking.objects.create(
            listing=listing,
            user="test@example.com",
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=8)
        )

        self.stdout.write(
            self.style.SUCCESS(f'Created test booking: {booking.booking_id}')
        )

        if options['sync']:
            # Test synchronously
            self.stdout.write('Running email task synchronously...')
            result = send_booking_confirmation_email(str(booking.booking_id))
            
            if result:
                self.stdout.write(
                    self.style.SUCCESS('✅ Email task completed successfully')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Email task failed')
                )
        else:
            # Test asynchronously
            self.stdout.write('Triggering email task asynchronously...')
            result = send_booking_confirmation_email.delay(str(booking.booking_id))
            
            self.stdout.write(
                self.style.SUCCESS(f'Task submitted with ID: {result.id}')
            )
            self.stdout.write(
                self.style.WARNING(
                    'Check your Celery worker logs to see the task execution'
                )
            )

        self.stdout.write(
            self.style.SUCCESS('=== Test Complete ===')
        )
        self.stdout.write(
            'Make sure your Celery worker is running:'
        )
        self.stdout.write(
            'celery -A alx_travel_app worker --loglevel=info'
        ) 