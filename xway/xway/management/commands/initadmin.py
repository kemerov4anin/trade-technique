from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    args = "<database_name admin_name admin_password>"

    def add_arguments(self, parser):
        parser.add_argument('admin_name')
        parser.add_argument('admin_password')

    def handle(self, *args, **options):
        admin_name = options['admin_name']
        admin_password = options['admin_password']

        u, created = User.objects.get_or_create(username=admin_name)
        if created:
            u.id = 0
            u.is_superuser = True
            u.is_staff = True
            u.set_password(admin_password)
            u.save()
        else:
            raise CommandError("user '%s' already exist" % admin_name)

        return "Password changed successfully for user '%s'" % u.username
