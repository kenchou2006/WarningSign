#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "無法啟動Django"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()