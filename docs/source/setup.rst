Setup
=====

Dependencies
------------
Before setting up this project, you'll need the following installed

- Python 3.8+ (https://www.python.org/downloads/)
- Git (https://git-scm.com/downloads)

Instructions
------------

To setup a play the games detailed in this documentation, for best usage, open a terminal on your machine.

For Windows, **powershell** or **command prompt** work great

For MacOS, **terminal** works great

For Linux, typically whatever default terminal exists is sufficient

In your operating system's associated terminal application, navigate to the directory of your choice using:

    ``cd <directory//on//your//machine>``

then enter the command:

    ``git clone https://github.com/VitruviusTheMighty/Maestro.git``

The entire codebase should now exist in the directory you cloned it into.



Installation
------------

Now that you have the codebase cloned, you should install all necessary packages.
There is a list of required packages in `requirements.txt`

Creating a Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use this repository, create a virtual environment in the parent directory **Maestro** with:

``python -m venv`` **.< virtual python env name >**

Activating Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Then activate this environment, use ``.env-name//Scripts//activate``

For MacOS and Linux systems, you can use ``source .env-name/bin/activate``

Once you have activated your virtual python environment. Install the dependencies using ``python -m pip install -r requirements.txt``

Running
-------

You can run the main menu to access *most* of the games using:

    ``python maestro.py``

Development
-----------

If you want to have a better look at the code in this project. I recommend using 
**VSCode** for development. (https://code.visualstudio.com/)

Once you've installed it, opening this codebase can be easily accomplished in two ways

Via File Explorer / VSCode Menu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Open VSCode 
- Select `Open Folder`
- Navigage to the Folder / Directory you installed the project to
- Select `Maestro` 
- You should open up with all associated files for this project accessible

.. note:: 

    All projects outlined in the documentation are currently accessible in: **portfolio/projects/***

Via Terminal
~~~~~~~~~~~~

- Open terminal
- Navigage to the Folder / Directory you installed the project to, using **cd**
- Once you are in **path//to//Maestro//** enter the command **code .**
- VSCode should open up with all associated project files