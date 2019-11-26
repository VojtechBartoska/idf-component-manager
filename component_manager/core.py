"""Core module of component manager"""
from __future__ import print_function

import os
from typing import List, Union

from .component_sources.base import BaseSource
from .component_sources.fetcher import ComponentFetcher
from .lock.manager import LockManager
from .manifest_builder import ManifestBuilder
from .manifest_pipeline import ManifestParser
from .version_solver.version_solver import VersionSolver
from .version_solver.solver_result import SolverResult


class ComponentManager(object):
    def __init__(
            self, path, lock_path=None, manifest_path=None,
            sources=None):  # type: (str, Union[None, str], Union[None, str], List[BaseSource]) -> None
        # Working directory
        self.path = path if os.path.isdir(path) else os.path.dirname(path)

        # Set path of manifest file for the project
        self.manifest_path = manifest_path or (os.path.join(path, 'idf_project.yml') if os.path.isdir(path) else path)

        # Lock path
        self.lock_path = lock_path or (os.path.join(path, 'dependencies.lock') if os.path.isdir(path) else path)

        # Components directory
        self.components_path = os.path.join(self.path, 'managed_components')

    def install(self, components=None):
        parser = ManifestParser(self.manifest_path).prepare()
        manifest = ManifestBuilder(parser.manifest_tree).build()
        lock_manager = LockManager(self.lock_path)
        lock = lock_manager.load()
        solution = SolverResult.from_yaml(manifest, lock)

        if manifest.manifest_hash != lock['manifest_hash']:
            print('Updating lock file at %s' % self.lock_path)
            solver = VersionSolver(manifest, lock)
            solution = solver.solve()
            lock_manager.dump(solution.as_ordered_dict())

        # Download components
        if not solution.solved_components:
            return solution

        components_count = len(solution.solved_components)
        count_string = 'dependencies' if components_count != 1 else 'dependency'
        print('Processing %s %s' % (components_count, count_string))
        line_len = 0
        for i, component in enumerate(solution.solved_components):
            # Check hash if hash present and download component if necessary
            line = ('[%d/%d] Processing component %s' % (i + 1, components_count, component.name)).rjust(line_len, ' ')
            line_len = len(line)
            print(line, end='\r')
            ComponentFetcher(component, self.components_path).download()

        print('Successfully processed %s %s ' % (components_count, count_string))
        return solution

    def eject(self, components=None):
        print('Ejecting %s' % ', '.join(components))
        print('Not implemented yet')
