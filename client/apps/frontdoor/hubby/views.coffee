define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'
  Marionette = require 'marionette'

  Templates = require 'hubby/templates'

  Models = require 'hubby/models'
  FormView = require 'common/form_view'
  require 'jquery-ui'
  
  #require 'ace'

  class SideBarView extends Backbone.Marionette.ItemView
    template: Templates.sidebar
    events:
      'click .maincalendar': 'maincalendar_pressed'
      'click .adduser': 'add_user_pressed'
      'click .listgroups': 'list_groups_pressed'
      'click .addgroup': 'add_group_pressed'
      
    _navigate: (url) ->
      r = new Backbone.Router
      r.navigate url, trigger:true
      
    maincalendar_pressed: () ->
      console.log 'maincalendar_pressed called'
      @_navigate '#hubby'
      
    add_user_pressed: () ->
      console.log 'add_user called'
      @_navigate '#useradmin/adduser'
      
    list_groups_pressed: () ->
      console.log 'list_groups_pressed called'
      @_navigate '#useradmin/listgroups'

    add_group_pressed: () ->
      console.log 'add_group_pressed called'
      @_navigate '#useradmin/addgroup'



  class SimpleMeetingView extends Backbone.Marionette.ItemView
    template: Templates.meeting_list_entry
    
  class MeetingListView extends Backbone.Marionette.CollectionView
    template: Templates.meeting_list
    itemView: SimpleMeetingView

  class MeetingCalendarView extends Backbone.Marionette.ItemView
    template: Templates.meeting_calendar

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
    
    