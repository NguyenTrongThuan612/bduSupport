from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from bduSuport.models.academic_level import AcademicLevel
from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.models.evaluation_method import EvaluationMethod
from bduSuport.models.training_location import TrainingLocation

class Major(models.Model):
    class Meta:
        db_table = "major"
    
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, db_index=True)
    name = models.CharField(max_length=255)
    expected_target = models.IntegerField(validators=[MinValueValidator(0)])
    college_exam_groups = models.ManyToManyField(CollegeExamGroup, through="bduSuport.MajorM2MCollegeExamGroup", related_name="majors")
    description = models.CharField(max_length=255)
    year = models.IntegerField(db_index=True, validators=[MinValueValidator(0)])
    benchmark_30 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(30)])
    benchmark_school_record = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(30)])
    benchmark_competency_assessment_exam = models.IntegerField(validators=[MinValueValidator(0)])
    tuition_fee = models.IntegerField(validators=[MinValueValidator(0)])
    training_location = models.ForeignKey(TrainingLocation, on_delete=models.CASCADE, related_name="majors")
    academic_level = models.ForeignKey(AcademicLevel, on_delete=models.CASCADE, related_name="majors")
    evaluation_methods = models.ManyToManyField(EvaluationMethod, related_name="majors", null=True)
    number_of_credits = models.IntegerField(validators=[MinValueValidator(0)])
    open_to_recruitment = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)