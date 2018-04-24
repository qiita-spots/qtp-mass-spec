# -----------------------------------------------------------------------------
# Copyright (c) 2017, Qiita development team.
#
# Distributed under the terms of the BSD 3-clause License License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------


from os.path import join
import xmltodict

def generate_html_summary(qclient, job_id, parameters, out_dir):
    """Generates the HTML summary of an artifact

    Parameters
    ----------
    qclient : qiita_client.QiitaClient
        The Qiita server client
    job_id : str
        The job id
    parameters : dict
        The parameter values to validate and create the artifact
    out_dir : str
        The path to the job's output directory

    Returns
    -------
    bool, None, str
        Whether the job is successful
        Ignored
        The error message, if not successful
    """
    # Step 1: gather file information from qiita using REST api
    qclient.update_job_step(job_id, "Step 1: Gathering information from Qiita")
    # This is the only parameter provided by Qiita: the artifact id. From here,
    # the developer should be able to retrieve any further information needed
    # to generate the HTML summary
    artifact_id = parameters['input_data']
    qclient_url = "/qiita_db/artifacts/%s/" % artifact_id
    artifact_info = qclient.get(qclient_url)
    # Get the artifact files
    artifact_files = artifact_info['files']
    print(artifact_files["plain_text"])
    for filename in artifact_files["plain_text"]:
        file_status = ""
        try:
            parsed_dict = xmltodict.parse(open(filename).read())
            file_status = "Number of Spectra: %s" % ("1") 
        except:
            file_status = "Invalid XML"

    # Step 2: generate HTML summary
    # TODO: Generate the HTML summary and store it in html_summary_fp
    qclient.update_job_step(job_id, "Step 2: Generating HTML summary")
    html_summary_fp = join(out_dir, "summary.html")

    summary_output = open(html_summary_fp, "w")
    

    # Step 3: add the new file to the artifact using REST api
    qclient.update_job_step(job_id, "Step 3: Transferring summary to Qiita")
    success = True
    error_msg = ""
    try:
        qclient.patch(qclient_url, 'add', '/html_summary/',
                      value=html_summary_fp)
    except Exception as e:
        success = False
        error_msg = str(e)

    return success, None, error_msg
