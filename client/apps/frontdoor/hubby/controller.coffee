define (require, exports, module) ->
  $ = require 'jquery'
  Backbone = require 'backbone'
  Marionette = require 'marionette'
  MSGBUS = require 'msgbus'

  Views = require 'hubby/views'
  Collections = require 'hubby/collections'

  fullCalendar = require 'fullcalendar'
  #gcal = require 'fc_gcal'
  
  class Controller extends Backbone.Marionette.Controller
    make_sidebar: ->
      meetings = MSGBUS.reqres.request 'hubby:meetinglist'
      
      MSGBUS.events.trigger 'sidebar:close'
      view = new Views.MeetingListView
        collection: meetings
      MSGBUS.events.trigger 'sidebar:show', view
      #if meetings.length == 0
      #  console.log 'fetching pages for sidebar'
      #  meetings.fetch()
      
      
    set_header: (title) ->
      header = $ '#header'
      header.text title
      
    start: ->
      console.log 'hubby start'
      MSGBUS.events.trigger 'rcontent:close'
      MSGBUS.events.trigger 'sidebar:close'
      @set_header 'Hubby'
      #@make_sidebar()
      @show_calendar()
      
    show_calendar: () ->
      console.log 'hubby show calendar'
      @make_sidebar()
      view = new Views.MeetingCalendarView
      MSGBUS.events.trigger 'rcontent:show', view
      #MSGBUS.events.trigger 'maincalendar:display'
      MSGBUS.commands.execute 'maincalendar:display'
      
    show_meeting: (meeting_id) ->
      @make_sidebar()
      meeting = MSGBUS.reqres.request 'hubby:getmeeting', meeting_id
      
    show_page: (page_id) ->
      @make_sidebar()
      page = MSGBUS.reqres.request 'wiki:pagecontent', page_id
      view = new Views.ShowPageView
        model: page
      MSGBUS.events.trigger 'rcontent:show', view

    edit_page: (page_id) ->
      @make_sidebar()
      page = MSGBUS.reqres.request 'wiki:pagecontent', page_id
      view = new Views.EditPageView
        model: page
      MSGBUS.events.trigger 'rcontent:show', view
      
      
              
  module.exports = Controller
  
