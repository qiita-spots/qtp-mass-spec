# -----------------------------------------------------------------------------
# Copyright (c) 2016, Ming Wang.
#
# Distributed under the terms of the BSD 3-clause License License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from unittest import TestCase, main
from tempfile import mkdtemp
from os import remove, environ
from os.path import exists, isdir
from shutil import rmtree
from json import dumps

from qiita_client import QiitaClient, ArtifactInfo

from qtp_mass_spec.validate import validate

CLIENT_ID = '19ndkO3oMKsoChjVVWluF7QkxHRfYhTKSFbAVt8IhK7gZgDaO4'
CLIENT_SECRET = ('J7FfQ7CQdOxuKhQAf1eoGgBAE81Ns8Gu3EKaWFm3IO2JKh'
                 'AmmCWZuabe0O5Mp28s1')


class CreateTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the Qiita Client
        server_cert = environ.get('QIITA_SERVER_CERT', None)
        cls.qclient = QiitaClient("https://localhost:21174", CLIENT_ID,
                                  CLIENT_SECRET, server_cert=server_cert)

    @classmethod
    def tearDownClass(cls):
        # Reset the test database
        cls.qclient.post("/apitest/reset/")

    def setUp(self):
        self.out_dir = mkdtemp()
        self._clean_up_files = [self.out_dir]

    def tearDown(self):
        for fp in self._clean_up_files:
            if exists(fp):
                if isdir(fp):
                    rmtree(fp)
                else:
                    remove(fp)

    def _create_job(self, artifact_type, files, command, template=1):
        """Creates a new job in Qiita so we can update its step during tests

        Parameters
        ----------
        artifact_type: str
            The artifact type
        files: dict of {str: list of str}
            The files to be validated, keyed by filepath type
        command: int
            Qiita's command id for the 'validate' operation
        template: int, optional
            The template id to which the artifact will be added

        Returns
        -------
        str, dict
            The job id and the parameters dictionary
        """
        # Create a new job
        parameters = {'template': template,
                      'files': dumps(files),
                      'artifact_type': artifact_type}
        data = {'command': command,
                'parameters': dumps(parameters),
                'status': 'running'}
        res = self.qclient.post('/apitest/processing_job/', data=data)
        job_id = res['job']

        return job_id, parameters

    def test_validate(self):
        # TODO: fill the following variables to create the job in the Qiita
        # test server
        artifact_type = "TODO"
        files = {"TODO": ["TODO"]}
        command = "TODO"
        template = "TODO"
        job_id, parameters = self._create_job(
            artifact_type, files, command, template)
        obs_success, obs_ainfo, obs_error = validate(
            self.qclient, job_id, parameters, self.out_dir)

        self.assertTrue(obs_success)
        # TODO: Fill filepaths with the expected filepath list and provide
        # the expected artifact type
        filepaths = [("TODO", "TODO")]
        exp_ainfo = [ArtifactInfo(None, 'TODO: artifact type', filepaths)]
        self.assertEqual(obs_ainfo, exp_ainfo)
        self.assertEqual(obs_error, "")

    # TODO: Write any other tests needed to get your coverage as close as
    # possible to 100%!!

if __name__ == '__main__':
    main()
