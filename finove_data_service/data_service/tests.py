import json
import datetime
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


import os

from django.test import TestCase
from .models import ResponseRecord

# Create your tests here.
from finove_data_service.data_service.services.SerasaService import SerasaService
from finove_data_service.data_service.services.BigDataService import BigDataService

null, false, true = None, False, True

result = {
    "Message": {"MessageDesc": "Sucess", "MessageId": 200},
    "ReturnDataSerasa": {
        "DataSourceFrom": null,
        "StatusRequest": 0,
        "GeneralData": {
            "CNPJ": "14379210000147",
            "SocialName": "Easytech Tecnologia da Informacao Eireli Epp",
            "FantasyName": "Easytech Telecom",
            "StateCode": "AM",
            "City": "Manaus",
            "Neighborhood": "Pc 14 de Janeiro",
            "FullAdress": "Av Vsc de Porto Alegre 1680 Sl 12 - Pc 14 de Janeiro",
            "Adress": "Av Vsc de Porto Alegre 1680 Sl 12",
            "AdressComplement": null,
            "PostalCode": "069020130",
            "Phone": "",
            "FaxNumber": "",
            "AreaCode": "00",
            "HomePage": "",
            "Email": null,
            "Status": "02",
            "RecordNumber": "1037341",
            "DateRecordNumber": "2020-02-03T00:00:00",
            "TypeSociety": "",
            "TaxOption": "SIMPLES NACIONAL",
            "FoundationDate": "2011-09-26T00:00:00",
            "RecordDateCNPJ": "2011-09-29T00:00:00",
            "BusinessActivity": "SERVICOS DE TELEFONIA FIXA",
            "SerasaCode": "S130601",
            "NumberOfEmployees": "00000",
            "PercentagePurchase": "000",
            "PercentageSale": "000",
            "NumberOfBranches": "000000",
            "CNAE": "6110803",
            "DateOfLastTvcgMaintenance": "2020-10-10T00:00:00",
            "Nire": "13101327201",
            "TypeData": "0",
            "TaxID": "000000053508416",
            "Sic": "4899",
            "LineOfBusinessEng": "Communication services, nec",
            "LineOfBusinessPor": "Serviços de comunicação",
            "JudicialBlockade": false,
        },
        "Branch": null,
        "Products": null,
        "CorporateControlOfCapital": {
            "SocialCapitalValue": "0000000100000",
            "CapitalValuationAchieved": "0000000100000",
            "AuthorizedCapitalValue": "0000000000000",
            "DescriptionNationality": "2",
            "DescriptionOrigin": "Fechado",
            "DescriptionNature": null,
            "BoardOfTrade": false,
            "DateLastUpdateContract": "2020-11-14T00:00:00",
        },
        "Partner": [
            {
                "LegalIdentification": "F",
                "CPFCNPJ": "583187552",
                "CNPJSEQ": "0001",
                "DIGCPF": "00",
                "PartnerName": "Hellen Regina Araujo de Souza",
                "CountryOrigin": "76",
                "PercentageCapital": 100.0,
                "EntryDate": "2011-09-26T00:00:00",
                "RestrictionIndicator": "N",
                "PercentageVotingCapital": 0.0,
                "CodeSituationCompany": "02",
                "SerasaCode": "",
            }
        ],
        "AdministrativeBoard": {
            "DateLastUpdatedAdministrativeBoard": "2020-03-03T00:00:00",
            "BoardOfTradeDatabase": false,
        },
        "AdministrativeBoardDetail": [
            {
                "LegalIdentification": "F",
                "CPFCNPJ": "583187552",
                "CNPJSEQ": "0001",
                "DIGCPF": "00",
                "NameAdministrator": "Hellen Regina Araujo de Souza",
                "OfficePosition": "",
                "Country": "76",
                "CivilState": "",
                "StartDateMandate": "2011-09-26T00:00:00",
                "EndDateMandate": null,
                "RestrictionIndicator": "N",
                "CodeSituationCompany": "00",
                "EntryDate": "1022-01-10T00:00:00",
            }
        ],
        "Participated": null,
        "Antecedente": [
            {
                "SocialName": "H R A DE SOUZA EPP                                                    ",
                "DateChange": "2011-09-26T00:00:00",
                "FirstSocialName": true,
            },
            {
                "SocialName": "Easytech Tecnologia da Informacao Eireli Epp",
                "DateChange": "2020-11-14T00:00:00",
                "FirstSocialName": false,
            },
        ],
        "MergerAcquisitions": null,
        "ReferenceBusiness": null,
        "PaymentHistory": null,
        "Inquiries": [
            {
                "InquiriesDate": "2020-11-30T00:00:00",
                "InquiriesName": "Aymore Credito Financiamento e Inve.",
                "InquiriesCNPJ": "007707650",
                "QuantityInquiries": 2,
            },
            {
                "InquiriesDate": "2020-10-10T00:00:00",
                "InquiriesName": "Banco Panamericano S/A - Sp.",
                "InquiriesCNPJ": "059285411",
                "QuantityInquiries": 1,
            },
            {
                "InquiriesDate": "2020-10-02T00:00:00",
                "InquiriesName": "Dun & Bradstreet do Brasil Ltda.",
                "InquiriesCNPJ": "001485092",
                "QuantityInquiries": 1,
            },
            {
                "InquiriesDate": "2020-08-14T00:00:00",
                "InquiriesName": "Bv Financeira Sa Credito Financiame.",
                "InquiriesCNPJ": "001149953",
                "QuantityInquiries": 1,
            },
            {
                "InquiriesDate": "2020-08-13T00:00:00",
                "InquiriesName": "Banco Honda S/A.",
                "InquiriesCNPJ": "003634220",
                "QuantityInquiries": 1,
            },
        ],
        "InquiriesLastMonthly": [
            {"RecordData": "2020-11-01T00:00:00", "QuantityConsults": 1},
            {"RecordData": "2020-10-01T00:00:00", "QuantityConsults": 2},
            {"RecordData": "2020-09-01T00:00:00", "QuantityConsults": 0},
            {"RecordData": "2020-08-01T00:00:00", "QuantityConsults": 2},
            {"RecordData": "2020-07-01T00:00:00", "QuantityConsults": 1},
            {"RecordData": "2020-06-01T00:00:00", "QuantityConsults": 0},
            {"RecordData": "2020-05-01T00:00:00", "QuantityConsults": 1},
            {"RecordData": "2020-04-01T00:00:00", "QuantityConsults": 0},
            {"RecordData": "2020-03-01T00:00:00", "QuantityConsults": 0},
            {"RecordData": "2020-02-01T00:00:00", "QuantityConsults": 0},
            {"RecordData": "2020-01-01T00:00:00", "QuantityConsults": 0},
            {"RecordData": "2019-12-01T00:00:00", "QuantityConsults": 0},
            {"RecordData": "2019-11-01T00:00:00", "QuantityConsults": 0},
            {"RecordData": "2019-10-01T00:00:00", "QuantityConsults": 0},
        ],
        "Pefin": [
            {
                "QuantityPendingFinancial": 3,
                "QuantityFinancialPendingLastOccurrence": 3,
                "DateFinancialPending": "2020-01-05T00:00:00",
                "Type": "03",
                "TitleOcurrencePendingFinancial": "50",
                "FinancialPendencyGuarantor": "02",
                "FinancialPendencyValue": 50685.0,
                "FinancialPendencyContract": "0090109412",
                "FinancialPendencyOrigin": "SPC-TELEBRAS",
                "FinancialPendencyBranch": "BSA",
                "FinancialPendencyMessage": "                                ",
                "FinancialPendencyJudicialSquare": "    ",
                "FinancialPendencyDistrict": "  ",
                "FinancialPendencyCivilCourt": "",
                "FinancialPendencyDate": null,
                "FinancialPendencyProcess": "                ",
                "FinancialPendencyNetureCode": "OO ",
                "FinancialPendencyMessageSubJudice": "                                                                            ",
                "FinancialPendencyTotalValue": 163257.0,
            },
            {
                "QuantityPendingFinancial": 3,
                "QuantityFinancialPendingLastOccurrence": 3,
                "DateFinancialPending": "2019-12-05T00:00:00",
                "Type": "03",
                "TitleOcurrencePendingFinancial": "50",
                "FinancialPendencyGuarantor": "02",
                "FinancialPendencyValue": 53812.0,
                "FinancialPendencyContract": "0090103826",
                "FinancialPendencyOrigin": "SPC-TELEBRAS",
                "FinancialPendencyBranch": "BSA",
                "FinancialPendencyMessage": "                                ",
                "FinancialPendencyJudicialSquare": "    ",
                "FinancialPendencyDistrict": "  ",
                "FinancialPendencyCivilCourt": "",
                "FinancialPendencyDate": null,
                "FinancialPendencyProcess": "                ",
                "FinancialPendencyNetureCode": "OO ",
                "FinancialPendencyMessageSubJudice": "                                                                            ",
                "FinancialPendencyTotalValue": 163257.0,
            },
            {
                "QuantityPendingFinancial": 3,
                "QuantityFinancialPendingLastOccurrence": 3,
                "DateFinancialPending": "2019-11-05T00:00:00",
                "Type": "03",
                "TitleOcurrencePendingFinancial": "50",
                "FinancialPendencyGuarantor": "02",
                "FinancialPendencyValue": 58759.0,
                "FinancialPendencyContract": "0090099782",
                "FinancialPendencyOrigin": "SPC-TELEBRAS",
                "FinancialPendencyBranch": "BSA",
                "FinancialPendencyMessage": "                                ",
                "FinancialPendencyJudicialSquare": "    ",
                "FinancialPendencyDistrict": "  ",
                "FinancialPendencyCivilCourt": "",
                "FinancialPendencyDate": null,
                "FinancialPendencyProcess": "                ",
                "FinancialPendencyNetureCode": "OO ",
                "FinancialPendencyMessageSubJudice": "                                                                            ",
                "FinancialPendencyTotalValue": 163257.0,
            },
        ],
        "Refin": null,
        "ConcentreSummary": null,
        "Protests": null,
        "Lawsuit": null,
        "ParticipationBankruptcy": null,
        "BankruptcyConcordata": null,
        "FoundCheck": null,
        "CheckCCF": null,
        "PresumedSales": {
            "DTUpdates": "2020-11-30T00:00:00",
            "Value": 460000.0,
        },
        "PaymentHabits": null,
        "ReferenceBusinessSummarized": {
            "AppointmentScore": 0,
            "CreditObtained": 0,
            "PunctualityScore": 0,
            "ValueScale": 0.0,
            "CreditLimit": 36907.0,
            "CalculationDate": "2020-11-30T00:00:00",
        },
        "CommercialPositiveHistory": [],
        "CommercialPositiveAmounts": [],
        "BusinessReferences": [],
    },
}

resultBigData = {
    "Result": [
        {
            "Circles": [
                {
                    "AvgAge": 54.0,
                    "MaxAge": 54.0,
                    "MinAge": 54.0,
                    "TotalPEPs": 0,
                    "CircleType": "FIRST_LEVEL_OWNERS",
                    "TotalEntities": 1,
                    "TotalLawsuits": 159,
                    "TotalPassages": 849,
                    "LastPassageDate": "0001-01-01T00:00:00",
                    "MaxESellerLevel": "A",
                    "MinESellerLevel": "A",
                    "FirstPassageDate": "0001-01-01T00:00:00",
                    "MaxEShopperLevel": "A",
                    "MinEShopperLevel": "A",
                    "TotalBadPassages": 288,
                    "AvgEducationLevel": "FUND COMPL",
                    "AvgNameUniqueness": 0.0,
                    "MaxEducationLevel": "FUND COMPL",
                    "MaxNameUniqueness": 0.0,
                    "MinEducationLevel": "FUND COMPL",
                    "MinNameUniqueness": 0.0,
                    "StateDistribution": {
                        "AC": 0.0,
                        "AL": 0.0,
                        "AM": 0.0,
                        "AP": 0.0,
                        "BA": 0.0,
                        "CE": 0.0,
                        "DF": 0.0,
                        "ES": 0.0,
                        "EX": 0.0,
                        "GO": 0.0,
                        "MA": 0.0,
                        "MG": 1.0,
                        "MS": 0.0,
                        "MT": 0.0,
                        "PA": 0.0,
                        "PB": 0.0,
                        "PE": 0.0,
                        "PI": 0.0,
                        "PR": 0.0,
                        "RJ": 0.0,
                        "RN": 0.0,
                        "RO": 0.0,
                        "RR": 0.0,
                        "RS": 0.0,
                        "SC": 0.0,
                        "SE": 0.0,
                        "SP": 1.0,
                        "TO": 0.0,
                    },
                    "TotalClassMembers": 0,
                    "TotalESellerLevel": "A",
                    "TotalLivingPeople": 1,
                    "GenderDistribution": {"F": 0.0, "M": 1.0, "U": 0.0},
                    "TotalEShopperLevel": "A",
                    "ESellerDistribution": {
                        "A": 1.0,
                        "B": 0.0,
                        "C": 0.0,
                        "D": 0.0,
                        "E": 0.0,
                        "F": 0.0,
                        "G": 0.0,
                        "H": 0.0,
                    },
                    "Last3MonthsPassages": -2,
                    "Last6MonthsPassages": -2,
                    "TotalCompaniesOwned": 57,
                    "TotalDeceasedPeople": 0,
                    "TotalDistinctEmails": 7,
                    "TotalDistinctPhones": 11,
                    "TotalPublicServants": 0,
                    "AgeRangeDistribution": {
                        "70+": 0.0,
                        "0-16": 0.0,
                        "16-18": 0.0,
                        "18-25": 0.0,
                        "25-30": 0.0,
                        "30-40": 0.0,
                        "40-50": 0.0,
                        "50-60": 1.0,
                        "60-70": 0.0,
                        "SEM INFORMACAO": 0.0,
                    },
                    "EShopperDistribution": {
                        "A": 1.0,
                        "B": 0.0,
                        "C": 0.0,
                        "D": 0.0,
                        "E": 0.0,
                        "F": 0.0,
                        "G": 0.0,
                        "H": 0.0,
                    },
                    "Last12MonthsPassages": -2,
                    "Last18MonthsPassages": -2,
                    "MonthAveragePassages": 849,
                    "TotalRelatedEntities": 6,
                    "AvgGeographicDistance": -1.0,
                    "MaxGeographicDistance": -1.0,
                    "MinGeographicDistance": -1.0,
                    "TotalEmployedEntities": 0,
                    "TotalLawsuitsAsAuthor": 114,
                    "CircleTotalIncomeRange": "4 A 10 SM",
                    "EntitiesAvgIncomeRange": "4 A 10 SM",
                    "EntitiesMaxIncomeRange": "4 A 10 SM",
                    "EntitiesMinIncomeRange": "4 A 10 SM",
                    "TotalDistinctAddresses": 22,
                    "IncomeRangeDistribution": {
                        "2 A 4 SM": 0.0,
                        "ATE 2 SM": 0.0,
                        "4 A 10 SM": 1.0,
                        "10 A 20 SM": 0.0,
                        "ACIMA DE 20 SM": 0.0,
                        "SEM INFORMACAO": 0.0,
                    },
                    "TaxIdStatusDistribution": {
                        "Outros": 0.0,
                        "Regular": 1.0,
                        "Suspensa": 0.0,
                        "Cancelada": 0.0,
                        "TitularFalecido": 0.0,
                        "PendenteDeRegularizacao": 0.0,
                    },
                    "TotalLawsuitsAsDefendant": 36,
                    "EducationLevelDistribution": {
                        "MESTRADO": 0.0,
                        "SUP COMP": 0.0,
                        "DOUTORADO": 0.0,
                        "5A CO FUND": 0.0,
                        "6 A 9 FUND": 0.0,
                        "ANALFABETO": 0.0,
                        "ATE 5A INC": 0.0,
                        "FUND COMPL": 1.0,
                        "SUP INCOMP": 0.0,
                        "MEDIO COMPL": 0.0,
                        "MEDIO INCOMP": 0.0,
                        "SEM INFORMACAO": 0.0,
                    },
                }
            ],
            "MatchKeys": "doc{04697985000107}",
            "Collections": {
                "LastCollectionDate": "9999-12-31T23:59:59.9999999",
                "FirstCollectionDate": "0001-01-01T00:00:00",
                "TotalCollectionMonths": 0,
                "TotalCollectionOrigins": 0,
                "IsCurrentlyOnCollection": false,
                "TotalCollectionOccurrences": 0,
                "Last30DaysCollectionOrigins": 0,
                "Last90DaysCollectionOrigins": 0,
                "Last180DaysCollectionOrigins": 0,
                "Last365DaysCollectionOrigins": 0,
                "MaxConsecutiveCollectionMonths": 0,
                "Last30DaysCollectionOccurrences": 0,
                "Last90DaysCollectionOccurrences": 0,
                "Last180DaysCollectionOccurrences": 0,
                "Last365DaysCollectionOccurrences": 0,
                "CurrentConsecutiveCollectionMonths": 0,
            },
            "CompanyGroups": [
                {
                    "MaxSites": 10.0,
                    "MinSites": 0.0,
                    "TotalMEIs": 0,
                    "TotalSites": 11.0,
                    "AverageSites": 0.19298245614035087,
                    "MaxCompanyAge": 19.0,
                    "MinCompanyAge": 0.0,
                    "TotalBranches": 636,
                    "MaxIncomeRange": "ACIMA DE 25MM ATE 50MM",
                    "MinIncomeRange": "EMPRESA NAO ATIVA",
                    "TotalCompanies": 57,
                    "CNAEDistribution": {
                        "0113000": 22,
                        "0115600": 2,
                        "0131800": 3,
                        "0139306": 3,
                        "0151201": 2,
                        "0990403": 1,
                        "3530100": 1,
                        "4110700": 6,
                        "4399105": 1,
                        "4637199": 1,
                        "4639701": 2,
                        "4644301": 1,
                        "4646001": 1,
                        "4646002": 1,
                        "4649408": 1,
                        "4729699": 2,
                        "4771701": 1,
                        "4772500": 1,
                        "4781400": 1,
                        "4789001": 1,
                        "4789005": 1,
                        "5211799": 1,
                        "5611203": 1,
                        "6209100": 1,
                        "6462000": 3,
                        "6463800": 11,
                        "6810201": 8,
                        "6810202": 6,
                        "6810203": 1,
                        "7312200": 1,
                        "7420001": 1,
                        "8211300": 1,
                        "8219999": 1,
                        "8230001": 1,
                        "8299799": 1,
                        "9102301": 1,
                        "9321200": 1,
                    },
                    "CityDistribution": {
                        "ALTAIR": 9,
                        "GASPAR": 1,
                        "PASSOS": 1,
                        "BARUERI": 4,
                        "GUARACI": 2,
                        "OLIMPIA": 60,
                        "TABAPUA": 4,
                        "BARRETOS": 7,
                        "BLUMENAU": 1,
                        "GUAPIACU": 1,
                        "BEBEDOURO": 1,
                        "RIOLANDIA": 1,
                        "SEVERINIA": 3,
                        "SAO JOSE DO RIO PRETO": 2,
                    },
                    "CompanyGroupType": "OWNERS",
                    "MaxActivityLevel": 1.0,
                    "MaxDeclaredValue": 3200000000.0,
                    "MinActivityLevel": 0.0,
                    "MinDeclaredValue": 0.0,
                    "TotalHeadquarter": 28,
                    "TotalIncomeRange": "ACIMA DE 50MM ATE 100MM",
                    "TotalUniqueCNAES": 5,
                    "AverageCompanyAge": 8.350877192982455,
                    "CompanyDocNumbers": [
                        "04697985000107",
                        "04697985000298",
                        "05583187000117",
                        "07957619000138",
                        "07957619000219",
                        "07957619000308",
                        "07957619000480",
                        "07957619000561",
                        "07957619000642",
                        "07957619000723",
                        "07957619000804",
                        "07957619000995",
                        "07957619001029",
                        "07957619001100",
                        "07957619001371",
                        "07957619001452",
                        "07957619001533",
                        "07957619001614",
                        "07957619001703",
                        "07957619001886",
                        "07957619001967",
                        "07957619002009",
                        "07957619002181",
                        "07957619002262",
                        "07957619002343",
                        "07957619002424",
                        "07957619002505",
                        "07957619002696",
                        "07957619002777",
                        "08669016000101",
                        "10436727000170",
                        "11158891000125",
                        "16895987000190",
                        "18762629000134",
                        "19378407000185",
                        "19547974000118",
                        "19805583000156",
                        "20510654000172",
                        "20547537000183",
                        "20722672000118",
                        "20722672000207",
                        "20722672000380",
                        "20722672000460",
                        "21900359000195",
                        "23304846000110",
                        "26628047000198",
                        "26779951000102",
                        "26787111000183",
                        "26796033000183",
                        "27048742000143",
                        "27771010000187",
                        "29067102000106",
                        "29131160000151",
                        "30889002000144",
                        "31248938000159",
                        "34362078000178",
                        "35855415000121",
                    ],
                    "MaxEmployeesRange": "100 A 499",
                    "MaxNumberOfOwners": 6.0,
                    "MinEmployeesRange": "SEM VINCULOS",
                    "MinNumberOfOwners": 0.0,
                    "StateDistribution": {
                        "AC": 0.0,
                        "AL": 0.0,
                        "AM": 0.0,
                        "AP": 0.0,
                        "BA": 0.0,
                        "CE": 0.0,
                        "DF": 0.0,
                        "ES": 0.0,
                        "EX": 0.0,
                        "GO": 0.0,
                        "MA": 0.0,
                        "MG": 1.0,
                        "MS": 0.0,
                        "MT": 0.0,
                        "PA": 0.0,
                        "PB": 0.0,
                        "PE": 0.0,
                        "PI": 0.0,
                        "PR": 0.0,
                        "RJ": 0.0,
                        "RN": 0.0,
                        "RO": 0.0,
                        "RR": 0.0,
                        "RS": 0.0,
                        "SC": 2.0,
                        "SE": 0.0,
                        "SP": 94.0,
                        "TO": 0.0,
                    },
                    "TotalUniqueCities": 14,
                    "TotalUniqueStates": 3,
                    "AverageIncomeRange": "ACIMA DE 1MM ATE 2.5MM",
                    "TotalDeclaredValue": 12156545000.0,
                    "TotalEmployeesRange": ">= 500",
                    "TotalNumberOfOwners": 47.0,
                    "AverageActivityLevel": 0.3603492527615333,
                    "AverageDeclaredValue": 213272719.2982456,
                    "AverageEmployeeRange": ">= 500",
                    "MaxMarketplaceStores": 0.0,
                    "MinMarketplaceStores": 0.0,
                    "TotalActiveCompanies": 50,
                    "AverageNumberOfOwners": 0.8245614035087719,
                    "TaxRegimeDistribution": {
                        "LTDA": 19,
                        "EIRELI": 3,
                        "ISENTO": 1,
                        "NAO ATIVA": 7,
                        "LUCRO REAL": 1,
                        "LUCRO PRESUMIDO": 26,
                    },
                    "TotalSimplesCompanies": 0,
                    "TotalInactiveCompanies": 7,
                    "TotalMarketplaceStores": 0.0,
                    "LegalNatureDistribution": {
                        "SOCIEDADE ANONIMA FECHADA": 1,
                        "SOCIEDADE EMPRESARIA LIMITADA": 21,
                        "PRODUTOR RURAL (PESSOA FISICA)": 31,
                        "SOCIEDADE EM CONTA DE PARTICIPACAO": 1,
                        "EMPRESA INDIVIDUAL DE RESPONSABILIDADE LIMITADA (DE NATUREZA EMPRESARIA)": 3,
                    },
                    "TaxIdStatusDistribution": {"ATIVA": 50, "BAIXADA": 7},
                    "AverageMarkerplaceStores": 0.0,
                }
            ],
            "ActivityIndicators": {
                "HasActivity": true,
                "IncomeRange": "ACIMA DE 25MM ATE 50MM",
                "HasActiveSSL": true,
                "ActivityLevel": 0.25,
                "EmployeesRange": "100 A 499",
                "HasRecentEmail": true,
                "HasRecentPhone": true,
                "HasActiveDomain": true,
                "HasRecentAddress": true,
                "NumberOfBranches": 0,
                "HasCorporateEmail": false,
                "HasRecentPassages": true,
                "FirstLevelEconomicGroupMaxActivityLevel": 0.25,
                "FirstLevelEconomicGroupMinActivityLevel": 0.25,
                "FirstLevelEconomicGroupAverageActivityLevel": 0.25,
            },
        }
    ],
    "Status": {
        "collections": [{"Code": 0, "Message": "OK"}],
        "activity_indicators": [{"Code": 0, "Message": "OK"}],
        "company_group_owners": [{"Code": 0, "Message": "OK"}],
        "circles_first_level_owners": [{"Code": 0, "Message": "OK"}],
    },
    "QueryId": "3931b617-8934-451a-abde-914b02083bfb",
    "ElapsedMilliseconds": 2945.0,
}


class SerasaTests(TestCase):
    def setUp(self):
        ResponseRecord.objects.create(
            source="serasa",
            source_url="http://serasa-test.com",
            data={"GeneralData": {"CNPJ": "123456789"}},
            cnpj="123456789",
            last_update=datetime.date.today(),
        )
        self.serasaService = SerasaService()

    def test_get_serasa_data_from_db(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        responseRecord = self.serasaService.fetchData(
            cnpj="123456789", noOlder=yesterday
        )
        self.assertIsNotNone(responseRecord)
        self.assertEqual(responseRecord.cnpj, "123456789")

    @patch("finove_data_service.data_service.apis.CialProxy.CialProxy.fetchSerasaData")
    def test_fetch_serasa_data_from_free_source(self, cialProxyMock):
        cialProxyMock.return_value = result
        threeMonthsAgo = datetime.date.today() - datetime.timedelta(weeks=12)
        responseRecord = self.serasaService.fetchData(
            cnpj="14379210000147", noOlder=threeMonthsAgo
        )
        self.assertIsNotNone(responseRecord)
        cialProxyMock.assert_called_with(cnpj="14379210000147")

    @patch("finove_data_service.data_service.apis.SerasaApi.SerasaApi.fetchSerasaData")
    @patch("finove_data_service.data_service.apis.CialProxy.CialProxy.fetchSerasaData")
    def test_fetch_paid_data(self, cialProxyMock, serasaApiMock):
        cialProxyMock.return_value = None
        serasaApiMock.return_value = result
        threeMonthsAgo = datetime.date.today() - datetime.timedelta(weeks=12)
        responseRecord = self.serasaService.fetchData(
            cnpj="14379210000147", noOlder=threeMonthsAgo
        )
        self.assertIsNotNone(responseRecord)
        cialProxyMock.assert_called_with(cnpj="14379210000147")
        serasaApiMock.assert_called_with(cnpj="14379210000147")

        self.serasaService = SerasaService()

    @patch("finove_data_service.data_service.apis.CialProxy.CialProxy.fetchSerasaData")
    def test_fetch_serasa_data_from_free_source(self, cialProxyMock):
        cialProxyMock.return_value = result
        threeMonthsAgo = datetime.date.today() - datetime.timedelta(weeks=12)
        responseRecord = self.serasaService.fetchData(
            cnpj="14379210000147", noOlder=threeMonthsAgo
        )
        self.assertIsNotNone(responseRecord)
        cialProxyMock.assert_called_with(cnpj="14379210000147")

    @patch("finove_data_service.data_service.apis.SerasaApi.SerasaApi.fetchSerasaData")
    @patch("finove_data_service.data_service.apis.CialProxy.CialProxy.fetchSerasaData")
    def test_fetch_paid_data(self, cialProxyMock, serasaApiMock):
        cialProxyMock.return_value = None
        serasaApiMock.return_value = result
        threeMonthsAgo = datetime.date.today() - datetime.timedelta(weeks=12)
        responseRecord = self.serasaService.fetchData(
            cnpj="14379210000147", noOlder=threeMonthsAgo
        )
        self.assertIsNotNone(responseRecord)
        cialProxyMock.assert_called_with(cnpj="14379210000147")
        serasaApiMock.assert_called_with(cnpj="14379210000147")


class BigDataTests(TestCase):
    def setUp(self):
        ResponseRecord.objects.create(
            source="bigData",
            source_url="http://bigData-test.com",
            data={"Result": [{"MatchKeys": "doc{123456789}"}]},
            cnpj="123456789",
            last_update=datetime.date.today(),
        )
        self.bigDataService = BigDataService()

    def test_get_bigdata_data_from_db(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        responseRecord = self.bigDataService.fetchData(
            cnpj="123456789", noOlder=yesterday, companyType=1
        )
        self.assertIsNotNone(responseRecord)
        self.assertEqual(responseRecord.cnpj, "123456789")

    @patch(
        "finove_data_service.data_service.apis.BigDataApi.BigDataApi.fetchBigDataData"
    )
    def test_fetch_bigdata_data_from_paid_source(self, bigDataMock):
        bigDataMock.return_value = resultBigData
        threeMonthsAgo = datetime.date.today() - datetime.timedelta(weeks=12)
        responseRecord = self.bigDataService.fetchData(
            cnpj="07751667000175", noOlder=threeMonthsAgo, companyType=1
        )
        self.assertIsNotNone(responseRecord)
        bigDataMock.assert_called_with(cnpj="07751667000175", companyType=1)

    @patch(
        "finove_data_service.data_service.apis.BigDataApi.BigDataApi.fetchBigDataData"
    )
    def test_big_data_endpoint(self, bigDataMock):
        bigDataMock.return_value = resultBigData
        client = APIClient()
        user = User.objects.create_user(
            username="testuser", password="123456789", email="test@test.com"
        )
        token_created, created = Token.objects.get_or_create(user=user)
        token = json.loads(
            client.post(
                "/api/login/", data={"username": "testuser", "password": "123456789"}
            ).content
        )

        client.credentials(HTTP_AUTHORIZATION="Token " + token["token"])

        response = client.get("/api/data/bigData/07751667000175?companyType=1")
        data = json.loads(response.content)

        self.assertEqual(token_created.key, token["token"])
        self.assertEqual(data["otherCompaniesMaxRevenue"], 650)
        self.assertEqual(data["totalLawsuitsAsDefendant"], -350)
        self.assertEqual(data["collectionProcess"], 0)
        self.assertEqual(data["totalInquiries"], -350)

        response = client.get(
            "/api/data/bigData/07751667000175?companyType=1&rawData=true"
        )
        data = json.loads(response.content)
        self.assertEqual(
            all(
                [
                    data["Status"][z][0]["Message"] == "OK"
                    for z in [i for i in data["Status"]]
                ]
            ),
            True,
        )

        @patch(
            "finove_data_service.data_service.apis.BigDataApi.BigDataApi.fetchBigDataData"
        )
        def test_big_data_fixed_token(self, bigDataMock):
            bigDataMock.return_value = resultBigData
            client = APIClient()
            user = User.objects.create_user(
                username="testuser", password="123456789", email="test@test.com"
            )
            token_created, created = Token.objects.get_or_create(user=user)
            token = json.loads(
                client.post(
                    "/api/login/",
                    data={
                        "username": "DigiFi",
                        "password": "7ThDVQJ5uecM6Z=?Q*u5_KyjjGxRG5",
                    },
                ).content
            )

            client.credentials(
                HTTP_AUTHORIZATION="Token " + "1e946d2db914e0efc4c5bf8ae2a0cadc22e03ec2"
            )  # "token["token"])
            response = client.get("/api/data/bigData/07751667000175?companyType=1")
            data = json.loads(response.content)

            # self.assertEqual(token_created.key, token["token"])
            self.assertEqual(data["otherCompaniesMaxRevenue"], 650)
            self.assertEqual(data["totalLawsuitsAsDefendant"], -350)
            self.assertEqual(data["collectionProcess"], 0)
            self.assertEqual(data["totalInquiries"], -350)

            response = client.get(
                "/api/data/bigData/07751667000175?companyType=1&rawData=true"
            )
            data = json.loads(response.content)
            self.assertEqual(
                all(
                    [
                        data["Status"][z][0]["Message"] == "OK"
                        for z in [i for i in data["Status"]]
                    ]
                ),
                True,
            )