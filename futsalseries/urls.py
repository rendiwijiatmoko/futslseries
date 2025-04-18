from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

ADMIN_SITE_HEADER = "Futsal Series CMS"
ADMIN_SITE_TITLE = "Futsal Series Admin"
ADMIN_INDEX_TITLE = "Dashboard Futsal Series"

admin.site.site_header = ADMIN_SITE_HEADER
admin.site.site_title = ADMIN_SITE_TITLE
admin.site.index_title = ADMIN_INDEX_TITLE


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('teams/', include('apps.teams.urls')),
    path('matches/', include('apps.matches.urls')), 
    path('blog/', include('apps.blog.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
