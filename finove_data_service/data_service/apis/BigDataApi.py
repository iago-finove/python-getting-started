import os
from typing import Union

import requests
import base64

import json


class BigDataApi(object):
    @staticmethod
    def fetchBigDataData(cnpj: str, companyType: int) -> Union[dict, None]:
        try:
            if companyType == 1:
                datasets = "?Datasets=collections,activity_indicators,circles_first_level_owners,company_group_owners"

            else:
                datasets = "?Datasets=collections,activity_indicators"

            url = (
                os.environ.get("BIGBOOST_COMPANIES_URL")
                + datasets
                + "&q=doc{%s}&AccessToken=%s" % (cnpj, os.environ.get("BIGBOOST_TOKEN"))
            )
            payload = {}
            headers = {"Content-Type": "application/json"}
            response = json.loads(
                requests.request("GET", url, headers=headers, data=payload).content
            )
            # checking if all datasets are OK
            if all(
                [
                    response["Status"][z][0]["Message"] == "OK"
                    for z in [i for i in response["Status"]]
                ]
            ):

                return response

            else:
                print("deu ruim em todos os dataset")
                return None

        except:
            print("query falhou")
            return None
