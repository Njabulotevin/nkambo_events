from marshmallow import Schema, fields


class Guest:
    def __init__(
            self,
            name: str,
            bio: str,
            occupation: str,
            profile_image: str

    ) -> None:
        self.name = name
        self.bio = bio
        self.occupation = occupation
        self.profile_image = profile_image

    def to_dict(self):
        return {
            "name": self.name,
            "bio": self.bio,
            "occupation": self.occupation,
            "profile_image": self.profile_image
        }

    @classmethod
    def create_guest(cls, guest_data):
        return cls(
            name=guest_data["name"],
            bio=guest_data["bio"],
            occupation=guest_data["occupation"],
            profile_image=guest_data["profile_image"]
        )

    @classmethod
    def serialize_guest_db(cls, guest_dict):
        if guest_dict:
            return {
                "_id": str(guest_dict["_id"]),
                "name": guest_dict["name"],
                "bio": guest_dict["bio"],
                "occupation": guest_dict["occupation"],
                "profile_image": guest_dict["profile_image"]
            }
        return None

    @classmethod
    def serialize_guests_db(cls, guests: list) -> list:
        """
        Serialize a list of MongoDB guests.
        """
        return [cls.serialize_guest_db(guest) for guest in guests]


class GuestSchema(Schema):
    name = fields.Str(required=True)
    bio = fields.Str(required=True)
    occupation = fields.Str(required=True)
    profile_image = fields.Str(required=True)




