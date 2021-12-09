
from django.shortcuts import render

from .models import Contact
from .forms import ContactForm


def ContactView(request):
    model = Contact
    form = ContactForm()
    context = {'form': form}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # if form.is_valid():
        form.save()
        return render(request, 'contact/success.html')
    
    
    return render(request, 'contact.html', context)
