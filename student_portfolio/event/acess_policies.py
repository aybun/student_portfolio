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

