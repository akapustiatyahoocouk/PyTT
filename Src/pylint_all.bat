c:\cygwin64\bin\find . -name __pycache__ | xargs rm -rf
c:\cygwin64\bin\find . -name "*.py" | xargs pylint --disable invalid-name --disable no-method-argument --disable abstract-method --disable wildcard-import --disable unused-wildcard-import --disable too-many-arguments --disable relative-beyond-top-level --disable fixme --disable too-many-ancestors --disable import-outside-toplevel --disable broad-exception-caught --disable duplicate-code --disable too-few-public-methods --disable too-many-instance-attributes --disable protected-access --disable too-many-locals --disable too-many-branches --disable too-many-statements --disable deprecated-decorator
