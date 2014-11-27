from glob import glob
import os

from dock.buildimage import BuildImageBuilder
from dock.core import DockerTasker


PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
TEST_BUILD_IMAGE = "test-build-image"


def test_tarball_generation_local_repo(tmpdir):
    b = BuildImageBuilder(dock_local_path=PARENT_DIR)
    tarball_path = b.get_dock_tarball_path(str(tmpdir))
    assert os.path.exists(tarball_path)
    assert len(glob(os.path.join(str(tmpdir), 'dock-*.tar.gz'))) == 1


def test_tarball_generation_upstream_repo(tmpdir):
    b = BuildImageBuilder(use_official_dock_git=True)
    tarball_path = b.get_dock_tarball_path(str(tmpdir))
    assert os.path.exists(tarball_path)
    assert len(glob(os.path.join(str(tmpdir), 'dock-*.tar.gz'))) == 1


def test_image_creation_upstream_repo():
    b = BuildImageBuilder(use_official_dock_git=True)
    df_dir_path = os.path.join(PARENT_DIR, 'images', 'privileged-builder')
    b.create_image(df_dir_path, TEST_BUILD_IMAGE)

    dt = DockerTasker()
    assert dt.image_exists(TEST_BUILD_IMAGE)
    dt.remove_image(TEST_BUILD_IMAGE)


def test_image_creation_local_repo():
    b = BuildImageBuilder(dock_local_path=PARENT_DIR)
    df_dir_path = os.path.join(PARENT_DIR, 'images', 'privileged-builder')
    b.create_image(df_dir_path, TEST_BUILD_IMAGE)

    dt = DockerTasker()
    assert dt.image_exists(TEST_BUILD_IMAGE)
    dt.remove_image(TEST_BUILD_IMAGE)