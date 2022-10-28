from rest_access_policy import FieldAccessMixin, AccessPolicy


class EventApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>", "<method:post>", "<method:put>", "<method:delete>"],
            "principal": ["group:staff", "group:student"],
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
            fields.pop('used_for_calculation', None)
            fields.pop('approved', None)

        elif method == "PUT":

            if 'student' in groups:
                fields.pop('used_for_calculation', None)
                fields.pop('approved', None)

        return fields

    def is_created_by(self, request, view, action) -> bool:
        pass


class EventAttendanceOfStudentsApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>", "<method:post>", "<method:put>", "<method:delete>"],
            "principal": ["group:staff"],
            "effect": "allow"
        },
        {
            "action": ["eventAttendanceOfStudents"],
            "principal" : ["group:staff"],
            "effect": "allow",
        },
        {
            "action": ["eventAttendanceOfStudents"],
            "principal": ["group:student"],
            "effect": "deny",
        }
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
        {
            "action": ["<method:put>"],
            "principal": ["staff"],
            "effect": "allow"
        },
    ]

