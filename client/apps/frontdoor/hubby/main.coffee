#
# Simple RSS app
define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'

  Controller = require 'hubby/controller'
  

  class Router extends Backbone.Marionette.AppRouter
    appRoutes:
      'hubby': 'start'
      'hubby/showpage/:id': 'show_page'
      'hubby/editpage/:id': 'edit_page'
      
      
      
  MSGBUS.commands.setHandler 'hubby:route', () ->
    console.log "hubby:route being handled"
    controller = new Controller
    router = new Router
      controller: controller
    #MSGBUS.commands.setHandler 'sdfsdfrssfeed:create', (model) ->
    #  console.log "rssfeed:create being handled"
    #MSGBUS.commands.setHandler 'sdfsdfrssfeed:update', (model) ->
    #  console.log 'rssfeed:update being handled'
      
      
          