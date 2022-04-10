from django.shortcuts import redirect, render 
from django.http import  JsonResponse
import json
from fileManage.models import Folder,File,workspace

from django.utils import timezone


# Code for workspace Encryption
from cryptography.fernet import Fernet
key = Fernet.generate_key()
f = Fernet(key)
def encrypt(message):
    message = message.encode()
    cipher_text = f.encrypt(message).decode('utf-8')
    return cipher_text

def decrypt(message):
    message = message.encode()
    decrypted_message = f.decrypt(message)
    return decrypted_message



def home(request,id):
    ws = workspace.objects.get(id=decrypt(id))
    folders = Folder.objects.filter(workspace=ws)
    files = File.objects.filter(workspace=ws)
    return render(request, 'index.html', {'folders':folders,'files':files})
    # return render(request,"index.html")

def newFolder(request):
    if request.method == 'POST':
        fetched_data = request.body.decode('utf-8')
        fetched_data = json.loads(fetched_data)
        folderName = fetched_data['name']
        workspace_id = decrypt(fetched_data['workspace'])
        ws = workspace.objects.get(id=workspace_id)
        ws.updated_at = timezone.now()
        ws.save()
        folder = Folder.objects.create(name=folderName,workspace = ws)
        print(folder.id)
        return JsonResponse({'id':folder.id})


def newFile(request):
    if request.method == 'POST':
        fileName = request.body.decode('utf-8')
        fileName = json.loads(fileName)
        print(fileName)
        fName = fileName['name']
        pFolder = fileName['parent']
        wId = decrypt(fileName['workspace'])
        ws = workspace.objects.get(id=wId)
        ws.updated_at = timezone.now()
        ws.save(0)
        try:
            extension = pFolder.split('.')[1]
        except:
            extension = ''
        if pFolder == -1:
            file = File.objects.create(name=fName,description='',workspace = ws,filt_type=extension)
            return JsonResponse({'id':file.id})
        file = File.objects.create(name=fName,filt_type = extension)
        folder = Folder.objects.get(id=pFolder)
        folder.files.add(file)
        folder.save()
        return JsonResponse({'id':file.id})

def theme_dracula(request):
    return redirect('/static/language_library/theme-dracula.js')

def mode_javascript(request):
    return redirect('/static/language_library/mode-javascript.js')

def mode_python(request):
    return redirect('/static/language_library/mode-python.js')

def theme_chaos(request):
    return redirect('/static/language_library/theme-chaos.js')

def mode_java(request):
    return redirect('/static/language_library/mode-java.js')


def mode_c_cpp(request):
    return redirect('/static/language_library/mode-c_cpp.js')
def fetchFile(request):
    if request.method == 'POST':
        fileId = request.body.decode('utf-8')
        fileId = json.loads(fileId)
        fileId = fileId['id']
        file = File.objects.get(id=fileId)
        print(file.description)
        return JsonResponse({'content':file.description,'name':file.name})

def submitCode(request):
    if request.method == 'POST':
        code = request.body.decode('utf-8')
        code = json.loads(code)
        fileId = code['id']
        code = code['content']
        file = File.objects.get(id=fileId)
        file.description = code
        file.save()
        return JsonResponse({'status':'success'})


def workspaces(request):

    if request.method == 'POST':
        workspace_name = request.POST.get('workspace_name')
        new_workspace = workspace.objects.create(name=workspace_name, owner = request.user)
        return redirect('/workspace/'+encrypt(str(new_workspace.id)))


    workspaces = workspace.objects.filter(owner=request.user)
    for ws in workspaces:
        ws.id = encrypt(str(ws.id))

    return render(request,'workspaces.html',{'workspaces':workspaces})
