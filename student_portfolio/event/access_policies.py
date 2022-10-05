from rest_access_policy import FieldAccessMixin, AccessPolicy


class EventApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"
        },

        {
            "action": ["<method:post>", "<method:put>", "<method:delete>"],
            "principal": ["group:staff"],
            "effect": "allow"
        },

    ]

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:
        groups = request.user.groups.values_list('name', flat=True)
        method = request.method

        # Field Access
        # if 'staff' not in groups:
        #     fields.pop('approved', None)
        #     fields.pop('used_for_calculation', None)

        # Cleaning data
        if method == "POST":
            # We force the user to create an event first.
            fields.pop('attachment_link', None)
            fields.pop('attachment_file', None)

        return fields

    def is_created_by(self, request, view, action) -> bool:
        pass


class EventAttendanceOfStudentsApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>"],
            "principal": ["group:staff"],
            "effect": "allow"
        },
        {
            "action": ["<method:post|put|delete>"],
            "principal": ["group:staff"],
            "effect": "allow"
        },
    ]

class SyncStudentAttendanceByStudentIdAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:put>"],
            "principal": ["group:staff"],
            "effect": "allow"
        },
    ]

class SkillTableApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>"],
            "principal": ["*"],
            "effect": "allow"
        },
    ]

class EventRegisterRequestApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get|post|put>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"
        },
        #Hadle DELETE
        # {
        #     "action": ["<method:delete>"],
        #     "principal": ["group:staff", "group:student"],
        #     "effect": "allow"
        # },
    ]

