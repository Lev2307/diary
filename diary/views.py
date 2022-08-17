from urllib import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from .models import DiaryModel
from django.views.generic import CreateView, UpdateView
from .forms import CreateDiaryForm, EditDiaryForm
from django.http import Http404

class HomeView(View):
    model = DiaryModel
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name, {'user': user})

class ReadDiaryView(ListView):
    model = DiaryModel
    template_name = 'diary/read_diary.html'
    paginate_by = 4
    context_object_name = 'diarys'

    def get_queryset(self):
        user = self.request.user
        return DiaryModel.objects.filter(user=self.request.user)

class CreateDiaryView(CreateView):
    model = DiaryModel
    form_class = CreateDiaryForm
    template_name = 'diary/create_diary.html'
    success_url = reverse_lazy('read_diary')

    def post(self, request, *args, **kwargs):
        form = CreateDiaryForm()
        if request.method == 'POST':
            form = CreateDiaryForm(request.POST or None)
            if form.is_valid():
                text = form.cleaned_data.get('text')
                if len(text) > 55:
                    header = text[:55] + '...'
                else:
                    header = text
                day = form.cleaned_data.get('day_of_the_week')
                new_model = DiaryModel.objects.create(user=request.user, text=text, header=header, day_of_the_week=day)
                new_model.save()
                return redirect('read_diary')     
        return render(request, self.template_name, {'form': form})

class DetailDiaryView(DetailView):
    model = DiaryModel
    template_name = 'diary/detail_diary.html'

    def get(self, request, pk, *args, **kwargs):
        diary = DiaryModel.objects.get(id=pk)
        text = diary.text
        day = diary.day_of_the_week
        date = diary.date
        return render(request, self.template_name, {'diary': diary, 'text': text, 'day': day, 'date': date})

class EditDiaryView(UpdateView):
    model = DiaryModel
    form_class = EditDiaryForm
    template_name = 'diary/edit_diary.html'
    success_url = reverse_lazy('read_diary')

    def post(self, request, pk, *args, **kwargs):
        try:
            obj = DiaryModel.objects.get(id=pk)
        except DiaryModel.DoesNotExist:
            raise Http404
        if request.method == 'POST':
            form = EditDiaryForm(request.POST, instance=obj)
            if form.is_valid():
                edited_obj = form.save(commit=False)
                edited_obj.user = request.user
                if len(edited_obj.text) > 55:
                    edited_obj.header = edited_obj.text[:55] + '...'
                else:
                    edited_obj.header = edited_obj.text
                edited_obj.save()
                return redirect(self.success_url)
        else:
            form = EditDiaryForm(instance=obj)

        return render(request, self.template_name, {'single_object': obj, 'form': form})

# def createDiaryView(request, *args, **kwargs):
#     model = DiaryModel
#     form = CreateDiaryForm()
#     if request.method == 'POST':
#         form = CreateDiaryForm(request.POST)
#         if form.is_valid():
#             text = form.cleaned_data.get('text')
#             day = form.cleaned_data.get('days_of_the_week')
#             new_model = DiaryModel.objects.create(text=text, day_of_the_week=day)
#             new_model.save()
#             return redirect('home')
#     return render(request, 'diary/create_diary.html', {'form': form})
        