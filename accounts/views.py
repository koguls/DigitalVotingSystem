from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from .forms import *
from .models import *





# Create your views here.

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Role to URL mapping
            role_redirects = {
                0: 'adminpanle',
                1: 'authority',  # careful, your URL name is 'authprity' not 'authoritypanle'
            }

            redirect_url = role_redirects.get(user.role)
            if redirect_url:
                return redirect(redirect_url)
            else:
                # If somehow role is not mapped
                return render(request, 'login.html', {'error': 'No redirect available for your role.'})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def adminpanel(request):
    return render(request, 'admin_panel.html')

def authority(request):
    return render(request, 'authority_panel.html')

def AddCanditate(request):
    
    context= {
        'canditateform' : CanditateForm()
    }
    
    if request.method == 'POST':
        
        canditateform = CanditateForm(request.POST, request.FILES)
        
        if canditateform.is_valid():
            canditateform.save() 
            messages.success(request, "Canditate Add Successfully")
            
    return render(request, 'add_canditate.html', context)

def AllCanditate(request):
    
    context = {
        "all_canditate" : Candidate.objects.all()
    }
    
    return render(request, 'canditate.html', context)

def DeleteCanditate(request, id):
    
    selected = Candidate.objects.get(id = id)
    
    selected.delete()
    
    return redirect('/adminpanle/canditate/') 

def UpdateCanditatesss(request, id):
    
    selected_p = Candidate.objects.get(id = id)
    
    context = {
        "candidate_form" : CanditateForm(instance=selected_p)
    }
    
    if request.method == 'POST':
                                                        #selected_p
        candidate_form = CanditateForm(request.POST, request.FILES)
        
        if candidate_form.is_valid():
            candidate_form.save()
            return redirect('/adminpanle/canditate/') 
        
    
    
    return render(request, 'add_canditate.html', context)

def UpdateCanditate(request, id):
    selected_p = Candidate.objects.get(id=id)
    
    if request.method == 'POST':
        candidate_form = CanditateForm(request.POST, request.FILES, instance=selected_p)
        if candidate_form.is_valid():
            candidate_form.save()
            return redirect('/adminpanle/canditate/') 
    else:
        candidate_form = CanditateForm(instance=selected_p)
    
    context = {
        "canditateform": candidate_form
    }
    return render(request, 'add_canditate.html', context)

def Dasboard(request):
    
    return render(request, 'dashboard.html')

def Result(request):
    
    return render(request, 'result.html')

def Logouts(request):
    return render(request, 'login.html')



import cv2
import face_recognition
import numpy as np
import pickle
from django.shortcuts import render, redirect
from django.contrib import messages

def add_voter(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        election_id = request.POST.get('election_id')

        # Save form values temporarily in session
        request.session['temp_name'] = name
        request.session['temp_election_id'] = election_id

        if 'capture' in request.POST:
            video = cv2.VideoCapture(0)
            ret, frame = video.read()
            video.release()
            cv2.destroyAllWindows()

            if not ret:
                messages.error(request, "Failed to capture face.")
                return redirect('add_voter')

            face_encodings = face_recognition.face_encodings(frame)
            if face_encodings:
                request.session['temp_face_encoding'] = face_encodings[0].tolist()
                messages.success(request, "Face captured successfully!")
            else:
                messages.error(request, "No face detected.")
            return redirect('add_voter')  # Refresh to show form again

        if 'save' in request.POST:
            encoding = request.session.get('temp_face_encoding')
            name = request.session.get('temp_name')
            election_id = request.session.get('temp_election_id')

            if encoding is None or name is None or election_id is None:
                messages.error(request, "Please complete all fields and capture face before saving.")
                return redirect('add_voter')

            voter = Voter(name=name, election_id=election_id, face_encoding=str(encoding))
            voter.save()

            # Clean up session
            for key in ['temp_face_encoding', 'temp_name', 'temp_election_id']:
                if key in request.session:
                    del request.session[key]

            messages.success(request, "Voter saved successfully!")
            return redirect('adminpanle')

    # If GET or after redirect, pre-fill form values
    context = {
        'name': request.session.get('temp_name', ''),
        'election_id': request.session.get('temp_election_id', '')
    }
    return render(request, 'add_voter.html', context)


import cv2
import face_recognition
import time

def capture_preview_frame():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Cannot open camera")

    start_time = time.time()
    captured_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect face locations
        face_locations = face_recognition.face_locations(frame)

        # Draw green rectangles around each detected face
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow("Live Camera Preview - Face Detection", frame)
        captured_frame = frame

        # Auto capture after 3 seconds
        if time.time() - start_time > 3:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if captured_frame is not None:
        return captured_frame
    else:
        raise Exception("Failed to capture frame")


@login_required
def verify_voter(request):
    if request.method == 'POST':
        entered_election_id = request.POST.get('election_id')

        # Live camera preview and auto-capture
        try:
            frame = capture_preview_frame()
        except Exception as e:
            messages.error(request, f"Camera error: {e}")
            return redirect('verify_voter')

        # Detect face in captured frame
        unknown_encodings = face_recognition.face_encodings(frame)
        if len(unknown_encodings) != 1:
            messages.error(request, "Please ensure only one face is visible to the camera.")
            return redirect('verify_voter')

        unknown_encoding = unknown_encodings[0]

        # Step 1: Match face with all voters
        matched_voter = None
        for voter in Voter.objects.all():
            try:
                known_encoding = np.array(eval(voter.face_encoding))
                match = face_recognition.compare_faces([known_encoding], unknown_encoding)[0]
                if match:
                    matched_voter = voter
                    break
            except Exception as e:
                continue  # Skip broken encodings

        if not matched_voter:
            messages.error(request, "Face not recognized. Please try again or contact admin.")
            return redirect('verify_voter')

        # Step 2: Check if election ID matches the matched voter's ID
        if matched_voter.election_id != entered_election_id:
            messages.error(request, "Election ID does not match the recognized face.")
            return redirect('verify_voter')

        # Step 3: Check if already voted
        if matched_voter.has_voted:
            messages.warning(request, "You have already voted.")
            return redirect('verify_voter')

        # Verified voter
        request.session['verified_voter_id'] = matched_voter.id
        return redirect('vote', voter_id=matched_voter.id)

    return render(request, 'verify_voters.html')



def cast_vote(request):
    return render(request, 'cast_vote.html', {"candidates" : Candidate.objects.all()})




# views.py



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect after successful registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


from django.shortcuts import redirect
from django.utils import timezone
# from voters.models import Voter  # adjust to your app name
from .models import Election
# from votes.models import Vote  # adjust to your app name

def reset_election(request):
    # Mark all voters as not voted
    Voter.objects.all().update(has_voted=False)
    
     # Reset candidate votes
    Candidate.objects.all().update(votes=0)

    # End the active election if any
    active_election = Election.objects.filter(is_active=True).last()
    if active_election:
        active_election.is_active = False
        active_election.ended_at = timezone.now()
        active_election.save()

    # Optionally clear previous votes Vote.objects.all().delete()

    # (Optional) Start a new election entry
    Election.objects.create(
        title="New Election - " + timezone.now().strftime("%Y-%m-%d %H:%M"),
        is_active=False
    )

    return redirect('admin_dashboard')  # Update this to your admin dashboard URL





from django.shortcuts import render, redirect
from .models import Election, Voter, Candidate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Election, Voter, Candidate

@login_required
def election_control(request):
    # Ensure only Admins can access this page
    # if not request.user.role == 'Admin':
    #     return redirect('home')

    # Get the latest (most recent) election
    election = ElectionMention.objects.last()

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if not election:
            messages.error(request, "❌ No election created. Please create an election first.")
            return redirect('election_control')

        if action == "start":
            election.is_active = True
            election.start_time = timezone.now()
            messages.success(request, "✅ Election Started Successfully.")

        elif action == "stop":
            election.is_active = False
            election.end_time = timezone.now()
            messages.success(request, "🛑 Election Stopped.")

        elif action == "reset":
            # Reset voting status and candidate vote count
            Voter.objects.all().update(has_voted=False)
            Candidate.objects.all().update(votes=0)
            election.is_active = False
            election.start_time = None
            election.end_time = None
            messages.success(request, "♻️ Election Reset Complete.")

        election.save()
        return redirect('election_control')

    return render(request, 'election_control.html', {'election': election})


## election create all function ***

from django.shortcuts import render, redirect, get_object_or_404
from .models import Election
from .forms import ElectionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# @login_required
def create_election(request):
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Election created successfully.")
            return redirect('all_elections')
    else:
        form = ElectionForm()
    return render(request, 'create_election.html', {'form': form})


# @login_required
def edit_election(request, pk):
    election = get_object_or_404(ElectionMention, pk=pk)
    if request.method == 'POST':
        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            form.save()
            messages.success(request, "Election updated successfully.")
            return redirect('all_elections')
    else:
        form = ElectionForm(instance=election)
    return render(request, 'create_election.html', {'form': form})


# @login_required
def delete_election(request, pk):
    election = get_object_or_404(ElectionMention, pk=pk)
    election.delete()
    messages.success(request, "Election deleted successfully.")
    return redirect('all_elections')


# @login_required
def all_elections(request):
    elections = ElectionMention.objects.all().order_by('-start_time')
    return render(request, 'election_list.html', {'elections': elections})



#### authority panel 


def ElectionGoingOrNot(request):
    election = ElectionMention.objects.last()
    if not election or not election.is_active:
        messages.error(request, "No active election.")
        return redirect('authprity')
    return render(request, 'verify_voters.html', {'election': election})


# thank page
def voted_thanks(request):
    # Render thank you page and auto-redirect
    return render(request, 'voted_thanks.html')

# show election candidate

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def vote(request, voter_id):
    voter = get_object_or_404(Voter, id=voter_id)

    if voter.has_voted:
        messages.error(request, "❌ This voter has already voted.")
        return redirect('verify_voter')

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')

        if not candidate_id:
            messages.error(request, "⚠️ No candidate selected.")
            return redirect(request.path)

        candidate = get_object_or_404(Candidate, id=candidate_id)

        # Cast the vote
        candidate.votes += 1
        candidate.save()

        voter.has_voted = True
        voter.save()

        messages.success(request, f"✅ You have successfully voted ")#for {candidate.name}.
        return HttpResponseRedirect(reverse('voted_thanks'))

    candidates = Candidate.objects.all()
    return render(request, 'cast_vote.html', {'candidates': candidates, 'voter': voter})


## live result and download

from django.shortcuts import render
from django.http import HttpResponse
import openpyxl
from .models import Candidate

def live_results(request):
    candidates = Candidate.objects.all().order_by('-votes')
    return render(request, 'live_results.html', {'candidates': candidates})

def download_results_excel(request):
    candidates = Candidate.objects.all().order_by('-votes')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Election Results"

    ws.append(["Rank", "Candidate Name", "Votes"])
    for idx, candidate in enumerate(candidates, start=1):
        ws.append([idx, candidate.name, candidate.votes])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Election_Results.xlsx'
    wb.save(response)
    return response


from django.shortcuts import render
from .models import ElectionMention, Voter, Candidate

def live_dashboard(request):
    # Assuming only one election for simplicity
    election = ElectionMention.objects.first()
    active_election = election.is_active if election else False

    total_voters = Voter.objects.count()
    voted_voters = Voter.objects.filter(has_voted=True).count()

    candidates = Candidate.objects.all()

    # Calculate total votes for percentage calculation
    total_votes = sum(c.votes for c in candidates)

    context = {
        'active_election': active_election,
        'total_voters': total_voters,
        'voted_voters': voted_voters,
        'candidates': candidates,
        'total_votes': total_votes,
    }
    return render(request, 'live_dashboard.html', context)
