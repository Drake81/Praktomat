# This module collects all defaults settings for the praktomat
# It exports one function, load_defaults, which will set the settings in the
# parameter, but only if it is not already defined.

# The following variables have _no_ sane default, and need to be set!
no_defaults = [ "SITE_NAME", "PRAKTOMAT_ID", "BASE_HOST", "BASE_PATH", "UPLOAD_ROOT", "PRIVATE_KEY"]

import os
from os.path import dirname, join

def load_defaults(settings):
    missing = [ v for v in no_defaults if v not in settings]
    if missing:
        raise RuntimeError("Variables without defaults not set: %s" % ", ".join(missing))

    # import settings so that we can conveniently use the settings here
    for k,v in settings.iteritems():
        if not callable(v) and not k.startswith('__'):
            globals()[k] = v

    class D:
        def __setattr__(self,k,v):
            if k not in globals():
                settings[k] = v
                globals()[k] = v
    d = D()

    # Absolute path to the praktomat source
    d.PRAKTOMAT_ROOT = dirname(dirname(dirname(__file__)))

    #############################################################################
    # Django Settings                                                           #
    #############################################################################

    # General setup

    # This will show debug information in the browser if an exception occurs.
    # Note that there are always going to be sections of your debug output that 
    # are inappropriate for public consumption. File paths, configuration options, 
    # and the like all give attackers extra information about your server.
    # Never deploy a site into production with DEBUG turned on.
    d.DEBUG = True

    # Local time zone for this installation. Choices can be found here:
    # http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
    # although not all choices may be available on all operating systems.
    # If running in a Windows environment this must be set to the same as your
    # system time zone.
    d.TIME_ZONE = 'Europe/Berlin'

    # Language code for this installation. All choices can be found here:
    # http://www.i18nguy.com/unicode/language-identifiers.html
    d.LANGUAGE_CODE = 'en-us'

    # A tuple that lists people who get code error notifications. When
    # DEBUG=False and a view raises an exception, Django will email these
    # people with the full exception information. Each member of the tuple
    # should be a tuple of (Full name, email address). 
    d.ADMINS = []

    # A tuple in the same format as ADMINS that specifies who should get broken
    # link notifications when BrokenLinkEmailsMiddleware is enabled.
    d.MANAGERS = ADMINS

    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    d.USE_I18N = True

    # Apps and plugins

    d.INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'django.contrib.markup',
        'django.contrib.staticfiles',

        # ./manage.py runserver_plus allows for debugging on werkzeug traceback page. invoke error with assert false
        # not needed for production
        'django_extensions',

        # intelligent schema and data migrations
        'south', 

        # contains a widget to render a form field as a TinyMCE editor
        'tinymce',

        'configuration',
        'accounts',
        'tasks',
        'solutions',
        'attestation',
        'checker',
        'utilities',
                      
        'sessionprofile', #phpBB integration
    )

    d.MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'sessionprofile.middleware.SessionProfileMiddleware', #phpBB integration
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'accounts.middleware.AuthenticationMiddleware',	
        'accounts.middleware.LogoutInactiveUserMiddleware',
        'django.middleware.transaction.TransactionMiddleware',
    )

    d.DEFAULT_FILE_STORAGE = 'utilities.storage.UploadStorage'

    # URL and file paths
    
    d.TEMPLATE_DIRS = (
        join(PRAKTOMAT_ROOT, "src", "templates") 
    )

    d.STATICFILES_DIRS = (
        join(PRAKTOMAT_ROOT, "media"),
    )

    d.ROOT_URLCONF = 'urls'

    d.LOGIN_REDIRECT_URL = BASE_PATH + '/tasks/'

    # URL to use when referring to static files located in STATIC_ROOT.
    # Example: "/static/" or "http://static.example.com/"
    # If not None, this will be used as the base path for asset definitions
    # (the Media class) and the staticfiles app.
    # It must end in a slash if set to a non-empty value.
    d.STATIC_URL = BASE_PATH + 'static/'

	# The URL prefix for admin media - CSS, JavaScript and images used by the
    # Django administrative interface. Make sure to use a trailing slash, and to
    # have this be different from the MEDIA_URL setting (since the same URL cannot
    # be mapped onto two different sets of files). For integration with
    # staticfiles, this should be the same as STATIC_URL followed by 'admin/'.
    d.ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

    # Security

    d.SESSION_COOKIE_PATH = BASE_PATH

    d.CSRF_COOKIE_NAME = 'csrftoken_' + PRAKTOMAT_ID

    # Make this unique, and don't share it with anybody.
    if 'SECRET_KEY' not in globals():
        secret_keyfile = join(UPLOAD_ROOT, 'SECRET_KEY')
        if os.path.exists(secret_keyfile):
            d.SECRET_KEY = open(secret_keyfile).read()
            if not SECRET_KEY:
                raise RuntimeError("File %s empty!" % secret_keyfile)
        else:
            import uuid
            d.SECRET_KEY = uuid.uuid4().hex
            os.fdopen(os.open(secret_keyfile,os.O_WRONLY | os.O_CREAT,0600),'w').write(SECRET_KEY)

    # Templates

    # A boolean that turns on/off template debug mode. If this is True, the fancy 
    # error page will display a detailed report for any TemplateSyntaxError. 
    # Note that Django only displays fancy error pages if DEBUG is True.
    d.TEMPLATE_DEBUG = True

    # List of callables that know how to import templates from various sources.
    d.TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.load_template_source',
        'django.template.loaders.app_directories.load_template_source',
    )

    d.TEMPLATE_CONTEXT_PROCESSORS = (
        'context_processors.settings.from_settings',
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.request',
        'django.core.context_processors.static',
        'django.contrib.messages.context_processors.messages',
    )


    # Database

    d.DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    d.DATABASE_NAME = UPLOAD_ROOT+'/Database'   # Or path to database file if using sqlite3.
    d.DATABASE_USER = ''             # Not used with sqlite3.
    d.DATABASE_PASSWORD = ''         # Not used with sqlite3.
    d.DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
    d.DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


    # Email
    
    # Default email address to use for various automated correspondence from
    # the site manager(s).
    d.DEFAULT_FROM_EMAIL = ""
    d.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    d.EMAIL_HOST = "smtp.googlemail.com"
    d.EMAIL_PORT = 587
    d.EMAIL_HOST_USER = ""
    d.EMAIL_HOST_PASSWORD = ""
    d.EMAIL_USE_TLS = False

    # TinyMCE

    d.TINYMCE_JS_URL = STATIC_URL + 'frameworks/tiny_mce/tiny_mce_src.js'
    d.TINYMCE_DEFAULT_CONFIG = {
      'plugins': 'safari,pagebreak,table,advhr,advimage,advlink,emotions,iespell,inlinepopups,media,searchreplace,print,contextmenu,paste,fullscreen,noneditable,visualchars,nonbreaking,syntaxhl',

      'theme': "advanced",
      'theme_advanced_buttons1' : "formatselect,|,bold,italic,underline,strikethrough,|,forecolor,|,bullist,numlist,|,sub,sup,|,outdent,indent,blockquote,syntaxhl,|,visualchars,nonbreaking,|,link,unlink,anchor,image,cleanup,help,code,|,print,|,fullscreen",
        'theme_advanced_buttons2' : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,tablecontrols,|,hr,removeformat,visualaid,|,charmap,emotions,iespell,media,advhr",				   
        'theme_advanced_buttons3' : "",
        'theme_advanced_buttons4' : "",
        'theme_advanced_toolbar_location' : "top",
        'theme_advanced_toolbar_align' : "left",
        'theme_advanced_statusbar_location' : "bottom",
        'theme_advanced_resizing' : True,
        'extended_valid_elements' : "textarea[cols|rows|disabled|name|readonly|class]" ,
        
        'content_css' : STATIC_URL + '/styles/style.css',
      'relative_urls': False,
    }
    d.TINYMCE_SPELLCHECKER = False
    d.TINYMCE_COMPRESSOR = False

    #############################################################################
    # Praktomat-specific settings                                               #
    #############################################################################

    # Private key used to sign uploded solution files in submission confirmation email
    #d.PRIVATE_KEY = '/home/praktomat/certificates/privkey.pem'

	# Is this a mirror of another instance (different styling)
    d.MIRROR = False

    # The Compiler binarys used to compile a submitted solution
    d.C_BINARY = 'gcc'
    d.CXX_BINARY = 'c++'
    d.JAVA_BINARY = 'javac'
    d.JAVA_BINARY_SECURE = PRAKTOMAT_ROOT + '/src/checker/scripts/javac'
    d.JAVA_GCC_BINARY = 'gcj'
    d.JVM = 'java'
    d.JVM_SECURE = PRAKTOMAT_ROOT + '/src/checker/scripts/java'
    d.FORTRAN_BINARY = 'g77'
    d.ISABELLE_BINARY = '/data1/praktomat/Isabelle2013/bin/isabelle'
    d.DEJAGNU_RUNTEST = '/usr/bin/runtest'
    d.CHECKSTYLEALLJAR = '/home/praktomat/contrib/checkstyle-all-4.4.jar'
    d.JUNIT38='junit'
    d.JAVA_LIBS = { 'junit3' : '/usr/share/java/junit.jar', 'junit4' : '/usr/share/java/junit4.jar' }
    d.JCFDUMP='jcf-dump'
    d.JCLASSINFO='jclassinfo'
    d.GHC='ghc'

    # Enable to run all scripts (checker) as the unix user 'tester'. Therefore
    # put 'tester' as well as the Apache user '_www' (and your development user
    # account) into a new group called praktomat. Also edit your sudoers file
    # with "sudo visudo". Add the following lines to the end of the file to
    # allow the execution of commands with the user 'tester' without requiring
    # a password:
    # "_www    		ALL=(tester)NOPASSWD:ALL"
    # "developer	ALL=(tester)NOPASSWD:ALL"
    d.USEPRAKTOMATTESTER = False

    # This enables Shibboleth-Support.
    # In order to actually get it working, you need to protec the location
    # .../accounts/shib_login in the apache configuration, e.g. with this
    # stanca:
    #	<Location /shibtest/accounts/shib_login>
    #		Order deny,allow
    #		AuthType shibboleth
    #		ShibRequireSession On
    #		Require valid-user
    #	</Location>
    #
    # You probably want to disable REGISTRATION_POSSIBLE if you enable
    # Shibboleth support
    d.SHIB_ENABLED = False

    d.SHIB_ATTRIBUTE_MAP = {
        "mail": (True, "email"),
        "givenName": (True, "first_name"),
        "sn": (True, "last_name"),
        "matriculationNumber": (False, "matriculationNumber"),
        "fieldOfStudyText" : (False, "programme"),
    }

    d.SHIB_USERNAME = "email"
    d.SHIB_PROVIDER = "kit.edu"

    # Set this to False to disable registration via the website, e.g. when
    # Single Sign On is used
    d.REGISTRATION_POSSIBLE = True

    # Length of timeout applied whenever an external check that runs a students
    # submission is executed,
    # for example: JUnitChecker, DejaGnuChecker
    d.TEST_TIMEOUT=60

    # Maximal size (in kbyte) of files created whenever an external check that
    # runs a students submission is executed,
    # for example: JUnitChecker, DejaGnuChecker
    d.TEST_MAXFILESIZE=64

    # Maximal size (in kbyte) of checker logs accepted. This setting is
    # respected currently only by:
    # JUnitChecker, ScriptChecker, 
    d.TEST_MAXLOGSIZE=64

    d.NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 1

    d.MIMETYPE_ADDITIONAL_EXTENSIONS = [("text/plain",".properties")]

    # Subclassed TestSuitRunner to prepopulate unit test database.
    d.TEST_RUNNER = 'utilities.TestSuite.TestSuiteRunner'

    # This is actually a django setting, but depends on a praktomat setting:
    if SHIB_ENABLED:
        d.LOGIN_URL = BASE_PATH + 'accounts/shib_hello/'
    else:
		d.LOGIN_URL = BASE_PATH + 'accounts/login/'


