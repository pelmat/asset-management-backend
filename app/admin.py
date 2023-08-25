from django.contrib import admin
from app.models import (
    Customership,
    Provider,
    Contract,
    License,
    Application,
    Service,
    Server,
    Integration,
    Directory,
    Keyword,
    KeywordSet,
    KeywordLabel,
)


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = (
        'base_id',
        'base_token',
        'id_prefix',
        'created_time',
        'last_modified_time',
    )


class CustomershipAdmin(BaseAdmin):
    ordering = ('-last_modified_time',)


admin.site.register(Customership, CustomershipAdmin)


class ProviderAdmin(BaseAdmin):
    ordering = ('-last_modified_time',)


admin.site.register(Provider, ProviderAdmin)


class ContractAdmin(BaseAdmin):
    ordering = ('-last_modified_time',)


admin.site.register(Contract, ContractAdmin)


class LicenseAdmin(BaseAdmin):
    ordering = ('-last_modified_time',)


admin.site.register(License, LicenseAdmin)


class ApplicationAdmin(BaseAdmin):
    ordering = ('-last_modified_time',)


admin.site.register(Application, ApplicationAdmin)


class ServiceAdmin(BaseAdmin):
    ordering = ('-last_modified_time',)


admin.site.register(Service, ServiceAdmin)


class ServerAdmin(BaseAdmin):
    ordering = ('-last_modified_time',)


admin.site.register(Server, ServerAdmin)


class IntegrationAdmin(BaseAdmin):
    ordering = ('-last_modified_time',)


admin.site.register(Integration, IntegrationAdmin)


class DirectoryAdmin(BaseAdmin):
    ordering = ('-last_modified_time',)


admin.site.register(Directory, DirectoryAdmin)


class KeywordAdmin(BaseAdmin):
    ordering = ('-last_modified_time',)


admin.site.register(Keyword, KeywordAdmin)


class KeywordSetAdmin(BaseAdmin):
    ordering = ('-last_modified_time',)


admin.site.register(KeywordSet, KeywordSetAdmin)


class KeywordLabelAdmin(BaseAdmin):
    ordering = ('-last_modified_time',)


admin.site.register(KeywordLabel, KeywordLabelAdmin)
