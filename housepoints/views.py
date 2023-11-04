from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from .models import House, Student
from .forms import CreateStudentForm, AwardPointsForm, CreateHouseForm, NewUserForm

def homepage(request):
    if request.user.is_authenticated:
        houses = House.objects.filter(user = request.user).order_by('name')
        house_points = []
        for x in houses:
            total_points = 0
            students = x.students.all()
            for y in students:
                total_points += y.points
            house_points.append({"name": x.name, "points": total_points, "logo_url": x.logo_url})

        template = loader.get_template('homepage.html')
        context = {
            'houses': houses,
            'house_points': house_points
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/login')

def summary(request):
    top_student = Student.objects.filter(user = request.user).order_by('-points')[0]
    template = loader.get_template('summary.html')
    context = {
        'top_student': top_student,
    }
    return HttpResponse(template.render(context, request))

###########################################################

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context={"register_form": form}
    return render(request, "register.html", context)

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password) # imported method
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    context={"login_form": form}
    return render(request, "login.html", context)

def logout_request(request):

	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("/")

###########################################################

def houses(request):
    houses = House.objects.filter(user = request.user).order_by('name')
    # houses = House.objects.all().order_by('name')
    template = loader.get_template('houses.html')
    context = {
        'houses': houses
    }
    return HttpResponse(template.render(context, request))

def createHouse(request):
    form = CreateHouseForm()
    if request.method == "POST":
        # print('PRINTING POST REQUEST...: ', request.POST) # this is useful
        form = CreateHouseForm(request.POST)
        if form.is_valid():
            house = form.save(commit=False)
            house.user = request.user
            house.save() # does this for you!
            return redirect('/houses/')

    context = {'form': form}
    return render(request, 'create_house.html', context)

def houseDetails(request, id):
    house = House.objects.get(id=id)

    context = {
        'house': house,
    }
    return render(request, 'house_details.html', context)

def updateHouse(request, id):
    house = House.objects.get(id=id)
    form = CreateHouseForm(instance=house)

    if request.method == "POST":
        form = CreateHouseForm(request.POST, instance=house)
        if form.is_valid():
            form.save()
            return redirect('/houses/')

    context = {
        'house': house,
        'form': form,
    }
    return render(request, 'update_house.html', context)

def deleteHouse(request, id):
    house = House.objects.get(id=id)

    if request.method == "POST":
        house.delete()
        return redirect('/houses/')

    context = {
        'item': house
    }
    return render(request, 'delete_house.html', context)

###########################################################

def students(request):
    students = Student.objects.filter(user = request.user).order_by('first_name')
    # students = Student.objects.all().order_by('-points') # creates object with all instances of Student model
    template = loader.get_template('students.html') # loads in the html template
    context = {
        'students': students
    } # creates context object which contains reference for students object
    return HttpResponse(template.render(context, request)) # sends context object to template and renders HTML

def studentsSortByPoints(request):
    students = Student.objects.filter(user = request.user).order_by('-points')
    # students = Student.objects.all().order_by('-points') # creates object with all instances of Student model
    template = loader.get_template('students.html') # loads in the html template
    context = {
        'students': students
    } # creates context object which contains reference for students object
    return HttpResponse(template.render(context, request)) # sends context object to template and renders HTML

def studentsClearPoints(request):
    students = Student.objects.filter(user = request.user)
    for student in students:
        student.points = 0
        student.save()
    return redirect('/students')

def studentsAwardAll(request):
    if request.method == "POST":
        form = AwardPointsForm(request.POST)
        students = Student.objects.filter(user = request.user)
        if form.is_valid():
            for student in students:
                current_points = student.points
                data = form.cleaned_data
                points = data['points']
                student.points = current_points + points
                student.save()
            return redirect('/students/')

    form = AwardPointsForm(initial={'points': 10})
    context = {'form': form}
    return render(request, 'award_points.html', context)

def studentsAwardSelected(request):
    if request.method == "POST":
        points = int(request.POST.get("custom-points"))
        selected_student_ids = request.POST.getlist("selected_students")
        selected_students = Student.objects.filter(id__in=selected_student_ids)

        for student in selected_students:
            student.points += points
            student.save()

    return redirect('/students/')

def createStudent(request):
    if request.method == "POST":
        form = CreateStudentForm(data=request.POST, user=request.user)
        # print('PRINTING POST REQUEST...: ', request.POST) # this is useful
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('/students')
    else:
        form = CreateStudentForm(user=request.user)

    context = {'houses': houses, 'form': form}
    return render(request, 'create_student.html', context)

def updateStudent(request, id):
    student = Student.objects.get(id=id)
    form = CreateStudentForm(instance=student)

    if request.method == "POST":
        form = CreateStudentForm(data=request.POST, instance=student, user=request.user)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('/students')
    else:
        form = CreateStudentForm(instance=student, user=request.user)

    context = {
        'houses': houses,
        'student': student,
        'form': form,
    }
    return render(request, 'update_student.html', context)

def awardPoints(request, id):
    student = Student.objects.get(id=id)
    current_points = student.points

    if request.method == "POST":
        form = AwardPointsForm(request.POST, instance=student)
        if form.is_valid():
            data = form.cleaned_data
            points = data['points']
            student_updated = form.save(commit=False)
            student_updated.points = current_points + points
            student_updated.save()
            return redirect('/students/')

    form = AwardPointsForm(instance=student, initial={'points': 10})
    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'award_points.html', context)

def deleteStudent(request, id):
    student = Student.objects.get(id=id)

    if request.method == "POST":
        student.delete()
        return redirect('/students/')

    context = {
        'item': student
    }
    return render(request, 'delete_student.html', context)

def clearPoints():
    students = Student.objects.filter(user = request.user).order_by('-points')
    for student in students:
        student.points = 0
    return redirect('/students/')

###########################################################
