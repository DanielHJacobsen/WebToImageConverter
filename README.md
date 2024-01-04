# Web-to-Image Converter #
The Web-to-Image converter uses the config.json file to visit a website (with or with authorization), take a screenshot and save the screenshot in the defined location (see the 'image_directory'-property).

## Configuration ##

All configurations of the Web-to-Image converter tool is done through a config.json file in the same location as the tool script.
* "image_directory" - Directory for where to save the screenshots. It should be noted that the script does not create the directory if the path-location is not available. 
* "websites" - An array of websites. Each website containing the following properties.
  * "image_name" - Name of the image when save.
  * "url" - URL to the website for each the screenshot shall be taken.
  * "selector" - Used to provide a HTML selector, which the tool will focus and resize the screenshot according to. 
  * "username" - Username for authorization on the website if necessary. Left empty "" by default.
  * "username" - Password for authorization on the website if necessary. Left empty "" by default.