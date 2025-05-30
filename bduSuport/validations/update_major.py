from rest_framework import serializers

from bduSuport.models.major import Major
from bduSuport.models.academic_level import AcademicLevel
from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.models.evaluation_method import EvaluationMethod
from bduSuport.models.training_location import TrainingLocation

class UpdateMajorValidator(serializers.Serializer):
    code = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    expected_target = serializers.IntegerField(required=False, min_value=0)
    college_exam_groups = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=CollegeExamGroup.objects.filter(deleted_at=None),
        many=True,
        allow_empty=True
    )
    description = serializers.CharField(required=False, allow_blank=True)
    year = serializers.IntegerField(required=False, min_value=0)
    benchmark_30 = serializers.FloatField(required=False, min_value=0.00, max_value=30.00)
    benchmark_school_record = serializers.FloatField(required=False, min_value=0.00, max_value=30.00)
    benchmark_competency_assessment_exam = serializers.IntegerField(required=False, min_value=0)
    tuition_fee = serializers.IntegerField(required=False, min_value=0)
    academic_level = serializers.PrimaryKeyRelatedField(required=False, queryset=AcademicLevel.objects.filter(deleted_at=None))
    evaluation_methods = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=EvaluationMethod.objects.filter(deleted_at=None), 
        many=True, 
        allow_empty=True
    )
    training_location = serializers.PrimaryKeyRelatedField(required=False, queryset=TrainingLocation.objects.filter(deleted_at=None))
    number_of_credits = serializers.IntegerField(required=False, min_value=0)
    open_to_recruitment = serializers.BooleanField(required=False)

    def validate_benchmark_30(self, value: float):
        s = str(value)
        _, decimal_places = s.split(".")

        if len(decimal_places) > 2:
            raise serializers.ValidationError("invalid_benchmark_30_value")
        
        return value
    
    def validate_benchmark_school_record(self, value: float):
        s = str(value)
        _, decimal_places = s.split(".")

        if len(decimal_places) > 2:
            raise serializers.ValidationError("invalid_benchmark_school_record_value")
        
        return value