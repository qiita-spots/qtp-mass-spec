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

from qiita_client import QiitaClient

from qtp_mass_spec import generate_html_summary


CLIENT_ID = '19ndkO3oMKsoChjVVWluF7QkxHRfYhTKSFbAVt8IhK7gZgDaO4'
CLIENT_SECRET = ('J7FfQ7CQdOxuKhQAf1eoGgBAE81Ns8Gu3EKaWFm3IO2JKh'
                 'AmmCWZuabe0O5Mp28s1')


class SummaryTestsWith(TestCase):
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

    def _create_job(self, artifact, command):
        """Creates a new job in Qiita so we can update its step during tests

        Parameters
        ----------
        artifact: int
            The artifact id to be validated during tests
        command: int
            Qiita's command id for the 'Generate HTML summary' operation

        Returns
        -------
        str, dict
            The job id and the parameters dictionary
        """
        # Create a new job
        parameters = {'input_data': artifact}
        data = {'command': command,
                'parameters': dumps(parameters),
                'status': 'running'}
        res = self.qclient.post('/apitest/processing_job/', data=data)
        job_id = res['job']

        return job_id, parameters

    def test_generate_html_summary(self):
        # TODO: fill the following variables to create the job in the Qiita
        # test server
        artifact = "TODO"
        command = "TODO"
        job_id, parameters = self._create_job(artifact, command)

        obs_success, obs_ainfo, obs_error = generate_html_summary(
            self.qclient, job_id, parameters, self.out_dir)

        # asserting reply
        self.assertTrue(obs_success)
        self.assertIsNone(obs_ainfo)
        self.assertEqual(obs_error, "")

        # asserting content of html
        res = self.qclient.get("/qiita_db/artifacts/%s/" % artifact)
        html_fp = res['files']['html_summary'][0]
        self._clean_up_files.append(html_fp)

        with open(html_fp) as html_f:
            html = html_f.read()
        self.assertEqual(html, '\n'.join(EXP_HTML))

    # TODO: Write any other tests needed to get your coverage as close as
    # possible to 100%!!

EXP_HTML = """TODO: write your expected HTML result here"""

if __name__ == '__main__':
    main()
