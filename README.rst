.. ***************************************************************************
.. Copyright (c) 2013 SAP AG or an SAP affiliate company. All rights reserved.
.. ***************************************************************************

SQL Anywhere Django Driver
==========================
This is a SQL Anywhere database backend for Django. The backend is
distributed as a stand-alone python module. This backend has been
tested with SQL Anywhere 12 and Django versions 1.1, 1.2.7, 1.3.3, and 1.4.1.

This driver is licensed under the terms of the BSD license. See the
file name "LICENSE" included with this package for more information.

#. Install the required software

    (a) SQL Anywhere 12.0.1

       The SQL Anywhere Web Edition is a free, full-featured version for
       development and deployment of browser based applications. If you don't
       already have a license for SQL Anywhere, the Web Edition is a great
       place to start. Get the Web Edition at
       http://www.sybase.com/detail?id=1057560
    
    (b) Python (2.4 or greater)

       Install Python if you don't already have it installed. We recommend
       Python 2.7 but any version greater than 2.4 is supported. Note however
       that Python 3 introduced backwards incompatible features and many
       projects including Django do not currently have support for Python 3.
       You can download python from http://www.python.org/download/
    
       If you are running on Linux you will most likely also be able to find
       python through your distribution's package management system.
    
    (c) Python setuptools
   
       The setuptools project for python acts as a package manager for Python
       code. Using setuptools will make it trivial to install the correct
       version of Django to use with SQL Anywhere. You can get setuptools for
       python from http://pypi.python.org/pypi/setuptools/
    
       Again, if you are running on Linux you most likely be able to find
       setuptools through your distribution's package management
       system. This package is called "python-setuptools" on Ubuntu and
       "python-setuptools-devel" on Fedora.
    
    (d) Django 1.4
    
       Once you have installed setuptools, installing Django is a snap, simply run::
    
           $ easy_install Django--1.4
    
    (e) Python SQL Anywhere Database Interface
    
       If you are using pip to install the SQL Anywhere Django driver, you can
       skip this step since the SQL Anywhere Python driver will be installed
       as part of that step.

       The SQL Anywhere Database Interface for Python provides a Database API v2
       compliant driver (see Python PEP 249) for accessing SQL Anywhere
       databases from Python. The SQL Anywhere backend for Django is built on
       top of this interface so installing it is required.
    
       You can use pip to make this easy::

           pip install sqlanydb

       Alternatively, you can obtain the Python SQL Anywhere Database Interface 
       from http://code.google.com/p/sqlanydb/. Install the driver by downloading
       the source and running the following command::
    
           $ python setup.py install

    (f) SQL Anywhere Django Backend
    
        Again, use pip to install this easily::

           pip install sqlany-django

	This will install the SQL Anywhere python driver if it was not already
	installed.

        Or you can obtain the SQL Anywhere Database backend for Django from
        http://code.google.com/p/sqlany-django/. Install the backend by downloading
        the source and running the following command::
    
           $ python setup.py install

#. Setup your environment

    (Linux/Unix/Mac OS X only)
    
    SQL Anywhere requires several environment variables to be set to run
    correctly -- the most important of which are PATH and
    LD_LIBRARY_PATH. The SQL Anywhere install creates a file named
    sa_config.sh to set all necessary environment variables automatically
    (Note the file is named sa_config.csh if you are using a csh
    derivative as your shell).
    
    This file is located in the "bin32" and/or the "bin64" directories of
    your install. Before trying to run the SQL Anywhere server or connect
    to a running server in a given shell you should make sure to source
    the file (with the "." command) corresponding to the bitness of the
    SQL Anywhere binaries you want to use. For example, if the product is
    installed in /opt/sqlanywhere12 you should run::
    
        $ . /opt/sqlanywhere12/bin32/sa_config.sh

#. Create a database

    Issue the following command to create a new database to use with
    Django. Note that we are specifying the UCA collation so that that CHAR
    columns in the database will support unicode strings. ::
    
       $ dbinit -z UCA django.db
    
    If all goes well SQL Anywhere will have created a new database file
    named 'django.db' in the directory where you ran the dbinit
    command. Feel free to move this database file to any location you
    want. You can even copy it to a machine running a different operating
    system if you wish.

#. Start the Database Server

    SQL Anywhere includes two different database servers -- The personal
    server (dbeng12) and the network server (dbsrv12). Both servers
    servers support the same complete set of features except that the
    personal server is limited to running on one CPU, allows a maximum of
    10 concurrent connections and does not accept network connections from
    other machines. We will use the network server for our example. ::
    
       $ dbsrv12 django.db
    
#. Configure Django

    Creating a new Django site and configuring it to use SQL Anywhere is
    very easy. First create the site in the normal fashion::
    
        $ django-admin.py startproject mysite
    
    Then edit the file mysite/mysite/settings.py and change the DATABASES
    setting to match what is given below::
    
        DATABASES = {
	  'default' : {
 	      'ENGINE': 'sqlany_django',
	      'NAME': 'django',
	      'USER': 'dba',
	      'PASSWORD': 'sql',
	      'HOST': 'myhost',
	      'PORT': 'portnum'
	  }
        }

    Here's how the parameters correspond to SQL Anywhere connection parameters:
    
       * NAME = DBN
       * USER = USR
       * PASSWORD = PWD
       * HOST = HOST
       * PORT = (port number in host, i.e. myhost:portnum)
    
    If you need to specify other connection parameters (eg. ENG, which is required
    for client versions prior to v12.0.0), you can set a value with the key
    "OPTIONS", like this::
    
       DATABASES = {
	  'default' : {
 	      'ENGINE': 'sqlany_django',
	      'NAME': 'django',
	      'USER': 'dba',
	      'PASSWORD': 'sql',
	      'OPTIONS': {'eng': 'django'}
	  }
       }
    
    Note: SQL Anywhere allows you to run several database servers on one
    machine. For this reason you should always specify the server you want
    to connect to as well as the database name. However if you want to connect to
    a server running in a SA OnDemand (cloud) environment, you should specify the
    NAME and HOST (and optionally PORT) options, and *not* specify the server name.
    
#. Test to make sure everything is working
    
    The SQL Anywhere database backend for Django makes use of the Python
    SQL Anywhere Database interface. We first want to test that this
    interface is working correctly before testing Django connectivity
    itself. Create a file named test_sqlany.py with the following
    contents::
    
       import sqlanydb
       conn = sqlanydb.connect(uid='dba', pwd='sql', eng='django', dbn='django')
       curs = conn.cursor()
       curs.execute("select 'Hello, world!'")
       print "SQL Anywhere says: %s" % curs.fetchone()
       curs.close()
       conn.close()
    
    Run the test script and ensure that you get the expected output::
    
       $ python test_sqlany.py
       SQL Anywhere says: Hello, world!
    
    To test that Django can make use of the SQL Anywhere Database backend
    simply change to the "mysite" directory created in step 5 and ask
    Django to create the tables for the default applications. ::
    
       $ python manage.py syncdb
    
    If you don't receive any errors at this point then
    congratulations. Django is now correctly configured to use SQL
    Anywhere as a backend.
    
#. What to do if you have problems?

    If you run into problems, don't worry. First try re-reading the
    instructions above and make sure you haven't missed a step. If you are
    still having issues here are a few resources to help you figure
    out what went wrong. You can consult the documentation, or post to a
    forum where many of the SQL Anywhere engineers hang out.
    
    | SQL Anywhere Online Documentation: http://dcx.sybase.com/
    | SQL Anywhere Development Forum: http://sqlanywhere-forum.sybase.com/
    
#. Where to go from here?

    SQL Anywhere should now be successfully configured as a backend for
    your Django site. To learn more about creating web applications with
    Django try the excellent series of tutorials provided by the Django
    project:
    http://docs.djangoproject.com/en/dev/intro/tutorial01/#intro-tutorial01
