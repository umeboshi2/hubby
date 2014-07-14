# require config comes first
require.config
  baseUrl: 'client/apps/frontdoor'
  paths:
    jquery: '/client/bower_components/jquery/dist/jquery'
    #underscore: '/client/bower_components/underscore-amd/underscore'
    underscore: '/client/bower_components/lodash/dist/lodash.compat'
    backbone: '/client/bower_components/backbone/backbone'
    'backbone.wreqr': '/client/bower_components/backbone.wreqr/lib/amd/backbone.wreqr'
    'backbone.babysitter': '/client/bower_components/backbone.babysitter/lib/backbone.babysitter'
    marionette: '/client/bower_components/marionette/lib/core/amd/backbone.marionette'
    validation: '/client/bower_components/backbone.validation/dist/backbone-validation-amd'
    bootstrap: '/client/bower_components/bootstrap/dist/js/bootstrap'
    'jquery-ui': '/client/bower_components/jquery-ui/ui/jquery-ui'
    requirejs: '/client/bower_components/requirejs/require'
    text: '/client/bower_components/requirejs-text/text'
    teacup: '/client/bower_components/teacup/lib/teacup'
    ace: '/client/bower_components/ace-builds/src/ace'
    marked: '/client/bower_components/marked/lib/marked'
    
    common: '/client/apps/common'

    # FIXME: work with using bootstrap components
    bsModal: '/client/bower_components/bootstrap/js/modal'

    fullcalendar: '/client/bower_components/fullcalendar/fullcalendar'
    fc_gcal: '/client/bower_components/fullcalendar/gcal'
    
  # FIXME:  try to reduce the shim to only the
  # necessary resources
  shim:
    #jquery:
    #  exports: ['$', 'jQuery']
    bootstrap:
      deps: ['jquery']
    bsModal:
      deps: ['jquery']


requirements = [
  'application'
  'frontdoor/main'
  ]

require [
  'application'
  'frontdoor/main'
  ], (App) ->
  # debug
  window.app = App
  
  start_app_one = () ->
    if App.ready == false
      setTimeout(start_app_two, 100)
    else
      App.start()
        
  start_app_two = () ->
    if App.ready == false
      setTimeout(start_app_one, 100)
    else
      App.start()
    
  start_app_one()
    
