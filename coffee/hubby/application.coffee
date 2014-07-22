define (require, exports, module) ->
  $ = require 'jquery'
  jQuery = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'
  bootstrap = require 'bootstrap'
  Marionette = require 'marionette'

  
  MSGBUS = require 'msgbus'
  Models = require 'models'
  
  require 'mainpage'
  require 'frontdoor/main'

  prepare_app = (app) ->
    app.addRegions
      mainview: 'body'

      navbar: '#main-navbar'
      content: '#main-content'
      footer: '#footer'
      
      sidebar: '#sidebar'
      rcontent: '#main-content'
      
    app.on 'initialize:after', ->
      console.log "start event being handled"
      Backbone.history.start() unless Backbone.history.started
      
    app.on 'start', ->
      console.log "start event being handled"
      Backbone.history.start() unless Backbone.history.started
      
    app.msgbus = MSGBUS

    app.addInitializer ->
      # execute code to generate basic page
      # layout
      MSGBUS.commands.execute 'mainpage:init'

      # then setup the routes
      MSGBUS.commands.execute 'frontdoor:route'
      
    # connect events
    MSGBUS.events.on 'mainpage:show', (view) =>
      console.log 'mainpage:show called'
      app.mainview.show view
      
    MSGBUS.events.on 'main-menu:show', (view) =>
      console.log 'main-menu:show called'
      app.main_menu.show view
      

    MSGBUS.events.on 'sidebar:show', (view) =>
      console.log 'sidebar:show called'
      app.sidebar.show view

    MSGBUS.events.on 'sidebar:close', () =>
      console.log 'sidebar:close called'
      if 'sidebar' in app
        app.sidebar.destroy()

    MSGBUS.events.on 'main-navbar:show', (view) =>
      console.log 'main-navbar:show called'
      app.navbar.show view
      
    MSGBUS.events.on 'rcontent:show', (view) =>
      console.log 'rcontent:show called'
      app.rcontent.show view
      
    MSGBUS.events.on 'rcontent:close', () =>
      app.rcontent.destroy()
      
            
      
  app = new Marionette.Application()
  app.current_user = new Models.User
  response = app.current_user.fetch()


  MSGBUS.reqres.setHandler 'current:user', ->
    app.current_user
    
  app.ready = false

  response.done ->
    prepare_app app
    app.ready = true
    
  
  module.exports = app
  
    
