import subprocess
import os
import json
from django.shortcuts import redirect, render 
from django.http import  HttpResponse, JsonResponse,HttpResponse
from fileManage.models import Folder,File,workspace,SharedWithMe
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .ocr import ocr_core


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dir = str(os.getcwd()).replace('\\','/')
print(dir)


# Code for Encryption and Decryption

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


languages = {"c": "c", "cpp": "cpp", "java": "java", "py": "python", "js": "javascript"}

# Compiling function
def compile(code,lang):
    if lang == 'python':
        file = open('code.py','w')
        file.write(code)
        file.close()
        output = subprocess.run(['python', 'code.py'],capture_output=True)
        exit_code = output.returncode
        error = output.stderr
        result = output.stdout
    elif lang == 'cpp':
        file = open('code.cpp','w')
        file.write(code)
        file.close()
        output = subprocess.run(['g++',dir+'/code.cpp', '-o', 'output'], input=code.encode(), capture_output=True)
        print(output)
        output = subprocess.run(dir+'/output', input=code.encode(), capture_output=True)
        exit_code = output.returncode
        error = output.stderr
        result = output.stdout
    elif lang == 'c':
        file = open('code.c','w')
        file.write(code)
        file.close()
        output = subprocess.run(['gcc',dir+'/code.c', '-o', 'output'], input=code.encode(), capture_output=True)
        output = subprocess.run(dir+'/output', input=code.encode(), capture_output=True)
        exit_code = output.returncode
        error = output.stderr
        result = output.stdout
    elif lang == 'java':
        file = open('code.java','w')
        file.write(code)
        file.close()
        output = subprocess.run(['javac',dir+'/code.java'], input=code.encode(), capture_output=True)
        output = subprocess.run(['java', 'code'], input=code.encode(), capture_output=True)
        exit_code = output.returncode
        error = output.stderr
        result = output.stdout
    elif lang == 'javascript':
        file = open('code.js','w')
        file.write(code)
        file.close()
        output = subprocess.run(['node', 'code.js'], input=code.encode(), capture_output=True)
        exit_code = output.returncode
        error = output.stderr
        result = output.stdout
    else:
        exit_code = 0
        error = ''
        result = ''
    data = {
        'code' : code,
        'exit_code': str(exit_code),
        'error': error.decode("utf-8") ,
        'result': str(result.decode("utf-8") )
    }
    return data


@login_required
def home(request,id):
    if request.method == 'POST':
        codeFile = request.FILES['code']
        fileId =request.POST.get('fileId')
        file = File.objects.get(id=fileId)
        fs = FileSystemStorage(location='media/')
        filename = fs.save(codeFile.name, codeFile)
        print(filename)
        code = ocr_core(os.path.join(BASE_DIR, 'media/')+filename)
        file.description = code
        file.save()
        result = compile(code,file.filt_type)
        os.remove(dir+'/media/'+filename)

    ws = workspace.objects.get(id=decrypt(id))
    if request.user != ws.owner:
        if request.user in ws.permissions.all():
            folders = Folder.objects.filter(workspace=ws)
            files = File.objects.filter(workspace=ws)
            return render(request, 'index.html', {'folders':folders,'files':files, 'workspace':ws})
    
    if request.user == ws.owner:
        folders = Folder.objects.filter(workspace=ws)
        files = File.objects.filter(workspace=ws)
        return render(request, 'index.html', {'folders':folders,'files':files, 'workspace':ws})
    
    return HttpResponse('You are not authorized to view this workspace')


@login_required
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

@login_required
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
            extension = languages[pFolder.split('.')[1].lower()]
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


@login_required
def fetchFile(request):
    if request.method == 'POST':
        fileId = request.body.decode('utf-8')
        fileId = json.loads(fileId)
        fileId = fileId['id']
        file = File.objects.get(id=fileId)
        print(file.description)
        return JsonResponse({'content':file.description,'name':file.name})


# Ajax Code Runs Here
@login_required
def submitCode(request):
    if request.method == 'POST':
        code = request.body.decode('utf-8')
        code = json.loads(code)
        fileId = code['id']
        code = code['content']
        file = File.objects.get(id=fileId)
        file.description = code
        file.save()
        code = file.description
        result = compile(code,file.filt_type)
        print(result)
        return JsonResponse({"output": result})
    

# Function to add new workspace for a user
@login_required
def workspaces(request):

    if request.method == 'POST':
        workspace_name = request.POST.get('workspace_name')
        new_workspace = workspace.objects.create(name=workspace_name, owner = request.user)
        return redirect('/workspace/'+encrypt(str(new_workspace.id)))


    workspaces = workspace.objects.filter(owner=request.user)
    try:
        shared_workspaces = SharedWithMe.objects.get(user=request.user).workspaces.all()
    except:
        shared_workspaces = []
    for ws in workspaces:
        ws.id = encrypt(str(ws.id))

    return render(request,'workspaces.html',{'workspaces':workspaces,'shared_workspaces':shared_workspaces})


# Function to grant permission to another User
@login_required
def addNewGrant(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data = json.loads(data)
        workspace_id = decrypt(data['workspace'])
        ws = workspace.objects.get(id=workspace_id)
        ws.updated_at = timezone.now()
        grantee = data['grantee']
        grantee_user = User.objects.get(username=grantee)
        ws.permissions.add(grantee_user)
        try:
            permission_table = SharedWithMe.objects.get(user=grantee_user)
            permission_table.workspaces.add(ws)
            permission_table.save()
        except:
            permission_table = SharedWithMe.objects.create(user=grantee_user)
            permission_table.workspaces.add(ws)
            permission_table.save()
        ws.save()
        return JsonResponse({'success':'true'})

@login_required
def Workspace_redirect(request):
    return redirect('/workspace')

# Functions of IDE static route redirects
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