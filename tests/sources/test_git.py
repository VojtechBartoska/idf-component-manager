from idf_component_tools import sources
from idf_component_tools.git_client import GitClient

COMMIT_ID = '38041fa9e7f8a79b8ff8cd247c73cf92b7e3c23a'


def test_validate_version_spec_git():
    source = sources.GitSource({'git': ''})
    assert source.validate_version_spec(None)
    assert source.validate_version_spec('*')
    assert source.validate_version_spec('feature/new_test_branch')
    assert source.validate_version_spec('test_branch')
    assert source.validate_version_spec(COMMIT_ID)
    assert not source.validate_version_spec('..non_valid_branch')
    assert not source.validate_version_spec('@{non_valid_too')
    assert not source.validate_version_spec('wrong\\slash')


def test_normalize_spec(monkeypatch):
    source = sources.GitSource({'git': ''})
    monkeypatch.setattr(sources.GitSource, '_checkout_git_source', lambda *_: COMMIT_ID)

    assert '*' == source.normalize_spec(None)
    assert COMMIT_ID == source.normalize_spec('*')


def test_checkout_git_source(monkeypatch):
    source = sources.GitSource({'git': ''})
    monkeypatch.setattr(GitClient, 'prepare_ref', lambda *args, **kwargs: COMMIT_ID)

    assert COMMIT_ID == source._checkout_git_source('*')
