from typing import Optional

from .models import Profile


def get_profile(**query_filter) -> Optional[Profile]:
    return Profile.objects.get(**query_filter)
