BlueChips is a simple finance tracking application designed for small groups of
people with shared expenses. It was designed and developed by groups of
students who got tired of the headaches of managing lots of little payments
between roommates.

Demo
----

If you want to try out BlueChips, you can go to http://demo.bluechi.ps

Example Scenario
----------------

1. Larry lives with Curly and Moe.
2. Larry gets the utility bill, and enters it as an expenditure on
   their BlueChips site. Everyone shares the utilities, so it's just an
   even split.
3. A week later, Moe pays the rent. Curly has a smaller room, so he
   pays a smaller fraction of the rent.
4. At any time, any user can visit the BlueChips site and see who
   needs to pay who how much in order to settle the books.
5. After a few months, Moe has paid for a disproportionate amount of
   stuff, so the other roommates each make a transfer to Moe, and
   enter the amounts in BlueChips.

Additional Features
-------------------

* Support for negative expenses
* Uses any authentication mechanism which can set the REMOTE_USER
  environment variable, including authentication modules supported by
  Apache, nginx, lighttpd, and others.
* Email notifications of changes (optional)
* 100% test coverage

Installation and Setup
----------------------

Install ``BlueChips`` using easy_install::

    easy_install BlueChips

Make a config file as follows::

    paster make-config BlueChips config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Host the application behind an authentication layer which sets REMOTE_USER.

Apache Configuration
--------------------

The recommended deployment platform for BlueChips is Apache, mod_wsgi, and any
Apache module which provides authentication. Here is an example vhost
configuration::

    <VirtualHost bluechips.example.com:80>
        ServerName bluechips.example.com

        WSGIScriptAlias / /var/www/bluechips.wsgi
        <Directory /var/www>
            Order deny,allow
            Allow from all
        </Directory>

        <Location />
            AuthType Basic
            AuthName "Example BlueChips Site"
            AuthUserFile /etc/apache2/passwords
            Require valid-user
        </Location>
    </VirtualHost>

The ``bluechips.wsgi`` wrapper script looks just like::

    from paste.deploy import loadapp
    application = loadapp('config:/var/www/ssl/config.ini')

Acknowledgments
---------------

BlueChips is the latest in a long line of software to make managing
group finances easier, and would not be possible without the
intellectual inspiration of those predecessors.

CUTCAT's `accounting software`_ started the trend of
software-based accounting mechanisms. It inspired a re-implementation
as a curses script by `Nelson Elhage`_, which introduced the
notion of "pushing expenditures" to simplify transfers. The algorithm
used in BlueChips for settling the books is directly cargo-culted from
Nelson's implementation.

.. _accounting software: http://cutc.at/accounting-software.html
.. _Nelson Elhage: http://nelhage.com/
