from django.contrib.auth.models import  User
from django.core.management.base import BaseCommand

DEFAULT_PASSWORD = 'test1234'


class Command(BaseCommand):
    args = ''
    help = 'Loads Initial Data For The App'

    def handle(self, *args, **options):
        # Create Admin User
        self.generate_admin_user()


    @classmethod
    def generate_admin_user(cls):

        if not User.objects.filter(username=u'admin').exists():
            User.objects.create_superuser(
                username=u'admin',
                email=u'admin@example.com',
                password=DEFAULT_PASSWORD,
                first_name=u'Admin',
                last_name=u'Administrator',
            )
            print "Created the Admin User : 'admin'"
        else:
            print "Admin User already exists: 'admin'"