from django.shortcuts import render

# Create your views here.
def forum_view(request):
    return render(request, 'forum/forum.html')
