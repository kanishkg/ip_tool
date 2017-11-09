
## Welcome

This is an image processing toolbox that gives the functionality of selective blurring and object removal. It has a web-based GUI and can easily be used by following the instructions below. It incorporates:
1. Selective Search based object selection
2. Grab Cut based object selection
3. Motion Blur
4. Exemplar Based image inpainting
5. TELEA image Inpaintaing

<hr>


<hr>





Project Structure
--------

  ```sh
  ├── Procfile
  ├── Procfile.dev
  ├── README.md
  ├── app.py
  ├── config.py
  ├── error.log
  ├── forms.py
  ├── models.py
  ├── requirements.txt
  ├── ip_scripts
  │   ├── __init__.py
  │   ├── blobs.py
  │   ├── color_utils.py
  │   ├── hist.py
  │   ├── inpaint.py
  │   ├── inpainter.py
  │   ├── segment_image.py
  │   ├── selective_blur.py
  │   ├── ssearch.py
  │   ├── sim_features.py
  ├── static
  │   ├── css
  │   │   ├── bootstrap-3.0.0.min.css
  │   │   ├── bootstrap-theme-3.0.0.css
  │   │   ├── bootstrap-theme-3.0.0.min.css
  │   │   ├── font-awesome-3.2.1.min.css
  │   │   ├── layout.forms.css
  │   │   ├── layout.main.css
  │   │   ├── main.css
  │   │   ├── main.quickfix.css
  │   │   └── main.responsive.css
  │   ├── font
  │   │   ├── FontAwesome.otf
  │   │   ├── fontawesome-webfont.eot
  │   │   ├── fontawesome-webfont.svg
  │   │   ├── fontawesome-webfont.ttf
  │   │   └── fontawesome-webfont.woff
  │   ├── ico
  │   │   ├── apple-touch-icon-114-precomposed.png
  │   │   ├── apple-touch-icon-144-precomposed.png
  │   │   ├── apple-touch-icon-57-precomposed.png
  │   │   ├── apple-touch-icon-72-precomposed.png
  │   │   └── favicon.png
  │   ├── img
  │   └── js
  │       ├── libs
  │       │   ├── bootstrap-3.0.0.min.js
  │       │   ├── jquery-1.10.2.min.js
  │       │   ├── modernizr-2.6.2.min.js
  │       │   └── respond-1.3.0.min.js
  │       ├── plugins.js
  │       └── script.js
  └── templates
      ├── errors
      │   ├── 404.html
      │   └── 500.html
      ├── forms
      │   ├── home.html
      ├── layouts
      │   └── main.html
      └── pages
          ├── placeholder.about.html
          └── placeholder.home.html
  ```

### Algorithmic Details
Refer to the report for details an the various algorithms implemented
### Quick Start

1. Clone the repo
  ```
  $ git clone https://github.com/kanishkg/ip_tool.git
  $ cd ip_tool
  ```

2. Initialize and activate a virtualenv:
  ```
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

5. Run the development server:
  ```
  $ python app.py
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)


Deploying to Heroku
------

1. Signup for [Heroku](https://api.heroku.com/signup)
2. Login to Heroku and download the [Heroku Toolbelt](https://toolbelt.heroku.com/)
3. Once installed, open your command-line and run the following command - `heroku login`. Then follow the prompts:

  ```
  Enter your Heroku credentials.
  Email: michael@mherman.org
  Password (typing will be hidden):
  Could not find an existing public key.
  Would you like to generate one? [Yn]
  Generating new SSH public key.
  Uploading ssh public key /Users/michaelherman/.ssh/id_rsa.pub
  ```

4. Activate your virtualenv
5. Heroku recognizes the dependencies needed through a *requirements.txt* file. Create one using the following command: `pip freeze > requirements.txt`. Now, this will only create the dependencies from the libraries you installed using pip. If you used easy_install, you will need to add them directly to the file.
6. Create a Procfile. Open up a text editor and save the following text in it:

  ```
  web: gunicorn app:app --log-file=-
  ```

   Then save the file in your applications root or main directory as *Procfile* (no extension). The word "web" indicates to Heroku that the application will be attached to the HTTP routing stack once deployed.

7. Create a local Git repository (if necessary):

  ```
  $ git init
  $ git add .
  $ git commit -m "initial files"
  ```

8. Create your app on Heroku:

  ```
  $ heroku create <name_it_if_you_want>
  ```

9. Deploy your code to Heroku:

  ```
  $ git push heroku master
  ```

10. View the app in your browser:

  ```
  $ heroku open
  ```



11. Having problems? Look at the Heroku error log:

  ```
  $ heroku logs
  ```

### Deploying to PythonAnywhere

1. Install [Git](http://git-scm.com/downloads) and [Python](http://install.python-guide.org/) - if you don't already have them, of course.

  > If you plan on working exclusively within PythonAnywhere, which you can, because it provides a cloud solution for hosting and developing your application, you can skip step one entirely. :)

2. Sign up for [PythonAnywhere](https://www.pythonanywhere.com/pricing/), if you haven't already
3. Once logged in, you should be on the Consoles tab.
4. Clone this repo:
  ```
  $ git clone git://github.com/kanishkg/ip_tool.git
  $ cd ip_tool
  ```

5. Create and activate a virtualenv:
  ```
  $ virtualenv venv --no-site-packages
  $ source venv/bin/activate
  ```

6. Install requirements:
  ```
  $ pip install -r requirements.txt
  ```

7. Next, back on PythonAnywhere, click Web tab.
8. Click the "Add a new web app" link on the left; by default this will create an app at your-username.pythonanywhere.com, though if you've signed up for a paid "Web Developer" account you can also specify your own domain name here. Once you've decided on the location of the app, click the "Next" button.
9. On the next page, click the "Flask" option, and on the next page just keep the default settings and click "Next" again.
Once the web app has been created (it'll take 20 seconds or so), you'll see a link near the top of the page, under the "Reload web app" button, saying "It is configured via a WSGI file stored at..." and a filename.  Click this, and you get to a page with a text editor.
10. Put the following lines of code at the start of the WSGI file (changing "your-username" appropriately)

  ```
  activate_this = '/home/your-username/ip_tool/venv/bin/activate_this.py'
  execfile(activate_this, dict(__file__=activate_this))
  ```

11. Then update the following lines of code:

  from

  ```
  project_home = u'/home/your-username/mysite'
  ```

  to

  ```
  project_home = u'/home/your-username/ip_tool'
  ```

  from

  ```
  from flask_app import app as application
  ```

  to

  ```
  from app import app as application
  ```

12. Save the file.
13. Go to the website http://your-username.pythonanywhere.com/ (or your own domain if you specified a different one earlier), and you should see something like this - [http://www.flaskboilerplate.com/](http://www.flaskboilerplate.com/).

*Now you're ready to start developing!*

***Need to PUSH your PythonAnywhere repo to Github?***

1. Start a bash console
2. Run:

  ```
  $ ssh-keygen -t rsa
  ```

3. Just accept the defaults, then show the public key:

  ```
  $ cat ~/.ssh/id_rsa.pub
  ```

4. Log in to GitHub.
5. Go to the "Account settings" option at the top right (currently a wrench and a screwdriver crossed)
6. Select "SSH Keys" from the list at the left.
7. Click the "Add SSH key" button at top right.
8. Enter a title (I suggest something like "From PythonAnywhere" and then paste the output of the previous "cat" command into the Key box.
9. Click the green "Add key" button.  You'll be prompted to enter your password.

PUSH and PULL away!



