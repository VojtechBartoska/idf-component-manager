"""Classes to work with manifest file"""
from typing import List, Union

from semantic_version import Version


class Manifest(object):
    def __init__(
            self,
            name=None,  # type: Union[str, None]
            version=None,  # type: Union[str, None]
            maintainers=None,  # type: Union[str, None]
            dependencies=None,  # type: Union[List[ComponentRequirement], None]
            url=None,  # type: Union[str, None]
            manifest_hash=None  # type: Union[str, None]
    ):
        # type: (...) -> None
        self.name = str(name)
        self.version = version
        self.maintainers = maintainers
        if dependencies is None:
            dependencies = []
        self.dependencies = dependencies
        self.url = url
        self.manifest_hash = manifest_hash


class ComponentRequirement(object):
    def __init__(self, name, source, versions=None, version_spec='*'):
        self.version_spec = version_spec
        self.source = source
        self.name = name


class ComponentVersion(object):
    def __init__(self, version, url_or_path=None, component_hash=None):
        self.component_hash = component_hash
        self.version = version if isinstance(version, Version) else Version(version)
        self.url_or_path = url_or_path

    def __str__(self):
        return str(self.version)


class ComponentWithVersions(object):
    def __init__(self, name, versions):
        self.versions = versions
        self.name = name
