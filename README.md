# Web-to-Image Converter #
The Web-to-Image converter uses the config.json file to visit a website (with or with authorization), take a screenshot and save the screenshot in the defined location (see the 'image_directory'-property).

## Configuration ##

All configurations of the Web-to-Image converter tool is done through a config.json file in the same location as the tool script.
* **"image_directory"** - Directory for where to save the screenshots. It should be noted that the script does not create the directory if the path-location is not available.
* **"time_per_slide"** - The time paused on each slide. (default 5 sec)
* **"refresh_interval"** - The number of rotations which the slide show will continue before refreshing all the images collected. (default 5)
* **"allowed_timeout"** - The allowed time delay for a CSS selector to wait until the application will fail due to missing selector. (default 5 sec)
* **"websites"** - An array of websites. Each website containing the following properties.
  * **"image_name"** - Name of the image when save.
  * **"url"** - URL to the website for each the screenshot shall be taken.
  * **"selector"** - [Navigation 🔄] Used to provide an HTML selector, which the tool will focus and resize the screenshot according to.
  * **"scroll_to_selector"** - [Navigation 🔄] If this property is set to true, the "selector"-property is used as a point to scroll to. Otherwise, the selector will be used as described in its own description.
  * **"clicks"** - [Navigation 🔄] Sets an array of CSS selectors, which will be clicked before taking the screenshot.*
  * **"captions"** - [Caption 🆎] Sets an array of captions-objects, which contains all the "Caption"-information found below.
    * **"caption_text"** - [Caption 🆎] Caption text can be used to add a text message to the screenshot.
    * **"caption_x"** - [Caption 🆎] Sets the x-axis position of the captions on the screenshot. Requires the "caption"-property to be set.
    * **"caption_y"** - [Caption 🆎] Sets the y-axis position of the captions on the screenshot. Requires the "caption"-property to be set.
    * **"caption_color"** - [Caption 🆎] Sets the font color of the captions on the screenshot. Requires the "caption"-property to be set.
    * **"caption_size"** - [Caption 🆎] Sets the font size of the captions on the screenshot. Requires the "caption"-property to be set.
  * **"credentials"** - [Credentials 🔐] The credentials sections can be used to add login credentials to the screenshot collector. This can be useful if the desired view is secured my an authentication stage. E.g. Account for pipeline monitoring. 
    * **"username"** - [Credentials 🔐] Sets the username for the login.
    * **"username_selector"** - [Credentials 🔐] Sets the CSS selector in which the username can be inserted. Aim for input-tag.
    * **"password"** - [Credentials 🔐] Sets the password for the login.
    * **"password_selector"** - [Credentials 🔐] Sets the CSS selector in which the password can be inserted. Aim for input-tag.
    * **"submit_selector"** - [Credentials 🔐] Sets the CSS selector for which the button or element that shall be used to trigger authentication of the username and password.

[Navigation🔄]-configuration: Any website-configuration marked with "Navigation", cannot be used together with any other "Navigation"-marked configuration (unless explicitly specified).
## Contact ##
* Author: Daniel Høyer Bjørnskov
* Mail: daniel.h.bjornskov@gmail.com
* Website: www.integu.net

## Preview ##
*(Images from google and personal blog)*
![](https://github.com/DanielHJacobsen/WebToImageConverter/blob/master/resources/Preview.gif)