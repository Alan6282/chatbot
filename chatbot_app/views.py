from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from .forms import *
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.utils import timezone
import datetime
import json
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
        if form.is_valid() and form_1.is_valid():
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
        users = user_det.objects.select_related('login_id').prefetch_related(
        'login_id__user_lan_selection').all()

        return render(request,'admin_userview.html',{'users':users})
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
def conference(request,id):
    req=get_object_or_404(Expert_request,id=id)
    return render(request,'video_conference.html',{'req':req})
def expert_request(request,login_id):
    #getting userid from session 
    user_id=request.session.get('userid')
    #getting user,expert instance from user_login table 
    user_data=user_login.objects.get(id=user_id)   
    expert = user_login.objects.get(id=login_id)
    #save the Value in database with status 1 as Pending 
    Expert_request.objects.create(user_id=user_data,expert_id=expert,status=1)
    #redirect to the same page 
    return redirect('user_expert_search')
def expert_dashboard(request):
    #getting the expertid from session
    expert_id=request.session.get('expertid')
    if not expert_id:
        return redirect('logins')  #Redirect to login if not authenticated
    # Getting the requests for the expert
    requests=Expert_request.objects.filter(
        expert_id=expert_id#Pending Requests
    ).select_related('user_id__user_det')     #.prefetch_related('user_id__user_lan_selection')
    return render(request,'expert_request.html',{'requests':requests})
def accept_request(request, request_id):
    # Update request status to accepted (assuming 2 = accepted)
    Expert_request.objects.filter(id=request_id).update(status=2)
    
    # Redirect to video conference page
    return redirect('expert_request')

def reject_request(request, request_id):
    # Update request status to rejected (assuming 3 = rejected)
    Expert_request.objects.filter(id=request_id).update(status=3)
    return redirect('expert_request')
def schedule_conference(request,request_id):
    # Getting  Expert who's id from url and expert_id from session  matches Expert_request Table row
    expert_id_session=request.session.get('expertid')
    expert_request=get_object_or_404(Expert_request,id=request_id,expert_id=expert_id_session) 
    if request.method == 'POST':
        try:
            schedule_date=request.POST.get('schedule_date')
            schedule_time=request.POST.get('schedule_time')
            if not schedule_time or not schedule_date:
                raise ValueError("Date and Time are Required")
            
            #combine Time and Date
            schedule_datetime = datetime.datetime.strptime(
                f"{schedule_date} {schedule_time}",
                "%Y-%m-%d %H:%M"
            )
            schedule_datetime = timezone.make_aware(schedule_datetime)
            #check the selected date is in future 
            if schedule_datetime <= timezone.now():
                return render(request, 'schedule_conference.html', {
                    'error': 'Please select a future date and time',
                    'request_id': request_id
                })
            expert_request.schedule_date = schedule_date
            expert_request.schedule_time = schedule_time
            expert_request.status = 4  # Mark as scheduled
            expert_request.save()

            return redirect('expert_request')


        except Exception as e:
            return render(request, 'schedule_conference.html', {
                'error': 'Invalid date/time format',
                'request_id': request_id
            })
    # GET request - show form
    return render(request, 'Schedule_conference.html', {
        'today': timezone.now().date(),
        'request_id': request_id
    })
def user_request(request):
  # getting the user_id from session
  user_id=request.session.get('userid')
  # Fetch the requests based on the user_id from the Expert_request table
  requests=Expert_request.objects.filter(user_id=user_id).select_related('expert_id__expert')
  return render(request,'user_view_request.html',{'requests':requests})
def save_video_url(request,request_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')

        if url:
            Video_url = get_object_or_404(Expert_request, id=request_id)
            
            Video_url.url = url
            
            Video_url.save()

            return JsonResponse({'success': True, 'message': 'URL saved successfully'})

        return JsonResponse({'success': False, 'message': 'No URL provided'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
#API endpoint view function for fetch the latest url from Expert_request table
def get_latest_url(request,request_id):
    try:
        conf_url = Expert_request.objects.get(id=request_id)
        return JsonResponse({'url': conf_url.url})
    # catches the user.DoesNotExist Exception from the try block 
    except Expert_request.DoesNotExist:
        return JsonResponse({'error':'Not found'},status=404)
#
def create_mock_test(request):
    if request.method == 'POST':
        form=Mock_Test(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('create-mocktest')
            
    else:
        form=Mock_Test()
    return render(request,'create_mock_test.html',{'form':form})
def start_test(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        request.session['test_started'] = True
        request.session['language'] = language
        request.session['current_question'] = 0
        request.session['start_time'] = datetime.datetime.now().isoformat()
        return redirect('take_test')
    return render(request, 'start_test.html')

def take_test(request):
    if not request.session.get('test_started'):
        return redirect('start_test')
    
    language = request.session['language']
    questions = list(mock_test.objects.filter(language=language))
    total_questions = len(questions)
    current_index = request.session['current_question']
    
    if request.method == 'POST':
        form = MockTestForm(request.POST, question=questions[current_index])
        if form.is_valid():
            # Save answers in session
            request.session.setdefault('answers', {})
            request.session['answers'][str(current_index)] = form.cleaned_data['answer']
            request.session.modified = True
            
            if 'next' in request.POST:
                current_index += 1
            elif 'previous' in request.POST:
                current_index -= 1
            
            request.session['current_question'] = current_index
            return redirect('take_test')
    
    form = MockTestForm(question=questions[current_index])
    
    progress = ((current_index + 1) / total_questions) * 100
    
    context = {
        'question': questions[current_index],
        'form': form,
        'current_index': current_index + 1,
        'total_questions': total_questions,
        'progress': progress,
        'time_limit': 10 * 60  # 10 minutes in seconds
    }
    return render(request, 'mock_test.html', context)