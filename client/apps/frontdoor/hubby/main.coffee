#
# Simple RSS app
define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'

  Controller = require 'hubby/controller'
  

  class Router extends Backbone.Marionette.AppRouter
    appRoutes:
      'hubby': 'start'
      'hubby/viewmeeting/:id': 'show_meeting'
      
      
          
      
  MSGBUS.commands.setHandler 'hubby:route', () ->
    console.log "hubby:route being handled..."
    controller = new Controller
    router = new Router
      controller: controller
    render_cal_event = (calEvent, element) ->
      calEvent.url = '#hubby/viewmeeting/' + calEvent.id
      window.myevent = calEvent
      console.log  'render_cal_event called'
      element.css
        'font-size' : '0.7em'
        
    display_calendar = () ->
      console.log 'display_calendar called'
      cal = $ '#maincalendar'
      cal.fullCalendar
        header:
          left: 'month, agendaWeek, agendaDay'
          center: 'title'
        theme: true
        defaultView: 'month'
        eventSources:
          [
            url: '/hubcal'
          ]
        eventRender: render_cal_event
        #eventAfterRender: render_cal_event
        eventClick: (event) ->
          console.log event.url
          url = event.url
          Backbone.history.navigate url
          
          
        
        
    MSGBUS.commands.setHandler 'maincalendar:display', () ->
      console.log 'maincalendar:display handled'
      display_calendar()
          