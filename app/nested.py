from rest_framework import serializers
from .models import (
    BaseModel,
    Customership,
    Provider,
    Application,
    Server,
    License,
    Contract,
    Integration,
    Service,
    Keyword,
    KeywordSet,
    KeywordLabel,
)


class NestedBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        exclude = ('base_token',)


class NestedCustomershipSerializer(NestedBaseSerializer):
    class Meta:
        model = Customership
        fields = ['base_id', 'id_prefix', 'name', 'description']


class NestedProviderSerializer(NestedBaseSerializer):
    class Meta:
        model = Provider
        fields = ['base_id', 'id_prefix', 'name', 'description']


class NestedServiceSerializer(NestedBaseSerializer):
    class Meta:
        model = Service
        fields = ['base_id', 'id_prefix', 'name', 'description']


class NestedIntegrationSerializer(NestedBaseSerializer):
    class Meta:
        model = Integration
        fields = ['base_id', 'id_prefix', 'name', 'description']


class NestedApplicationSerializer(NestedBaseSerializer):
    class Meta:
        model = Application
        fields = ['base_id', 'id_prefix', 'name', 'description']


class NestedServerSerializer(NestedBaseSerializer):
    class Meta:
        model = Server
        fields = ['base_id', 'id_prefix', 'name', 'description']


class NestedLicenseSerializer(NestedBaseSerializer):
    class Meta:
        model = License
        fields = ['base_id', 'id_prefix', 'name', 'description', 'valid_until_date']


class NestedContractSerializer(NestedBaseSerializer):
    class Meta:
        model = Contract
        fields = ['base_id', 'id_prefix', 'name', 'description']


class NestedKeywordSerializer(NestedBaseSerializer):
    class Meta:
        model = Keyword
        fields = ['base_id', 'id_prefix', 'name', 'description', 'narrower', 'broader']


class NestedKeywordSetSerializer(NestedBaseSerializer):
    class Meta:
        model = KeywordSet
        fields = ['base_id', 'id_prefix', 'name', 'description']


class NestedKeywordLabelSerializer(NestedBaseSerializer):
    class Meta:
        model = KeywordLabel
        fields = ['name']
