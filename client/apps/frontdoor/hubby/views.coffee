define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'
  Marionette = require 'marionette'

  Templates = require 'hubby/templates'

  Models = require 'hubby/models'
  FormView = require 'common/form_view'
  require 'jquery-ui'
  
  class SideBarView extends Backbone.Marionette.ItemView
    template: Templates.sidebar
    events:
      'click .maincalendar': 'maincalendar_pressed'
      'click .listmeetings': 'list_meetings_pressed'
      
    _navigate: (url) ->
      r = new Backbone.Router
      r.navigate url, trigger:true
      
    maincalendar_pressed: () ->
      console.log 'maincalendar_pressed called'
      @_navigate '#hubby'
      
    list_meetings_pressed: () ->
      console.log 'list_meetings_pressed called'
      @_navigate '#hubby/listmeetings'
      

  render_calendar_event = (calEvent, element) ->
    calEvent.url = '#hubby/viewmeeting/' + calEvent.id
    element.css
      'font-size' : '0.9em'

  calendar_view_render = (view, element) ->
    MSGBUS.commands.execute 'hubby:maincalendar:set_date'

  loading_calendar_events = (bool) ->
    loading = $ '#loading'
    header = $ '.fc-header'
    if bool
      loading.show()
      header.hide()
    else
      loading.hide()
      header.show()
      
      
    
  class SimpleMeetingView extends Backbone.Marionette.ItemView
    template: Templates.meeting_list_entry
    
  class MeetingListView extends Backbone.Marionette.CollectionView
    template: Templates.meeting_list
    itemView: SimpleMeetingView

  class MeetingCalendarView extends Backbone.Marionette.ItemView
    template: Templates.meeting_calendar

    onDomRefresh: () ->
      # get the current calendar date that has been stored
      # before creating the calendar
      date  = MSGBUS.reqres.request 'hubby:maincalendar:get_date'
      cal = $ '#maincalendar'
      cal.fullCalendar
        header:
          left: 'month, today'
          center: 'title'
          right: 'prev, next'
        theme: true
        defaultView: 'month'
        eventSources:
          [
            url: '/hubcal'
          ]
        eventRender: render_calendar_event
        viewRender: calendar_view_render
        loading: loading_calendar_events
        eventClick: (event) ->
          url = event.url
          Backbone.history.navigate url, trigger: true
      # if the current calendar date that has been set,
      # go to that date
      if date != undefined
        cal.fullCalendar('gotoDate', date)
        
  class ShowMeetingView extends Backbone.Marionette.ItemView
    template: Templates.show_meeting_view

    onDomRefresh: () ->
      attachments = $ '.hubby-meeting-item-attachments'
      attachments.hide()
      attachments.draggable()
      $('.hubby-meeting-item-info').click ->
        $(this).next().toggle()
      $('.hubby-meeting-item-attachment-marker').click ->
        $(this).next().toggle()
      $('.hubby-meeting-item-action-marker').click ->
        if $(this).hasClass('itemaction-loaded')
          $(this).next().toggle()
        else
          itemid = $(this).attr('id')
          url = '/hubby/frag/itemactions/' + itemid
          $(this).next().load(url)
          $(this).addClass('itemaction-loaded')
        
        
  class ShowPageView extends Backbone.Marionette.ItemView
    template: Templates.page_view

  class BaseEditPageView extends FormView

  class EditPageView extends Backbone.Marionette.ItemView
    template: Templates.edit_page

    onDomRefresh: () ->
      savebutton = $ '#save-button'
      savebutton.hide()
      editor = ace.edit('editor')
      editor.setTheme 'ace/theme/twilight'
      session = editor.getSession()
      session.setMode('ace/mode/markdown')
      content = @model.get 'content'
      editor.setValue(content)

      session.on('change', () ->
        savebutton.show()
      )
      
      savebutton.click =>
        @model.set('content', editor.getValue())
        response = @model.save()
        response.done ->
          console.log 'Model successfully saved.'
          savebutton.hide()
          
          
      
  module.exports =
    SimpleMeetingView: SimpleMeetingView
    MeetingListView: MeetingListView
    MeetingCalendarView: MeetingCalendarView
    ShowMeetingView: ShowMeetingView
    SideBarView: SideBarView
    
    
