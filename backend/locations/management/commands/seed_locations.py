import json
from pathlib import Path

from django.core.management.base import BaseCommand

from locations.models import Country, State, City


class Command(BaseCommand):
    help = "Seed Indian states and cities"

    def handle(self, *args, **options):

        data_file = (
            Path(__file__).resolve().parent.parent.parent
            / "data"
            / "india_cities.json"
        )

        with open(data_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        country, _ = Country.objects.get_or_create(
            code="IN",
            defaults={
                "name": "India",
            },
        )

        states_created = 0
        cities_created = 0

        for item in data:

            state_name = item["state"].strip()
            city_name = item["city"].strip()

            state, state_created = State.objects.get_or_create(
                country=country,
                name=state_name,
            )

            if state_created:
                states_created += 1

            _, city_created = City.objects.get_or_create(
                state=state,
                name=city_name,
            )

            if city_created:
                cities_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Indian locations seeded successfully."
            )
        )

        self.stdout.write(
            f"States created: {states_created}"
        )

        self.stdout.write(
            f"Cities created: {cities_created}"
        )