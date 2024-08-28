from django.shortcuts import render, get_object_or_404
from .models import Course, Chapter, Quiz, Question, Enrollment

from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    courses = Course.objects.all()[:3]
    return render(request, 'main/home.html', {'courses': courses})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'main/course_list.html', {'courses': courses})

def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    chapters = Chapter.objects.filter(course=course)
    return render(request, 'main/course_detail.html', {'course': course, 'chapters': chapters})

def quiz(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'main/quiz.html', {'quiz': quiz, 'questions': questions})

def profile(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'main/profile.html', {'enrollments': enrollments})


from django.shortcuts import render, get_object_or_404
from .models import Chapter

def video_view(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    context = {
        'chapter': chapter,
        'embed_url': chapter.get_embed_url(),
    }
    return render(request, 'main/video.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Chapter, Quiz, Question
from django.contrib import messages

def quiz_view(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    quiz = get_object_or_404(Quiz, chapter=chapter)
    questions = Question.objects.filter(quiz=quiz)
    
    if request.method == 'POST':
        total_questions = questions.count()
        correct_answers = 0

        for question in questions:
            selected_option = request.POST.get(f'question-{question.id}')
            correct_option_text = getattr(question, f'option{question.correct_option}')
            if selected_option == correct_option_text:
                correct_answers += 1

        score = correct_answers
        percentage_score = (score / total_questions) * 100
        passing_criteria = 60  # 60% passing criteria

        if percentage_score >= passing_criteria:
            return render(request, 'main/quiz_result.html', {
                'score': score, 
                'total_questions': total_questions, 
                'chapter': chapter, 
                'course': chapter.course,
                'passed': True
            })
        else:
            return render(request, 'main/quiz_result.html', {
                'score': score, 
                'total_questions': total_questions, 
                'chapter': chapter, 
                'course': chapter.course,
                'passed': False
            })
    
    context = {
        'chapter': chapter,
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'main/quiz.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        if request.POST['password']:
            user.set_password(request.POST['password'])
            update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
        user.save()
        return redirect('dashboard')
    return render(request, 'main/edit_profile.html')

def about_view(request):
    return render(request, 'main/about.html')

def contact_view(request):
    if request.method == 'POST':
        # Handle form submission
        # Process form data (not shown here)
        # Assuming form processing is successful
        # Redirect to home page with success message
        messages.success(request, 'Message sent successfully. Thank you!')
        return redirect('home')  # Adjust this URL name based on your project
    return render(request, 'main/contact.html')

from django.contrib import messages
from django.shortcuts import render, redirect

def submit_contact_form(request):
    if request.method == 'POST':
        # Process the form data
        # Example: Saving to database, sending emails, etc.
        
        # Assuming the form is processed successfully
        messages.success(request, 'Message sent successfully. Thank you!')
        
        # Redirect to the appropriate page, e.g., 'home'
        return redirect('home')

    # Handle GET request if needed
    return render(request, 'contact.html')
