bimprint
========

your free open source construction document generator, directly from IFC files


Abstract
========

This is the glorious result of a Hackathon in Eindhoven, The Netherlands.


Organization of this repository
===============================

user_interface
--------------

A 3D web-interface, based on BIMsurfer, to select the product to generate detailed construction documents for.


svg_generator
-------------

A collection of Python scripts, based on IfcOpenShell and PythonOCC, that generates relevant 2d floor plans from 3d IFC models. A single product is to be selected in the user_interface, which is annotated relative to the closest IfcGrid intersection point.


documentation_server
--------------------

A PHP interface that accepts commands from the user_interface and returns the generated file to the user.
