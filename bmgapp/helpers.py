# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import os
import sys
import contextlib


@contextlib.contextmanager
def to_file(where):
    sys.stdout = open(where, 'a')
    try:
        yield where
    finally:
        sys.stdout = sys.__stdout__


def get_list_of_files(directory, ext='', full_path=True):
    files = []
    for file_name in os.listdir(directory):
        if file_name.endswith(ext):
            file_path = os.path.join(directory, file_name) if full_path else file_name
            yield file_path


def get_only_files(directory, ext='', full_path=True):
    for file_name in os.listdir(directory):
        path = os.path.join(directory, file_name)
        if not os.path.isdir(path):
            if file_name.endswith(ext):
                yield path if full_path else file_name