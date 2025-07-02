"""Facility views for managing facility operations."""

import logging
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.audit import audit_back_office
from bduSuport.helpers.paginator import CustomPageNumberPagination
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.facility import Facility
from bduSuport.serializers.facility import (
    FacilitySerializer,
    FacilityCreateSerializer,
    FacilityUpdateSerializer
)

logger = logging.getLogger(__name__)


class FacilityManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication,)
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_description="Create a new facility",
        request_body=FacilityCreateSerializer,
        responses={
            201: FacilitySerializer,
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def create(self, request: Request) -> Response:
        try:
            logger.info("FacilityManagementView.create req=%s", request.data)
            
            serializer = FacilityCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return RestResponse(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    message="Please check your data!"
                ).response
            
            facility = serializer.save()
            audit_back_office(request.user, "Tạo tài liệu cơ sở vật chất mới", facility.name)
            
            return RestResponse(
                data=FacilitySerializer(facility).data,
                status=status.HTTP_201_CREATED
            ).response
            
        except Exception as e:
            logger.exception("FacilityManagementView.create exc=%s, req=%s", e, request.data)
            return RestResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error"
            ).response

    @swagger_auto_schema(
        operation_description="Get list of facilities",
        manual_parameters=[
            openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: FacilitySerializer(many=True),
            500: "Internal Server Error"
        }
    )
    def list(self, request: Request) -> Response:
        try:
            queryset = Facility.get_active_facilities().order_by('-created_at')
            paginator = CustomPageNumberPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            data = FacilitySerializer(paginated_queryset, many=True).data

            return RestResponse(
                data=paginator.get_paginated_data(data),
                status=status.HTTP_200_OK
            ).response
            
        except Exception as e:
            logger.exception("FacilityManagementView.list exc=%s", e)
            return RestResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error"
            ).response


    @swagger_auto_schema(
        operation_description="Update facility by ID",
        request_body=FacilityUpdateSerializer,
        responses={
            200: FacilitySerializer,
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error"
        }
    )
    def update(self, request: Request, pk: int) -> Response:
        try:
            try:
                facility = Facility.objects.get(id=pk, deleted_at=None)
            except Facility.DoesNotExist:
                return RestResponse(
                    status=status.HTTP_404_NOT_FOUND,
                    message="Facility not found"
                ).response
            
            serializer = FacilityUpdateSerializer(facility, data=request.data, partial=True)
            if not serializer.is_valid():
                return RestResponse(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    message="Please check your data!"
                ).response
            
            updated_facility = serializer.save()
            audit_back_office(request.user, "Cập nhật tài liệu cơ sở vật chất", facility.name)
            
            return RestResponse(
                data=FacilitySerializer(updated_facility).data,
                status=status.HTTP_200_OK
            ).response
            
        except Exception as e:
            logger.exception("FacilityManagementView.update exc=%s, pk=%s, req=%s", e, pk, request.data)
            return RestResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error"
            ).response

    @swagger_auto_schema(
        operation_description="Delete facility by ID",
        responses={
            204: "No Content",
            404: "Not Found",
            500: "Internal Server Error"
        }
    )
    def destroy(self, request: Request, pk: int) -> Response:
        try:
            try:
                facility = Facility.objects.get(id=pk, deleted_at=None)
            except Facility.DoesNotExist:
                return RestResponse(
                    status=status.HTTP_404_NOT_FOUND,
                    message="Facility not found"
                ).response
            
            facility.soft_delete()
            audit_back_office(request.user, "Xoá tài liệu cơ sở vật chất", facility.name)
            
            return RestResponse(status=status.HTTP_204_NO_CONTENT).response
            
        except Exception as e:
            logger.exception("FacilityManagementView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error"
            ).response
