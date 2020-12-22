import os
from typing import Union

import requests
import base64


class SerasaApi(object):
    @staticmethod
    def fetchSerasaData(cnpj: str) -> Union[dict, None]:
        try:
            return requests.get(
                os.environ.get("CIAL_SERASA_DB_URL_PAID") + cnpj,
                headers={
                    "Authorization": "Basic "
                    + base64.b64encode(
                        f"{os.environ.get('CIAL_SERASA_DB_USER_PAID')}:{os.environ.get('CIAL_SERASA_DB_PASS_PAID')}".encode(
                            "ascii"
                        )
                    ).decode("ascii")
                },
            ).json()

        except requests.RequestException:
            return None
