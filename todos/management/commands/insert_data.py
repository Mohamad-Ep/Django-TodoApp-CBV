from faker import Faker
from django.core.management.base import BaseCommand
import random
from todos.models import Todo
from accounts.models import CustomUser, Profile

# ________________________________________________


class Command(BaseCommand):
    help = "Insert Todo Data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = CustomUser.objects.create(email=self.fake.email(), password="Af123456#")
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.save()

        for _ in range(5):
            todo = Todo.objects.create(
                title=self.fake.paragraph(nb_sentences=1), author=user
            )
            todo.is_done = random.choice([True, False])  # complate
            todo.save()


# ________________________________________________
