from logging import getLogger

from .utils import get_service_permission, get_service_name

logger = getLogger(__name__)


class IsAuthorizedService:

    def has_permission(self, request, view):
        required_permission = get_service_name()
        if request.auth.get('service_permissions', False) and get_service_name() in request.auth['service_permissions']:
            return True
        logger.error('Permission {} not provided'.format(required_permission))
        return False

    def has_object_permission(self, request, view, obj):
        required_permission = get_service_permission(obj, request.method)
        if request.auth and 'service_permissions' in request.auth and required_permission in request.auth[
            'service_permissions']:
            return True
        logger.error('Permission {} not provided'.format(required_permission))
        return False


# TODO this is only stub
class IsAuthorizedUser:

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True
