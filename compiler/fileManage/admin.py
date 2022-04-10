from django.contrib import admin

from .models import *

admin.site.register(workspace)
admin.site.register(Folder)
admin.site.register(File)
