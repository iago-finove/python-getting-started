# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import uuid


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    legal_name = models.CharField(max_length=999999)
    cep = models.CharField(max_length=999999, blank=True, null=True)
    address = models.CharField(max_length=999999, blank=True, null=True)
    cnpj = models.CharField(unique=True, max_length=999999, blank=True, null=True)
    phone_number = models.CharField(max_length=999999, blank=True, null=True)
    annual_gross = models.BigIntegerField(blank=True, null=True)
    is_verified = models.BooleanField()
    city_name = models.CharField(max_length=999999, blank=True, null=True)
    state_code = models.CharField(max_length=999999, blank=True, null=True)
    neighborhood = models.CharField(max_length=999999, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    address_compliment = models.CharField(max_length=999999, blank=True, null=True)
    annual_gross_2019 = models.BigIntegerField(blank=True, null=True)
    rating = models.TextField(blank=True, null=True)  # This field type is a guess.
    cnae = models.TextField(blank=True, null=True)  # This field type is a guess.
    confirmed_annual_revenue = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = "company"


class ResponseRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=999999)
    source_url = models.CharField(max_length=999999)
    data = models.JSONField()
    verification = models.ForeignKey(
        "Verification", models.DO_NOTHING, blank=True, null=True
    )
    cnpj = models.CharField(max_length=999999, null=True)
    last_update = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "response_record"


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=999999)
    last_name = models.CharField(max_length=999999)
    legal_name = models.CharField(max_length=999999, blank=True, null=True)
    email = models.CharField(unique=True, max_length=999999)
    phone_number = models.CharField(max_length=999999, blank=True, null=True)
    cpf = models.CharField(max_length=999999, blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField()
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    company_role = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    address = models.CharField(max_length=999999, blank=True, null=True)
    address_compliment = models.CharField(max_length=999999, blank=True, null=True)
    neighborhood = models.CharField(max_length=999999, blank=True, null=True)
    city_name = models.CharField(max_length=999999, blank=True, null=True)
    state_code = models.CharField(max_length=999999, blank=True, null=True)
    cep = models.CharField(max_length=999999, blank=True, null=True)

    class Meta:
        db_table = "user"


class Verification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.TextField()  # This field type is a guess.
    status = models.TextField()  # This field type is a guess.
    details_code = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = "verification"
