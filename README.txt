===== Code structure =====
*   Code base is organised into Components
*   Each Compinent has an API and an Implementation
*   An API for a Component X is a top-level module <X>.py.
    Component API naves are short all-lowercase identifiers
*   Component X implementation files are under a package
    <X>_impl. In there the'll normally be be one module per
    class named <ClassName>.py.

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
*   Uses Epytext - style docstrings
*   """...""" is for docstrings, "..." is for non-localisable strings,
    '...' is for localisable strings; the latter shall eventually be
    fetched from various resource factories.
