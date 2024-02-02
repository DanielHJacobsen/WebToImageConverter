# Web-to-Image Converter #
The Web-to-Image converter uses the config.json file to visit a website, navigates to a defined location, takes a screenshot and save the screenshot in the defined location.\
A repository ideal for a flexible dashboard slideshow.

## How to get started ##
1. Download all required dependencies:\
`pip install -r requirements.txt`
2. Create and configure your own `config.json` file in the root of the project (see Configuration-section).
3. Start the script. Working directory of the script is intended to be the 'src'-directory. \
`python main.py`

## Configuration ##
>**_The project includes an "example_config.json", which can be used as inspiration to create your own configuration.\
\
It will be necessary to create your own 'config.json'-file in the root of the repository in order to run the program.\
\
Your own configuration file is by default added to the gitignore-filter._**

All configurations of the Web-to-Image converter tool is done through a config.json file in the same location as the tool script.
* **"image_directory"** - [String] Directory for where to save the screenshots. It should be noted that the script does not create the directory if the path-location is not available.
* **"time_per_slide"** - [Integer] The time paused on each slide. (default 5 sec)
* **"allowed_timeout"** - [Integer] The allowed time delay for a CSS selector to wait until the application will fail due to missing selector. (default 5 sec)
* **"websites"** - [Array] An array of websites. Each website containing the following properties.
  * **"image_name"** - [String] Name of the image when save.
  * **"skip_if_failed"** - [Boolean] A boolean property, which configured if the program shall terminate if the image cannot be found. (default set to "true")
  * **"url"** - [String] URL to the website for each the screenshot shall be taken. If the 'URL'-property leads to a GIF-, JPEG- or PNG-file, it will not be possible to use the 'credential'-configuration.
  * **"selector"** - [String] [Navigation 🔄] Used to provide an HTML selector, which the tool will focus and resize the screenshot according to.
  * **"scroll_to_selector"** - [Boolean] [Navigation 🔄] If this property is set to true, the "selector"-property is used as a point to scroll to. Otherwise, the selector will be used as described in its own description.
  * **"clicks"** - [Array of Strings] [Navigation 🔄] Sets an array of CSS selectors, which will be clicked before taking the screenshot.*
  * **"time_for_slide_override"** - [Integer] An integer-property used to override the default time per slide for this specific screenshot. The default time is set by the 'time_per_slide'-property.*
  * **"captions"** - [Array] [Caption 🆎] Sets an array of captions-objects, which contains all the "Caption"-information found below.
    * **"caption_text"** - [String] [Caption 🆎] Caption text can be used to add a text message to the screenshot.
    * **"caption_x"** - [Integer] [Caption 🆎] Sets the x-axis position of the captions on the screenshot. Requires the "caption"-property to be set.
    * **"caption_y"** - [Integer] [Caption 🆎] Sets the y-axis position of the captions on the screenshot. Requires the "caption"-property to be set.
    * **"caption_color"** - [String] [Caption 🆎] Sets the font color of the captions on the screenshot. Requires the "caption"-property to be set.
    * **"caption_size"** - [Integer] [Caption 🆎] Sets the font size of the captions on the screenshot. Requires the "caption"-property to be set.
  * **"credentials"** - [Array] [Credentials 🔐] The credentials sections can be used to add login credentials to the screenshot collector. This can be useful if the desired view is secured my an authentication stage. E.g. Account for pipeline monitoring. If the 'URL'-property leads to a GIF-, JPEG- or PNG-file, it will not be possible to use the 'credential'-configuration.
    * **"username"** - [String] [Credentials 🔐] Sets the username for the login.
    * **"username_selector"** - [String] [Credentials 🔐] Sets the CSS selector in which the username can be inserted. Aim for input-tag.
    * **"password"** - [String] [Credentials 🔐] Sets the password for the login.
    * **"password_selector"** - [String] [Credentials 🔐] Sets the CSS selector in which the password can be inserted. Aim for input-tag.
    * **"submit_selector"** - [String] [Credentials 🔐] Sets the CSS selector for which the button or element that shall be used to trigger authentication of the username and password.

[Navigation🔄]-configuration: Any website-configuration marked with "Navigation", cannot be used together with any other "Navigation"-marked configuration (unless explicitly specified).
## Contact ##
* Author: Daniel Høyer Bjørnskov
* Mail: daniel.h.bjornskov@gmail.com
* Website: www.integu.net

## Preview ##
*(Images from google and personal blog)*
![](https://github.com/DanielHJacobsen/WebToImageConverter/blob/master/resources/Preview.gif)