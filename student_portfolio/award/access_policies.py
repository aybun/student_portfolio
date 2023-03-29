from django.db.models import Q
from rest_access_policy import AccessPolicy

class AwardApiAccessPolicy(AccessPolicy):

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


        if method == "GET":
            pass

        elif method == "POST":
            fields.pop('id', None)

            if 'staff' not in groups:
                fields.pop('used_for_calculation', None)
                fields.pop('approved', None)
                fields.pop('approved_by', None)

        elif method == "PUT":
            fields.pop('created_by', None)

            if 'staff' not in groups:
                fields.pop('used_for_calculation', None)
                fields.pop('approved', None)
                fields.pop('approved_by', None)

        return fields

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q(receivers=request.user.id) | Q(created_by=request.user.id)

        elif request.method == "PUT":
            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q(approved=False) & Q(created_by=request.user.id)

        elif request.method == "DELETE":

            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q(approved=False) & Q(created_by=request.user.id)