# hypertexthero.com

Features
----

- [Markdown (including footnotes support) for editing, HTML for display](https://code.djangoproject.com/wiki/UsingMarkup).
- Dates on homepage are displayed only once for notes published on the same day. Using '[ifchanged](https://docs.djangoproject.com/en/dev/ref/templates/builtins/?from=olddocs#ifchanged).'
- Links and original article note types published to the same content column.
- Code syntax highlighting in markup courtesy of [Pygments](http://pygments.org/) and [CodeHilite](http://freewisdom.org/projects/python-markdown/CodeHilite).
- Simple search
- Simple interface (in progress).


## TODO

- Combine django-staticgenerator or django-medusa with this application so we are serving static files in HTML on server and Markdown and HTML columns in database. Also try to find a way to have static files in Markdown format on the server.
- Keywords/tags for posts