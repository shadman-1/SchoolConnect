from django.shortcuts import get_object_or_404, render, redirect
from Admin.models import School,Student
from Admin.forms import SchoolForm
from rest_framework import generics, status
from rest_framework.response import Response
from Admin.serializers import SchoolSerializer
from rest_framework.views import APIView

def school_list(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form to create a new School object
            return redirect('school_list')  # Redirect to the same page to display the updated list
    else:
        form = SchoolForm()

    schools = School.objects.all()  # Fetch all School objects
    # return render(request, 'shadman.html', {'form': form, 'schools': schools})

    search_term = request.GET.get('search_term', '')
    filter_option = request.GET.get('filter_option', 'name')

    if search_term:
        if filter_option == 'name':
            schools = School.objects.filter(name__icontains=search_term)
        elif filter_option == 'email':
            schools = School.objects.filter(contact_email__icontains=search_term)
    else:
        schools = School.objects.all()

    return render(request, 'shadman.html', {'form':form,'schools': schools})


def delete_school(request, pk):
    school = get_object_or_404(School, pk=pk)
    school.delete()
    return redirect('school_list')

def edit_school(request, pk):
    school= get_object_or_404(School, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact_email = request.POST.get('contact_email')

        # Update school object
        school.name = name
        school.address = address
        school.contact_email = contact_email
        school.save()  # Save changes to the database

        # Redirect back to the school list
        return redirect('school_list')

    return render(request, 'shadman.html', {'school': school})



def add_student(request, school_id):
    school = get_object_or_404(School, id=school_id)
    if request.method == "POST":
        asdfname = request.POST.get('name')
        email = request.POST.get('email')
        registration_number = request.POST.get('registration_number')

        student = Student.objects.create(school= school, name= asdfname,
                                         email=email,registration_number= registration_number)

    
    return render(request, 'shadman.html', {'student':student})
    
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('school_list')

def school_detail(request, school_id):
    school = get_object_or_404(School, id=school_id)
    return render(request, 'school_detail.html', {'school': school})

class SchoolList(generics.ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolAPIView(APIView):
    # GET method for retrieving a list of schools or a single school by ID
    def get(self, request, school_id=None):
        if school_id:
            # Retrieve a specific school by ID
            school = get_object_or_404(School, id=school_id)
            serializer = SchoolSerializer(school)
            return Response(serializer.data)
        else:
            # Retrieve a list of all schools
            schools = School.objects.all()
            serializer = SchoolSerializer(schools, many=True)
            return Response(serializer.data)

    # POST method for creating a new school
    def post(self, request):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH method for partially updating an existing school by ID
    def patch(self, request, school_id=None):
        school = get_object_or_404(School, id=school_id)
        serializer = SchoolSerializer(school, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
