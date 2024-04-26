===== Code structure =====
*   Code base is organised into Components, then sub-Components, etc.

===== Naming ===== TODO bring up-to-date
*   Component API modules are <all_lowercase>.py at a top level.
    These import implementation modules and declare type aliases.
*   Component C's implementation modules are <ClassName>.py under
    the package <C>_impl.
*   Class names use PascalCase.
*   Variables and functions use all_lowercase_with_underscores names.
*   Try to keep everything __private. For "protected" use _underscore
    naming.

===== Strings and docstrings =====
*   Uses Epytext - style docstrings.
*   """...""" is for docstrings, "..." is for non-localizable strings,
    '...' is for localizable strings; the latter shall eventually be
    fetched from various resource factories.

===== Module structure =====
*   Imports first (unless local imports are required within functions
    to obercome the circular-dependency issues). Organize imports into
    these consecutive sections:
    #   Python standard library
        (e.g. from typing import ...)
    #   Dependencies on other PyTT components
        (e.g. from util.interface.api import *)
    #   Internal dependencies on modules within the same component
        (e.g. from .<module> import <what>.
*   Then:
    ##########
    #   Public entities
    <declarations>
