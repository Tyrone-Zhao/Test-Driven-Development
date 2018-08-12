from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random
import os

REPO_URL = "https://github.com/Tyrone-Zhao/Test-Driven-Development.git"


def deploy():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    source_folder = site_folder + "/source"
    _install_python_and_nginx()
    _install_nodejs_npm_and_phantomjs()
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _config_systemd_when_reboot_enable(source_folder, env.host)


def update():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    source_folder = site_folder + "/source"
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _update_systemd_when_reboot_enable(source_folder, env.host)


def _install_nodejs_npm_and_phantomjs():
    run("sudo apt-get install nodejs-legacy nodejs -y"
        " && sudo apt-get update -y"
        " && sudo apt-get install npm -y"
        " && sudo apt-get install phantomjs -y")


def _install_python_and_nginx():
    run("sudo add-apt-repository ppa:deadsnakes/ppa -y"
        " && sudo apt-get update -y"
        " && sudo apt-get install nginx git python3.6 python3.6-venv -y")


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ("database", "static", "virtualenv", "source"):
        run(f"mkdir -p {site_folder}/{subfolder}")


def _get_latest_source(source_folder):
    if exists(source_folder + "/.git"):
        run(f"cd {source_folder} && git fetch")
    else:
        run(f"git clone {REPO_URL} {source_folder}")
    # current_commit = local("git log -n 1 --format=%H", capture=True)
    # run(f"cd {source_folder} && git reset --hard {current_commit}")
    run("sudo locale-gen zh_CN.UTF-8")  # 解决ubuntu中文乱码问题
    run(f"sudo rm -rf {source_folder}/*"
        f" && cd {source_folder} && git reset --hard && git pull")


def _update_settings(source_folder, site_name):
    settings_path = source_folder + "/superlists/settings.py"
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        "ALLOWED_HOSTS = .+$",
        f'ALLOWED_HOSTS = ["{site_name}"]'
        )
    secret_key_file = source_folder + "/superlists/secret_key.py"
    if not exists(secret_key_file):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f"SECRET_KEY='{key}'")
    append(settings_path, "\nfrom .secret_key import SECRET_KEY")


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + "/../virtualenv"
    if not exists(virtualenv_folder + "/bin/pip"):
        run(f"python3.6 -m venv {virtualenv_folder}")
    run(f"{virtualenv_folder}/bin/pip "
        f"install -r {source_folder}/requirements.txt")


def _update_static_files(source_folder):
    run(
        f"cd {source_folder}"
        " && ../virtualenv/bin/python manage.py collectstatic --noinput"
    )


def _update_database(source_folder):
    run(
        f"cd {source_folder}"
        " && rm -rf ../database/db.sqlite3"
        " && ../virtualenv/bin/python manage.py migrate --noinput"
    )


def _config_systemd_when_reboot_enable(source_folder, site_name):
    run(
        f"cd {source_folder}"
        " && sudo rm -rf /etc/nginx/sites-available/tyrone-zhao.club"
        " && sudo rm -rf /etc/nginx/sites-enabled/tyrone-zhao.club"
        " && sudo rm -rf /etc/systemd/system/gunicorn-tyrone-zhao.club.service"
        f" && sed 's/SITENAME/{site_name}/g' deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/tyrone-zhao.club"
        " && sudo ln -s /etc/nginx/sites-available/tyrone-zhao.club /etc/nginx/sites-enabled/tyrone-zhao.club"
        f" && sed 's/SITENAME/{site_name}/g' deploy_tools/gunicorn-systemd.template.service | sudo tee /etc/systemd/system/gunicorn-tyrone-zhao.club.service"
        " && sudo systemctl daemon-reload"
        " && sudo systemctl reload nginx"
        " && sudo systemctl enable gunicorn-tyrone-zhao.club.service"
        " && sudo systemctl start gunicorn-tyrone-zhao.club.service "
        " && sudo systemctl restart gunicorn-tyrone-zhao.club.service "
    )


def _update_systemd_when_reboot_enable(source_folder, site_name):
    run(
        "sudo systemctl daemon-reload"
        " && sudo systemctl restart gunicorn-tyrone-zhao.club.service "
    )
