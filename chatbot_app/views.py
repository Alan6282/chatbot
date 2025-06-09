from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django.db.models import Q
from .forms import *
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.utils import timezone
import datetime
import json
from datetime import timedelta
from django.contrib.auth import authenticate, login ,update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


LANGUAGE_NAME_TO_CODE = {
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Mandarin": "zh"
}
def index(request):
    return render(request,'index.html')
def admin(request):
    return render(request,'admin.html')
def user_registration(request):  
    if request.method == 'POST' :
        form = user_details(request.POST)
        form_1=login_data(request.POST)
        if form.is_valid() and form_1.is_valid():
            login_data_u=form_1.save(commit=False)
            login_data_u.user_type=1
            login_data_u.set_password(form_1.cleaned_data['password'])
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
                user_session =user_login.objects.get(email=email)
                user = authenticate(request,email=email,password=password)
                if user is not None:
                     
                      # log the user in and setting sessions by django built-in auth system
                     login(request, user) 
                     print('user_type',user.user_type)
                     if user.user_type == 1:
                      print('users_id',user.id)
                      request.session['userid'] = user.id
                      return redirect('user_home')
                     elif user.user_type == 2 and user.status == 1:
                      print('expert_id',user.id)
                      request.session['expertid'] = user.id
                      return redirect('expert_home')
                     elif user.user_type == 3:
                        request.session['adminid'] = user.id
                        return redirect('admin') 
                     
                     print('expert_id',request.session['expertid'])
                     print('user_id',request.session['userid'])

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
       form = Expert_login(request.POST,request.FILES)
       form_1 = login_data(request.POST,request.FILES)
       if form.is_valid() and form_1.is_valid():
            expert_data=form_1.save(commit=False)
            expert_data.set_password(form_1.cleaned_data['password'])
            expert_data.user_type=2
            expert_data.save()
            user_data=form.save(commit=False)
            user_data.login_id=expert_data
            user_data.save()
            return redirect('logins')
       else:
            print("Form Errors:", form.errors)  # Debugging
            print("Form_1 Errors:", form_1.errors)  # Debugging

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
    print(user_id)
    login=get_object_or_404(user_login,id=user_id)
    print(user_id)
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
          if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})  # Return JSON response

          else:
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
                  # NEW: Check if it's an AJAX request
          if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})  # Return JSON response

          else:
           return redirect('chat_with_user',login_id=login_id)
    return render(request,'chat1.html',{'messages':messages,'receiver_id':receiver_id,'sender_id':sender_id,'name':user_id.name})
def Assessment(request):
    return render(request,'assessment_quest.html')
def lang_selection(request):
        # languages = [
        # ('es', 'Spanish', 'https://flagcdn.com/w40/es.png', 
        #  'Learn the world\'s second-most spoken native language'),
        # ('fr', 'French', 'https://flagcdn.com/w40/fr.png',
        #  'Language of love, fashion, and cuisine'),
        # ('de', 'German', 'https://flagcdn.com/w40/de.png',
        #  'Key language for business in Europe'),
        # ('it', 'Italian', 'https://flagcdn.com/w40/it.png',
        #  'Discover the language of art and history'),
        # ('ja', 'Japanese', 'https://flagcdn.com/w40/jp.png',
        #  'Master the language of anime and technology'),
        # ('zh', 'Mandarin', 'https://flagcdn.com/w40/cn.png',
        #  'Learn the world\'s most spoken language')
        #             ]
        languages=list(Language.objects.all())
        
        session_id=request.session.get('userid')
        print(session_id)
        id=get_object_or_404(user_login,id=session_id)
        user=get_object_or_404(user_det,login_id=id)
        print(user.id)
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
def quiz_page(request, id):
    user = Language_selection.objects.get(id=id)
    selected_language = user.language
    selected_difficulty = user.difficulty
    selected_language_code = LANGUAGE_NAME_TO_CODE.get(selected_language)


    questions = list(AssessmentQuestion.objects.filter(language=selected_language_code, difficulty=selected_difficulty))

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
    return redirect('Join_conf')
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
def mocktest_start(request):
    session_id = request.session.get('userid')
    if not session_id:
        return redirect('logins')
    
    # Get user objects
    user_id = get_object_or_404(user_login, id=session_id)
    
    selected_langs = Language_selection.objects.filter(user_id=user_id)\
                        .values_list('language', flat=True).distinct()

    LANGUAGE_NAMES = {
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',  # Fixed typo in 'German'
        'it': 'Italian',
        'ja': 'Japanese',
        'zh': 'Mandarin'
    }
    
    lang_choices = [(code, LANGUAGE_NAMES.get(code, code)) for code in selected_langs]
    
    if not lang_choices:
        return redirect('language_selection')

    if request.method == 'POST':
        form = MockTestLanguageForm(lang_choices, request.POST)
        if form.is_valid():
            lang_code = form.cleaned_data['language']
            # Initialize test session without flushing entire session
            request.session.update({
                'test_data': {
                    'current_index': 0,
                    'answers': {},
                    'start_time': timezone.now().isoformat(),
                    'lang_code': lang_code
                }
            })
            return redirect('take_test', lang_code=lang_code)
    
    form = MockTestLanguageForm(lang_choices)
    return render(request, 'mocktest_language_select.html', {'form': form})

def take_test(request, lang_code):
    # Check user session
    if 'userid' not in request.session:
        return redirect('logins')
    
    test_data = request.session.get('test_data', {})
    
    # Verify test session matches requested language
    if test_data.get('lang_code') != lang_code:
        return redirect('mocktest_start')
    
    # Initialize or reset test session
    if 'reset' in request.GET:
        del request.session['test_data']
        return redirect('take_test', lang_code=lang_code)
    
    questions = list(mock_test.objects.filter(language=lang_code))
    total_questions = len(questions)
    
    # Handle test completion
    if test_data.get('current_index', 0) >= total_questions:
        return redirect('mocktest_results', lang_code=lang_code)
    
    # Calculate remaining time
    start_time = timezone.datetime.fromisoformat(test_data['start_time'])
    time_limit = timedelta(minutes=10)
    elapsed = timezone.now() - start_time
    remaining = time_limit - elapsed
    
    if remaining.total_seconds() <= 0:
        return redirect('mocktest_results', lang_code=lang_code)
    
    # Handle question navigation
    if request.method == 'POST':
        form = MockTestForm(request.POST, question=questions[test_data['current_index']])
        if form.is_valid():
            # Save answer
            test_data['answers'][str(test_data['current_index'])] = form.cleaned_data['answer']
            
            # Update index
            if 'next' in request.POST and test_data['current_index'] < total_questions - 1:
                test_data['current_index'] += 1
            elif 'previous' in request.POST and test_data['current_index'] > 0:
                test_data['current_index'] -= 1
            elif 'submit' in request.POST :
                return redirect('mocktest_results',lang_code=lang_code)
            
            # Update session
            request.session['test_data'] = test_data
            request.session.modified = True
    
    # Prepare context
    context = {
        'question': questions[test_data['current_index']],
        'form': MockTestForm(question=questions[test_data['current_index']]),
        'current_index': test_data['current_index'] + 1,
        'total_questions': total_questions,
        'progress': ((test_data['current_index'] + 1) / total_questions) * 100,
        'lang_code': lang_code,
        'time_limit': max(int(remaining.total_seconds()),0)
    }
    
    return render(request, 'mock_test.html', context)
def mocktest_results(request, lang_code):
    # Check user session
    if 'userid' not in request.session:
        return redirect('logins')
    
    test_data = request.session.get('test_data', {})
    
    # Get test questions and answers
    questions = list(mock_test.objects.filter(language=lang_code))
    user_answers = test_data.get('answers', {})
    
    results = []
    score = 0
    
    for idx, question in enumerate(questions):
        user_answer = user_answers.get(str(idx), "No answer")
        is_correct = user_answer == question.correct_answer
        if is_correct:
            score += 1
            
        results.append({
            'question': question,
            'user_answer': user_answer,
            'is_correct': is_correct,
            'options': [
                question.options1,
                question.options2,
                question.options3,
                question.options4
            ]
        })
    
    total_questions = len(questions)
    percentage = (score / total_questions * 100) if total_questions > 0 else 0
    
    context = {
        'results': results,
        'score': score,
        'total_questions': total_questions,
        'percentage': round(percentage, 2),
        'lang_code': lang_code
    }
    
    # Clear test session data
    if 'test_data' in request.session:
        del request.session['test_data']
    
    return render(request, 'mocktest_results.html', context)
def forgot_password(request):
    if request.method == 'POST':
        email =request.POST['email']
        password=request.POST['password']
        confirm_password = request.POST['confirm_password']
        if user_login.objects.filter(email=email).exists():
            if password == confirm_password:
                password_update = get_object_or_404(user_login,email=email)
                password_update.password=password
                password_update.save()
                return redirect('logins')
            else:
                messages.info(request,"Password Not Matching")
                return redirect('forgot_password')
        
        else:
            messages.info(request,"Email Doesn t Exists")
            return redirect('forgot_password')
        
    else:
        
        return render(request,'forgot-password.html')
def admin_assess_question(request):
    assessment_questions = AssessmentQuestion.objects.all()
    return render(request,'admin_assessment_view.html',{'assessment_questions':assessment_questions})
def admin_mocktest_question(request):
    mock_questions=mock_test.objects.all()
    return render(request,'admin_mocktest_view.html',{'mock_questions':mock_questions})
def language_create(request):
    if request.method == 'POST':
        form=language(request.POST)
        form.save()
        redirect('create_lang')
    else:
        form=language()
    return render(request,'lang_creation.html',{'form':form})
def language_view(request):
    if request.method == 'POST':
        lang_id = request.POST.get('lang_id')
        language_instance = get_object_or_404(Language, id=lang_id)
        form = language(request.POST, instance=language_instance)
        if form.is_valid():
            form.save()
            return redirect('language_view')
    else:
        form = None

        languages = Language.objects.all()
        return render(request,'admin_language_view.html',{'languages':languages,'edit_form': form})
def edit_language(request, lang_id):
    language_instance = get_object_or_404(Language, id=lang_id)
    if request.method == 'POST':
        form = language(request.POST, instance=language_instance)
        if form.is_valid():
            form.save()
            return redirect('language_view')
    else:
        form = language(instance=language_instance)
    return render(request, 'edit_language.html', {'form': form})
def delete_language(request,lang_id):
    language_instance =get_object_or_404(Language, id=lang_id)
    language_instance.delete()
    return redirect('language_view')
def get_new_messages(request):
    # Authentication check
    # getting session id from user or expert
    user_id = request.session.get('userid')
    expert_id = request.session.get('expertid')
    # Check if user_id or expert_id is present in the session
    if not user_id and not expert_id:
        return JsonResponse({'error':'Unauthorized'},status=401)
        return redirect('logins')
    # Get Request Parameters
    last_id = request.GET.get('last_id',0)
    receiver_id =request.GET.get('receiver_id')
    sender_id =request.GET.get('sender_id')

    #validate parameters
    try:
        last_id = int(last_id)
        receiver = user_login.objects.get(id=receiver_id)
        sender = user_login.objects.get(id=sender_id)
    except (ValueError,user_login.DoesNotExist):
        return JsonResponse({'error':'Invalid Parameters'},status=400)
    
    # Check authorization
    loggedin_id = str(user_id or expert_id)
    if loggedin_id not in [receiver_id,sender_id]:
        return JsonResponse({'error':'Unauthorized'},status=401)
    
    # Fetch new messages
    messages = Expert_user_chat.objects.filter(
        Q(sender_id=receiver,receiver_id=receiver) | Q(sender_id=receiver,receiver_id= sender),
        id__gt=last_id
    ).order_by('current_time')


    # Serialize messages 
    message_list =[]
    for msg in messages:
        message_list.append({
            'id':msg.id,
            'message':msg.message,
            'sender_id':msg.sender_id.id,
            'current_time':msg.current_time.strftime("%H:%M"),
            'current_date':msg.current_date.strftime("%B %d, %Y"),
            })
    return JsonResponse({'messages':message_list})
def logout(request):
    # clear the session data
    request.session.flush()
    return redirect('logins')

def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if check_password(form.cleaned_data['old_password'], user.password):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)  # keep user logged in
                request.session['userid'] = user.id
                return redirect('user_prof')  # or wherever you want
            else:
                form.add_error('old_password', 'Incorrect current password.')
    else:
        form = ChangePasswordForm()
    return render(request, 'user_change_password.html', {'form': form})

def expert_change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if check_password(form.cleaned_data['old_password'], user.password):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)  # keep user logged in
                request.session['expertid'] = user.id
                return redirect('user_prof')  # or wherever you want
            else:
                form.add_error('old_password', 'Incorrect current password.')
    else:
        form = ChangePasswordForm()
    return render(request, 'expert_change_password.html', {'form': form})
def bot(request):
    user = request.user
    latest_selection = (
        Language_selection.objects.filter(user_id=user)
        .order_by('-current_date', '-current_time')
        .first()
    )
    context = {
        'user_languages': Language_selection.objects.filter(
            user_id=request.user
        ).values('language').distinct(),
        'levels': Language_selection.DIFFICULTY_LEVELS,
        'default_language': latest_selection.language if latest_selection else 'Spanish',
        'default_level': latest_selection.difficulty if latest_selection else 'A1'
    }
    return render(request,'bot.html',context)
def logout_admin(request):
    # clear the session data
    request.session.flush()
    return redirect('logins')
