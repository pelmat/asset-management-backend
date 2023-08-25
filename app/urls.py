from rest_framework.routers import DefaultRouter
from app.views import (
    LicenseViewSet,
    ApplicationViewSet,
    ServiceViewSet,
    ServerViewSet,
    DirectoryViewSet,
    ContractViewSet,
    ProviderViewSet,
    IntegrationViewSet,
    CustomershipViewSet,
    KeywordViewSet,
    KeywordSetViewSet,
)

router = DefaultRouter()
router.register(r'application', ApplicationViewSet, basename='Application')
router.register(r'service', ServiceViewSet, basename='Service')
router.register(r'server', ServerViewSet, basename='Server')
router.register(r'directory', DirectoryViewSet, basename='Directory')
router.register(r'license', LicenseViewSet, basename='License')
router.register(r'contract', ContractViewSet, basename='Contract')
router.register(r'provider', ProviderViewSet, basename='Provider')
router.register(r'integration', IntegrationViewSet, basename='Integration')
router.register(r'customership', CustomershipViewSet, basename='Customership')
router.register(r'keyword', KeywordViewSet, basename='Keyword')
router.register(r'keywordset', KeywordSetViewSet, basename='KeywordSet')
urlpatterns = router.urls
