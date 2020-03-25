=====
TO-DO
=====

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

Error-handling
==============

* Unique constraint failures
* Error feedback (in labels)
