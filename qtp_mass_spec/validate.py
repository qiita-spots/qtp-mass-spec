# -----------------------------------------------------------------------------
# Copyright (c) 2016, Ming Wang.
#
# Distributed under the terms of the BSD 3-clause License License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from json import loads

from qiita_client import ArtifactInfo


def validate(qclient, job_id, parameters, out_dir):
    """Validate and fix a new artifact

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
    bool, list of qiita_client.ArtifactInfo, str
        Whether the job is successful
        The artifact information, if successful
        The error message, if not successful
    """
    # Step 1: Gather information from Qiita
    qclient.update_job_step(job_id, "Step 1: Collecting information")
    # These are the 3 parameters provided by Qiita:
    # - prep_id: An integer with the prep information id
    # - files: A dictionary of the format {str: list of str}, in which keys
    #          are the filepath type and values a list of filepaths
    # - a_type: A string with the artifact type to be validated
    # From here, the developer should be able to gather any further information
    # needed to validate the files
    prep_id = parameters['template']
    files = loads(parameters['files'])
    a_type = parameters['artifact_type']
    # You may/may not need the prep information contents. If you need it,
    # uncomment the line below. Prep info is a dictionary with the following
    # format: {sample_id: {column_name: column_value}}
    # prep_info = qclient.get(
    #     "/qiita_db/prep_template/%s/data/" % prep_id)['data']

    qclient.update_job_step(job_id, "Step 2: Validating files")
    # TODO: Validate if the files provided by Qiita generate a valid
    # artifact of type "a_type"

    qclient.update_job_step(job_id, "Step 3: Fixing files")
    # TODO: If the files are not creating a valid artifact but they can be
    # corrected, correct them here

    # TODO: fill filepaths with a list of tuples with (filepath, filepath type)
    filepaths = []
    return True, [ArtifactInfo(None, a_type, filepaths)], ""
