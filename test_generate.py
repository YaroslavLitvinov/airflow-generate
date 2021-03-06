import generate
from crontab import CronTab


def test_remove_user_from_command():
    test_cases = [
        ('{{ acumen_pipeline_runtime_user }} {{ acumen_cron_scripts_dir }}/\
 cron-clickstream-schema-load.sh', '{{ acumen_cron_scripts_dir }}/\
 cron-clickstream-schema-load.sh'),
        ('root {{ acumen_cron_scripts_dir }}/cron-jt-status.sh',
         '{{ acumen_cron_scripts_dir }}/cron-jt-status.sh')
    ]

    for input, result in test_cases:
        assert generate.remove_user_from_command(input) == result


def test_replace_template_variables():
    input, output = ('{{ acumen_cron_scripts_dir }}/cron-stacktach-load.{{ sh }}',
                     '\'sudo env PATH=$PATH su -c \"{acumen_cron_scripts_dir}/cron-stacktach-load.{sh}\" \
{user}\'.format(acumen_cron_scripts_dir=task_config[\'acumen_cron_scripts_dir\'],\
 sh=task_config[\'sh\'], user=task_config[\'user\'])')

    assert (generate.replace_template_variables(input)[0]
            == output)

    assert (generate.replace_template_variables(input)[1]
            == ['acumen_cron_scripts_dir', 'sh', 'user'])


def test_task_name():
    test_cases = [
        ('{{ acumen_pipeline_runtime_user }}\
 {{ acumen_cron_scripts_dir }}/cron-stacktach-load.sh',
         'cron_stacktach_load')
    ]

    for input, output in test_cases:
        assert generate.task_name(input) == output


def test_wrap_command():
    assert generate.wrap_command('/usr/bin/run', []) == (
        'sudo env PATH=$PATH su -c \"/usr/bin/run\" {user}', ['user']
    )


def test_job_start_time():
    cron = CronTab(tab="*/1 * * * * root {{ acumen_cron_scripts_dir }}/cron-jt-status.sh")
    assert generate.job_start_time(cron[0]) == ('0', '0')

    cron = CronTab(tab="18 21 * * * root {{ acumen_cron_scripts_dir }}/cron-jt-status.sh")
    assert generate.job_start_time(cron[0]) == ('21', '18')


def test_job_delta_time():
    cron = CronTab(tab="*/1 * * * * root {{ acumen_cron_scripts_dir }}/cron-jt-status.sh")
    assert generate.job_delta_time(cron[0]) == ('0', '0', '5')

    cron = CronTab(tab="18 21 * * * root {{ acumen_cron_scripts_dir }}/cron-jt-status.sh")
    assert generate.job_delta_time(cron[0]) == ('1', '0', '0')
