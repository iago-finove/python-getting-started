import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser


class SerasaData:
    @staticmethod
    def companyType(data):
        # checking shareholders
        if data.get("Partner") is None:
            return 1
        elif max([i["PercentageCapital"] for i in data["Partner"]]) > 80:
            return 1
        else:
            # checking the revenue of the company if the the sharehlders are pulverized
            if (
                data.get("PresumedSales")
                if data.get("PresumedSales") is not None
                else {"PresumedSales": 0}
            ).get("Value", 0) < 1750000:
                return 2
            else:
                return 3

    @staticmethod
    def findSummaryItem(data, groupName):
        item = data.get("ConcentreSummary", None)
        if item is None:
            return None

        result = [k for k in item if groupName in k["GroupOccurrence"]]

        if len(result) > 0:
            return result
        else:
            return None

    @staticmethod
    def diffInMonths(item, dateIdentifier, today):
        try:
            currentDate = parser.isoparse(item[dateIdentifier]).date()
            r = relativedelta(currentDate, today)

            return round(abs(r.months) + abs(12 * r.years) + abs(r.days) / 30, 2)

        except:

            return None

    @staticmethod
    def getNumberOfMonthsSinceLatest(data, dateIdentifier):
        if data is None:
            return -1

        today = datetime.datetime.now().date()

        try:
            return min(
                filter(
                    lambda x: x is not None,
                    [SerasaData.diffInMonths(k, dateIdentifier, today) for k in data],
                )
            )

        except:
            return -1

    @staticmethod
    def getPositiveHistoryPercent(data, periodDescription):
        if data.get("CommercialPositiveHistory") is None:
            return 0.0

        positiveHistoryObject = data["CommercialPositiveHistory"]

        try:
            return [
                k["PercentageOfPeriodFrom"]
                for k in positiveHistoryObject
                if k["PeriodDescription"] == periodDescription
            ][0]
        except:
            return 0.0

    @staticmethod
    def shareholderHasRestrictions(data):
        if data.get("Partner") is None:
            return False

        return any([i["RestrictionIndicator"] == "S" for i in data["Partner"]])

    @staticmethod
    def getUpdateDate(data) -> datetime.date:
        return parser.isoparse(
            sorted(
                data["ReturnDataSerasa"]["InquiriesLastMonthly"],
                key=lambda l: l["RecordData"],
            )[-1]["RecordData"]
        ).date()

    @staticmethod
    def dataNotOlderThan(data, minDate: datetime.date) -> bool:
        return SerasaData.getUpdateDate(data=data) > minDate

    @staticmethod
    def formatForDigifi(data: dict) -> dict:
        lawsuitSummary = SerasaData.findSummaryItem(data, "ACAO JUDICIAL")
        protestSummary = SerasaData.findSummaryItem(data, "PROTESTO")
        overdueSummary = SerasaData.findSummaryItem(data, "DIVIDA VENCIDA")

        result = {
            "cnpj": data["GeneralData"]["CNPJ"],
            "bankruptcy": data.get("BankruptcyConcordata", 0),
            "lawsuit_quantity": 0
            if lawsuitSummary is None
            else sum(item["Amount"] for item in lawsuitSummary),
            "lawsuit_value": 0
            if lawsuitSummary is None
            else sum(
                item["SummationOccurrenceConcentreSummary"] for item in lawsuitSummary
            ),
            "lawsuit_number_of_months_since_last": SerasaData.getNumberOfMonthsSinceLatest(
                data["Lawsuit"], "Date"
            ),
            "protest_quantity": 0
            if protestSummary is None
            else sum(item["Amount"] for item in protestSummary),
            "protest_value": 0
            if protestSummary is None
            else sum(
                item["SummationOccurrenceConcentreSummary"] for item in protestSummary
            ),
            "protest_number_of_months_since_last": SerasaData.getNumberOfMonthsSinceLatest(
                data["Protests"], "Date"
            ),
            "pefin_quantity": 0
            if data["Pefin"] is None
            else data["Pefin"][0]["QuantityPendingFinancial"],
            "pefin_value": 0
            if data["Pefin"] is None
            else data["Pefin"][0]["FinancialPendencyTotalValue"],
            "pefin_number_of_months_since_last": SerasaData.getNumberOfMonthsSinceLatest(
                data["Pefin"], "DateFinancialPending"
            ),
            "refin_quantity": 0
            if data["Refin"] is None
            else data["Refin"][0]["QuantityPendingFinancial"],
            "refin_value": 0
            if data["Refin"] is None
            else data["Refin"][0]["FinancialPendencyTotalValue"],
            "refin_number_of_months_since_last": SerasaData.getNumberOfMonthsSinceLatest(
                data["Refin"], "DateFinancialPending"
            ),
            "overdue_quantity": 0
            if overdueSummary is None
            else sum(item["Amount"] for item in overdueSummary),
            "overdue_value": 0
            if overdueSummary is None
            else sum(
                item["SummationOccurrenceConcentreSummary"] for item in overdueSummary
            ),
            "website": data["GeneralData"]["HomePage"],
            "number_of_employees": int(data["GeneralData"]["NumberOfEmployees"], 10),
            "presumed_sales": (
                data.get("PresumedSales")
                if data.get("PresumedSales") is not None
                else 0
            ).get("Value", 0),
            "estimated_credit_limit": data.get("ReferenceBusinessSummarized", {}).get(
                "CreditLimit", 0
            )
            if data.get("ReferenceBusinessSummarized") is not None
            else 0,
            "payment_habits_on_time_percent": (
                data.get("PaymentHabits")
                if data.get("PaymentHabits") is not None
                else {"PaymentHabits": 0}
            ).get("PERAVISTA", 0),
            "payment_habits_8_15_percent": (
                data.get("PaymentHabits")
                if data.get("PaymentHabits") is not None
                else {"PaymentHabits": 0}
            ).get("PER8A15", 0),
            "payment_habits_16_30_percent": (
                data.get("PaymentHabits")
                if data.get("PaymentHabits") is not None
                else {"PaymentHabits": 0}
            ).get("PER16A30", 0),
            "payment_habits_31_60_percent": (
                data.get("PaymentHabits")
                if data.get("PaymentHabits") is not None
                else {"PaymentHabits": 0}
            ).get("PER31A60", 0),
            "payment_habits_60_plus_percent": (
                data.get("PaymentHabits")
                if data.get("PaymentHabits") is not None
                else {"PaymentHabits": 0}
            ).get("PERAC60", 0),
            "positive_history_on_time_percent": SerasaData.getPositiveHistoryPercent(
                data, "A VISTA"
            )
            + SerasaData.getPositiveHistoryPercent(data, "PONTUAL"),
            "positive_history_8_15_percent": SerasaData.getPositiveHistoryPercent(
                data, "8-15"
            ),
            "positive_history_16_30_percent": SerasaData.getPositiveHistoryPercent(
                data, "16-30"
            ),
            "positive_history_31_60_percent": SerasaData.getPositiveHistoryPercent(
                data, "31-60"
            ),
            "positive_history_60_plus_percent": SerasaData.getPositiveHistoryPercent(
                data, "+60"
            ),
            "months_since_last_shareholder_addition": SerasaData.getNumberOfMonthsSinceLatest(
                data["Partner"], "EntryDate"
            ),
            "shareholder_has_restriction": SerasaData.shareholderHasRestrictions(data),
            "inquiries_quantity": len(data["Inquiries"]),
            "companyType": SerasaData.companyType(data),
        }

        return result
