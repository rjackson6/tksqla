=====
TO-DO
=====

Bugs
====

* Check enabled/disabled behavior with form callbacks

Application Features
====================

General
-------

* Record views
* Record saved successfully feedback

Forms
-----

* Save and add another + save and close
* Preview of existing records
   * Prevention of obvious unique constraint failues
* Load existing record for editing
* Expand validation
* Combobox casefold() validation with integer entries

Record Views
------------

* Scrollbars for Treeview

Configuration
=============

* Paths for application data storage

Design
======

* Expand form/classes
   * Common get/save behavior
* Use of Tk variables
   * Can associate one variable with more than one widget
   * Can bind functions to be called when values change (trace)
   * Variables persist beyond the destruction of a widget
   * Some recommendations are to not use them unless needed in one of the above
     cases
* New DB fields, validators
* SQLite-specific types in SQLAlchemy
* Column-to-widget mapping (i.e., get the data types from the column)

Error-handling
==============

* Route & parse from @contextmanager for starters
* Unique constraint failures
* Error feedback (in labels)
