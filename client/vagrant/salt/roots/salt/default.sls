# -*- mode: yaml -*-

pager:
  alternatives.set:
    - name: pager
    - path: /usr/bin/most


screen:
  pkg:
    - latest

screen-config:
  file.managed:
    - name: /home/vagrant/.screenrc
    - source: salt://files/screenrc
    - group: vagrant
    - user: vagrant
    - mode: 644
    - require:
      - pkg: screen

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
