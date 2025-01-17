import os

from pytest import raises

from idf_component_manager.local_component_list import parse_component_list
from idf_component_tools.errors import ProcessingError


def test_parse_valid_component_list():
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'fixtures',
        'local_component_list',
        'valid.yml',
    )
    result = parse_component_list(path)
    assert len(result) == 4
    assert result[3]['name'] == 'bootloader'
    assert result[1]['path'].endswith('app_update')


def test_parse_broken_component_list():
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'fixtures',
        'local_component_list',
        'invalid.yml',
    )
    with raises(ProcessingError):
        parse_component_list(path)
