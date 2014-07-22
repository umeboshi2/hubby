# Creating a Static Website with GitHub

## GitHub Pages

GitHub Pages provide a static website for your project that is, 
by nature of the service, kept in a git repository.  This makes 
updating the site, and even reverting parts of it back to an 
earlier version easy.

For coding projects, I often make my websites by taking specially 
formatted text files, such as restructured text or markdown, and 
render the files to html, then post the html files to the 
document root.  For the GitHub sites, I decided to basically 
write the pages in the same manner, except for now I am limited to 
using markdown.  The difference is that I am not rendering the 
markdown text to html, rather the web browser will be doing this.

The desire is to use [requirejs-text](https://github.com/requirejs/text) 
to retrieve the file content by name, then have the client render 
the text.  At the moment, this isn't working, so I am using a 
script to take the markdown files and create a 
[JSON](http://en.wikipedia.org/wiki/JSON) object that is 
stored in a corresponding .json file, which is retrieved in an 
[xhr](http://en.wikipedia.org/wiki/XMLHttpRequest) request.  When 
this difficulty is overcome, all that will need to be done will be 
manage *one* directory of text files.


## Vagrant

I am using [Vagrant](http://vagrantup.com) to house the development 
tools to build the website.  I use a [nodejs](http://nodejs.org) 
environment to develop the website, using [Grunt](http://gruntjs.com) 
to handle much of the work.  I am also using the basebox I created 
to help with web development, 
[trumpet-i386](https://vagrantcloud.com/umeboshi/trumpet-i386).

The trumpet box comes with fairly recent versions of nodejs,
[compass](http://compass-style.org), 
[coffee script](http://coffeescript.org), Grunt,
[Bower](http://bower.io), and some ruby gems to help with 
stylesheet development.


## Trumpet without pyramid

[Trumpet](https://github.com/umeboshi2/trumpet) is the code that 
I use to create websites.  The trumpet web server is a 
[Pyramid](http://www.pylonsproject.org/) based server that serves 
[REST](http://en.wikipedia.org/wiki/Representational_state_transfer) 
resources and the static resources built in the nodejs environment.

With the GitHub sites serving only static resources, the web 
server portion of trumpet isn't needed, but the tools that provide 
the client side applications and stylesheets are still quite 
useful.

## Stylesheet Development

Here I should mention compass, the gems I've installed on the 
trumpet basebox, and how to maintain the stylesheets.

## Client Application Development

Here I should mention all those tools that I have had a hard time 
selecting and putting together in the manner I have chosen to 
develop.

### Basic Guidelines

Three axioms I've chosen to follow:

1. Use a stack built of minimal components that perform specific 
   jobs.
   
2. Write all code in coffeescript, but do not depend on coffee
   script upstream, when good javascript serves better.
   
3. Use components that support amd loading as much as possible
   to keep the coding environment as clean as possible.
   
(The marriage of coffeescript and amd loading provides the ability 
to maintain a large code base in a manner almost comparable to
python.)

### Base Library

Due to the necessity of amd loading, the primary javascript 
library that is used is [Requirejs](http://requirejs.org).  This 
library works for me in two distinct scenarios.  The first 
scenario is the development process, where the library handles 
the loading of all of the resources.  While this scenario is 
great for development, the astounding number of http requests 
that are done can be a show stopper if this was used in 
production.  The second scenario that requirejs is used for is 
in the building of a single static resources that contains the 
bulk of the modules that are loaded into your app by scanning 
the files and including all the top level requirements 
recusively in each module loaded. This is done in the nodejs 
environment with the r.js command line tool that requirejs 
provides.  This base library is the code that helps to load and 
manage all of the other parts of the application stack.

### Lower Libraries

These lower libraries form the common base that each application 
is based upon.  The most notable of the lower libraries is 
[jQuery](http://jquery.com).  This library is very useful for 
selecting and manipulating 
[DOM](http://en.wikipedia.org/wiki/Document_Object_Model) elements.  
This library has possibly the largest user base of any javascript 
library being used by anybody.

I decided to use [Backbone](http://backbonejs.org/) to provide the 
model/view framework for the applications.  [Lo-Dash](http://lodash.com/) 
was chosen, mainly for the amd support, to provide the underscore 
dependency for backbone.

I wanted something better than the underscore templates that were 
already available in the stack.  I just happened to wander 
across [Teacup](http://goodeggs.github.io/teacup/) one day and decided 
that this would be the best way to create templates, although the 
boilerplate for the tag names can be tedious to keep up with.

### Middle Level Libraries

[MarionetteJS](http://marionettejs.com/) was chosen to help manage 
the backbone objects in a coherent manner.  While this 
[chapter](http://addyosmani.github.io/backbone-fundamentals/#marionettejs-backbone.marionette) in the backbone fundamentals book does a good job of 
describing the benefits of using Marionette, it doesn't say much 
about the [Wreqr](https://github.com/marionettejs/backbone.wreqr) object 
that is very useful in managing the collection of objects and interactions.




[static](#pages/trumpet-resources) resources
