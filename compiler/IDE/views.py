from django.shortcuts import render 
from django.http import HttpResponse, JsonResponse
import json
from fileManage.models import Folder,File,workspace
def home(request):
    ws = workspace.objects.get(id=1)
    folders = Folder.objects.filter(workspace=ws)
    files = File.objects.filter(workspace=ws)
    return render(request, 'index.html', {'folders':folders,'files':files})
    # return render(request,"index.html")

def newFolder(request):
    if request.method == 'POST':
        folderName = request.body.decode('utf-8')
        folderName = json.loads(folderName)
        folderName = folderName['name']
        ws = workspace.objects.get(id=1)
        folder = Folder.objects.create(name=folderName,workspace = ws)
        print(folder.id)
        return JsonResponse({'id':folder.id})


def newFile(request):
    if request.method == 'POST':
        fileName = request.body.decode('utf-8')
        fileName = json.loads(fileName)
        print(fileName)
        y = fileName['name']
        x = fileName['parent']
        try:
            extension = x.split('.')[1]
        except:
            extension = ''
        file = File.objects.create(name=y,filt_type = extension)
        folder = Folder.objects.get(id=x)
        folder.files.add(file)
        folder.save()
        return JsonResponse({'id':file.id})
