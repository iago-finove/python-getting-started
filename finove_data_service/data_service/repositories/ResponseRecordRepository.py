from typing import Union

from finove_data_service.data_service.models import ResponseRecord


class ResponseRecordRepository:
    @staticmethod
    def get(cnpj: str, noOlder, source: str) -> Union[ResponseRecord, None]:
        try:
            return ResponseRecord.objects.filter(
                cnpj=cnpj, source=source, last_update__gte=noOlder
            ).latest("last_update")
        except ResponseRecord.DoesNotExist:
            return None

    @staticmethod
    def create(data: dict) -> ResponseRecord:
        return ResponseRecord.objects.create(**data)
