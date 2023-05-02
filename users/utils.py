
from users.models import Skill,Profile
from django.db.models import Q


from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


def paginateProfiles(request,profiles,results):
    page = request.GET.get('page')
    results = 3 # 3 results per page 
    paginator = Paginator(profiles,results)
    try: # if page number is there then go to that page
        profiles = paginator.page(page)
    except PageNotAnInteger: # if not then render page 1 projects
        page = 1 
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages # get last page 
        profiles = paginator.page(page)
    
    leftIndex = (int(page)-1)
    if leftIndex<1:
        leftIndex =  1 
    rightIndex = (int(page)+2)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages+1

    custom_range = range(leftIndex,rightIndex)

    return custom_range,profiles


def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(skill__in=skills))

    return profiles,search_query