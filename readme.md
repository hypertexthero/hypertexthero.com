# hypertexthero.com

Features
----

- [Markdown (including footnotes support) for editing, HTML for display](https://code.djangoproject.com/wiki/UsingMarkup).
- Links and original article note types published to the same content column.
- Dates on homepage are displayed only once for notes published on the same day. Using '[ifchanged](https://docs.djangoproject.com/en/dev/ref/templates/builtins/?from=olddocs#ifchanged)'.
- Code syntax highlighting in markup courtesy of [Pygments](http://pygments.org/) (here are [some CSS styles](https://github.com/richleland/pygments-css)) and [CodeHilite](http://pythonhosted.org/Markdown/extensions/code_hilite.html).
- Simple search.
- Uses Django admin interface.
- [Mozilla Persona for authentication](http://django-browserid.readthedocs.org/)
- XML feeds in both Atom and RSS flavours.
- Tags with auto-suggest widget for post keywords

## Things to do

- Set up [Fabric](http://docs.fabfile.org/en/1.6/tutorial.html) script for deployment.
- Set up [SSL for privacy](https://www.tbray.org/ongoing/When/201x/2012/12/02/HTTPS).
- Set up own instance of nginx?
- Add to portfolio:
    - Graphite logo prototype
    - http://www.angelopaionni.it/
    - ippc identity work, including redrawn logo, trifold brochure, etc
- Add Textile as a text syntax option.
- Set up pagedown for markdown preview.
- [Automatically post new articles to Twitter](http://djangosnippets.org/snippets/1339/).
- Find a way to run django tests so each url on the site is accessed and generated automatically with a command.
- Finalize data import. Don't forget to fix macroman->utf-8 encoding problems and import keywords into tag field.
- Refactor breadcrumbs into templatetag to remove repetition.
- [Images in entries](http://stackoverflow.com/a/537966/412329)? [Image](http://stackoverflow.com/questions/1021487/add-functionality-to-django-flatpages-without-changing-the-original-django-app) and [thumbnail](https://bitbucket.org/winsmith/django-thumbnail/wiki/Home) functionality for flatpages?
- [Ordering](https://github.com/iambrandontaylor/django-admin-sortable) (or [this](http://djangosnippets.org/snippets/2047/, or [this](http://djangosnippets.org/snippets/1053/)) of flatpages?
- Make Work category pages and list of categories page titled 'What'.
- Articles available in Markdown format on the server (article-title.txt).
- JavaScript-based search for static files on server?
- Learn how to [write tests](http://www.tdd-django-tutorial.com/) for views, then write unit and functional tests.
- Consider using [prettify](http://google-code-prettify.googlecode.com/svn/trunk/README.html) for syntax highlighting (shows line numbers).
- Combine [django-medusa](https://github.com/mtigas/django-medusa/) with this application so we are serving static HTML files from disk on server and Markdown and HTML columns in database.
