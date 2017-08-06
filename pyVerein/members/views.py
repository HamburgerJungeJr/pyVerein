# Import django render shortcut.
from django.shortcuts import render, get_object_or_404 as get
# Import members.
from .models import Member

# Index-View.
def index(request):
    # Get list of all members.
    members = Member.objects.order_by('last_name').order_by('first_name')
    # Set Context.
    context = {'members': members}
    # Return rendered template.
    return render(request, 'members/index.html', context)

# Detail-View.
def detail(request, member_id):
    # Get member.
    member = get(Member, pk=member_id)
    # Return rendered template.
    return render(request, 'members/detail.html', {'member': member})
