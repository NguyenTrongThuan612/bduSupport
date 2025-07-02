"""Views for managing facility images."""

import logging
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.audit import audit_back_office
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.facility_image import FacilityImage
from bduSuport.serializers.facility_image import (
    FacilityImageSerializer,
    FacilityImageCreateSerializer
)

logger = logging.getLogger(__name__)


class FacilityImageManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication,)
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_description="Create a new facility image",
        request_body=FacilityImageCreateSerializer,
        responses={
            201: FacilityImageSerializer,
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def create(self, request: Request) -> Response:
        try:
            logger.info("FacilityImageManagementView.create req=%s", request.data)
            
            serializer = FacilityImageCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return RestResponse(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    message="Please check your data!"
                ).response
            
            facility_image = serializer.save()
            audit_back_office(
                request.user,
                "Tạo hình ảnh mới cho cơ sở vật chất",
                f"{facility_image.facility.name} - Image {facility_image.id}"
            )
            
            return RestResponse(
                data=FacilityImageSerializer(facility_image).data,
                status=status.HTTP_201_CREATED
            ).response
            
        except Exception as e:
            logger.exception("FacilityImageManagementView.create exc=%s, req=%s", e, request.data)
            return RestResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error"
            ).response

    @swagger_auto_schema(
        operation_description="Delete facility image by ID",
        responses={
            204: "No Content",
            404: "Not Found",
            500: "Internal Server Error"
        }
    )
    def destroy(self, request: Request, pk: int) -> Response:
        try:
            try:
                facility_image = FacilityImage.objects.get(id=pk, deleted_at=None)
            except FacilityImage.DoesNotExist:
                return RestResponse(
                    status=status.HTTP_404_NOT_FOUND,
                    message="Facility image not found"
                ).response
            
            facility_image.soft_delete()
            audit_back_office(
                request.user,
                "Xoá hình ảnh của cơ sở vật chất",
                f"{facility_image.facility.name} - Image {facility_image.id}"
            )
            
            return RestResponse(status=status.HTTP_204_NO_CONTENT).response
            
        except Exception as e:
            logger.exception("FacilityImageManagementView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error"
            ).response 