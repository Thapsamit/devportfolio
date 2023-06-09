from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project,Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import searchProject,paginateProjects
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.

def projects(request):
    projects,search_query = searchProject(request)

    custom_range,projects = paginateProjects(request,projects,6)

    context= {'projects':projects,'search_query':search_query,'custom_range':custom_range}


    return render(request,'projects.html',context)
def project(request,id):
    project = Project.objects.get(project_uuid=id)
    context = {'project':project}
    
    return render(request,'single-project.html',context)

@login_required(login_url="login") # page to redirect 
def createProject(request):
    profile = request.user.profile
    form = ProjectForm() # instantiate class of project form to create form
    if request.method == "POST":
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit = False) # create project instance but do not save it 
            project.owner = profile 
            project.save()
            return redirect('user-account')
         
    context = {'form':form}
    return render(request,"project_form.html",context)

@login_required(login_url="login") # page to redirect
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(project_uuid=pk) # getting only that project which is associated with the user profile
    form = ProjectForm(instance=project)

    if request.method=="POST":
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('user-account')
        
    context = {'form':form}
    return render(request,'project_form.html',context)

@login_required(login_url="login")
def deleteProject(request,pk):
    profile = request.user.profile 
    project = profile.project_set.get(project_uuid=pk) # getting
    if request.method=="POST":
        project.delete()
        return redirect('user-account')
    context = {'object':project}
    return render(request,'delete_template.html',context)

