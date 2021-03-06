==================
V&A Digital Labels
==================

## Installation

Check out [these wise words](https://github.com/vanda/DigitalLabels/wiki/Digital-Labels-Installation)

## Requirements

If you follow the installation instructions above, these requirements should automatically be satifisfied.

The Django application currently has the following requirements:

* django 1.4 https://github.com/django/django
* django-reversion https://github.com/etianen/django-reversion
* sorl-thumbnail https://github.com/sorl/sorl-thumbnail
* django-grappelli https://github.com/sehmaschine/django-grappelli [branch grappelli_2_4]

## Quick Commands

Collate the static files by running:

    python manage.py collectstatic

Create the database tables. This will also create superusers for staff.

    python manage.py syncdb

Then populate it with some test data (a fake Chippendale display)

    python manage.py populatedb
    
…or with the included CSV look up (builds portals and digitallabels)

    python manage.py populatedb labels/data/objects_labels.csv  
    
Run tests by running:

    python manage.py test labels --settings=labelsite.settings_build
	 
You can then create a static build of all digital labels and portals:

    python manage.py build --settings=labelsite.settings_build -o /Output/Directory

# Digital Labels User Documentation

## Users

Admin users can be created by clicking `Users` under the __Auth__ heading on the admin homepage. Click the __Add User__ button in the top right, provide a username and password then __Save__.

You will then be prompted to add permissions for this user. This is necessary to enable them to create and edit content. The main tasks here are to grant the user _Staff status_ using the checkbox, so they can log in. The _User permissions_ box lists all the types of data that the user can change, add or delete. Shift-select all those rows beginning with `label |` and move them to the right box using the arrows provided. Save this page to make this user active.

## Editable Content

Underneath the __Labels__ heading on the admin homepage are all the types of data we can edit and create. The 2 most important items are the _Digital labels_ and the _Portals_. These represent the screens in the galleries. _Digital labels_ screens are made up of _Objects_; _Portals_ screens are made up of both _Objects_ and _Text labels_. The _Objects_ represent a typical label for each physical object; the _Text labels_ perform the role of biographies or historical context for the _Portals_. _Images_ are shared between _Objects_ and _Text labels_; whilst also providing time-out screens. Essentially, there is one pool of images.

## Objects and Digital Labels

As many objects as possible have been ready-imported into the admin system. Portals and Digital Labels have been created in order to group these objects into screens for the gallery. If you click on the `Objects` link under the __Labels__ heading, you will see a list of objects, and columns containing some summary information and a link to which _Digital Label_ or _Portal_ the object belongs.

Click the object image thumbnail or object number to edit the object details. These details have been pre-populated from the Search the Collections API. We have also downloaded all available images from VADAR and any previous label text that was available. 

If label texts were available in Search the Collections, the most recent is added to the _Main text_ field. Any other label texts are available lower down the page under the _Cms labels_ heading.

_Main text_ is what appears on the right-hand side of the label. The other fields, including _Place_ and _Artist maker_ are arranged on the left-hand side of the label.

_Gateway object_: this check box colours the label blue and the _Digital Label_ screen will start on this object.

_Artfund_: There is a checkbox to display and Artfund logo. 

_Images_: These images are collected from VADAR and Search the Collections. They can be deleted and replaced with different and new examples. 
- The contents of the __Caption__ field is displayed underneath the image in their "pop-up" form on the screen.
- To change the order in which object images appear on the label, you can grab hold of the diamond-shaped icon on the right of the image row and drag the image to change its position. The first image in the list is the main image for the object label on the screen.
- To remove an image altogether, click the cross on the right of the image row. The row will turn pink; this image is marked for deletion. The image will be removed when you _Save_ this screen using one of the buttons at the bottom of the page.

_Cms labels_: These are labels that have been written for previous displays and exhibitions, extracted from CMS. They might assist you in writing the _Main text_.


## Text labels and Portals

_Portals_ are a mixture of object labels and text labels. Text labels have a _Title_,  one _Image_ and a some body text. You can mark one _Text label_ as a __Biography__. A _Portal_ screen will start on the _Text label_ marked as __Biography__.  This label will be coloured blue and the text in the label will be arranged in a single column. Other _Text labels_ will have their text arranged in two columns.

You can choose the __Biography__ whilst you're on a _Portal_ admin screen.

## Adding new Text labels to a Portal screen

Whilst you're administrating a Portal, you'll need to create the biographies and historical contexts. To do this,

1. Click __Add another Text label__, under the _Text labels_ heading.
2. Write a title for your Text label, e.g. _Frank LLoyd Wright_ or _Historical Context_. This text will appear above the image on the screen in the gallery. Use the Preview link at the top of the page to check.
3. Click `Save and continue editing` at the bottom of the page. You will now see a row under the _Text labels_ heading for your new text label.
4. Click the _No images_ link on the left of this row. Your image thumbnail will eventually appear here.
5. You can now edit the main text for the label in the large text box. Click `Save and continue editing` when you are done.
6. You will also need to upload an image to associate with the label using the __Add another image__ link on the page.
7. The _Caption_ field is the text that will appear beneath the "zoomed" version when the image is touched in the gallery.
8. Click `Choose file` to upload a picture from you computer. Images should be under 2MB in size and have a `.png` or `.jpg` extension.
9. To change the order in which these labels appear on the gallery screen, you can grab hold of the diamond-shaped icon on the right of the row and drag the image to change its position in the "carousel".
10. You can `Preview` the whole Portal at any time by using the `Preview` button at the top of the admin screen.

## Adding new Object labels to a Portal or Digital label

We have tried to create as many Digital labels and Portals in advance as possible but there may be objects that are not available to Search the Collections (which is where the data comes from). In these cases, the object information will need to be manually added and images uploaded.

On a Portal or Digital label admin screen,

1. Click __Add another Digital Label Object__, under the _Digital label objects_ heading. A new row will appear.
2. If you know that the object has already been added to the system, you will be able to find it in the pull-down menu on the new row. This allows you to share the same object record with multiple screens.
3. Once you have selected the object from the pull-down menu, you can choose to make it the _Gateway object_ by clicking the radio button.
4. Click `Save and continue editing` at the bottom of the page.
5. If you would like to add a completely new object record to the system, you should click the blue plus next to the pull-down menu instead. A new window will pop up to allow you to create a new object.
6. If you know the object to be in Search the Collections, please add the unique `O` number in the Object number box. Otherwise, create a title or name for the object in the _Name_ column
3. Click `Save` at the bottom of the page. You will now see the new object has been automatically selected in the pull-down on the new row.
4. Click `Save and continue editing` at the bottom of the page. This object is now part of the digital label or portal screen.
4. Click the _No images_ link on the left of this row. Your image thumbnail will eventually appear here.
5. You can now edit the main text and other fields for the label. Click `Save and continue editing` when you are done.
6. You will also need to upload some images to associate with object using the __Add another image__ link on the page.
7. The _Caption_ field is the text that will appear beneath the "zoomed" version when the image is touched in the gallery.
8. Click `Choose file` to upload a picture from you computer. Images should be under 2MB in size and have a `.png` or `.jpg` extension.
9. To change the order in which objects appear on the gallery screen, you can grab hold of the diamond-shaped icon on the right of the row and drag the image to change its position in the "carousel".
10. You can `Preview` the whole Digital label or  Portal at any time by using the `Preview` button at the top of the admin screen.
    