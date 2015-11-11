This is a SQL Anywhere database backend for Django. The backend is
distributed as a stand-alone python module. This backend has been
tested with SQL Anywhere 12 and Django versions 1.2.7, 1.3.3, and 1.4.1.

This driver is licensed under the terms of the BSD license. See the
file name "LICENSE" included with this package for more information.

Getting Started

---

<ol><li><b>Install the required software</b>

<ol type='a'><li><b>SQL Anywhere 12.0.1</b> The SQL Anywhere Web Edition is a free, full-featured version for development and deployment of browser based applications. If you don't already have a license for SQL Anywhere, the Web Edition is a great place to start. Get the Web Edition <a href='http://www.sybase.com/detail?id=1057560'>here</a>.</li>

<li><b>Python (2.4 or greater)</b> Install Python if you don't already have it installed. We recommend Python 2.7 but any version greater than 2.4 is supported. Note however that Python 3 introduced backwards incompatible features and many projects including Django do not currently have support for Python 3. You can download python from <a href='http://www.python.org/download/'>here</a>.<br>
<br>
If you are running on Linux you will most likely also be able to find<br>
python through your distribution's package management system.</li>

<li><b>Python setuptools</b> The setuptools project for python acts as a package manager for Python code. Using setuptools will make it trivial to install the correct version of Django to use with SQL Anywhere. You can get setuptools for python from <a href='http://pypi.python.org/pypi/setuptools/'>here</a>.<br>
<br>
Again, if you are running on Linux you most likely be able to find<br>
setuptools through your distribution's package management<br>
system. This package is called "python-setuptools" on Ubuntu and<br>
"python-setuptools-devel" on Fedora.</li>

<li><b>Django 1.4</b> Once you have installed setuptools, installing Django is a snap, simply run:<br>
<br>
<code>$ easy_install Django==1.4</code>
</li>
<li><b>Python SQL Anywhere Database Interface</b> The SQL Anywhere Database Interface for Python provides a Database API v2 compliant driver (see Python PEP 249) for accessing SQL Anywhere databases from Python. The SQL Anywhere backend for Django is built on top of this interface so installing it is required.<br>
<br>
You can obtain the Python SQL Anywhere Database Interface <a href='http://code.google.com/p/sqlanydb'>here</a>.<br>
<br>
Install the driver by extracting the archive and running the following<br>
command in the resulting directory:<br>
<br>
<code>$ python setup.py install</code>
</li>

<li><b>SQL Anywhere Django Backend</b> You can obtain the SQL Anywhere Database backend for Django <a href='http://code.google.com/p/sqlany-django'>here</a>.<br>
<br>
Install the backend by extracting the archive and running the following<br>
command in the resulting directory:<br>
<br>
<code>$ python setup.py install</code>
</li></ol></li>

<li><b>Setup your environment (Linux/Unix/Mac OS X only)</b> SQL Anywhere requires several environment variables to be set to run<br>
correctly -- the most important of which are PATH and LD_LIBRARY_PATH. The SQL Anywhere install creates a file named sa_config.sh to set all necessary environment variables automatically (Note the file is named sa_config.csh if you are using a csh derivative as your shell).<br>
<br>
This file is located in the "bin32" and/or the "bin64" directories of<br>
your install. Before trying to run the SQL Anywhere server or connect<br>
to a running server in a given shell you should make sure to source<br>
the file (with the "." command) corresponding to the bitness of the<br>
SQL Anywhere binaries you want to use. For example, if the product is<br>
installed in /opt/sqlanywhere12 you should run:<br>
<br>
<code>$ . /opt/sqlanywhere12/bin32/sa_config.sh</code>
</li>

<li><b>Create a database</b> Issue the following command to create a new database to use with Django. Note that we are specifying the UCA collation so that that CHAR columns in the database will support unicode strings.<br>
<br>
<code>$ dbinit -z UCA django.db</code>

If all goes well SQL Anywhere will have created a new database file<br>
named 'django.db' in the directory where you ran the dbinit<br>
command. Feel free to move this database file to any location you<br>
want. You can even copy it to a machine running a different operating<br>
system if you wish.</li>

<li><b>Start the Database Server</b> SQL Anywhere includes two different database servers -- The personal server (dbeng12) and the network server (dbsrv12). Both servers servers support the same complete set of features except that the personal server is limited to running on one CPU, allows a maximum of 10 concurrent connections and does not accept network connections from other machines. We will use the network server for our example.<br>
<br>
<code>$ dbsrv12 django.db</code>
</li>

<li><b>Configure Django</b> Creating a new Django site and configuring it to use SQL Anywhere is very easy. First create the site in the normal fashion:<br>
<br>
<code>$ django-admin.py startproject mysite</code>

Then edit the file mysite/mysite/settings.py and change the DATABASES<br>
setting to match what is given below:<br>
<br>
<pre><code>DATABASES = {<br>
	  'default' : {<br>
 	      'ENGINE': 'sqlany_django',<br>
	      'NAME': 'django',<br>
	      'USER': 'dba',<br>
	      'PASSWORD': 'sql',<br>
	      'HOST': 'myhost',<br>
	      'PORT': 'portnum'<br>
	  }<br>
}<br>
</code></pre>

Here's how the parameters correspond to SQL Anywhere connection parameters:<br>
<ul><li>NAME = DBN</li>
<li>USER = USR</li>
<li>PASSWORD = PWD</li>
<li>HOST = HOST</li>
<li>PORT = (port number in host, i.e. myhost:portnum)</li></ul>

If you need to specify other connection parameters (eg. ENG, which is required for client versions prior to v12.0.0), you can set a value<br>
with the key "OPTIONS", like this:<br>
<br>
<pre><code>DATABASES = {<br>
	  'default' : {<br>
 	      'ENGINE': 'sqlany_django',<br>
	      'NAME': 'django',<br>
	      'USER': 'dba',<br>
	      'PASSWORD': 'sql',<br>
	      'OPTIONS': {'eng': 'django'}<br>
	  }<br>
}<br>
</code></pre>

Note: SQL Anywhere allows you to run several database servers on one<br>
machine. For this reason you should always specify the server you want<br>
to connect to as well as the database name. However if you want to connect to a server running in a SA OnDemand (cloud) environment, you should specify the NAME and HOST (and optionally PORT) options, and <b>not</b> specify the server name.</li>

<li><b>Test to make sure everything is working</b> The SQL Anywhere database backend for Django makes use of the Python SQL Anywhere Database interface. We first want to test that this interface is working correctly before testing Django connectivity itself. Create a file named test_sqlany.py with the following contents:<br>
<br>
<pre><code>import sqlanydb<br>
conn = sqlanydb.connect(uid='dba', pwd='sql', eng='django', dbn='django')<br>
curs = conn.cursor()<br>
curs.execute("select 'Hello, world!'")<br>
print "SQL Anywhere says: %s" % curs.fetchone()<br>
curs.close()<br>
conn.close()<br>
</code></pre>

Run the test script and ensure that you get the expected output:<br>
<br>
<pre><code>$ python test_sqlany.py<br>
SQL Anywhere says: Hello, world!<br>
</code></pre>

To test that Django can make use of the SQL Anywhere Database backend<br>
simply change to the "mysite" directory created in step 5 and ask<br>
Django to create the tables for the default applications.<br>
<br>
<code>$ python manage.py syncdb</code>

If you don't receive any errors at this point then<br>
congratulations. Django is now correctly configured to use SQL<br>
Anywhere as a backend.</li>

<li><b>What to do if you have problems?</b> If you run into problems, don't worry. First try re-reading the instructions above and make sure you haven't missed a step. If you are still having issues here are a few resources to help you figure out what went wrong. You can consult the documentation, or post to a forum where many of the SQL Anywhere engineers hang out.<br>
<br>
Links:<ul>
<li><a href='http://dcx.sybase.com'>SQL Anywhere Online Documentation</a></li>
<li><a href='http://sqlanywhere-forum.sybase.com'>SQL Anywhere Development Forum</a></li></ul></li>

<li><b>Where to go from here?</b> SQL Anywhere should now be successfully configured as a backend for your Django site. To learn more about creating web applications with Django try the excellent series of <a href='http://docs.djangoproject.com/en/dev/intro/tutorial01/#intro-tutorial01'>tutorials provided by the Django project</a>.</li>
</ol>