# **ltp-ci**

A CI/CD pipeline for automated running and reporting on the [Linux Test Project (LTP)](https://github.com/linux-test-project/ltp). ltp-ci is designed to run LTP on a remote machine, collect results, and publish an HTML report from Allure while maintaining a history of previous test runs.

## 📁 Pipeline structure

The pipeline consists of three stages:

1. **run_ltp** — running LTP tests on a remote machine, copying `results.json` and cleaning up old `results.json`
2. **report** — copying `results.json`, `ltp_to_allure.py`, `generate_allure.sh` to the web server. Converting `results.json` to `allure-results` and generating it into an `allure-report` with the history of previous test runs saved.
3. **cleaning** — cleaning up temporary files and scripts on the web server

## ⚙️ Dependencies

On remote machines (`LTP_HOST` and `WEB_HOST`):
- Create a user `LTP_USER` and add it to the sudo group.
- Configure sudo for `LTP_USER` without a password (NOPASSWD).
- Create a `.ssh directory` for `LTP_USER` and add the `GitLab Runner` public key to `authorized_keys`.
- Grant access:
- sudo mkdir -p /home/LTP_USER/.ssh 
- sudo touch /home/LTP_USER/.ssh/authorized_keys 
- sudo chmod 700 /home/LTP_USER/.ssh 
- sudo chmod 600 /home/LTP_USER/.ssh/authorized_keys 
- sudo chown -R LTP_USER:LTP_USER /home/LTP_USER/.ssh

On the `LTP_HOST` machine:
- Must have ssh and scp python3
and LTP and kirk installed in /opt/ltp [Installation](https://linux-test-project.readthedocs.io/en/latest/users/quick_start.html).
- `LTP_USER` must have permission to run /opt/ltp/kirk
- Change permissions on /tmp/kirk.LTP_USER and change owner, results.json is created there and `LTP_USER` must have read access to it.

On the machine with `GitLab Runner`:
- Make sure that the user under which the runner runs has a private SSH key, and its public part is copied to remote machines.

On the `WEB_HOST` machine:
- Must have ssh and scp, python3 and also allure installed in /opt/allure
`LTP_USER` must have full access and be the owner of /opt/allure/allure-report and all files and directories in it.

📄 License

The project is distributed under the [MIT](LICENSE).