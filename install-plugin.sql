-- Add the plugin

INSERT INTO qiita.software (name, version, description, environment_script, start_script, software_type_id)
    VALUES ('QTP-MASS-SPEC', '0.0.1', 'Mass spec types', 'workon qtp-mass-spec', 'start_qtp_mass_spec', 2);

-- Add the commands
INSERT INTO qiita.software_command (software_id, name, description) VALUES
    (4, 'Validate', 'Validates a new artifact'),
    (4, 'Generate HTML summary', 'Generates the HTML summary');

-- Add the parameters
INSERT INTO qiita.command_parameter (command_id, parameter_name, parameter_type, required)
    VALUES (8, 'template', 'prep_template', True),
           (8, 'files', 'string', True),
           (8, 'artifact_type', 'string', True),
           (9, 'input_data', 'artifact', True);

-- Add the new filepath type (ID: 22)
-- Some are XML, other are new line separated
INSERT INTO qiita.filepath_type (filepath_type) VALUES ('open_format_mass_spec');

-- Add the new artifact type (ID: 8)
INSERT INTO qiita.artifact_type (artifact_type, description, can_be_submitted_to_ebi, can_be_submitted_to_vamps)
    VALUES ('Mass Spec Peak', 'Mass Spec Peak', false, false);

-- Link the files and type
INSERT INTO qiita.artifact_type_filepath_type (artifact_type_id, filepath_type_id, required)
    VALUES (8, 22, True);

-- Link the parameter type with the artifact type
INSERT INTO qiita.parameter_artifact_type (command_parameter_id, artifact_type_id)
    VALUES (43, 8);

INSERT INTO qiita.oauth_software (client_id, software_id)
    VALUES ('4MOBzUBHBtUmwhaC258H7PS0rBBLyGQrVxGPgc9g305bvVhf6h', 4);
