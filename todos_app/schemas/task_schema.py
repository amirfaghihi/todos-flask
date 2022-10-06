from todos_app.schemas import ma


class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "story_points", "deadline")


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
