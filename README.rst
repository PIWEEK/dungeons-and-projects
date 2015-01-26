dungeons-and-projects
=====================

Visualize technical debt as a fantasy city whose buildings have subterranean dungeons populated by hideous monsters.

What is technical debt? Those defects in the source code of a program, like lack of readabilty or modularity, that
do not affect directly to the program operation (so they are not bugs), but any programmer touching the code knows
that they may cause hard to detect bugs in the future, or make further changes slow and difficult (this is why it's
called debt). By its nature, technical debt is not visible to end users and product owners, so it's not easy to
convince them to dedicate time and effort to solve it (a.k.a. 'paying the debt').

Dungeons and Projects offer a way to display debt in a very grahpical, simple and funny way. Our code base is shown
as a fantasy world map, where main modules are cities and submodules are buildings, shiny and proud, but... beneath
them there are dark dungeons populated by nasty debt creatures.

The application comes with a default set of tools for code analysis in search of 'code monsters', but is very modular,
and you can program your own ways to detect issues, or even can completely change the display style by writing a new
presentation engine but keeping the business logic.

Features
========

- Store in a database the representation of a project, with directories (that match the directory structure of your
  source code) and modules (that initially match the directory tree, but may be manually rearranged for a more convenient
  organization, if you like). Display the modules as cities and buildings.

- Store defects and display them as monsters in the dungeons beneath the module buildings.

- By default there is a tool to initialize a new project, reading the tree structure of your code, and other one that
  scans source files looking for "TODO", "FIXME" and "NOTE" comments, creating a monster for each one.

- But there is a complete API REST that allows you to access all data and display any way you want, or to define you
  own methods of code analysis (you can connect a linter, a code complexity analysis tool, link with your version control
  system to launch analyzer with each commit, etc.).

Installation
============

Server
------

This is a normal Django setup.

- Create a database in any supported SQL server (if you omit this step, you can use the default sqlite database and you
  don't need to configure anything else; this is not recommended in production).

- Create a python virtualenv (optional but very recommended).

- Clone the D&P code::

      git checkout git@github.com:PIWEEK/dungeons-and-projects.git

- Copy ``server/settings/local.py.example`` to ``local.py``. Set the connection data for your database (if any) and any other
  configuration you need.

- If this is a development environment, run the server with::

      python manage.py runserver

- If this is a production environment, change ``local.py`` to::

      from .deployment import *

  and set all configuration needed for deployment, as indicated in the Django manual https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/.
  Then put it under your favourite application server with WSGI protocol (nginx, apache or the like).

Client
------

In the future we will probably upload this to PyPi, but now the procedure is

- Create a python virtualenv (optional but very recommended).

- Clone the D&P code::

      git checkout git@github.com:PIWEEK/dungeons-and-projects.git

- Install the client library::

      cd client/daprojects_python; python setup.py install

- Use the client with::

      client/daprojects_cli/daprojects -h

