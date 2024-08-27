from io import BytesIO
from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import person
import requests
from PIL import Image
from main_app.models import CustomUser


class Command(BaseCommand):
    help = "Generate fake users with profile pictures"

    def handle(self, *args, **kwargs):
        fake = Faker()
        fake.add_provider(person)

        for _ in range(10):  # Generate 10 fake users
            user = CustomUser(
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_active=True,
                is_superuser=False,
                is_staff=False,
                gender=fake.random_element(elements=("M", "F")),
                user_type=fake.random_element(elements=("1", "2", "3")),
            )

            try:
                # Generate and save a profile picture
                profile_picture_url = fake.image_url()
                response = requests.get(profile_picture_url)

                img = Image.open(BytesIO(response.content))  # Open image using PIL
                img = img.convert("RGB")  # Convert image to RGB mode

                img_io = BytesIO()  # Create a BytesIO object
                img.save(img_io, format="JPEG")  # Save the image to BytesIO
                user.profile_pic.save(
                    f"profile_pic_{user.first_name}.jpg", img_io, save=True
                )  # Save the image to the profile_picture field
            except Exception as e:
                pass
            user.set_password("password123")  # Set a default password
            user.save()

        self.stdout.write(
            self.style.SUCCESS("Fake users with profile pictures created successfully!")
        )
