import os
import sys

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "src")
)

from resource_manager import (
    resource_path,
    font_resource,
    image_resource,
    sound_resource,
)


def test_resouce_manager() -> None:
    resouce_base_path = os.path.join(os.path.abspath("."), "res")
    font_base_path = os.path.join(resouce_base_path, "font")
    image_base_path = os.path.join(resouce_base_path, "img")
    sound_base_path = os.path.join(resouce_base_path, "sound")
    test_file_name = "testname.ext"
    if resource_path(test_file_name) != os.path.join(resouce_base_path, test_file_name):
        assert False
        pass
    if font_resource(test_file_name) != os.path.join(font_base_path, test_file_name):
        assert False
        pass
    if image_resource(test_file_name) != os.path.join(image_base_path, test_file_name):
        assert False
        pass
    if sound_resource(test_file_name) != os.path.join(sound_base_path, test_file_name):
        assert False
        pass
    assert True
    return None
