from flask import current_app


users = current_app.db.users.find()

for user in users:
    print(user)
