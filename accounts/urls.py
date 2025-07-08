from django.urls import path
from .views import *

urlpatterns = [
    path('', Login, name='login'),
    path('adminpanle/', adminpanel, name='adminpanle'),
    path('authoritypanle/', authority, name='authority'), 
    path('adminpanle/addcanditate/', AddCanditate),
    path('adminpanle/canditate/', AllCanditate, ),
    path('adminpanle/canditate/delete/<int:id>', DeleteCanditate, name='canditate_delete'),
    path('adminpanle/canditate/update/<int:id>/', UpdateCanditate, name='canditate_update'),
    path('authoritypanle/verify', verify_voter, name='verify_voter'),
    path('', Logouts, name='logout'),
    path('adminpanle/addvoter/', add_voter, name='add_voter'),
    path('authoritypanle/verifed/election_poll/<int:voter_id>/', vote, name='vote'),
    #path('verifed/election_poll/<int:voter_id>/', vote, name='vote'),

    path('register/', register, name='register'),
    path('adminpanle/dasboard', Dasboard, name='dashboard'),
    path('adminpanle/live-dashboard/', live_dashboard, name='live_dashboard'),

    path('adminpanle/result', Result, name='result'), 
    
    path('adminpanle/create-election/', create_election, name='create_election'),
    path('adminpanle/elections/', all_elections, name='election_list'),
    path('adminpanle/electioncontrol/', election_control, name='election_control'),
    path('election/edit/<int:pk>/', edit_election, name='edit_election'),
    path('election/delete/<int:pk>/', delete_election, name='delete_election'),
    #path('adminpanle/elections/<int:id>/', edit_election, name='edit_election'),
    
    path('authoritypanle/verify', ElectionGoingOrNot, name='electioncheck'),
    
    path('voted-thanks/', voted_thanks, name='voted_thanks'),
    
    path('adminpanle/results/live/', live_results, name='live_results'),
    path('adminpanle/results/download/', download_results_excel, name='download_results'),


]
