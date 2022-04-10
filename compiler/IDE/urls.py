from django.urls import path
from .views import * 
urlpatterns = [

    # IDE libraries paths 
    path('workspace/theme-dracula.js', theme_dracula),
    path('workspace/mode-javascript.js', mode_javascript),
    path('workspace/mode-python.js', mode_python),
    path('workspace/mode-java.js', mode_java),
    path('workspace/theme-chaos.js', theme_chaos),
    path('workspace/mode-c_cpp.js', mode_c_cpp),

    # path('', home),

    # Ajax call urls
    path('createFolder', newFolder),
    path('createFile', newFile),
    path('fetchFile', fetchFile),
    path('submitCode', submitCode),
    path('workspace', workspaces),
    path('workspace/<str:id>', home),
]