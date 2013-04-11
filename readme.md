# hypertexthero.com

Features
----

- [Markdown (including footnotes support) for editing, HTML for display](https://code.djangoproject.com/wiki/UsingMarkup).
- Links and original article note types published to the same content column.
- Dates on homepage are displayed only once for notes published on the same day. Using '[ifchanged](https://docs.djangoproject.com/en/dev/ref/templates/builtins/?from=olddocs#ifchanged)'.
- Code syntax highlighting in markup courtesy of [Pygments](http://pygments.org/) and [CodeHilite](http://freewisdom.org/projects/python-markdown/CodeHilite).
- Simple search.
- Uses Django admin interface.
- Combine [django-medusa](https://github.com/mtigas/django-medusa/) with this application so we are serving static HTML files from disk on server and Markdown and HTML columns in database.

## TODO

- Learn how to [write tests](http://www.tdd-django-tutorial.com/) for views, then write unit and functional tests.
- Articles available in Markdown format on the server (article-title.txt).
- JavaScript-based search for static files on server.
- Set up [Fabric](http://docs.fabfile.org/en/1.6/tutorial.html) script for deployment to github-powered site, maybe also github pages.
- [Automatically post new articles to Twitter](http://djangosnippets.org/snippets/1339/).
- [SSL](https://www.tbray.org/ongoing/When/201x/2012/12/02/HTTPS).
