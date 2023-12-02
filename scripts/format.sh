#!/bin/sh -e
set -x

ruff check gsoc2 tests --fix
black gsoc2 tests
isort gsoc2 tests
