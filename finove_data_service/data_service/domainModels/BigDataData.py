from datetime import datetime
from finove_data_service.data_service.models import ResponseRecord

# working with numbers in text
from quantulum3 import parser

# working with sensitive information
from dotenv import load_dotenv
import os


class BigDataData:
    def __init__(self):
        pass

    @staticmethod
    def totalLawsuitsAsDefendant(data):
        value = data["Result"][0]["Circles"][0]["TotalLawsuitsAsDefendant"]

        if value == 0:
            return 0
        if value == 1:
            return -50
        if value <= 3:
            return -150
        if value > 3:
            return -350

    @staticmethod
    def totalInquiries(data):
        value = data["Result"][0]["Circles"][0]["TotalBadPassages"]

        if value == 0:
            return 0
        if value == 1:
            return -50
        if value <= 5:
            return -150
        if value > 5:
            return -350

    @staticmethod
    def otherCompaniesMaxRevenue(data):
        maxIncomeValues = parser.parse(
            data["Result"][0]["CompanyGroups"][0]["MaxIncomeRange"]
        )
        r = []
        for incomeValue in maxIncomeValues:
            if "m" in incomeValue.surface.lower():
                r.append(float(incomeValue.value) * 10 ** 6)
            elif "k" in incomeValue.surface.lower():
                r.append(float(incomeValue.value) * 10 ** 3)
            else:
                r.append(int(incomeValue.value) * 10 ** 0)
        try:
            value = sum(r) / len(r)
        except:
            return 0

        if value < 150 * 10 ** 3:
            return 0
        if value <= 500 * 10 ** 3:
            return 50
        if value <= 3 * 10 ** 6:
            return 150
        if value <= 10 * 10 ** 6:
            return 400
        if value > 10 * 10 ** 6:
            return 650

    @staticmethod
    def revenueRange(data):
        value = data["Result"][0]["ActivityIndicators"]["IncomeRange"]
        value = parser.parse(value)
        r = []
        for i in value:
            if "MM" in i.surface:
                r.append(float(i.value) * 10 ** 6)
            elif "k" in i.surface.lower():
                r.append(float(i.value) * 10 ** 3)
            else:
                r.append(float(i.value) * 10 ** 0)

        value = sum(r) / len(r)

        if value <= 100 * 10 ** 3:
            return 0
        if value <= 250 * 10 ** 3:
            return 50
        if value <= 1 * 10 ** 6:
            return 150
        if value <= 2.5 * 10 ** 6:
            return 200
        if value > 2.5 * 10 ** 6:
            return 350

    @staticmethod
    def collectionProcess(data):
        try:
            if data["Result"][0]["Collections"]["IsCurrentlyOnCollection"]:
                return 1
            else:
                return 0
        except:
            return 0

    @staticmethod
    def employeesRange(data):
        value = data["Result"][0]["ActivityIndicators"]["EmployeesRange"]
        value = parser.parse(value)
        r = []
        for i in value:
            if "m" in i.surface.lower():
                r.append(float(i.value) * 10 ** 6)
            elif "k" in i.surface.lower():
                r.append(float(i.value) * 10 ** 3)
            else:
                r.append(float(i.value) * 10 ** 0)
        value = sum(r) / len(r)

        if value < 5:
            return 0
        if value < 10:
            return 50
        if value < 100:
            return 100
        if value < 500:
            return 150
        if value > 500:
            return 200

    @staticmethod
    def formatForDigifi(data, company_type):

        if company_type == 1:
            result = {
                "totalLawsuitsAsDefendant": BigDataData.totalLawsuitsAsDefendant(data),
                "totalInquiries": BigDataData.totalInquiries(data),
                "otherCompaniesMaxRevenue": BigDataData.otherCompaniesMaxRevenue(data),
                "revenueRange": BigDataData.revenueRange(data),
                "collectionProcess": BigDataData.collectionProcess(data),
                "employeesRange": BigDataData.employeesRange(data),
            }

            return result
        else:
            result = {
                "totalLawsuitsAsDefendant": 0,
                "totalInquiries": 0,
                "otherCompaniesMaxRevenue": 0,
                "revenueRange": BigDataData.revenueRange(data),
                "collectionProcess": BigDataData.collectionProcess(data),
                "employeesRange": BigDataData.employeesRange(data),
            }

            return result

    @staticmethod
    def getUpdateDate(data) -> datetime.date:
        # bigData do not return a confiable data about last atualization,
        # so we asume that was the instant date

        return datetime.now().date()

    @staticmethod
    def dataNotOlderThan(data, minDate: datetime.date) -> bool:
        try:
            cnpj = data["Result"][0]["MatchKeys"].split("{")[-1].split("}")[0]
            _ = ResponseRecord.objects.filter(
                cnpj=cnpj, source="bigData", last_update__gte=minDate
            ).latest("last_update")

            return True

        except ResponseRecord.DoesNotExist:
            return False
