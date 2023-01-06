from django.db.models import Q
from rest_access_policy import AccessPolicy


class StaffApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"
        },
    ]

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q()


class StudentApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"
        },
    ]

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q(user_id_fk=request.user.id)

class UserProfileApiAccessPolicy(AccessPolicy):

    statements = [
        {
            "action": ["<method:get>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"
        },
    ]


    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:

        groups = request.user.groups.values_list('name', flat=True)
        method = request.method

        # Cleaning data
        if method == "POST":
            pass

        elif method == "PUT":
            pass

        return fields

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q(user_id_fk=request.user.id)
