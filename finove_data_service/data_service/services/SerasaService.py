import os
from datetime import date
from typing import Union

from finove_data_service.data_service.apis.CialProxy import CialProxy
from finove_data_service.data_service.apis.SerasaApi import SerasaApi
from finove_data_service.data_service.domainModels.SerasaData import SerasaData
from finove_data_service.data_service.models import ResponseRecord
from finove_data_service.data_service.repositories.ResponseRecordRepository import (
    ResponseRecordRepository,
)


class SerasaService(object):
    def __init__(self):
        self.responseRecordRepo = ResponseRecordRepository()

    def getResponseRecord(
        self, cnpj: str, noOlder: date
    ) -> Union[ResponseRecord, None]:
        return self.responseRecordRepo.get(cnpj=cnpj, noOlder=noOlder, source="serasa")

    def fetchFreeSerasaData(self, cnpj, noOlder: date) -> Union[ResponseRecord, None]:
        data = CialProxy.fetchSerasaData(cnpj=cnpj)
        if (
            data is not None
            and type(data.get("Message")) == dict
            and (data.get("Message")).get("MessageId", None) == 200
        ):
            if data is not None and SerasaData.dataNotOlderThan(
                data=data, minDate=noOlder
            ):
                self.responseRecordRepo.create(
                    {
                        "cnpj": cnpj,
                        "data": data,
                        "last_update": SerasaData.getUpdateDate(data),
                        "source": "serasa",
                        "source_url": os.environ.get("CIAL_SERASA_DB_URL"),
                    }
                )
                return self.getResponseRecord(cnpj=cnpj, noOlder=noOlder)

    def fetchPaidSerasaData(self, cnpj, noOlder: date) -> ResponseRecord:
        data = SerasaApi.fetchSerasaData(cnpj=cnpj)

        if (
            type(data.get("Message")) == dict
            and (data.get("Message")).get("MessageId", None) == 200
        ):
            if data["ReturnDataSerasa"] is not None and SerasaData.dataNotOlderThan(
                data=data, minDate=noOlder
            ):
                self.responseRecordRepo.create(
                    {
                        "cnpj": cnpj,
                        "data": data,
                        "last_update": SerasaData.getUpdateDate(data),
                        "source": "serasa",
                        "source_url": os.environ.get("CIAL_SERASA_DB_URL_PAID"),
                    }
                )
                return self.responseRecordRepo.get(
                    cnpj=cnpj, noOlder=noOlder, source="serasa"
                )

    def fetchData(self, cnpj, noOlder: date) -> Union[ResponseRecord, None]:
        responseRecord = self.getResponseRecord(cnpj=cnpj, noOlder=noOlder)

        if responseRecord is not None:
            return responseRecord

        ###########################################################################################################
        # after checking the response records and not finding a useful data we proceed to check the cial database #
        ###########################################################################################################

        responseRecord = self.fetchFreeSerasaData(cnpj=cnpj, noOlder=noOlder)

        if responseRecord is not None:
            return responseRecord

        #############################################################################
        # if the client don't exist at response records and Cial DB or is overdated #
        # querying the LIVE SERASA DB (PAID)                                        #
        #############################################################################

        responseRecord = self.fetchPaidSerasaData(cnpj=cnpj, noOlder=noOlder)

        if responseRecord is not None:
            return responseRecord

        return None
