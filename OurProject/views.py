import base64

from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from hackthon.models import Complaint, Profile
from hackthon.forms import RegisterForm, ComplaintForm
from hackthon.notifications import notify_citizen_and_admin

from geopy.geocoders import Nominatim


def home(request):
    return render(request, "home.html")


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            print("USER CREATED:", user.username)

            logout(request)

            messages.success(
                request,
                "Account created successfully! Please login."
            )

            return redirect("login")

        else:

            print("FORM ERRORS:")
            print(form.errors)

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        try:

            user_obj = User.objects.get(
                email__iexact=email
            )

            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    "Login successful!"
                )

                if user.is_staff:
                    return redirect("admin_dashboard")
                else:
                    return redirect("dashboard")

            else:

                messages.error(
                    request,
                    "Invalid email or password."
                )

        except User.DoesNotExist:

            messages.error(
                request,
                "Invalid email or password."
            )

    return render(
        request,
        "login.html"
    )


def logout_view(request):

    logout(request)

    return redirect("home")


@login_required
def dashboard(request):

    complaints = Complaint.objects.filter(
        citizen=request.user
    ).order_by("-created_at")

    total = complaints.count()

    resolved = complaints.filter(
        status="resolved"
    ).count()

    pending = complaints.exclude(
        status__in=["resolved", "closed"]
    ).count()

    emergency = complaints.filter(
        is_emergency=True
    ).count()

    return render(
        request,
        "dashboard.html",
        {
            "complaints": complaints,
            "total": total,
            "resolved": resolved,
            "pending": pending,
            "emergency": emergency,
        }
    )


@login_required
def create_complaint(request):

    if request.method == "POST":

        form = ComplaintForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            complaint = form.save(commit=False)

            complaint.citizen = request.user

            # =====================================
            # SAVE LIVE CAMERA CAPTURED IMAGE
            # =====================================

            captured_image = request.POST.get(
                "captured_image"
            )

            if captured_image and captured_image.startswith("data:image"):

                try:

                    format_data, imgstr = captured_image.split(
                        ";base64,"
                    )

                    ext = format_data.split("/")[-1]

                    image_data = base64.b64decode(imgstr)

                    complaint.image.save(
                        f"live_complaint_{request.user.id}.{ext}",
                        ContentFile(image_data),
                        save=False
                    )

                except Exception as e:

                    print(
                        "Live Camera Image Error:",
                        e
                    )

            # =====================================
            # AI CLASSIFICATION
            # =====================================

            from hackthon.ai_module import classify_complaint

            category, priority, department, summary, is_emergency = classify_complaint(
                complaint.description
            )

            complaint.category = category
            complaint.priority = priority
            complaint.department = department
            complaint.status = "submitted"
            complaint.ai_summary = summary
            complaint.is_emergency = is_emergency

            # =====================================
            # GET LOCATION NAME
            # =====================================

            if complaint.latitude and complaint.longitude:

                complaint.location = get_location_name(
                    complaint.latitude,
                    complaint.longitude
                )

            # =====================================
            # SAVE COMPLAINT
            # =====================================

            complaint.save()

            if is_emergency:

                messages.error(
                    request,
                    "🚨 Emergency complaint detected and flagged!"
                )

            else:

                messages.success(
                    request,
                    "Complaint submitted successfully!"
                )

            return redirect(
                "complaint_detail",
                complaint_id=complaint.id
            )

    else:

        form = ComplaintForm()

    return render(
        request,
        "complaint_form.html",
        {
            "form": form
        }
    )


def get_location_name(lat, lon):

    try:

        if not lat or not lon:
            return "Location not available"

        geolocator = Nominatim(
            user_agent="jansahayak_ai"
        )

        location = geolocator.reverse(
            f"{lat}, {lon}",
            timeout=10
        )

        if location and location.address:
            return location.address

        return f"Lat: {lat}, Lon: {lon}"

    except Exception:

        return f"Lat: {lat}, Lon: {lon}"


@login_required
def complaint_detail(request, complaint_id):

    if request.user.is_staff:

        complaint = get_object_or_404(
            Complaint,
            id=complaint_id
        )

    else:

        complaint = get_object_or_404(
            Complaint,
            id=complaint_id,
            citizen=request.user
        )

    return render(
        request,
        "complaint_detail.html",
        {
            "complaint": complaint
        }
    )


@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect("dashboard")

    total_users = User.objects.filter(
        is_staff=False
    ).count()

    total_complaints = Complaint.objects.count()

    pending_complaints = Complaint.objects.exclude(
        status__in=["resolved", "closed"]
    ).count()

    resolved_complaints = Complaint.objects.filter(
        status="resolved"
    ).count()

    emergency_complaints = Complaint.objects.filter(
        is_emergency=True
    ).count()

    recent_complaints = Complaint.objects.select_related(
        "citizen",
        "assigned_to"
    ).order_by(
        "-created_at"
    )[:10]

    return render(
        request,
        "admin_dashboard.html",
        {
            "total_users": total_users,
            "total_complaints": total_complaints,
            "pending_complaints": pending_complaints,
            "resolved_complaints": resolved_complaints,
            "emergency_complaints": emergency_complaints,
            "recent_complaints": recent_complaints,
        }
    )


@login_required
def mark_resolved(request, complaint_id):

    if not request.user.is_staff:
        return redirect("dashboard")

    if request.method != "POST":
        return redirect("admin_dashboard")

    complaint = get_object_or_404(
        Complaint,
        id=complaint_id
    )

    complaint.status = "resolved"

    complaint.save()

    notify_citizen_and_admin(
        complaint,
        "Resolved"
    )

    messages.success(
        request,
        f"Complaint #{complaint.id} has been Resolved ✅"
    )

    return redirect(
        "complaint_detail",
        complaint_id=complaint.id
    )


@login_required
def registered_citizens(request):

    if not request.user.is_staff:
        return redirect("dashboard")

    citizens = Profile.objects.filter(
        role="citizen"
    ).select_related(
        "user"
    )

    return render(
        request,
        "registered_citizens.html",
        {
            "citizens": citizens
        }
    )


@login_required
def all_complaints(request):

    if not request.user.is_staff:
        return redirect("dashboard")

    complaints = Complaint.objects.select_related(
        "citizen",
        "assigned_to"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "all_complaints.html",
        {
            "complaints": complaints
        }
    )