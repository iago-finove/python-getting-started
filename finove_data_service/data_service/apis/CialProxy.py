import os
from typing import Union

import requests
import base64


class CialProxy(object):
    @staticmethod
    def fetchSerasaData(cnpj: str) -> Union[dict, None]:
        try:
            return requests.post(
                os.environ.get("CIAL_SERASA_DB_URL") + cnpj,
                headers={
                    "Authorization": "Basic "
                    + base64.b64encode(
                        f"{os.environ.get('CIAL_SERASA_DB_USER')}:{os.environ.get('CIAL_SERASA_DB_PASS')}".encode(
                            "ascii"
                        )
                    ).decode("ascii")
                },
            ).json()
        except requests.RequestException:
            return None
