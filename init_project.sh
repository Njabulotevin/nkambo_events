mkdir app
cd app
touch __init__.py config.py
mkdir models views authentication templates static
cd models
touch __init__.py content.py events.py forms.py
cd ../views
touch __init__.py content_views.py events_views.py forms_views.py
cd ../authentication
touch __init__.py auth_views.py
cd ..
touch run.py
cd ../..
mkdir migrations tests instance
touch requirements.txt
