# Web-to-Image Converter #
The Web-to-Image converter uses the config.json file to visit a website (with or with authorization), take a screenshot and save the screenshot in the defined location (see the 'image_directory'-property).

## Configuration ##

All configurations of the Web-to-Image converter tool is done through a config.json file in the same location as the tool script.
* **"image_directory"** - Directory for where to save the screenshots. It should be noted that the script does not create the directory if the path-location is not available.
* **"time_per_slide"** - The time paused on each slide.
* **"refresh_interval"** - The number of rotations which the slide show will continue before refreshing all the images collected.
* **"websites"** - An array of websites. Each website containing the following properties.
  * **"image_name"** - Name of the image when save.
  * **"url"** - URL to the website for each the screenshot shall be taken.
  * **"selector"** - Used to provide an HTML selector, which the tool will focus and resize the screenshot according to.
  * **"scroll_to_selector"** - If this property is set to true, the "selector"-property is used as a point to scroll to. Otherwise, the selector will be used as described in its own description.
  * **"username"** - Username for authorization on the website if necessary. Left empty "" by default. (Not yet implemented)
  * **"password"** - Password for authorization on the website if necessary. Left empty "" by default. (Not yet implemented)

## Contact ##
* Author: Daniel Høyer Bjørnskov
* Mail: daniel.h.bjornskov@gmail.com
* Website: www.integu.net

## Preview ##
*(Images from google and personal blog)*
![](https://github.com/DanielHJacobsen/WebToImageConverter/blob/master/resources/Preview.gif)