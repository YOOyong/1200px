from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin

class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "Owner only can update/delete the object"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if request.user == obj.user or request.user.is_admin:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


