# write third-part API's to response record
from django.db import connection


def write_on_response_records(data, source, source_url, verification_id="NULL"):
    d2 = (
        str(data)
        .replace("'", '"')
        .replace("None", "null")
        .replace("False", "false")
        .replace("True", "true")
        # .replace("\r", "")
        # .replace("/", "$/$")
        # .replace("\\", "")
        # .replace("\n", "")
    )
    query = f""" INSERT INTO response_record (source, source_url, data,verification_id) VALUES ('{source}', '{source_url}', to_jsonb('{d2}'::json),{verification_id})"""
    with connection.cursor() as cursor:
        cursor.execute(query)