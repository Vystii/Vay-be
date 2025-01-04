from  .plugin_manager import DashboardBase
from django.utils.translation import gettext_lazy as _


class RequestBlock(DashboardBase):
    class Meta:
        abstract = False
    
    title = _("My requests")
    description = _("list of your requests")
    routeName = "user_request"
    icon = """
    <svg  viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path fill="#324D5B" d="M50 0C22.386 0 0 22.386 0 50s22.386 50 50 50 50-22.387 50-50S77.614 0 50 0"/><path fill="#2B424D" d="M19 82.998v-56L.188 45.811A50 50 0 0 0 0 50c0 12.649 4.707 24.192 12.452 32.999z"/><path fill="#DA9C44" d="M89 81.272V57L49.975 38 11 57v24.272C20.164 92.687 34.224 100 50 100s29.836-7.313 39-18.728"/><path fill="#F3F3F3" d="M19 27h63a2 2 0 0 1 2 2v46a2 2 0 0 1-2 2H19a2 2 0 0 1-2-2V29a2 2 0 0 1 2-2"/><path fill="#26A6D1" d="M38 32h7l4-5h-7zm30-5-4 5h7l4-5zm-51 2v3h3l4-5h-5a2 2 0 0 0-2 2"/><path fill="#E2574C" d="M51 32h7l4-5h-7zm-26 0h7l4-5h-7zm57-5h-1l-4 5h7v-3a2 2 0 0 0-2-2"/><path fill="#DFE1E2" d="M73.5 47h-17a1.5 1.5 0 1 0 0 3h17a1.5 1.5 0 1 0 0-3m-3 6h-14a1.5 1.5 0 0 0 0 3h14a1.5 1.5 0 0 0 0-3m-31.483-4.04.682 3.585L34 43.999l-8 12c0 1.105 5.148 2 11.5 2s11.5-.895 11.5-2l-7-10zM40 43.999a2 2 0 1 0-.001-4.001A2 2 0 0 0 40 43.999M56.5 44h17a1.5 1.5 0 1 0 0-3h-17a1.5 1.5 0 1 0 0 3"/><path fill="#F4B459" d="M89 81.272V57L49.975 75.999 11 57v24.272C20.164 92.687 34.224 100 50 100s29.836-7.313 39-18.728"/><path fill="#F6C37A" d="M89 57 20.591 90.427A49.76 49.76 0 0 0 49.983 100h.034C65.786 99.994 79.84 92.682 89 81.272z"/></svg>
    """
    active = True
    
    @staticmethod
    def getPluginInfos()->dict:
        return DashboardBase.getPluginInfos(RequestBlock)

class CreateStudent(DashboardBase):
    class Meta:
        abstract = False
    
    title = _("Add people")
    description = _("add a new student or teacher")
    routeName = "add_user"
    icon = """
    <svg viewBox="-0.08 0 60.031 60.031" data-name="add user" xmlns="http://www.w3.org/2000/svg"><path d="M673.732 711.059c-.515 2.6-1.1 5.991-2.857 5.991a1.6 1.6 0 0 1-.568-.122c-.594 1.447-1.291 4.5-2.08 5.969a17.955 17.955 0 0 0-3.618 27.1H630s1.523-8.425 4.2-8.986c16.79-3.523 17.786-12.908 17.786-12.908v-4.839c-.875-1.261-1.643-4.763-2.289-6.338a1.6 1.6 0 0 1-.568.122c-1.759 0-2.342-3.389-2.857-5.991a6.6 6.6 0 0 1-.02-3.266c0-.123-.021-.248-.021-.37 0-9.285 3.642-16.34 11.773-17.321 0 0 1.306-.069 1.906-.107.44.036 2.094.107 2.094.107 8.131.981 11.773 8.036 11.773 17.321 0 .122-.019.247-.021.37a6.6 6.6 0 0 1-.024 3.268M660 689.974a.672.672 0 1 1-.094.021c-.152-.012-.161-.021.094-.021" data-name="user copy" transform="translate(-630 -689.969)" style="fill:#d9b78b;fill-rule:evenodd"/><path d="M677.875 726a12 12 0 1 1-12 12 12 12 0 0 1 12-12M672 740h4v4a2 2 0 0 0 4 0v-4h4a2 2 0 0 0 0-4h-4v-4a2 2 0 0 0-4 0v4h-4a2 2 0 0 0 0 4" transform="translate(-630 -689.969)" style="fill-rule:evenodd;fill:#699f4c"/></svg>    """
    active = True
    admin = True
    @staticmethod
    def getPluginInfos()->dict:
        return DashboardBase.getPluginInfos(CreateStudent)
    