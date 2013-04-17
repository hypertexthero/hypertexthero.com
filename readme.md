# hypertexthero.com

Features
----

- [Markdown (including footnotes support) for editing, HTML for display](https://code.djangoproject.com/wiki/UsingMarkup).
- Links and original article note types published to the same content column.
- Dates on homepage are displayed only once for notes published on the same day. Using '[ifchanged](https://docs.djangoproject.com/en/dev/ref/templates/builtins/?from=olddocs#ifchanged)'.
- Code syntax highlighting in markup courtesy of [Pygments](http://pygments.org/) (here are [some CSS styles](https://github.com/richleland/pygments-css)) and [CodeHilite](http://pythonhosted.org/Markdown/extensions/code_hilite.html).
- Simple search.
- Uses Django admin interface.
- Combine [django-medusa](https://github.com/mtigas/django-medusa/) with this application so we are serving static HTML files from disk on server and Markdown and HTML columns in database.
- XML feeds in both Atom and RSS flavours.

## TODO

- Get rid of footnotes title and ruler.
- Change Logbook plane to Macchi.
- Make Work category pages?
- List of tags (categories) page. Titled 'What'.
- Articles available in Markdown format on the server (article-title.txt).
- JavaScript-based search for static files on server?
- Set up [Fabric](http://docs.fabfile.org/en/1.6/tutorial.html) script for deployment to github-powered site, maybe also github pages.
- [Automatically post new articles to Twitter](http://djangosnippets.org/snippets/1339/).
- Learn how to [write tests](http://www.tdd-django-tutorial.com/) for views, then write unit and functional tests.
- [SSL](https://www.tbray.org/ongoing/When/201x/2012/12/02/HTTPS).
- Consider using [prettify](http://google-code-prettify.googlecode.com/svn/trunk/README.html) for syntax highlighting (shows line numbers)