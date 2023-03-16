#from .models import FirstAuth, Student, SecondAuth, SecondAuth2Budget, SecondAuth2Payment
from django.shortcuts import render
from .forms import RegistrationForm
from django.contrib.auth.models import User
from .utils import generate_password
from .models import Student

def register_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User.objects.create_user(password=request.POST['password'], username=request.POST['email'], is_superuser=True, is_staff=True)
            form.save()
            student = Student.objects.latest('id')
            student.user = user
            student.save()
            # FirstAuth.objects.create(student=student)
            # SecondAuth.objects.create(student=student)
            # SecondAuth2Payment.objects.create(student=student)
            # SecondAuth2Budget.objects.create(student=student)
            return render(request, 'register_submit.html', {'password': request.POST['password'], 'login': request.POST['email']})
    return render(request, 'register.html', {'form': form})
