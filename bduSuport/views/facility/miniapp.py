"""Facility views for miniapp operations."""

import logging
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.paginator import CustomPageNumberPagination
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.facility import Facility
from bduSuport.serializers.facility import FacilitySerializer

logger = logging.getLogger(__name__)


class MiniappFacilityView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )
    """ViewSet for facility operations in miniapp."""
    
    @swagger_auto_schema(
        operation_description="Get list of facilities for miniapp",
        manual_parameters=[
            openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: FacilitySerializer(many=True),
            500: "Internal Server Error"
        }
    )
    def list(self, request: Request) -> Response:
        """Get list of all active facilities for miniapp.
        
        Args:
            request: HTTP request
            
        Returns:
            Response: Paginated list of facilities
        """
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
            logger.exception("MiniappFacilityView.list exc=%s", e)
            return RestResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error"
            ).response
