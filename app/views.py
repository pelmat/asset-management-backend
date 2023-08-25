from rest_framework import viewsets

from .models import (
    Customership,
    Provider,
    License,
    Application,
    Service,
    Server,
    Directory,
    Integration,
    Contract,
    Keyword,
    KeywordSet,
)
from .endpoints import (
    CustomershipSerializer,
    ProviderSerializer,
    ProviderReadSerializer,
    LicenseSerializer,
    LicenseReadSerializer,
    ApplicationSerializer,
    ApplicationReadSerializer,
    ServiceSerializer,
    ServiceReadSerializer,
    ServerSerializer,
    ServerReadSerializer,
    DirectorySerializer,
    DirectoryReadSerializer,
    ContractSerializer,
    ContractReadSerializer,
    IntegrationSerializer,
    IntegrationReadSerializer,
    KeywordSerializer,
    KeywordReadSerializer,
    KeywordSetSerializer,
    KeywordSetReadSerializer,
)
from .pagination import CustomPageNumberPagination

from .filters import (
    FieldsFilter,
)


class CommonViewSet(viewsets.ModelViewSet):
    filter_backends = [FieldsFilter]
    pagination_class = CustomPageNumberPagination


class CustomershipViewSet(CommonViewSet):
    serializer_class = CustomershipSerializer

    def get_queryset(self):
        return Customership.objects.all().order_by('-last_modified_time')


class ProviderViewSet(CommonViewSet):
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ProviderReadSerializer
        return ProviderSerializer

    def get_queryset(self):
        return Provider.objects.prefetch_related(
            'related_services',
            'related_applications',
            'related_contracts',
        ).order_by('-last_modified_time')


class LicenseViewSet(CommonViewSet):
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return LicenseReadSerializer
        return LicenseSerializer

    def get_queryset(self):
        return License.objects.prefetch_related('contract').order_by(
            '-last_modified_time'
        )


class ApplicationViewSet(CommonViewSet):
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ApplicationReadSerializer
        return ApplicationSerializer

    def get_queryset(self):
        return Application.objects.prefetch_related(
            'contract',
            'license',
            'installed_server',
            'application_dependency',
            'service_dependency',
            'integration',
        ).order_by('-last_modified_time')


class ServiceViewSet(CommonViewSet):
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ServiceReadSerializer
        return ServiceSerializer

    def get_queryset(self):
        return Service.objects.prefetch_related(
            'contract', 'related_services', 'required_installations', 'provider'
        ).order_by('-last_modified_time')


class ServerViewSet(CommonViewSet):
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ServerReadSerializer
        return ServerSerializer

    def get_queryset(self):
        return Server.objects.prefetch_related('applications').order_by(
            '-last_modified_time'
        )


class DirectoryViewSet(CommonViewSet):
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return DirectoryReadSerializer
        return DirectorySerializer

    def get_queryset(self):
        return Directory.objects.prefetch_related(
            'applications', 'services', 'servers'
        ).order_by('-last_modified_time')


class ContractViewSet(CommonViewSet):
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ContractReadSerializer
        return ContractSerializer

    def get_queryset(self):
        return Contract.objects.prefetch_related('related_applications').order_by(
            '-last_modified_time'
        )


class IntegrationViewSet(CommonViewSet):
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return IntegrationReadSerializer
        return IntegrationSerializer

    def get_queryset(self):
        return Integration.objects.prefetch_related('server_platform').order_by(
            '-last_modified_time'
        )


class KeywordViewSet(CommonViewSet):
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return KeywordReadSerializer
        return KeywordSerializer

    def get_queryset(self):
        return Keyword.objects.prefetch_related('broader', 'narrower').order_by(
            '-last_modified_time'
        )


class KeywordSetViewSet(CommonViewSet):
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return KeywordSetReadSerializer
        return KeywordSetSerializer

    def get_queryset(self):
        return KeywordSet.objects.prefetch_related('keywords').order_by(
            '-last_modified_time'
        )
