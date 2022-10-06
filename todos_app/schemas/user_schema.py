from todos_app.schemas import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "name")


user_schema = UserSchema()
users_schema = UserSchema(many=True)
