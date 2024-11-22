"""
WSGI config for TCC project.

It exposes the WSGI callable as a module-level variable named ``app`` for Vercel.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Define o módulo de configurações do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TCC.settings")

# Configuração do WSGI
application = get_wsgi_application()

# Compatibilidade com Vercel: expõe a aplicação como 'app'
# A Vercel espera uma variável chamada `app` no WSGI
app = application
