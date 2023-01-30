from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect

from .models import House, Student
from .forms import CreateStudentForm, AwardPointsForm, CreateHouseForm

def homepage(request):
    houses = House.objects.all().order_by('name')
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

    ###########################################################

def houses(request):
    houses = House.objects.all().order_by('name')
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
            form.save() # does this for you!
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
    students = Student.objects.all().order_by('-points') # creates object with all instances of Student model
    template = loader.get_template('students.html') # loads in the html template
    context = {
        'students': students
    } # creates context object which contains reference for students object
    return HttpResponse(template.render(context, request)) # sends context object to template and renders HTML

def createStudent(request):
    form = CreateStudentForm()
    if request.method == "POST":
        # print('PRINTING POST REQUEST...: ', request.POST) # this is useful
        form = CreateStudentForm(request.POST)
        if form.is_valid():
            form.save() # does this for you!
            return redirect('/students/')

    context = {'form': form}
    return render(request, 'create_student.html', context)

def updateStudent(request, id):
    student = Student.objects.get(id=id)
    form = CreateStudentForm(instance=student)

    if request.method == "POST":
        form = CreateStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/students/')

    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'update_student.html', context)

def awardPoints(request, id):
    student = Student.objects.get(id=id)
    form = AwardPointsForm(instance=student)

    if request.method == "POST":
        form = AwardPointsForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/students/')

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

    ###########################################################

def testing(request):
    students = Student.objects.all()
    template = loader.get_template('template.html')
    context = {
        'fruits': ['Apple', 'Banana', 'Cherry'],
        'veg': ['Apple', 'Banana', 'Cherry'],
        'name': 'Oliver',
        'students': students
    }
    return HttpResponse(template.render(context, request))
