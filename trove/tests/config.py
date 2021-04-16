[DEFAULT]
code_dir = ./tests/example
data_dir = ./tests/data
processed_data_dir = ${data_dir}
figure_dir = ./tests/figures

[SCRIPTS]
# Code will be run in order from lowest to highest number
s001 = ${code_dir}/pre.py
s002 = ${code_dir}/main.py
s003 = ${code_dir}/post.py

[PARAMETERS]

    [identifier_A]
    

    [this_is_also_an_identifier]
