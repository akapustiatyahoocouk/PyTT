c:\cygwin64\bin\find . -name __pycache__ | xargs rm -rf
c:\cygwin64\bin\find . -name "*.py" | xargs pylint --disable invalid-name --disable no-method-argument --disable abstract-method --disable wildcard-import --disable unused-wildcard-import --disable too-many-arguments
