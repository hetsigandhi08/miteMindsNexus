from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UploadHistory, Profile
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .utils import send_forgot_password_mail
from django.http import JsonResponse
from ultralytics import YOLO
import uuid
import os
import csv
import torch





@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname = request.POST.get('name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            error_message = "Password does not match"
            return render(request, 'signup.html', {'error_message': error_message})
            
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')
    return render(request, 'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username = request.POST.get('name')
        pass1 = request.POST.get('password')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
   
    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

# def dashboard(request):
#     videos = Video.objects.all()
#     return render(request, 'dashboard.html', {'videos': videos})

def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']
        video_name = video_file.name

        video_path = os.path.join('C:\\Users\\HP\\Desktop\\Mites Detection', video_name)

        with open(video_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        model = YOLO('C:\\Users\\HP\\Desktop\\Mites Detection\\best.pt')
        conf_threshold = 0.30 

        results = model(video_path, conf=conf_threshold, save=True)

        csv_path = os.path.join('C:\\Users\\HP\\Desktop\\Mites Detection', 'class_counts.csv')
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Frame No", "Predator Mites", "Feeder Mites"])

            for i, result in enumerate(results):
                ob = result.boxes.cls
                pred_count = torch.sum(ob == 0).item()
                feeder_count = torch.sum(ob == 1).item()
                writer.writerow([i, pred_count, feeder_count])

        final_feeder_count = 0  
        final_pred_count = 0  
        frame_of_videos = len(results)

        for result in results:  
            classes = result.boxes.cls

    # Count the number of feeder mites (class 1) and predator mites (class 0) in each frame
            # feeder_count = torch.sum(classes == 0).item()
            pred_count = torch.sum(classes == 0).item()

    # Accumulate the counts over all frames
            # final_feeder_count += feeder_count
            final_pred_count += pred_count

        mites_count = round((final_pred_count / frame_of_videos) * 10)

        UploadHistory.objects.create(user=request.user, video_name=video_name, mites_count=mites_count)
        return redirect('profile_page')
    return render(request, 'home.html') 

def profile_page(request):
    if request.user.is_superuser:
        all_users_history = UploadHistory.objects.all().select_related('user').order_by('-upload_date')
        context = {
            'all_users_history': all_users_history,
        }
    else:
        upload_history = UploadHistory.objects.filter(user=request.user)
        username = request.user.username
        context={
            'upload_history': upload_history,
            'username': username,
            }
    if request.user.is_superuser:
        for history_entry in all_users_history:
            history_entry.user_name = history_entry.user.username
            
    return render(request, 'profile.html', context)

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        user_obj = User.objects.filter(username=username).first()
        if not user_obj:
            messages.error(request, 'No user found')
            return redirect('forgot_password')

        token = str(uuid.uuid4())
        profile_obj, created = Profile.objects.get_or_create(user=user_obj)
        profile_obj.forgot_password_token = token
        profile_obj.save()

        send_forgot_password_mail(user_obj, token)
        messages.success(request, 'An email has been sent to reset your password')
        return redirect('forgot_password')

    return render(request, 'forgot-password.html')

def change_password(request):
    context = {}
    profile_obj = Profile.objects.get(forgot_password_token = token)

    print(profile_obj)
    return render(request, 'change-password.html')

def aboutus(request):
    return render(request, 'about-us.html')

def delete_entry(request, item_id):
    if request.method == 'POST':
        # Get the entry by its ID
        entry = UploadHistory.objects.get(pk=item_id)
        
        # Delete the entry
        entry.delete()
        
        # Redirect to the profile page or any other appropriate page
        return redirect('profile_page')
    else:
        # If the request method is not POST, handle the error accordingly
        return HttpResponseNotAllowed(['POST'])
    