#
define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'

  Controller = require 'hubby/controller'
  

  class Router extends Backbone.Marionette.AppRouter
    appRoutes:
      'hubby': 'start'
      'hubby/viewmeeting/:id': 'show_meeting'
      
  current_calendar_date = undefined
  MSGBUS.commands.setHandler 'hubby:maincalendar:set_date', () ->
    cal = $ '#maincalendar'
    current_calendar_date = cal.fullCalendar 'getDate'

  MSGBUS.reqres.setHandler 'hubby:maincalendar:get_date', () ->
    current_calendar_date
    
  MSGBUS.commands.setHandler 'hubby:route', () ->
    #window.msgbus = MSGBUS
    #console.log "hubby:route being handled..."
    controller = new Controller
    router = new Router
      controller: controller
      
    render_cal_event = (calEvent, element) ->
      calEvent.url = '#hubby/viewmeeting/' + calEvent.id
      #console.log  'render_cal_event called'
      element.css
        'font-size' : '0.9em'

    calendar_view_render = (view, element) ->
      MSGBUS.commands.execute 'hubby:maincalendar:set_date'
          
    display_calendar = () ->
      # get the current calendar date that has been stored
      # before creating the calendar
      date = MSGBUS.reqres.request 'hubby:maincalendar:get_date'
      cal = $ '#maincalendar'
      cal.fullCalendar
        header:
          left: 'month, today, prev, next'
          center: 'title'
          right: 'prevYear, nextYear'
        theme: true
        defaultView: 'month'
        eventSources:
          [
            url: '/hubcal'
          ]
        eventRender: render_cal_event
        eventClick: (event) ->
          #console.log event.url
          url = event.url
          Backbone.history.navigate url, trigger: true
        viewRender: calendar_view_render
      # if the current calendar date has been set
      # go to that date
      if date != undefined
        cal.fullCalendar('gotoDate', date)
      
    MSGBUS.commands.setHandler 'maincalendar:display', () ->
      console.log 'maincalendar:display handled'
      display_calendar()
          