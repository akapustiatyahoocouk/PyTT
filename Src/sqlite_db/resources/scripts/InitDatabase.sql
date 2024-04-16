CREATE TABLE objects
(
    pk CHAR(36) NOT NULL PRIMARY KEY,       --  GUID XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    object_type_name VARCHAR(32) NOT NULL   --  e.g. "User", "PublicTask", etc. - type_name
);
