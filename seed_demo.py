from django.contrib.auth.models import User
from apps.teams.models import Region, Team, Player
from faker import Faker
import random, sys

fake = Faker('id_ID')
regions = {n: Region.objects.get_or_create(name=n)[0] for n in ["Jakarta","Bandung","Surabaya"]}

for reg_name, reg in regions.items():
    for i in range(1, 3):
        school = f"{fake.company()} {reg_name} {i}"
        user = User.objects.create_user(
            username=f"{reg_name.lower()}{i}",
            email=f"{reg_name.lower()}{i}@ex.com",
            password="password123"
        )
        t = Team.objects.create(
            user=user, region=reg,
            school_name=school,
            school_nickname=fake.word().title(),
            coach_name=fake.name(), coach_phone=fake.msisdn()[:12],
            captain_name=fake.name(), captain_phone=fake.msisdn()[:12],
            supporter_name=fake.name(),
            category='sma', status='approved'
        )
        for j in range(5):
            Player.objects.create(
                team=t, name=fake.name(),
                position=random.choice(['kiper','anchor','flank','pivot']),
                jersey_number=str(random.randint(1,99)),
                guardian_name=fake.name(),
                is_captain=(j==0)
            )
print("Seed OK"); sys.exit()
