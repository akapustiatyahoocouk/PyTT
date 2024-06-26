CREATE TABLE [objects]
(
    [pk] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    [object_type_name] VARCHAR(32) NOT NULL   --  e.g. "User", "PublicTask", etc. - type_name
);

CREATE TABLE [users]
(
    [pk] INTEGER NOT NULL PRIMARY KEY,
    [enabled] CHAR(1) NOT NULL,         --  "Y" or "N"
    [real_name] VARCHAR(128) NOT NULL,
    [inactivity_timeout] INTEGER,       --  in minutes; NULL == none
    [ui_locale] VARCHAR(64),            --  "en_GB", etc; NULL == none
    [email_addresses] TEXT,             --  '\n' - separated list, NULL == none
    --- Foreign keys
    FOREIGN KEY([pk]) REFERENCES [objects]([pk])
);

CREATE TABLE [accounts]
(
    [pk] INTEGER NOT NULL PRIMARY KEY,
    [enabled] CHAR(1) NOT NULL,             --  "Y" (true) or "N" (false)
    [login] VARCHAR(128) NOT NULL UNIQUE,
    [password_hash] CHAR(40) NOT NULL,      --  SHA-1 uppercase hashstring
    --- Start of capability fields
    [is_administrator] CHAR(1) NOT NULL,        --  "Y" (true) or "N" (false)
    [can_manage_users] CHAR(1) NOT NULL,        --  "Y" (true) or "N" (false)
    [can_manage_stock_items] CHAR(1) NOT NULL,  --  "Y" (true) or "N" (false)
    [can_manage_beneficiaries] CHAR(1) NOT NULL,--  "Y" (true) or "N" (false)
    [can_manage_workloads] CHAR(1) NOT NULL,    --  "Y" (true) or "N" (false)
    [can_manage_public_activities] CHAR(1) NOT NULL,      --  "Y" (true) or "N" (false)
    [can_manage_public_tasks] CHAR(1) NOT NULL,    --  "Y" (true) or "N" (false)
    [can_manage_private_activities] CHAR(1) NOT NULL,      --  "Y" (true) or "N" (false)
    [can_manage_private_tasks] CHAR(1) NOT NULL,--  "Y" (true) or "N" (false)
    [can_log_work] CHAR(1) NOT NULL,            --  "Y" (true) or "N" (false)
    [can_log_events] CHAR(1) NOT NULL,          --  "Y" (true) or "N" (false)
    [can_generate_reports] CHAR(1) NOT NULL,    --  "Y" (true) or "N" (false)
    [can_backup_and_restore] CHAR(1) NOT NULL,  --  "Y" (true) or "N" (false)
    --- End of capability fields
    [email_addresses] TEXT,                     --  '\n' - separated list, NULL == none
    [fk_user] INTEGER NOT NULL,
    --- Foreign keys
    FOREIGN KEY([pk]) REFERENCES [objects]([pk]),
    FOREIGN KEY([fk_user]) REFERENCES [users]([pk])
);

CREATE TABLE [activity_types]
(
    [pk] INTEGER NOT NULL PRIMARY KEY,
    [name] VARCHAR(128) NOT NULL UNIQUE,
    [description] TEXT NOT NULL,
    --- Foreign keys
    FOREIGN KEY([pk]) REFERENCES [objects]([pk])
);

CREATE TABLE [activities]
(
    [pk] INTEGER NOT NULL PRIMARY KEY,
    [name] VARCHAR(128) NOT NULL,
    [description] TEXT NOT NULL,
    [timeout] INTEGER,                              --  in minutes; NULL == none
    [require_comment_on_start] CHAR(1) NOT NULL,    --  "Y" or "N"
    [require_comment_on_finish] CHAR(1) NOT NULL,   --  "Y" or "N"
    [full_screen_reminder] CHAR(1) NOT NULL,        --  "Y" or "N"
    [fk_activity_type] INTEGER,                     --  NULL == no link
    [completed] CHAR(1),                            --  "Y" or "N", NULL == activity, not task
    [fk_owner] INTEGER,                             --  NULL == public, else private
    [fk_parent_task] INTEGER,                       --  NULL == activity or root task, else != NULL
    UNIQUE([name], [fk_owner]) ON CONFLICT ABORT,
    UNIQUE([name], [fk_parent_task]) ON CONFLICT ABORT,
    --- Foreign keys
    FOREIGN KEY([pk]) REFERENCES [objects]([pk]),
    FOREIGN KEY([fk_activity_type]) REFERENCES [activity_types]([pk]),
    FOREIGN KEY([fk_owner]) REFERENCES [users]([pk]),
    FOREIGN KEY([fk_parent_task]) REFERENCES [activities]([pk])
);
