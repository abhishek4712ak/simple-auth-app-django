
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import OTP
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html', {'user': request.user})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password match check
        if password != confirm_password:
            return render(
                request,
                'register.html',
                {'error': 'Passwords do not match.'}
            )

        # Username exists
        if User.objects.filter(username=username).exists():
            return render(
                request,
                'register.html',
                {'error': 'Username already exists.'}
            )

       
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_active = False
        user.save()

        # Generate OTP
        otp_code = get_random_string(
            length=6,
            allowed_chars='0123456789'
        )
        
        print(f"Generated OTP for {user.username}: {otp_code}")  # Debugging line
        
        OTP.objects.create(
            user=user,
            otp=otp_code
        )

        # Store user id in session
        request.session['user_id'] = user.id

        # Send email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is: {otp_code}',
            settings.EMAIL_HOST_USER,
            [email],        
            fail_silently=False,
        )

        # Redirect instead of render
        return redirect('verify_otp')

    # GET request = blank page
    return render(request, 'register.html')


def verify_otp(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('register')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':

        entered_otp = request.POST.get('otp')

        otp_entry = OTP.objects.filter(
            user=user
        ).order_by('-created_at').first()

        if otp_entry and otp_entry.otp == entered_otp:

            if timezone.now() - otp_entry.created_at <= timedelta(minutes=5):

                user.is_active = True
                user.save()

                auth_login(request, user)

                del request.session['user_id']

                return redirect('dashboard')

            else:
                return render(
                    request,
                    'verify_otp.html',
                    {'error': 'OTP expired'}
                )

        return render(
            request,
            'verify_otp.html',
            {'error': 'Invalid OTP'}
        )

    return render(
        request,
        'verify_otp.html'
    )

def resend_otp(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("register")

    user = User.objects.get(id=user_id)

    otp_code = get_random_string(
        length=6,
        allowed_chars='0123456789'
    )
    
    print(f"Resending OTP for {user.username}: {otp_code}")  # Debugging line
    
    OTP.objects.filter(user=user).delete()

    OTP.objects.create(
        user=user,
        otp=otp_code
    )

    send_mail(
        'Your New OTP Code',
        f'Your new OTP code is: {otp_code}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    return redirect("verify_otp")



def login(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})

        return render(request, 'login.html')


def resend_otp(request):
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)

            if user.is_active:
                return render(request, 'verify_otp.html', {'error': 'Account is already verified.', 'user_id': user.id})

            otp_code = get_random_string(length=6, allowed_chars='0123456789')
            OTP.objects.create(user=user, otp=otp_code)

            send_mail(
                'Your OTP Code',
                f'Your new OTP code is: {otp_code}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return render(request, 'verify_otp.html', {'message': 'A new OTP has been sent to your email.', 'user_id': user.id})

        return redirect('register')


def logout(request):
        auth_logout(request)
        return redirect('dashboard')
    
    
    
from django.contrib.auth.decorators import login_required


def update_username(request):

    if request.method == "POST":

        username = request.POST.get("username")

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "update_username.html",
                {"error": "Username already exists"}
            )

        request.user.username = username
        request.user.save()

        return render(
            request,
            "update_username.html",
            {"success": "Username updated successfully"}
        )

    return render(request, "update_username.html")



def update_email(request):

    if request.method == "POST":

        email = request.POST.get("email")

        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            return render(
                request,
                "update_email.html",
                {"error": "Email already exists"}
            )

        request.user.email = email
        request.user.save()

        return render(
            request,
            "update_email.html",
            {"success": "Email updated successfully"}
        )

    return render(request, "update_email.html")

    

from django.contrib.auth import update_session_auth_hash


@login_required
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Check current password
        if not request.user.check_password(current_password):
            return render(
                request,
                "password_change.html",
                {"error": "Current password is incorrect."}
            )

        # Check password match
        if new_password != confirm_password:
            return render(
                request,
                "password_change.html",
                {"error": "New passwords do not match."}
            )

        # Set new password
        request.user.set_password(new_password)
        request.user.save()

        # Keep user logged in
        update_session_auth_hash(request, request.user)

        return render(
            request,
            "password_change.html",
            {"success": "Password updated successfully."}
        )

    return render(request, "password_change.html")