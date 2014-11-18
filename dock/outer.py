"""

"""
import json
import os
import shutil
import tempfile

from dock import CONTAINER_SHARE_PATH, BUILD_JSON, CONTAINER_RESULTS_JSON_PATH, RESULTS_JSON, BUILD_LOG
from dock.core import DockerTasker


class PrivilegedDockerBuilder(object):
    def __init__(self, build_image_id, build_args):
        self.build_image_id = build_image_id
        self.build_args = build_args
        self.temp_dir = None

    def build(self):
        """
        build image from provided build_args

        :return:
        """
        self.temp_dir = tempfile.mkdtemp()
        try:
            with open(os.path.join(self.temp_dir, BUILD_JSON), 'w') as build_json:
                json.dump(self.build_args, build_json)
            dt = DockerTasker()
            if not dt.image_exists(self.build_image_id):
                raise RuntimeError("Image '%s' does not exist! " % self.build_image_id,
                                   "You have to create it prior to build, "
                                   "see README of dock project.")
            container_id = dt.run(
                self.build_image_id,
                create_kwargs={'volumes': [self.temp_dir]},
                start_kwargs={'binds': {self.temp_dir: {'bind': CONTAINER_SHARE_PATH, 'rw': True}},
                              'privileged': True}
            )
            dt.wait(container_id)
            return self.load_results(container_id)
        finally:
            shutil.rmtree(self.temp_dir)

    def load_results(self,container_id):
        """

        :return:
        """
        if self.temp_dir:
            dt = DockerTasker()
            results_path = os.path.join(self.temp_dir, RESULTS_JSON)
            build_log_path = os.path.join(self.temp_dir, BUILD_LOG)
            df_path = os.path.join(self.temp_dir, 'Dockerfile')
            # FIXME: race
            if not os.path.isfile(results_path):
                return None
            with open(results_path, 'r') as results_fp:
                results = json.load(results_fp)
            df = open(df_path, 'r').read()
            build_log = open(build_log_path, 'w').write(dt.get_build_log(container_id))
            return results, df, build_log
