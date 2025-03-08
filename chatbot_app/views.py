from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from .forms import *
from django.contrib import messages
from .models import *
from django.http import JsonResponse
# Create your views here.
def index(request):
    return render(request,'index.html')
def admin(request):
    return render(request,'admin.html')
# def login(request):
#     return render(request,'login.html')
def user_registration(request):  
    if request.method == 'POST' :
        form = user_details(request.POST)
        form_1=login_data(request.POST)
        if form and form_1.is_valid():
            login_data_u=form_1.save(commit=False)
            login_data_u.user_type=1
            login_data_u.save()
            user_data=form.save(commit=False)
            user_data.login_id=login_data_u
            user_data.save()

            return redirect('logins')
        
    else:
        form = user_details()
        form_1 = login_data()
    return render(request,'user_details.html',{'form':form,'form_1':form_1})

def logins(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = user_login.objects.get(email=email)
                if user.password == password:
                     if user.user_type == 1:
                      request.session['userid'] = user.id
                      return redirect('user_home')
                     elif user.user_type == 2 and user.status == 1:
                      request.session['expertid'] = user.id
                      return redirect('expert_home')

                else:
                    messages.error(request,'Invalid Password')
            except user_login.DoesNotExist:
                messages.error(request,'User doesnot exist')            
    else:
        form = loginForm()
    return render (request,'login.html',{'form':form}) 


def user_home(request):
    return render(request,'user_home.html')

def expert_reg(request):
     if request.method == 'POST' :
       form = Expert_login(request.POST)
       form_1 = login_data(request.POST)
       if form and form_1.is_valid():
            expert_data=form_1.save(commit=False)
            expert_data.user_type=2
            expert_data.save()
            user_data=form.save(commit=False)
            user_data.login_id=expert_data
            user_data.save()
            return redirect('index')
     else:
         form = Expert_login()
         form_1 = login_data()
          
     return render(request,'expert.html',{'form':form,'form_1':form_1})
def expert_home(request):
    return render(request,'expert_home.html')
def user_profile(request):
    user_id=request.session.get('userid')
    login_det=get_object_or_404(user_login,id=user_id)
    user_data=get_object_or_404(user_det,login_id=user_id)
    if request.method=='POST':
        form=user_details(request.POST,instance=user_data)
        form1=logindata(request.POST,instance=login_det)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            return redirect('user_home')
    else:

        form=user_details(instance=user_data)
        form1=logindata(instance=login_det)
    return render(request,'user_profile.html',{'form':form,'form1':form1})

def expert_profile(request):
    expert_id=request.session.get('expertid')
    login_det=get_object_or_404(user_login,id=expert_id)
    expert_det=get_object_or_404(Expert_det,login_id=expert_id)
    if request.method=='POST':
        form=Expert_login(request.POST,instance=expert_det)
        form1=logindata(request.POST,instance=login_det)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            return redirect('expert_home')
    else:
        form=Expert_login(instance=expert_det)
        form1=logindata(instance=login_det)
    return render(request,'expert_profile.html',{'form':form,'form1':form1})
def admin_user(request):
    data=user_det.objects.all()
    return render(request,'admin_userview.html',{'data':data})
def admin_expert(request):
    expert_data=Expert_det.objects.all()
    return render(request,'admin_expertview.html',{'expert_data':expert_data})

def user_expert_search(request):
    query=request.GET.get('q','')
    results=Expert_det.objects.all()
    if query:
        results=results.filter(
            Q(experience__icontains=query)|
            Q(language__icontains=query)

        )
    return render(request,'user_expertsearch.html',{'results':results,'query':query})

def exp_approve(request,login_id):
    data=get_object_or_404(user_login,id=login_id)
    data.status=1
    data.save()
    return redirect('admin_expert')

def exp_reject(request,login_id):
    data=get_object_or_404(user_login,id=login_id)
    data.status=2
    data.save()
    return redirect('admin_expert')
def chatinterface(request):
    return render(request,'chat.html')


def chat_with_expert(request,login_id):
    user_id=request.session.get('userid')
    login=get_object_or_404(user_login,id=user_id)
    expert_id=get_object_or_404(Expert_det,login_id=login_id)
    expert_name=Expert_det.objects.all()

    sender=None
    if user_id:
        sender_id=user_login.objects.get(id=user_id)  
    elif expert_id:
        sender_id= user_login.objects.get(id=expert_id)   
    if sender_id is None:
        return render(request,"unauthorised acess") 
    try:
        receiver_id=user_login.objects.get(id=login_id)
    except login.DoesNotExist:
        return render(request,"receiver doesn't exist")
    name=None
    if user_det.objects.filter(login_id=receiver_id).exists():
        name=user_det.objects.get(login_id=receiver_id).name
    elif Expert_det.objects.filter(login_id=receiver_id).exists():
         name=Expert_det.objects.get(login_id=receiver_id).name
    else:
        name="unkown user"
    messages=Expert_user_chat.objects.filter(
        (Q(sender_id=sender_id,receiver_id=receiver_id) | Q(sender_id=receiver_id,receiver_id=sender_id))).order_by('current_time')
    if request.method=="POST":
        message=request.POST.get("message").strip()
        if message:
          Expert_user_chat.objects.create(sender_id=sender_id,receiver_id=receiver_id,message=message)
          return redirect('chat_with_expert',login_id=login_id)
    return render(request,'chat.html',{'messages':messages,'receiver_id':receiver_id,'sender_id':sender_id,'name':expert_id.name,'expert_name':expert_name})
def user_view(request):
    data=user_det.objects.all()
    return render(request,'user_view.html',{'data':data})

def chat_with_user(request,login_id):
    expert_id=request.session.get('expertid')
    login=get_object_or_404(user_login,id=expert_id)
    user_id=get_object_or_404(user_det,login_id=login_id)

    sender=None
    if expert_id:
        sender_id=user_login.objects.get(id=expert_id)  
    elif user_id:
        sender_id= user_login.objects.get(id=user_id)   
    if sender_id is None:
        return render(request,"unauthorised acess") 
    try:
        receiver_id=user_login.objects.get(id=login_id)
    except login.DoesNotExist:
        return render(request,"receiver doesn't exist")
    name=None
    if Expert_det.objects.filter(login_id=receiver_id).exists():
        name=Expert_det.objects.get(login_id=receiver_id).name
    elif user_det.objects.filter(login_id=receiver_id).exists():
         name=user_det.objects.get(login_id=receiver_id).name
    else:
        name="unkown user"
    messages=Expert_user_chat.objects.filter(
        (Q(sender_id=sender_id,receiver_id=receiver_id) | Q(sender_id=receiver_id,receiver_id=sender_id))).order_by('current_time')
    if request.method=="POST":
        message=request.POST.get("message").strip()
        if message:
          Expert_user_chat.objects.create(sender_id=sender_id,receiver_id=receiver_id,message=message)
          return redirect('chat_with_user',login_id=login_id)
    return render(request,'chat.html',{'messages':messages,'receiver_id':receiver_id,'sender_id':sender_id,'name':user_id.name})
# def lang_selection(request):
#     userid=request.session.get('userid')
#     user=user_login.objects.get(id=userid)
#     if request.method == 'POST':
#         selected_lang = request.POST.get('language')
#         # valid_languages = ['es', 'fr', 'de', 'it', 'ja', 'zh']
#         # if selected_lang not in valid_languages:
#         #     return JsonResponse({'status': 'error', 'message': 'Invalid language selected'})
#                 # Save to database
#         Language_selection.objects.update_or_create(
#             user_id=request.userid,
#             defaults={
#                 'language': selected_lang
#             }
#         )

#     return render(request,'language_selection.html')
def Assessment(request):
    return render(request,'assessment_quest.html')
def lang_selection(request):
        languages = [
        ('es', 'Spanish', 'https://flagcdn.com/w40/es.png', 
         'Learn the world\'s second-most spoken native language'),
        ('fr', 'French', 'https://flagcdn.com/w40/fr.png',
         'Language of love, fashion, and cuisine'),
        ('de', 'German', 'https://flagcdn.com/w40/de.png',
         'Key language for business in Europe'),
        ('it', 'Italian', 'https://flagcdn.com/w40/it.png',
         'Discover the language of art and history'),
        ('ja', 'Japanese', 'https://flagcdn.com/w40/jp.png',
         'Master the language of anime and technology'),
        ('zh', 'Mandarin', 'https://flagcdn.com/w40/cn.png',
         'Learn the world\'s most spoken language')
                    ]
        
        session_id=request.session.get('userid')
        id=get_object_or_404(user_login,id=session_id)
        user=get_object_or_404(user_det,login_id=id)
        if request.method == 'POST' :
         form = lang_selectionForm(request.POST)
         if form.is_valid():
            data=form.save(commit=False)
            data.user_id=id
            data.save()
            return redirect('difficulty',id=data.id)
        else:
            form=lang_selectionForm()
         
        return render(request,'language_selection2.html',{'form':form,'languages':languages})
def Question(request):
    if request.method == 'POST':

        form=Question_from(request.POST)
        if form.is_valid():
            form.save()
        
    else:
        form =Question_from()
    return render(request,'admin_assessment_quest.html',{'form':form})
def difficulty(request,id):
    if request.method == 'POST':
        diff=Language_selection.objects.get(id=id)
        form=Difficulty_form(request.POST,instance=diff)
        if form.is_valid():

          form.save()
          return redirect('quiz_page',id=diff.id)

    else:
       form=Difficulty_form()
    return render(request,'lang_difficulty.html',{'form':form})
# def quiz_page(request, id):
#     #current_question_index=[]
#     #request.session['current_question_index'] = 0
#     #print("deault value",current_question_index)
#     print("hi",id)
#     user = Language_selection.objects.get(id=id)
#     selected_language = user.language
#     selected_difficulty = user.difficulty
#     questions = AssessmentQuestion.objects.filter(language=selected_language, difficulty=selected_difficulty)
#     print("Total Questions Found:", len(questions))
#     if not questions:
#          messages.error(request, "No questions available for the selected language and difficulty.")
#          return redirect('user_home')

#     # Get the current question index from the session, default to 0 if not set
#     current_question_index = request.session.get('current_question_index',0)

#     # Check if the current question index is valid
#     # if current_question_index >= len(questions):
#     #     return redirect("quiz_result")

#     # Get the current question
#     #print(current_question_index)
#     current_question = questions[current_question_index]

#     if request.method == "POST":
#         form = QuizForm(request.POST, question=current_question)
#         if form.is_valid():
#             # Check the answer and update score if correct
#             user_answer = form.cleaned_data['answer']
#             score = request.session.get('score', 0)

#             if user_answer == current_question.correct_answer:
#                 score += 1

#             # Update score in session
#             request.session['score'] = score
#             # Move to the next question
#             if current_question_index < len(questions):
#                 current_question_index += 1
#                 request.session['current_question_index'] = current_question_index
#                 user.score=score
#                 user.save()
#                 return redirect('quiz_page', id=id)

#             # After the question is answered, delete the session variable if no longer needed
#             # del request.session['current_question_index']  # Delete the session variable after use
#             # Redirect to the same page to load the next question
#             else:
#              return redirect('lang_selection') 
   
#     else:
#         form = QuizForm(question=current_question)

#     return render(request, "quiz.html", {"form": form, "question": current_question})
def quiz_page(request, id):
    user = Language_selection.objects.get(id=id)
    selected_language = user.language
    selected_difficulty = user.difficulty
    questions = list(AssessmentQuestion.objects.filter(language=selected_language, difficulty=selected_difficulty))

    if not questions:
        messages.error(request, "No questions available for the selected language and difficulty.")
        return redirect('user_home')

    # Get the current question index from the session
    current_question_index = request.session.get('current_question_index', 0)

    # Ensure index is within bounds
    if current_question_index >= len(questions):
        return redirect('quiz_result',id=id)  # Redirect when all questions are answered

    current_question = questions[current_question_index]

    if request.method == "POST":
        form = QuizForm(request.POST, question=current_question)
        if form.is_valid():
            user_answer = form.cleaned_data['answer']
            score = request.session.get('score', 0)

            if user_answer == current_question.correct_answer:
                score += 1

            request.session['score'] = score
            user.score = score
            user.save()

            # Move to the next question
            request.session['current_question_index'] = current_question_index + 1

            return redirect('quiz_page', id=id)

    else:
        form = QuizForm(question=current_question)

    return render(request, "quiz.html", {"form": form, "question": current_question})

def quiz_result(request, id):
    user = Language_selection.objects.get(id=id)
    score = request.session.get('score', 0)  # Get the final score from session

    # Clear session data after quiz completion
    request.session.pop('current_question_index', None)
    request.session.pop('score', None)

    return render(request, "quiz_result.html", {"user": user, "score": score})
def admin_user_langSelect(request):
    return render(request,'admin_user_view.html')