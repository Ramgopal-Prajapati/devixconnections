"""
Run this script once to set up the database and create admin user.
Usage: python setup.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devix_project.settings')

# Run migrations first via subprocess
import subprocess
subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)

django.setup()

from django.contrib.auth.models import User
from core.models import Profile

# Create superuser (Ram Sir)
if not User.objects.filter(username='ramsir').exists():
    admin = User.objects.create_superuser(
        username='ramsir',
        password='RamSir@2024',
        first_name='Ram',
        last_name='Sir',
        email='ramsir@devix.com'
    )
    Profile.objects.get_or_create(user=admin, defaults={'student_id': 'ADMIN-001', 'nickname': 'Ram Sir'})
    print("✅ Admin created: username=ramsir, password=RamSir@2024")
else:
    print("ℹ️  Admin already exists.")

# Create sample students
students = [
    ('S001', 'Aarav Sharma', 'aarav', 'DevixPass@1'),
    ('S002', 'Priya Patel', 'priya', 'DevixPass@1'),
    ('S003', 'Rohan Gupta', 'rohan', 'DevixPass@1'),
]

for sid, name, uname, pwd in students:
    if not User.objects.filter(username=uname).exists():
        parts = name.split()
        u = User.objects.create_user(username=uname, password=pwd, first_name=parts[0], last_name=' '.join(parts[1:]))
        Profile.objects.get_or_create(user=u, defaults={'student_id': sid})
        print(f"✅ Student created: {name} ({sid}) — username={uname}")

print("\n🎉 Setup complete!")
print("➡️  Run: python manage.py runserver")
print("➡️  Admin panel: http://127.0.0.1:8000/admin/")
print("➡️  Admin login: ramsir / RamSir@2024")
