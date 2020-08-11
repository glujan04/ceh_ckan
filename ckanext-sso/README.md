# Plugin ckanext-sso
## Instalación
Activa tu entorno virtual CKAN:
```bash
. /usr/lib/ckan/default/bin/activate
```

Ir a ckan src:
```bash
cd/usr/lib/ckan/default/src/
```

Copiar e instalar el plugin sso en un entorno virtual:
```bash
cd ckanext-sso
python setup.py develop
```

Añadir 'sso' a la variable `ckan.plugins` de configuracion de ckan `production.ini`, por ejemplo:
```bash
ckan.plugins = resource_proxy stats datastore sso
```

Finalmente, reiniciar su servidor web.
```bash
sudo service apache2 reload
```
## Templates
Hay que verificar que los siguientes templates del plugin de  `ckanext-scds-theme` situado en la ruta `/usr/lib/ckan/default/src/ckanext-scds-theme/ckanext/scds_theme/templates` tienen estos contenidos:
- base.html: (URL de conexión con el componente de autenticación Smart Costa del SOl)
  ```bash
  {%- block scripts %}
  <script src="https://intranetscds.idomdev.es/auth/token-delivery-core.js"></script>
  <script src="https://intranetscds.idomdev.es/auth/token-delivery-ckan.js"></script>
  {% endblock -%}
  ```
- hearder.html:
  ```bash
  {% block header_account_notlogged %}
    <li>
        <a href="{{ h.url_for('/user/login/sso') }}" title="{{ _('Log in') }}"> {{ _('Log in') }} </a>
    </li>
  {% endblock %}

  ```
