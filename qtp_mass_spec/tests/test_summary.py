# -----------------------------------------------------------------------------
# Copyright (c) 2017, Qiita development team.
#
# Distributed under the terms of the BSD 3-clause License License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from unittest import main
from tempfile import mkstemp, mkdtemp
from os import remove, environ, close
from os.path import exists, isdir
from shutil import rmtree, copyfile
from json import dumps

from qiita_client.testing import PluginTestCase

from qtp_mass_spec import generate_html_summary
import time

class SummaryTestsWith(PluginTestCase):
    def setUp(self):
        self.out_dir = mkdtemp()
        self._clean_up_files = [self.out_dir]
        time.sleep(1)

    def tearDown(self):
        for fp in self._clean_up_files:
            if exists(fp):
                if isdir(fp):
                    rmtree(fp)
                else:
                    remove(fp)

    def _create_job(self, atype, files):
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

        aid = self._create_artifact()

        parameters = {'input_data' : aid}
        data = {'command': dumps(['Mass Spec Types type', '0.0.1', 'Generate HTML summary']),
                'parameters': dumps(parameters), 'status': 'running'}
        job_id = self.qclient.post(
            '/apitest/processing_job/', data=data)['job']
        return job_id, parameters

    def _create_artifact(self):
        fd, fp = mkstemp(suffix='.mzXML')
        close(fd)
        copyfile('support_files/112111_ES129_fr111109_jy_ft_ltq.mzXML', fp)
        prep_info_dict = {
            'SKB7.640196': {'description_prep': 'SKB7'}
        }
        data = {'prep_info': dumps(prep_info_dict),
                # magic #1 = testing study
                'study': 1,
                'data_type': 'Metabolomic'}
        pid = self.qclient.post('/apitest/prep_template/', data=data)['prep']

        # inserting artifacts
        data = {
            'filepaths': dumps([(fp, 'plain_text')]),
            'type': "mzxml",
            'name': "Spectra Collection",
            'prep': pid}
        aid = self.qclient.post('/apitest/artifact/', data=data)['artifact']
        return aid

    def test_generate_html_summary(self):
        # TODO: fill the following variables to create the job in the Qiita
        # test server
        #artifact = self._create_artifact()
        job_id, parameters = self._create_job("mzxml", {'plain_text': "support_files/112111_ES129_fr111109_jy_ft_ltq.mzXML"} )

        #obs_success, obs_ainfo, obs_error = generate_html_summary(
        #    self.qclient, job_id, parameters, self.out_dir)

        # asserting reply
        #self.assertTrue(obs_success)
        #self.assertIsNone(obs_ainfo)
        #self.assertEqual(obs_error, "")

        # asserting content of html
        #res = self.qclient.get("/qiita_db/artifacts/%s/" % artifact)
        #html_fp = res['files']['html_summary'][0]
        #self._clean_up_files.append(html_fp)

        #with open(html_fp) as html_f:
        #    html = html_f.read()
        #self.assertEqual(html, '\n'.join(EXP_HTML))

    # TODO: Write any other tests needed to get your coverage as close as
    # possible to 100%!!

EXP_HTML = """TODO: write your expected HTML result here"""

if __name__ == '__main__':
    main()
