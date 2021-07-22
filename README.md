# news_site
news blog

We used:
Ubuntu 20.04.2 LTS
PyCharm 2021.1.3 (Community Edition)
Python 3.8.10
Django 3.2.4 

Packages installed in a virtual environment (venv):
$ pip list
Package                Version
---------------------- -------
asgiref                3.3.4  
Django                 3.2.4  
django-ckeditor        6.1.0  
django-crum            0.7.9  
django-debug-toolbar   3.2.1  
django-js-asset        1.2.2  
django-ranged-response 0.2.0  
django-simple-captcha  0.5.14 
Pillow                 8.2.0  
pip                    20.0.2 
pkg-resources          0.0.0  
pytz                   2021.1 
setuptools             44.0.0 
six                    1.16.0 
sqlparse               0.4.1

Star project:
$ git clone https://github.com/KunisovIvan/news_site.git  #clone project
$ cd news_site                                            #change of directory to news_site 
$ source venv/bin/activate                                #activate virtual environment (venv) with packages 
$ cd news_site                                            #change of directory to news_site
$ python3 manage.py runserver                             #start server
