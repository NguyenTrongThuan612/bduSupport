import jwt
from django.conf import settings
import requests
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
import logging

from bduSuport.configs.zalo_api import ZALO_USER_INFO_API
from bduSuport.helpers.response import RestResponse
from bduSuport.models.mini_app_user import MiniAppUser
from bduSuport.validations.create_mini_app_session import CreateMiniAppSessionValidator

class MiniAppAuth(viewsets.ViewSet):
    authentication_classes = ()

    @action(methods=["POST"], url_path="session", detail=False)
    @swagger_auto_schema(request_body=CreateMiniAppSessionValidator)
    def register_session(self, request):
        try:
            logging.getLogger().info("MiniAppAuth.register_session req=%s", request.data)
            validate = CreateMiniAppSessionValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST).response
            
            _data = validate.validated_data
            access_token = _data["token"]

            resp = requests.get(
                url=ZALO_USER_INFO_API,
                headers={
                    "access_token": access_token
                }
            )
            logging.getLogger().info("MiniAppAuth.register_session get zalo user info resp=%s", resp.text)

            resp_data = resp.json()

            logging.getLogger().info("MiniAppAuth.register_session get zalo user info resp_data=%s", resp_data)

            if resp_data["error"] != 0:
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đã xảy ra lỗi khi chúng tôi cố gắng kiểm tra tài khoản của bạn!").response
            
            user_id = resp_data["id"]
            user_name = resp_data.get("name", "")
            user_avatar_url = resp_data.get("picture", {}).get("data", {}).get("url", "")

            if not self.__create_mini_app_user(user_id, user_name, user_avatar_url):
                return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
            
            self.__create_access_token(user_id, access_token)

            return RestResponse(status=status.HTTP_200_OK, data=resp_data).response
        except Exception as e:
            logging.getLogger().exception("MiniAppAuth.register_session exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def __create_mini_app_user(self, user_id, user_name, user_avatar_url):
        try:
            try:
                user = MiniAppUser.objects.get(mini_app_user_id=user_id)
                return True
            except MiniAppUser.DoesNotExist:
                logging.getLogger().info("MiniAppAuth.__create_mini_app_user DoesNotExist user_id=%s", user_id)
            
            user = MiniAppUser(
                mini_app_user_id=user_id,
                name=user_name,
                avatar_url=user_avatar_url
            )
            user.save()

            if user.id is None:
                logging.getLogger().error("MiniAppAuth.__create_mini_app_user create user failed user=%s", user)
                return False

            return True
        except Exception as e:
            logging.getLogger().error("MiniAppAuth.__create_mini_app_user exc=%s, user=%s", e, user)
            return False
        
    def __create_access_token(self, mini_app_user_id, mini_app_token):
        cache.delete(f"mini_app_session:access:*")

        cache.set(
            f"mini_app_session:access:{mini_app_token}", 
            {"user_id": mini_app_user_id},
            7*24*60*60
        )
        