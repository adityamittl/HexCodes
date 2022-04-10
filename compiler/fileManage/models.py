from django.db import models
from django.contrib.auth.models import User



class workspace(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    permissions = models.ManyToManyField(User, related_name='workspace_permissions', blank=True)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    workspace = models.ForeignKey(workspace, on_delete=models.CASCADE, null=True, blank=True)
    filt_type = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name

class Folder(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    workspace = models.ForeignKey(workspace, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    permissions = models.ManyToManyField(User, related_name='folder_permissions', blank=True, default=None)
    files = models.ManyToManyField(File, related_name='folder_files', blank=True, default=None)
    def __str__(self):
        return self.name

class SharedWithMe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ManyToManyField(workspace)