from django.db import models


class BaseModel(models.Model):
    HIDDEN = 'hidden'
    DRAFT = 'draft'
    PUBLISHED = 'published'

    VISIBILITY_TYPES = [
        (HIDDEN, 'Hidden'),
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]

    INDEPLOYMENT = 'in_deployment'
    INUSE = 'in_use'
    UNUSED = 'unused'
    SHUTDOWN = 'shutdown'
    ARCHIVED = 'archived'
    UNDEFINED = 'undefined'
    UNRELEASED = 'unreleased'
    DELETED = 'deleted'

    OBJ_STATUSES = [
        (INDEPLOYMENT, 'In Deployment'),
        (INUSE, 'In Use'),
        (UNUSED, 'Unused'),
        (SHUTDOWN, 'Shutdown'),
        (ARCHIVED, 'Archived'),
        (UNDEFINED, 'Waiting for Definition'),
        (UNRELEASED, 'Waiting for Release'),
        (DELETED, 'Deleted'),
    ]

    CRITICAL = 'critical'
    HIGH = 'high'
    NORMAL = 'normal'
    LOW = 'low'
    NOCLASS = 'noclass'

    OBJ_CRITICALITY = [
        (CRITICAL, 'Critical'),
        (HIGH, 'High'),
        (NORMAL, 'Normal'),
        (LOW, 'Low'),
        (NOCLASS, 'No Classification'),
    ]

    base_id = models.CharField(primary_key=True, max_length=20)
    base_token = models.CharField(max_length=16)
    id_prefix = models.CharField(max_length=5)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=1000, null=True, blank=True)
    created_time = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    last_modified_time = models.DateTimeField(
        null=True, blank=True, auto_now=True, db_index=True
    )
    visibility = models.CharField(
        max_length=140,
        choices=VISIBILITY_TYPES,
        default=DRAFT,
        verbose_name='object visibility type',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Customership(BaseModel):
    model_prefix = 'cus'


class KeywordLabel(BaseModel):
    model_prefix = 'alt'


class Keyword(BaseModel):
    model_prefix = 'key'

    CONCEPT = 'concept'
    HIERARCHY = 'hierarchy'

    ONTOLOGY_TYPES = (
        (CONCEPT, "OntologyConcept"),
        (HIERARCHY, "OntologyHierarchy"),
    )

    keyword_fi = models.CharField(max_length=400, verbose_name='keyword in finnish')
    keyword_en = models.CharField(max_length=400, verbose_name='keyword in english')
    keyword_sv = models.CharField(max_length=400, verbose_name='keyword in swedish')
    keyword_se = models.CharField(
        max_length=400, verbose_name='keyword in northern sami'
    )
    alt_label = models.ManyToManyField(
        'KeywordLabel',
        blank=True,
        related_name='keyword_labels',
        verbose_name='keyword synonyms',
    )
    deprecated = models.BooleanField(default=False)
    ontology_type = models.CharField(
        default=CONCEPT, choices=ONTOLOGY_TYPES, verbose_name='ontology type'
    )
    broader = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='keyword-broader+',
        verbose_name='broader concepts',
    )
    narrower = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='keyword-narrower+',
        verbose_name='narrower concepts',
    )
    replaced_by = models.ForeignKey(
        'Keyword',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='aliases',
        verbose_name='replaced by keyword',
    )


class KeywordSet(BaseModel):
    ANY = 'any'
    APPLICATION = 'application'

    USAGE_TYPES = [
        (ANY, 'Any'),
        (APPLICATION, 'Application'),
    ]

    usage = models.CharField(
        max_length=140,
        choices=USAGE_TYPES,
        default=ANY,
        verbose_name='Intended keyword usage',
    )
    keywords = models.ManyToManyField(Keyword, blank=False, related_name='sets')


class Provider(BaseModel):
    model_prefix = 'pro'

    FRAMEWORK = 'framework'
    INHOUSE = 'inhouse'

    PROVIDER_TYPES = [
        (FRAMEWORK, 'Framework Agreement'),
        (INHOUSE, 'Inhouse'),
    ]

    business_id = models.CharField(max_length=140, verbose_name='business ID')
    provider_type = models.CharField(
        max_length=140,
        choices=PROVIDER_TYPES,
        default=FRAMEWORK,
        verbose_name='provider type',
    )
    full_address = models.CharField(max_length=140, verbose_name='full address')
    switch_phone = models.CharField(max_length=20, verbose_name='switch phone number')
    general_email = models.EmailField(
        max_length=140, verbose_name='general email address'
    )
    support_phone = models.CharField(max_length=20, verbose_name='support phone number')
    support_email = models.EmailField(
        max_length=140, verbose_name='support email address'
    )
    additional_contact = models.CharField(
        max_length=140, verbose_name='additional contact info'
    )
    related_services = models.ManyToManyField(
        'Service',
        blank=True,
        related_name='pro_services',
        verbose_name='related services',
    )
    related_applications = models.ManyToManyField(
        'Application',
        blank=True,
        related_name='pro_applications',
        verbose_name='related applications',
    )
    related_contracts = models.ManyToManyField(
        'Contract',
        blank=True,
        related_name='pro_contracts',
        verbose_name='related contracts',
    )
    provider_user_contact = models.CharField(
        max_length=140, verbose_name='provider user contact'
    )
    extra_url = models.URLField(
        max_length=140, blank=True, verbose_name='provider extra url'
    )


class Contract(BaseModel):
    model_prefix = 'con'

    MAINTENANCE = 'maintenance'
    SUPPORT_ADMIN = 'support_admin'
    CONSULTATION = 'consultation'
    SOFTWARE = 'software'
    LICENSE = 'license'

    CONTRACT_TYPES = [
        (MAINTENANCE, 'Maintenance'),
        (SUPPORT_ADMIN, 'Support & Administration'),
        (CONSULTATION, 'Consultation'),
        (SOFTWARE, 'Software'),
        (LICENSE, 'License'),
    ]

    contract_number = models.CharField(max_length=140, verbose_name='contract number')
    contract_type = models.CharField(
        max_length=140,
        choices=CONTRACT_TYPES,
        default=MAINTENANCE,
        verbose_name='contract type',
    )

    provider = models.ForeignKey(
        Provider,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='con_provider',
        verbose_name='contract provider',
    )
    provider_contact = models.CharField(max_length=140, verbose_name='provider contact')
    invoices_per_year = models.IntegerField(verbose_name='invoices per year')
    value_per_year = models.FloatField(max_length=10, verbose_name='value per year')
    place_of_use = models.CharField(max_length=140, verbose_name='place of use')
    related_applications = models.ManyToManyField(
        'Application',
        blank=True,
        related_name='con_applications',
        verbose_name='related applications',
    )
    valid_from_date = models.DateField(verbose_name='valid from date')
    valid_until_date = models.DateField(verbose_name='valid until date')
    contract_continuation = models.CharField(
        max_length=140, verbose_name='contract continuation'
    )
    contract_decisions = models.CharField(
        max_length=140, verbose_name='contract decisions'
    )
    contract_holder = models.CharField(max_length=140, verbose_name='contract holder')
    fileUrl = models.FileField(
        db_column='file_url', blank=True, null=True, upload_to='contract/'
    )


class Integration(BaseModel):
    model_prefix = 'int'

    DEVELOPMENT = 'dev'
    TESTING = 'test'
    STAGING = 'stage'
    PRODUCTION = 'prod'

    ENVIRONMENT_TYPES = [
        (DEVELOPMENT, 'Development'),
        (TESTING, 'Testing'),
        (STAGING, 'Staging'),
        (PRODUCTION, 'Production'),
    ]

    server_platform = models.ForeignKey(
        'Server',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='integration server platform',
    )
    environment_type = models.CharField(
        max_length=140,
        choices=ENVIRONMENT_TYPES,
        default=DEVELOPMENT,
        verbose_name='integration environment type',
    )


class License(BaseModel):
    model_prefix = 'lcn'

    EA = 'ea'
    EES = 'ees'
    SA = 'sa'
    SCE = 'sce'
    ORACLE = 'oracle'
    OTHER = 'other'

    LICENSE_TYPES = [
        (EA, 'Microsoft EA'),
        (EES, 'Microsoft EES'),
        (SA, 'Microsoft SA'),
        (SCE, 'Microsoft SCE'),
        (ORACLE, 'Oracle'),
        (OTHER, 'Other'),
    ]

    contract = models.ForeignKey(
        Contract,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='contract object',
    )
    audits = models.CharField(max_length=140, verbose_name='license audits')
    valid_from_date = models.DateField(verbose_name='valid from date')
    valid_until_date = models.DateField(verbose_name='valid until date')
    license_type = models.CharField(
        max_length=140,
        choices=LICENSE_TYPES,
        default=EA,
        verbose_name='license type',
    )
    fileUrl = models.FileField(
        db_column='file_url', blank=True, null=True, upload_to='license/'
    )


class Application(BaseModel):
    model_prefix = 'app'

    TOSI = 'tosi'
    TORI = 'tori'
    INFRA = 'infra'

    APP_CLASSIFICATIONS = [
        (TOSI, 'TOSI'),
        (TORI, 'TORI'),
        (INFRA, 'Infra'),
    ]

    # Application description
    classification = models.CharField(
        max_length=140,
        choices=APP_CLASSIFICATIONS,
        default=TOSI,
        verbose_name='classification',
    )
    customership = models.ManyToManyField(
        Customership,
        blank=True,
        related_name='app_customerships',
        verbose_name='customership or place of use',
    )
    application_status = models.CharField(
        max_length=140,
        choices=BaseModel.OBJ_STATUSES,
        default=BaseModel.UNDEFINED,
        verbose_name='application status',
    )
    person_register = models.BooleanField(
        verbose_name='includes personal info register'
    )
    personal_info_logging = models.BooleanField(verbose_name='personal info logging')
    install_info = models.CharField(
        max_length=500, verbose_name='additional installation info'
    )
    keywords = models.ManyToManyField(
        Keyword,
        blank=True,
        related_name='app_keywords',
        verbose_name='keywords',
    )

    # Dependencies and relations

    contract = models.ForeignKey(
        Contract,
        on_delete=models.SET_NULL,
        related_name='app_contracts',
        blank=True,
        null=True,
        verbose_name='contract object',
    )
    license = models.ForeignKey(
        License,
        on_delete=models.SET_NULL,
        related_name='app_licenses',
        blank=True,
        null=True,
        verbose_name='license object',
    )
    installed_server = models.ManyToManyField(
        'Server', blank=True, verbose_name='installed server'
    )
    application_dependency = models.ManyToManyField(
        'self', blank=True, verbose_name='application dependency'
    )
    service_dependency = models.ManyToManyField(
        'Service', blank=True, verbose_name='service dependency'
    )
    integration = models.ManyToManyField(
        Integration, blank=True, verbose_name='integrations'
    )

    # Continuity, criticality and recovery data
    update_practice = models.CharField(max_length=140, verbose_name='update practices')
    security_practice_monitoring = models.CharField(
        max_length=140, verbose_name='security practices and monitoring'
    )
    recovery_practices_convalescence = models.CharField(
        max_length=140, verbose_name='recovery practices and convalescence'
    )
    log_archives = models.CharField(
        max_length=140, verbose_name='logs and log archival'
    )
    user_rights_management = models.CharField(
        max_length=140, verbose_name='user rights management'
    )
    security_solutions = models.CharField(
        max_length=140, verbose_name='security solutions'
    )

    # Responsibilities
    product_owner = models.CharField(max_length=140, verbose_name='product owner')
    # product_owner = UserRelation?(verbose_name='product owner')
    application_holder = models.CharField(
        max_length=140, verbose_name='application holder'
    )
    # application_holder = UserRelation?(verbose_name='application holder')
    admin_users = models.CharField(
        max_length=140, verbose_name='application admin users'
    )
    # admin_users = UserRelation?(verbose_name='admin users')
    liability_professional_users = models.CharField(
        max_length=140, verbose_name='liability and professional users'
    )
    # liability_professional_users = UserRelation?(verbose_name='liability and professional users')
    holder_extra_info = models.CharField(
        max_length=140, verbose_name='application holder extra info'
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='app_provider',
        verbose_name='application provider',
    )
    provider_responsibility = models.CharField(
        max_length=140, verbose_name='provider responsibility'
    )
    additional_contacts = models.CharField(
        max_length=140, verbose_name='additional contacts'
    )
    # additional_contacts = UserRelation?(verbose_name='additional contacts')

    # Additional information
    known_issues = models.CharField(max_length=140, verbose_name='known issues')
    fileUrl = models.FileField(
        db_column='file_url', blank=True, null=True, upload_to='application/'
    )


class Service(BaseModel):
    model_prefix = 'ser'

    ONPREMISES = 'onpremises'
    IAAS = 'iaas'
    PAAS = 'paas'
    CAAS = 'caas'
    FAAS = 'faas'
    SAAS = 'saas'
    OTHER = 'other'

    SERVICE_TYPES = [
        (ONPREMISES, 'OnPremises'),
        (IAAS, 'IaaS'),
        (PAAS, 'PaaS'),
        (CAAS, 'CaaS'),
        (FAAS, 'FaaS'),
        (SAAS, 'SaaS'),
        (OTHER, 'Other'),
    ]

    ONGOING = 'ongoing'
    TEMPORARY = 'temporary'

    VALIDITY_TYPES = [
        (ONGOING, 'Ongoing'),
        (TEMPORARY, 'Temporary'),
    ]

    service_status = models.CharField(
        max_length=140,
        choices=BaseModel.OBJ_STATUSES,
        default=BaseModel.UNDEFINED,
        verbose_name='service status',
    )
    contract = models.ForeignKey(
        Contract,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='contract object',
    )
    customership = models.ManyToManyField(
        Customership,
        blank=True,
        related_name='ser_customerships',
        verbose_name='customership or place of use',
    )
    criticality = models.CharField(
        max_length=140,
        choices=BaseModel.OBJ_CRITICALITY,
        default=BaseModel.NORMAL,
        verbose_name='service criticality',
    )
    service_level = models.CharField(max_length=140, verbose_name='service level')
    service_type = models.CharField(
        max_length=140,
        choices=SERVICE_TYPES,
        default=ONPREMISES,
        verbose_name='service type',
    )
    validity_type = models.CharField(
        max_length=140,
        choices=VALIDITY_TYPES,
        default=ONGOING,
        verbose_name='service validity time type',
    )
    limitations = models.CharField(max_length=140, verbose_name='service limitations')
    related_services = models.ManyToManyField(
        'self', blank=True, verbose_name='related services'
    )
    required_installations = models.ManyToManyField(
        Application,
        blank=True,
        related_name='ser_applications',
        verbose_name='required application installations',
    )
    product_owner = models.CharField(max_length=140, verbose_name='product owner')
    service_holder = models.CharField(max_length=140, verbose_name='service holder')
    provider = models.ForeignKey(
        Provider,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='ser_provider',
        verbose_name='service provider',
    )
    provider_role = models.CharField(max_length=140, verbose_name='provider role')
    provider_contact = models.CharField(
        max_length=140, verbose_name='provider contact information'
    )
    additional_contacts = models.CharField(
        max_length=140, verbose_name='additional contacts'
    )
    fileUrl = models.FileField(
        db_column='file_url', blank=True, null=True, upload_to='service/'
    )


class Server(BaseModel):
    model_prefix = 'srv'

    server_role = models.CharField(max_length=140, verbose_name='server role')
    customership = models.ManyToManyField(
        Customership,
        blank=True,
        related_name='srv_customerships',
        verbose_name='server customership',
    )
    place_of_use = models.CharField(
        max_length=140, verbose_name='server location or place of use'
    )
    product_owner = models.CharField(max_length=140, verbose_name='product owner')

    dns_names = models.CharField(max_length=140, verbose_name='dns names')
    server_model = models.CharField(max_length=140, verbose_name='server model')
    backup_data = models.CharField(max_length=140, verbose_name='backup data')
    backup_device = models.CharField(max_length=140, verbose_name='backup device')

    public_ip_addresses = models.CharField(
        max_length=140, verbose_name='public ip addresses'
    )
    dns_names = models.CharField(
        max_length=140, verbose_name='dns names and ip addresses'
    )
    server_type = models.CharField(max_length=140, verbose_name='server type')
    environment_type = models.CharField(max_length=140, verbose_name='environment type')

    dedicated = models.CharField(max_length=140, verbose_name='dedicated server')
    maintenance_window = models.CharField(
        max_length=140, verbose_name='maintenance window'
    )
    server_criticality = models.CharField(
        max_length=140,
        choices=BaseModel.OBJ_CRITICALITY,
        default=BaseModel.NORMAL,
        verbose_name='server criticality',
    )
    security_level = models.CharField(
        max_length=140, verbose_name='server security level'
    )
    service_level = models.CharField(max_length=140, verbose_name='service level')

    server_status = models.CharField(max_length=140, verbose_name='server status')
    install_date = models.DateField(verbose_name='install date')
    ip_address = models.CharField(max_length=140, verbose_name='server ip address')
    updates = models.CharField(
        max_length=140, verbose_name='information on server updates'
    )

    verification_practices = models.CharField(
        max_length=140, verbose_name='verification practices and controls'
    )
    recovery_practices_convalescence = models.CharField(
        max_length=140, verbose_name='recovery practices and convalescence'
    )
    logging = models.CharField(max_length=140, verbose_name='server logging')
    access_rights_management = models.CharField(
        max_length=140, verbose_name='access rights management'
    )

    security_solutions = models.CharField(
        max_length=140, verbose_name='security solutions'
    )
    external_rights = models.CharField(
        max_length=140, verbose_name='external rights access management'
    )
    domain_name = models.CharField(max_length=140, verbose_name='domain name')
    sub_domain = models.CharField(max_length=140, verbose_name='sub domain')

    ip_address_type = models.CharField(max_length=140, verbose_name='ip address type')
    subnet_mask = models.CharField(max_length=140, verbose_name='subnet mask')
    default_gateway = models.CharField(max_length=140, verbose_name='default gateway')
    mac_address = models.CharField(max_length=140, verbose_name='mac address')

    applications = models.ManyToManyField(
        Application, blank=True, related_name='servers'
    )


class Directory(BaseModel):
    model_prefix = 'dir'

    class Meta:
        verbose_name = 'Directory'
        verbose_name_plural = 'Directories'

    applications = models.ManyToManyField(
        Application, blank=True, related_name='directories'
    )
    services = models.ManyToManyField(Service, blank=True, related_name='directories')
    servers = models.ManyToManyField(Server, blank=True, related_name='directories')


'''

class Costs(BaseModel):

    app_relation = models.ForeignKey(Application, blank=True, null=True)
    service_relation = models.ForeignKey(Service, blank=True, null=True)
    server_relation = models.ForeignKey(Server, blank=True, null=True)

    costs_description = models.CharField(
        max_length=140, verbose_name='costs description')
    app_costs_sum = models.FloatField(
        max_length=10, verbose_name='float sum of application costs')
    license_costs_sum = models.FloatField(
        max_length=10, verbose_name='float sum of license costs')
    number_of_licenses = models.IntegerField(
        max_length=10, verbose_name='number of licenses')
    overall_costs = models.FloatField(
        max_length=10, verbose_name='overall costs')

'''
