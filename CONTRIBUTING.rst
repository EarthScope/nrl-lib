============
Contributing
============

Contributions are welcome, and they are greatly appreciated! You can
contribute in many ways.

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://git.passcal.nmt.edu/software_public/nrl/issues

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

Look through the GitLab issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

NRL could always use more documentation, whether as part of the
official NRL docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://git.passcal.nmt.edu/software_public/nrl/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Make sure that the feature can fit within the scope of the project

Get Started!
------------

Ready to contribute? Here's how to set up `NRL` for local development.

1. Clone the `NRL` repo:

 * $ git clone https://git.passcal.nmt.edu/software_public/nrl.git

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

6. Submit a merge request through the Gitlab website.

Pull Request Guidelines
-----------------------

Before you submit a merge request, check that it meets these guidelines:

1. The merge request should include tests.
2. If the merge request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.[9, 10, 11]

Tips
----

To run a subset of tests, for the nrl module for example, run:
  * $ python -m unittest tests/test_nrl.py

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run:

* $ git push
* $ git push --tags
