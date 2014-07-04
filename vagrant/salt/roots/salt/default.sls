# -*- mode: yaml -*-

pager:
  alternatives.set:
    - name: pager
    - path: /usr/bin/most


screen:
  pkg:
    - latest


virtualenv-basedir:
  file.directory:
    - name: /var/lib/hubby
    - makedirs: True
    - group: vagrant
    - user: vagrant
    - mode: 2775


virtualenv-hubby:
  virtualenv.managed:
    - name: /var/lib/hubby/venv
    - system_site_packages: False
    - user: vagrant
    - requirements: salt://files/venv-reqs.txt
    - require:
      - file: virtualenv-basedir
