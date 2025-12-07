# Postgres Migration Failure - Dec 5th 2025

## Raw log

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
Traceback (most recent call last):
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 103, in _execute
    return self.cursor.execute(sql)
           ~~~~~~~~~~~~~~~~~~~^^^^^
psycopg2.errors.InsufficientPrivilege: permission denied for schema public
LINE 1: CREATE TABLE "django_migrations" ("id" bigint NOT NULL PRIMA...
                     ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/db/migrations/recorder.py", line 78, in ensure_schema
    editor.create_model(self.Migration)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/db/backends/base/schema.py", line 513, in create_model
    self.execute(sql, params or None)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/db/backends/postgresql/schema.py", line 45, in execute
    return super().execute(sql, params)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/db/backends/base/schema.py", line 205, in execute
    cursor.execute(sql, params)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sql, params, many=False, executor=self._execute
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/db/utils.py", line 94, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 103, in _execute
    return self.cursor.execute(sql)
           ~~~~~~~~~~~~~~~~~~~^^^^^
django.db.utils.ProgrammingError: permission denied for schema public
LINE 1: CREATE TABLE "django_migrations" ("id" bigint NOT NULL PRIMA...
                     ^


During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/suhasg/Projects/task-habit-board/manage.py", line 22, in <module>
    main()
    ~~~~^^
  File "/Users/suhasg/Projects/task-habit-board/manage.py", line 18, in main
    execute_from_command_line(sys.argv)
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/core/management/__init__.py", line 443, in execute_from_command_line
    utility.execute()
    ~~~~~~~~~~~~~~~^^
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/core/management/__init__.py", line 437, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/core/management/base.py", line 416, in run_from_argv
    self.execute(*args, **cmd_options)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/core/management/base.py", line 460, in execute
    output = self.handle(*args, **options)
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/core/management/base.py", line 107, in wrapper
    res = handle_func(*args, **kwargs)
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/core/management/commands/migrate.py", line 354, in handle
    post_migrate_state = executor.migrate(
        targets,
    ...<3 lines>...
        fake_initial=fake_initial,
    )
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/db/migrations/executor.py", line 109, in migrate
    self.recorder.ensure_schema()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/Users/suhasg/Projects/task-habit-board/.venv/lib/python3.14/site-packages/django/db/migrations/recorder.py", line 80, in ensure_schema
    raise MigrationSchemaMissing(
        "Unable to create the django_migrations table (%s)" % exc
    )
django.db.migrations.exceptions.MigrationSchemaMissing: Unable to create the django_migrations table (permission denied for schema public
LINE 1: CREATE TABLE "django_migrations" ("id" bigint NOT NULL PRIMA...
                     ^
)
```

## Debugging Tree

> Error: 'InsufficientPrivilege' when running 'python3 manage.py migrate'
    > Check 1: Is the DB user correct in .env?
        -> Yes - DB_USER matches created postgres user
    > Check 2: Can the user connect to DB manually? 
        -> Yes - user can 'psql' manually
    > Check 3: Does the user own the public schema?
        X No - Schema owned by postgres user
            > Fix:
                ALTER SCHEMA public OWNER TO task_habit_user;
                GRANT ALL ON SCHEMA public TO task_habit_user;
    > Check 4: Retry Migrations
        -> Success - Migrations ran clearly.


## Final Fix Applied

```sql
ALTER SCHEMA public OWNER TO task_habit_user;
GRANT ALL ON SCHEMA public TO task_habit_user;
