from marshmallow import Schema, fields


class Session:
    def __init__(
            self,
            date: str,
            start_time: str,
            end_time: str
    ) -> None:
        self.date = date
        self.start_time = end_time
        self.end_time = end_time


class SessionSchema(Schema):
    date = fields.Str(required=True)
    start_time = fields.Str(required=True)
    end_time = fields.Str(required=True)
