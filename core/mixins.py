from django.utils.functional import cached_property
import logging

logger = logging.getLogger(__name__)

class UserMixin:
    """ Mixin related to user """

    @cached_property
    def user_groups(self):
        try:
            logger("Getting user groups ...")
            return set(self.user.group_list)
        except Exception:
            return set()
    
    @cached_property
    def user(self):
        return self.request.user
