import structlog
from uptainer.git import Git

log = structlog.get_logger()

def test_git_createworkdir():
    git_obj = Git(log=log, remote_url="git@github.com:Mirio/verbacap.git", branch="main", ssh_private_key="id_rsa")
    check = git_obj.create_workdir()
    assert check.startswith("/tmp")

def test_git_clone_repo():
    git_obj = Git(log=log, remote_url="git@github.com:Mirio/verbacap.git", branch="nonexists", ssh_private_key="id_rsa")
    git_obj.create_workdir()
    check = git_obj.clone_repo()
    assert check["error"] == True

    git_obj = Git(log=log, remote_url="git@github.com:Mirio/verbacap.git", branch="main", ssh_private_key="id_rsa")
    git_obj.create_workdir()
    check = git_obj.clone_repo()
    assert check["error"] == False

    git_obj = Git(log=log, remote_url="https://github.com/Mirio/verbacap.git", branch="main", ssh_private_key="id_rsa")
    git_obj.create_workdir()
    check = git_obj.clone_repo()
    assert check["error"] == True