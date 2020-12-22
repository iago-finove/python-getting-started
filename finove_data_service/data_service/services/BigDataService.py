import os
from datetime import date
from typing import Union

from finove_data_service.data_service.apis.BigDataApi import BigDataApi
from finove_data_service.data_service.models import ResponseRecord
from finove_data_service.data_service.repositories.ResponseRecordRepository import (
    ResponseRecordRepository,
)
from finove_data_service.data_service.domainModels.BigDataData import BigDataData


class BigDataService(object):
    def __init__(self):
        self.responseRecordRepo = ResponseRecordRepository()

    def getResponseRecord(
        self, cnpj: str, noOlder: date
    ) -> Union[ResponseRecord, None]:
        return self.responseRecordRepo.get(cnpj=cnpj, noOlder=noOlder, source="bigData")

    def fetchBigDataData(
        self, cnpj, noOlder: date, companyType: int
    ) -> Union[ResponseRecord, None]:
        data = BigDataApi.fetchBigDataData(cnpj=cnpj, companyType=companyType)
        if data is not None:
            self.responseRecordRepo.create(
                {
                    "cnpj": cnpj,
                    "data": data,
                    "last_update": BigDataData.getUpdateDate(data),
                    "source": "bigData",
                    "source_url": os.environ.get("BIGBOOST_COMPANIES_URL"),
                }
            )
            return self.getResponseRecord(cnpj=cnpj, noOlder=noOlder)

    def fetchData(
        self, cnpj, noOlder: date, companyType: int
    ) -> Union[ResponseRecord, None]:
        responseRecord = self.getResponseRecord(cnpj=cnpj, noOlder=noOlder)

        if responseRecord is not None and BigDataData.dataNotOlderThan(
            data=responseRecord.data, minDate=noOlder
        ):
            return responseRecord

        #################################################
        # if the client don't exist at response records #
        # querying the LIVE bigData Api (PAID)          #
        #################################################

        responseRecord = self.fetchBigDataData(
            cnpj=cnpj, noOlder=noOlder, companyType=companyType
        )

        return responseRecord