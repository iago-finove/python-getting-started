import datetime

from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from rest_framework.response import Response

from .seriallizers import UserSigninSerializer, UserSerializer
from .authentication import token_expire_handler, expires_in

# working with data providers
from finove_data_service.data_service.domainModels.BigDataData import BigDataData
from finove_data_service.data_service.services.BigDataService import BigDataService
from finove_data_service.data_service.domainModels.SerasaData import SerasaData
from finove_data_service.data_service.services.SerasaService import SerasaService

# validate cnpj
from brazilnum.cnpj import validate_cnpj as validateCnpj
import requests  # to check if is real cnpj
import json


@api_view(["POST"])
@permission_classes(
    (AllowAny,)
)  # here we specify permission by default we set IsAuthenticated
def signin(request):
    signin_serializer = UserSigninSerializer(data=request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = authenticate(
        username=signin_serializer.data["username"],
        password=signin_serializer.data["password"],
    )
    if not user:
        return Response(
            {"detail": "Invalid Credentials or activate account"},
            status=HTTP_404_NOT_FOUND,
        )

    # TOKEN STUFF
    token, _ = Token.objects.get_or_create(user=user)

    # token_expire_handler will check, if the token is expired it will generate new one
    is_expired, token = token_expire_handler(
        token
    )  # The implementation will be described further
    user_serialized = UserSerializer(user)

    return Response(
        {
            "user": user_serialized.data,
            "expires_in": expires_in(token),
            "token": token.key,
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def serasaService(request, *args, **kwargs):
    serasaService = SerasaService()
    cnpj = kwargs.get("cnpj", None)

    noOlder = request.GET.get(
        "noOlder", (datetime.datetime.now() - datetime.timedelta(days=90)).date()
    )

    rawData = request.GET.get("rawData", False)

    if type(noOlder) == str:
        noOlder = datetime.datetime.strptime(noOlder, "%d/%m/%Y").date()

    if cnpj is None:
        result = {
            "Message": {"MessageDesc": "CNPJ not provided", "MessageId": 101},
            "ReturnDataSerasa": None,
        }

        return JsonResponse(result)

    # testing if is a valid CNPJ
    if validateCnpj(cnpj) is False:
        result = {
            "Message": {
                "MessageDesc": "Please provide a valid CNPJ",
                "MessageId": 101,
            },
            "ReturnDataSerasa": None,
        }

        return JsonResponse(result)

    # testing if CNPJ exist
    try:
        real = json.loads(
            requests.get("https://www.receitaws.com.br/v1/cnpj/" + str(cnpj)).content
        )
    except:
        real = {"status": ""}

    if real["status"] == "ERROR":
        result = {
            "Message": {
                "MessageDesc": "Please provide a real CNPJ",
                "MessageId": 101,
            },
            "ReturnDataSerasa": real,
        }

        return JsonResponse(result)

    ##########################
    # fetch Data from Serasa #
    ##########################
    responseRecord = SerasaService().fetchData(cnpj=cnpj, noOlder=noOlder)

    if responseRecord:
        if rawData:
            return JsonResponse(responseRecord.data)
        else:
            return JsonResponse(
                data=SerasaData.formatForDigifi(responseRecord.data["ReturnDataSerasa"])
            )
    else:
        return JsonResponse({"message": "Serasa data not found!"})


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def bigDataService(request, *args, **kwargs):
    cnpj = kwargs.get("cnpj", None)

    noOlder = request.GET.get(
        "noOlder", (datetime.datetime.now() - datetime.timedelta(days=90)).date()
    )

    rawData = request.GET.get("rawData", False)

    if type(noOlder) == str:
        noOlder = datetime.datetime.strptime(noOlder, "%d/%m/%Y").date()

    companyType = request.GET.get("companyType", None)

    if cnpj is None:
        result = {
            "Message": {"MessageDesc": "CNPJ not provided", "MessageId": 101},
            "ReturnDataBigData": None,
        }

        return JsonResponse(result)

    if companyType is None:
        result = {
            "Message": {
                "MessageDesc": "Company type must be provided",
                "MessageId": 101,
            },
            "ReturnDataBigData": None,
        }

        return JsonResponse(result)
    else:
        companyType = int(companyType)

    # testing if is a valid CNPJ
    if validateCnpj(cnpj) is False:
        result = {
            "Message": {
                "MessageDesc": "Please inform a valid CNPJ",
                "MessageId": 101,
            },
            "ReturnDataBigData": None,
        }

        return JsonResponse(result)

    # testing if CNPJ exist
    try:
        real = json.loads(
            requests.get("https://www.receitaws.com.br/v1/cnpj/" + str(cnpj)).content
        )
    except:
        real = {"status": ""}

    if real["status"] == "ERROR":
        result = {
            "Message": {
                "MessageDesc": "Please provide a real CNPJ",
                "MessageId": 101,
            },
            "ReturnDataBigData": real,
        }

        return JsonResponse(result)
    ##########################
    # fetch Data from BigData #
    ##########################
    responseRecord = BigDataService().fetchData(
        cnpj=cnpj, noOlder=noOlder, companyType=companyType
    )

    if responseRecord is None:

        result = {
            "Message": {
                "MessageDesc": "CNPJ not Found",
                "MessageId": 101,
            },
            "ReturnDataBigData": responseRecord,
        }

        return JsonResponse(result)

    else:
        if rawData:
            return JsonResponse(responseRecord.data)
        else:
            return JsonResponse(
                BigDataData.formatForDigifi(responseRecord.data, companyType)
            )


@api_view(["GET"])
def healthCheck(request, *args, **kwargs):
    return JsonResponse({"STATUS": "RUNNING"})
