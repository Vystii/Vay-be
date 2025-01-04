from  users.dashboard_block.plugin_manager import DashboardBase
from django.utils.translation import gettext_lazy as _


class CourseBlock(DashboardBase):
    class Meta:
        abstract = False
    
    title = _("My Courses")
    description = _("list of courses")
    routeName = "user_course_page"
    icon = """
    <svg class="border-radius-50" viewBox="0 0 64 64" data-name="Layer 1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"><defs><style>.cls-4{fill:#274c77}</style></defs><path class="cls-4" d="M11 49v12H5V49m54 0v12h-6V49"/><path style="fill:#f5dd90" d="M3 3h58v46H3z"/><path class="cls-4" d="M32 45h-3l-2-2H10V13h4v24s12.15-3 18 8m18-8V13h4v30H37l-2 2h-3c5.85-11 18-8 18-8"/><path d="M32 45c-5.85-11-18-8-18-8V10l6-2v25c6.63 0 12 5.37 12 12M44 8l6 2v27s-12.15-3-18 8c0-6.63 5.37-12 12-12z" style="fill:#6096ba"/><path d="M32 19c0-6.63-5.37-12-12-12v26c6.63 0 12 5.37 12 12 0-6.63 5.37-12 12-12V7c-6.63 0-12 5.37-12 12" style="fill:#a3cef1"/></svg>
    """
    active = True
    weight = 3
    @staticmethod
    def getPluginInfos()->dict:
        return DashboardBase.getPluginInfos(CourseBlock)    

class NoteBlock(DashboardBase):
    class Meta: 
        abstract = False
        
    title = _("My notes")
    description = _("List of notes")
    routeName = "user_course_page"
    icon = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 514 514" xml:space="preserve"><path style="fill:#32bea6" d="M0 97v320h448.016V97.64z"/><path d="M464 154.088 339.28 352.104l50.256 31.648L514 186.152z"/><path style="fill:#fff" d="M244.656 337.848h-34.464l-13.696-35.632h-62.704l-12.944 35.632h-33.6l61.104-156.88h33.488zm-58.32-62.064L164.72 217.56l-21.184 58.224zm85.04-10.736v-31.552h-31.792V211.72h31.792v-31.552h21.216v31.552h31.872v21.776h-31.872v31.552z"/></svg>
    """
    active= True
    weight= 1
    
    
    @staticmethod
    def getPluginInfos():
        return DashboardBase.getPluginInfos(NoteBlock)
    
class AddCourseBlock(DashboardBase):
    class Meta:
        abstract = False
    
    title = _("Add course")
    description = _("add a new course")
    routeName = "add_course"
    icon = """
    <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill="#fff" fill-opacity=".01" d="M0 0h48v48H0z"/><path d="M38 4H10a2 2 0 0 0-2 2v36a2 2 0 0 0 2 2h28a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2" fill="#2F88FF" stroke="#000" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M17 30h14m-14 6h7m-5-19h10m-5 5V12" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
    """
    active = True
    admin = True
    weight = 3
    @staticmethod
    def getPluginInfos()->dict:
        return DashboardBase.getPluginInfos(AddCourseBlock)