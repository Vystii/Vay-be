from django.utils import timezone
from v_utilities.models import SiteConfiguration
from django.db.utils import ProgrammingError, OperationalError

class VUtilitiesService:
    @staticmethod
    def getCurrentYear() -> int:
        year = None
        try:
            if SiteConfiguration.objects.filter(pk="current_year").exists():
                _year: str = SiteConfiguration.objects.get(pk="current_year").config_value
                year = int(_year.split("/")[0])
        except (ProgrammingError, OperationalError):
            pass
        return year if year else int(timezone.now().year)
