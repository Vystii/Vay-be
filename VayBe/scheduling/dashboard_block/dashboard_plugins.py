from  users.dashboard_block.plugin_manager import DashboardBase
from django.utils.translation import gettext_lazy as _


class GenerateSchedule(DashboardBase):
    class Meta:
        abstract = False
    
    title = _("Generate schedules")
    description = _("Generate schdedules on courses for teachers and students")
    routeName = "generate_schedule"
    icon = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" xml:space="preserve"><path style="fill:#ad9a74" d="M8 12.99v15.448l4 2.006 12-7.115V7.882l-12 7.115z"/><path style="fill:#f8f7c5" d="m12 30.444 12-7.115V7.882l-12 7.115z"/><path style="fill:#be1e2d" d="m24 3.562-3.609-2.006L8 8.696v4.294l4 2.007v-4.32z"/><path d="M24 3.562v4.32l-12 7.115v-4.32zm-5.546 9.942c-1.548.894-2.639 2.881-2.639 4.821 0 1.967 1.205 2.38 2.556 1.6.551-.318 1.111-.918 1.63-1.717-.082 1.405-.519 2.863-1.713 3.553-.458.264-.925.297-1.174.192-.706-.41-1.526 1.45-.914 1.858.519.338 1.37.068 2.088-.346 1.713-.989 2.659-2.782 2.95-5.001.259-2.99.146-6.652-2.784-4.96m0 4.642c-.884.51-1.268.011-1.268-.612 0-.846.479-1.8 1.268-2.256.935-.54 1.392 0 1.392.721s-.457 1.606-1.392 2.147" style="fill:#f05a28"/></svg>
    """
    active = True
    admin = True
    weight = 3
    @staticmethod
    def getPluginInfos()->dict:
        return DashboardBase.getPluginInfos(GenerateSchedule)    
