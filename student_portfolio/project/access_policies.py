from rest_access_policy import AccessPolicy

class ProjectApiAccessPolicy(AccessPolicy):

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
        if 'staff' not in groups and (method != 'GET'):
            fields.pop('approved', None)
            fields.pop('approved_by', None)
            fields.pop('used_for_calculation', None)

        # Cleaning data
        if method == "POST":
            # We force users to create the project first.
            fields.pop('projectId', None)
            fields.pop('approved', None)
            fields.pop('approved_by', None)
            fields.pop('used_for_calculation', None)

            fields.pop('attachment_link', None)
            fields.pop('attachment_file', None)

        return fields
