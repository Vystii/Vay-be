from django.utils import timezone
from v_utilities.models import SiteConfiguration


class VUtilitiesService:
    @staticmethod
    def getCurrentYear()->int:
        year = None
        if SiteConfiguration.objects.filter(pk = "current_year").count() : 
            _year: str = SiteConfiguration.objects.get(pk = "current_year").config_value
            year = int(_year.split("/")[0])
        return  year if year else  int(timezone.now().year)