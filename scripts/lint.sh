#!/usr/bin/env bash

set -e
set -x

mypy gsoc2
ruff check gsoc2 tests
black gsoc2 tests --check
isort gsoc2 tests --check-only
