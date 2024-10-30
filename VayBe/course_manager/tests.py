import re

from django.test import TestCase
from django.utils import timezone

from users.models import Users
from v_utilities.models import StudyField, StudyLevel
from .models import Course


class CourseModelTest(TestCase):
    def test_get_only_users_courses(self):
        """
        Something wrong in the retrieval of the courses of a specific user
        @see users.views.GetCourse
        """
        StudyLevel(level=1, code="L1", label="Licence 1").save()
        StudyLevel(level=2, code="L2", label="Licence 2").save()
        
        StudyField(code="INF", label="Informatique").save()
        StudyField(code="BIOS", label="Bioscience").save()
        StudyField(code="GEO", label="Géographie").save()
        
        Users(study_field_id= "INF", study_level_id="L1" , email="test5@test.com", first_name = "lack", last_name="self").save()
        Course  (study_field_id= "INF", study_level_id="L1" , code_ue="MAT101", label = "mathématique").save()
        Course  (study_field_id= "BIOS", study_level_id="L1" , code_ue="MAT102", label = "mathématique").save()
        Course  (study_field_id= "GEO", study_level_id="L1" , code_ue="MAT103", label = "mathématique").save()
        Course  (study_field_id= "GEO", study_level_id="L1" , code_ue="MAT104", label = "mathématique").save()
        Course  (study_field_id= "INF", study_level_id="L1" , code_ue="MAT105", label = "mathématique").save()
        Course  (study_field_id= "INF", study_level_id="L1" , code_ue="MAT105", label = "mathématique", year=2023).save()
        
        courses = Course.objects.filter(study_field_id = "INF", study_level_id="L1", year = timezone.now().year)
        courses = [course.code_ue  for course in courses]
        print(courses)
        
        self.assertIs(courses == ["MAT101"], True)