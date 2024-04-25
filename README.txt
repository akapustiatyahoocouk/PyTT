===== Code structure =====
*   Code base is organised into Components, then sub-Components, etc.

===== Naming =====
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
