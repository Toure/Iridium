__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

auth_info = dict(
    v2=dict(
        auth_url='http://localhost:5000/v2.0',
        username='admin',
        password='secretword',
        tenant_name='admin'
    ),
    v3=dict(
        auth_url='http://localhost:5000/v3',
        username='admin',
        password='password',
        project_name='admin',
        user_domain_name='default',
        project_domain_name='default'
    )
)

hostnodes = dict(
    controller='192.168.0.1',
    controller2='192.168.0.2',
    compute='192.168.0.3',
    compute2='192.168.0.4',
    compute3='192.168.0.5',
    compute4='192.168.0.6',
    glance='192.168.0.7',
    cinder='192.168.0.8',
    swift='192.168.0.9'
)

logging = dict(
    log_dir='/tmp/rhea'
)
