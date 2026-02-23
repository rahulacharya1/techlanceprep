from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Create a super admin user'

    def handle(self, *args, **kwargs):
        email = 'admin@techlanceprep.in'
        username = 'admin'
        password = 'Admin@123'
        
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_superuser(
                email=email,
                username=username,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Super admin created: {email}'))
            self.stdout.write(self.style.WARNING(f'Password: {password}'))
            self.stdout.write(self.style.WARNING('⚠️ Please change the password after first login!'))
        else:
            user = User.objects.get(email=email)
            user.is_superuser = True
            user.is_admin = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Super admin updated: {email}'))
            
            