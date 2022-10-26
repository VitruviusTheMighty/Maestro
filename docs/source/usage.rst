Usage
=====

.. _installation:

Installation
------------

To use this repository, create a virtual environment in the parent directory **Maestro** with:

``python -m venv`` **.< virtual python env name >**

Then activate this environment, use ``.env-name//Scripts//activate``

*TODO: Added functionality for MACOS and LINUX*

Once you have activated your virtual python environment. Install the dependencies using ``python -m pip install -r requirements.txt``

.. .. code-block:: console

..    (.venv) $ pip install lumache

.. Creating recipes
.. ----------------

.. To retrieve a list of random ingredients,
.. you can use the ``lumache.get_random_ingredients()`` function:

.. .. autofunction:: lumache.get_random_ingredients

.. The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
.. or ``"veggies"``. Otherwise, :py:func:`lumache.get_random_ingredients`
.. will raise an exception.

.. .. autoexception:: lumache.InvalidKindError

.. For example:

.. >>> import lumache
.. >>> lumache.get_random_ingredients()
.. ['shells', 'gorgonzola', 'parsley']

