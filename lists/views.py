from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
from lists.forms import ItemForm,ExistingListItemForm
from lists.models import Item,List

# Create your views here.

def home_page(request):
    return render(request,'home.html',{'form':ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_,data=request.POST)
        if form.is_valid():
            #Item.objects.create(text=request.POST['text'], list=list_)
            form.save()
            return redirect('view_list', list_.id)
    return render(request, 'list.html', {'list': list_, 'form': form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(list_)
        return redirect('view_list', list_.id)
    else:
        return render(request, 'home.html', {'form':form})








