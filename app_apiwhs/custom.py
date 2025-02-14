from drf_yasg.inspectors import SwaggerAutoSchema


class CustomAutoSchema(SwaggerAutoSchema):

    def get_tags(self, operation_keys=None):
        tags = self.overrides.get("tags", None) or getattr(self.view, "swagger_viewset_tag", [])
        if not tags:
            tags = [operation_keys[0]]
        return tags
