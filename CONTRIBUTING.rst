============
Contributing
============

Contributions are welcome, and they are greatly appreciated! You can
contribute in many ways.

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/EarthScope/nrl-lib/issues.

If you are reporting a bug, please include:

* Your operating system name and version
* Your hardware architecture (ARM/X86)
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

NRL could always use more documentation, whether as part of the
official NRL docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/EarthScope/nrl-lib/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Make sure that the feature can fit within the scope of the project

Get Started!
------------

Ready to contribute? Here's how to set up `NRL` for local development.

1. Clone the `NRL` repo:

 * $ git clone git@github.com:EarthScope/nrl-lib.git

2. Install your local copy:

 * $ pip install -e .[dev]

3. Create a branch for local development:

 * $ git checkout -b name-of-your-bugfix-or-feature

 Now you can make your changes locally.

4. When you're done making changes, check that your changes pass the
   tests:

 * $ python -m unittest

5. Commit your changes and push your branch to GitHub:

 * $ git add .
 * $ git commit -m "Your detailed description of your changes."
 * $ git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.md.
3. The pull request should work for Python 3.11, 3.12, 3.13 and 3.14.
   GitHub Actions runs the checks automatically on each pull request.

Tips
----

To run a subset of tests, for the catalog query module for example, run:
  * $ python -m unittest tests.test_catalog_query

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are merged into ``main``, with the new version
set in ``nrl/__init__.py`` and an entry in HISTORY.rst. Then tag the release
and push the tag:

* $ git tag vX.Y.Z
* $ git push origin vX.Y.Z

Pushing the tag runs the "Publish to PyPI" GitHub Actions workflow, which
builds the package and uploads it to PyPI. The tag must match the version in
``nrl/__init__.py``, or the workflow stops before uploading.
