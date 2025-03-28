import datetime
from django.db.models import Q
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, status
from rest_framework.decorators import action

from bduSuport.helpers.audit import audit_back_office
from bduSuport.helpers.email import send_html_template_email
from bduSuport.helpers.paginator import CustomPageNumberPagination
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.admission_registration import AdmissionRegistration, ReviewStatusChoices
from bduSuport.serializers.admission_registration_serializer import AdmissionRegistrationSerializer
from bduSuport.validations.list_admission_registration_filter import ListAdmissionRegistrationFilter
from bduSuport.validations.review_registration import ReviewRegistrationValidator
from bduSuport.models.miniapp_notification import MiniappNotification
from bduSuport.middlewares.permissions.is_root import IsRoot

class AdmissionRegistrationManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("evaluation_method", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("major", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("college_exam_group", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("training_location", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("review_status", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=ReviewStatusChoices.values),
            openapi.Parameter("year", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ]
    )
    def list(self, request):
        try:
            logging.getLogger().info("AdmissionRegistrationManagementView.list query_params=%s", request.query_params)
            validate = ListAdmissionRegistrationFilter(data=request.query_params)

            if not validate.is_valid():
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            query_condition = Q(recalled_at=None)

            if "training_location" in validate.validated_data:
                query_condition = query_condition & Q(major__training_location=validate.validated_data.pop("training_location"))

            if "year" in validate.validated_data:
                query_condition = query_condition & Q(major__year=validate.validated_data.pop("year"))

            query_condition = query_condition & Q(**validate.validated_data)

            queryset = AdmissionRegistration.objects.filter(query_condition).order_by("-created_at")
            paginator = CustomPageNumberPagination()
            queryset = paginator.paginate_queryset(queryset, request)
            data = AdmissionRegistrationSerializer(queryset, many=True).data

            return RestResponse(data=paginator.get_paginated_data(data), status=status.HTTP_200_OK).response 
        except Exception as e:
            logging.getLogger().exception("AdmissionRegistrationManagementView.list exc=%s, params=%s", e, request.query_params)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response

    def retrieve(self, request, pk):
        try:
            logging.getLogger().info("AdmissionRegistrationManagementView.retrieve pk=%s", pk)
            try:
                registration = AdmissionRegistration.objects.get(id=pk)
                data = AdmissionRegistrationSerializer(registration).data
                return RestResponse(data=data, status=status.HTTP_200_OK).response 
            
            except AdmissionRegistration.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            logging.getLogger().exception("AdmissionRegistrationManagementView.retrieve exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(request_body=ReviewRegistrationValidator)
    @action(methods=["POST"], detail=True, url_path="review")
    def approve(self, request, pk):
        try:
            logging.getLogger().info("AdmissionRegistrationManagementView.approve pk=%s, req=%s", pk, request.data)
            validate = ReviewRegistrationValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            try:
                registration = AdmissionRegistration.objects.get(id=pk)

                if registration.is_reviewed:
                    return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đơn đăng ký này đã được xét duyệt!").response
                
                if validate.validated_data["is_approve"]:
                    if not registration.is_passed:
                        return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đơn đăng ký không đủ điều kiện xét duyệt!").response
                    
                    # if registration.major.expected_target <= len(registration.major.admission_registrations.filter(review_status=ReviewStatusChoices.APPROVED)):
                    #     return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đã vượt chỉ tiêu tuyển sinh cho ngành này!").response
                
                registration.reviewed_by = request.user
                registration.review_status = ReviewStatusChoices.APPROVED if validate.validated_data["is_approve"] else ReviewStatusChoices.REJECTED
                registration.save(update_fields=["reviewed_by", "review_status"])
                audit_back_office(
                    request.user, 
                    "Xét duyệt đơn đăng ký", 
                    f"{registration.student.fullname} - {registration.major.name} - {registration.major.academic_level.name}"
                )

                messages = {
                    ReviewStatusChoices.APPROVED: f"Đơn xét tuyển ngành {registration.major.name} của học sinh {registration.student.fullname} đã được duyệt!",
                    ReviewStatusChoices.REJECTED: f"Đơn xét tuyển ngành {registration.major.name} của học sinh {registration.student.fullname} không đủ điều kiện xét duyệt!"
                }

                self.__create_approve_registration_noti_in_miniapp(
                    messages[ReviewStatusChoices.APPROVED],
                    registration.user
                )

                send_html_template_email.apply_async(
                    kwargs={
                        "to": [registration.student.email],
                        "subject": "[Trường Đại học Bình Dương] Thông Báo Kết Quả Xét Duyệt Đơn Xét Tuyển Đại Học 2024",
                        "template_name": "approve_registration.html",
                        "context": {
                            "student__fullname": registration.student.fullname,
                            "student__gender": registration.student.gender,
                            "student__citizen_id": registration.student.citizen_id,
                            "student__email": registration.student.email,
                            "student__phone": registration.student.phone,
                            "student__address": registration.student.address,
                            "student__city": registration.student.city,
                            "student__high_school": registration.student.high_school,
                            "major_name": registration.major.name,
                            "evaluation_method_name": getattr(registration.evaluation_method, "name", "N\A"),
                            "college_exam_group_name": getattr(registration.college_exam_group, "name", "N\A"),
                            "academic_level_name": registration.major.academic_level.name,
                            "final_score": registration.final_score,
                            "created_at": registration.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                            "date_of_birth": registration.student.date_of_birth.strftime("%d/%m/%Y"),
                            "is_approved": registration.review_status == ReviewStatusChoices.APPROVED
                        }
                    }
                )

                return RestResponse(status=status.HTTP_200_OK).response 
            except AdmissionRegistration.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            logging.getLogger().exception("AdmissionRegistrationManagementView.approve exc=%s, pk=%s, req=%s", e, pk, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def __create_approve_registration_noti_in_miniapp(self, content, user):
        try:
            noti = MiniappNotification(content=content, user=user)
            noti.save()
        except Exception as e:
            logging.getLogger().exception("AdmissionRegistrationManagementView.__create_approve_registration_noti_in_miniapp exc=%s, user=%s", e, user)
            