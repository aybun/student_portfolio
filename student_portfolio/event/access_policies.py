from rest_access_policy import FieldAccessMixin, AccessPolicy
from django.db.models import Q

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

            fields = {
                'title' : fields['title'],
                'created_by' : fields['created_by']
            }

        elif method == "PUT":
            fields.pop('created_by')

            if 'staff' not in groups: #The user is a student or lower level users.
                fields.pop('used_for_calculation', None)
                fields.pop('approved', None)


        return fields

    def is_created_by(self, request, view, action) -> bool:
        pass

    # @classmethod
    # def scope_queryset(cls, request, qs):
    #     groups = request.user.groups.values_list('name', flat=True)
    #
    #     if 'staff' in groups:
    #         return qs
    #
    #     elif 'student' in groups:
    #         return qs.filter(Q(approved=True) | Q(created_by=request.user.id))

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q(approved=True) | Q(created_by=request.user.id)

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

class EventAttendanceApiAccessPolicy(AccessPolicy):
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

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "POST":
            fields.pop('id', None)

        elif request.method == "PUT":
            fields.pop('event_id', None)

        return fields

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if 'staff' in groups:
            return Q()


class CurriculumApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:post>", "<method:put>", "<method:delete>"],
            "principal": ["group:staff"],
            "effect": "allow"

        },

        {
            "action": ["<method:get>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"
        },

    ]

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:

        if request.method == "POST":
            fields = {'th_name': fields['th_name']}

        elif request.method == "PUT":
            pass

        return fields

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            if 'staff' in groups:
                return Q()
            elif 'student' in groups:
                return Q()

        elif request.method == "PUT":
            return Q()

        elif request.method == "DELETE":
            return Q()

class SkillGroupApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:post>", "<method:put>", "<method:delete>"],
            "principal": ["group:staff"],
            "effect": "allow"

        },

        {
            "action": ["<method:get>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"
        },
    ]

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:

        if request.method == "POST":
            fields = {'name': fields.get('name', None)}

        elif request.method == "PUT":
            pass

        return fields

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            if 'staff' in groups:
                return Q()
            elif 'student' in groups:
                return Q()

        elif request.method == "PUT":
            return Q()

        elif request.method == "DELETE":
            return Q()


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

