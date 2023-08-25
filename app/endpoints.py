from rest_framework import serializers

from .utils import query_param_validator
from .nested import (
    NestedCustomershipSerializer,
    NestedApplicationSerializer,
    NestedServiceSerializer,
    NestedServerSerializer,
    NestedLicenseSerializer,
    NestedContractSerializer,
    NestedIntegrationSerializer,
    NestedProviderSerializer,
    NestedKeywordSerializer,
    NestedKeywordLabelSerializer,
)
from .models import (
    BaseModel,
    Customership,
    Provider,
    License,
    Contract,
    Application,
    Service,
    Server,
    Directory,
    Integration,
    Keyword,
    KeywordSet,
)


class BaseSerializer(serializers.ModelSerializer):
    # Generated fields skip form field validation.
    base_id = serializers.CharField(required=False)
    id_prefix = serializers.CharField(required=False)

    def process_nested_objects(self, obj_attr):
        # Validate the nested_max_count parameter.
        nested_max_count = query_param_validator(
            request=self.context.get('request'), param='nested_max_count'
        )

        if nested_max_count is not None:
            return obj_attr.all()[:nested_max_count]
        return obj_attr.all()

    class Meta:
        model = BaseModel
        exclude = ('base_token',)


class CustomershipSerializer(BaseSerializer):
    class Meta:
        model = Customership
        exclude = ('base_token',)


class ProviderSerializer(BaseSerializer):
    class Meta:
        model = Provider
        exclude = ('base_token',)


class ProviderReadSerializer(BaseSerializer):
    # ManyToMany relations:
    related_services = serializers.SerializerMethodField()
    related_applications = serializers.SerializerMethodField()
    related_contracts = serializers.SerializerMethodField()

    def get_related_services(self, obj):
        return NestedServiceSerializer(
            self.process_nested_objects(obj.related_services), many=True
        ).data

    def get_related_applications(self, obj):
        return NestedApplicationSerializer(
            self.process_nested_objects(obj.related_applications), many=True
        ).data

    def get_related_contracts(self, obj):
        return NestedContractSerializer(
            self.process_nested_objects(obj.related_contracts), many=True
        ).data

    class Meta:
        model = Provider
        exclude = ('base_token',)


class LicenseSerializer(BaseSerializer):
    class Meta:
        model = License
        exclude = ('base_token',)


class LicenseReadSerializer(BaseSerializer):
    # ForeignKey relations:
    contract = NestedContractSerializer(read_only=True)

    class Meta:
        model = License
        exclude = ('base_token',)


class ContractSerializer(BaseSerializer):
    class Meta:
        model = Contract
        exclude = ('base_token',)


class ContractReadSerializer(BaseSerializer):
    # ManyToMany relations:
    related_applications = serializers.SerializerMethodField()

    # ForeignKey relations:
    provider = NestedProviderSerializer(read_only=True)

    class Meta:
        model = Contract
        exclude = ('base_token',)

    def get_related_applications(self, obj):
        return NestedContractSerializer(
            self.process_nested_objects(obj.related_applications), many=True
        ).data


class IntegrationSerializer(BaseSerializer):
    class Meta:
        model = Integration
        exclude = ('base_token',)


class IntegrationReadSerializer(BaseSerializer):
    # ForeignKey relations:
    server_platform = NestedServerSerializer(read_only=True)

    class Meta:
        model = Integration
        exclude = ('base_token',)


class ApplicationSerializer(BaseSerializer):
    class Meta:
        model = Application
        exclude = ('base_token',)


class ApplicationReadSerializer(BaseSerializer):
    # ManyToMany relations:
    service_dependency = serializers.SerializerMethodField()
    integration = serializers.SerializerMethodField()
    application_dependency = serializers.SerializerMethodField()
    installed_server = serializers.SerializerMethodField()
    customership = serializers.SerializerMethodField()

    # ForeignKey relations:
    license = NestedLicenseSerializer(read_only=True)
    contract = NestedContractSerializer(read_only=True)
    provider = NestedProviderSerializer(read_only=True)

    def get_service_dependency(self, obj):
        return NestedServiceSerializer(
            self.process_nested_objects(obj.service_dependency), many=True
        ).data

    def get_integration(self, obj):
        return NestedIntegrationSerializer(
            self.process_nested_objects(obj.integration), many=True
        ).data

    def get_application_dependency(self, obj):
        return NestedApplicationSerializer(
            self.process_nested_objects(obj.application_dependency), many=True
        ).data

    def get_installed_server(self, obj):
        return NestedServerSerializer(
            self.process_nested_objects(obj.installed_server), many=True
        ).data

    def get_customership(self, obj):
        return NestedCustomershipSerializer(
            self.process_nested_objects(obj.customership), many=True
        ).data

    class Meta:
        model = Application
        exclude = ('base_token',)


class ServiceSerializer(BaseSerializer):
    class Meta:
        model = Service
        exclude = ('base_token',)


class ServiceReadSerializer(BaseSerializer):
    # ManyToMany relations:
    required_installations = serializers.SerializerMethodField()
    related_services = serializers.SerializerMethodField()
    customership = serializers.SerializerMethodField()

    # ForeignKey relations:
    provider = NestedProviderSerializer(read_only=True)
    contract = NestedContractSerializer(read_only=True)

    def get_required_installations(self, obj):
        return NestedApplicationSerializer(
            self.process_nested_objects(obj.required_installations), many=True
        ).data

    def get_related_services(self, obj):
        return NestedServiceSerializer(
            self.process_nested_objects(obj.related_services), many=True
        ).data

    def get_customership(self, obj):
        return NestedCustomershipSerializer(
            self.process_nested_objects(obj.customership), many=True
        ).data

    class Meta:
        model = Service
        exclude = ('base_token',)


class ServerSerializer(BaseSerializer):
    class Meta:
        model = Server
        exclude = ('base_token',)


class ServerReadSerializer(BaseSerializer):
    # ManyToMany relations:
    applications = serializers.SerializerMethodField()
    customership = serializers.SerializerMethodField()

    def get_applications(self, obj):
        return NestedApplicationSerializer(
            self.process_nested_objects(obj.applications), many=True
        ).data

    def get_customership(self, obj):
        return NestedCustomershipSerializer(
            self.process_nested_objects(obj.customership), many=True
        ).data

    class Meta:
        model = Server
        exclude = ('base_token',)


class DirectorySerializer(BaseSerializer):
    class Meta:
        model = Directory
        exclude = ('base_token',)


class DirectoryReadSerializer(BaseSerializer):
    # ManyToMany relations:
    applications = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    servers = serializers.SerializerMethodField()

    def get_applications(self, obj):
        return NestedApplicationSerializer(
            self.process_nested_objects(obj.applications), many=True
        ).data

    def get_services(self, obj):
        return NestedServiceSerializer(
            self.process_nested_objects(obj.services), many=True
        ).data

    def get_servers(self, obj):
        return NestedServerSerializer(
            self.process_nested_objects(obj.servers), many=True
        ).data

    class Meta:
        model = Directory
        exclude = ('base_token',)


class KeywordSerializer(BaseSerializer):
    class Meta:
        model = Keyword
        exclude = ('base_token',)


class KeywordReadSerializer(BaseSerializer):
    # ManyToMany relations:
    broader = serializers.SerializerMethodField()
    narrower = serializers.SerializerMethodField()
    alt_label = serializers.SerializerMethodField()

    # ForeignKey relations:
    replaced_by = NestedKeywordSerializer(read_only=True)

    def get_broader(self, obj):
        return NestedKeywordSerializer(
            self.process_nested_objects(obj.broader), many=True
        ).data

    def get_narrower(self, obj):
        return NestedKeywordSerializer(
            self.process_nested_objects(obj.narrower), many=True
        ).data

    def get_alt_label(self, obj):
        return NestedKeywordLabelSerializer(
            self.process_nested_objects(obj.alt_label), many=True
        ).data

    class Meta:
        model = Keyword
        exclude = ('base_token',)


class KeywordSetSerializer(BaseSerializer):
    class Meta:
        model = KeywordSet
        exclude = ('base_token',)


class KeywordSetReadSerializer(BaseSerializer):
    # ManyToMany relations:
    keywords = serializers.SerializerMethodField()

    def get_keywords(self, obj):
        return NestedKeywordSerializer(
            self.process_nested_objects(obj.keywords), many=True
        ).data

    class Meta:
        model = KeywordSet
        exclude = ('base_token',)
