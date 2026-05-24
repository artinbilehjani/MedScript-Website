from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User,Profile
from blog.models import Post,Category
from datetime import datetime
import random

category_list = [
    "physics",
    "fun",
    "manga"
]

class Command(BaseCommand):
    help = 'Inserting dummy data'
    
    def __init__(self,*args,**kwargs):
        super(Command,self).__init__(*args,**kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(username=self.fake.name(),password="Test@123456")
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=5)
        profile.save()

        for name in category_list:
            Category.objects.get_or_create(name=name)

        for _ in range(10):
            Post.objects.create(
                author = profile,
                # image = "images/blank.jpg"
                title = self.fake.paragraph(nb_sentences=1),
                content = self.fake.paragraph(nb_sentences=10),
                status = random.choice([True,False]),
                category = Category.objects.get(name=random.choice(category_list)),
                published_date = datetime.now()
            )