
# Tell Django have change in models.py
python3 manage.py makemigrations jav

# Get SQL Schema. "0001" indicate which step should generate 
# python3 manage.py sqlmigrate jav 0001

# Apply change
python3 manage.py migrate
