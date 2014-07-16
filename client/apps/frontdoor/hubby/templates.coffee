# modular template loading
define (require, exports, module) ->
  $ = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'

  marked = require 'marked'
  
  teacup = require 'teacup'

  renderable = teacup.renderable

  div = teacup.div
  # I use "icon" for font-awesome
  icon = teacup.i
  strong = teacup.strong
  span = teacup.span
  label = teacup.label
  input = teacup.input

  text = teacup.text
  img = teacup.img
  # Main Templates must use teacup.
  # The template must be a teacup.renderable, 
  # and accept a layout model as an argument.

  # Tagnames to be used in the template.
  {div, span, link, text, strong, label, input, 
  button, a, nav, form, p,
  ul, li, b,
  h1, h2, h3,
  subtitle, section, hr
  } = teacup
            
  capitalize = (str) ->
    str.charAt(0).toUpperCase() + str.slice(1)
    
  ########################################
  # Templates
  ########################################
  sidebar = renderable (model) ->
    div '.listview-list.btn-group-vertical', ->
      for entry in model.entries
        div '.btn.btn-default.' + entry.name, entry.label
        
    
  page_list_entry = renderable (page) ->
    div '.listview-list-entry', ->
      span '.btn-default.btn-xs', ->
        a href:'#jellyfish/editpage/' + page.id,
        style:'color:black', ->
          icon '.edit-page.fa.fa-pencil'
      text "    "
      a href:'#jellyfish/showpage/' + page.id, page.name
        
  meeting_list_entry = renderable (meeting) ->
    div '.listview-list-entry', ->
      text meeting.title
        
  meeting_list = renderable () ->
    div '.listview-header', 'Meetings'
    div '.listview-list'
    
  meeting_calendar = renderable () ->
    div '.listview-header', 'Meetings'
    div '#maincalendar'

                  
  page_list = renderable () ->
    div '.listview-header', 'Wiki Pages'
    div '.listview-list'

  page_view = renderable (page) ->
    div '.listview-header', ->
      text page.name
    div '.listview-list', ->
      teacup.raw marked page.content

  show_meeting_view_orig = renderable (meeting) ->
    div '.listview-header', ->
      text meeting.title
    div '.listview-list', ->
      for mitem in meeting.meeting_items
        div '.listview-list-entry', mitem, ->
          item = meeting.items[mitem.item_id]
          div '.center-block', item.name
          div item.title
          
  show_meeting_view = renderable (meeting) ->
    div '.hubby-meeting-header', ->
      div '.hubby-meeting-header-agenda', ->
        text 'Agenda: ' + meeting.agenda_status
      div '.hubby-meeting-header-minutes', ->
        text 'Minutes: ' + meeting.minutes_status
    div '.hubby-meeting-item-list', ->
      agenda_section = 'start'
      for mitem in meeting.meeting_items
        item = meeting.items[mitem.item_id]
        #console.log agenda_section + '->' + mitem.type
        if mitem.type != agenda_section and mitem.type
          agenda_section = mitem.type
          section_header = capitalize agenda_section + ' Agenda'
          h3 '.hubby-meeting-agenda-header', section_header
        div '.hubby-meeting-item', ->
          div '.hubby-meeting-item-info', ->
            div '.hubby-meeting-item-agenda-num', mitem.agenda_num
            div '.hubby-meeting-item-fileid', item.file_id
            div '.hubby-meeting-item-status', item.status
          div '.hubby-meeting-item-content', ->
            p '.hubby-meeting-item-text', item.title
            if item.attachments != undefined and item.attachments.length
              div '.hubby-meeting-item-attachment-marker', 'Attachments'
              div '.hubby-meeting-item-attachments', ->
                for att in item.attachments
                  div ->
                    a href:'#ggg', att.name
                  
          
  edit_page = renderable (page) ->
    div '.listview-header', ->
      text "Editing " + page.name
      div '#save-button.pull-left.btn.btn-default.btn-xs', ->
        text 'save'
    div '#editor'
    

  
  ##################################################################
  # ##########################
  ##################################################################    
          
  module.exports =
    sidebar: sidebar
    page_list_entry: page_list_entry
    page_list: page_list
    page_view: page_view
    edit_page: edit_page
    meeting_list_entry: meeting_list_entry
    meeting_list: meeting_list
    meeting_calendar: meeting_calendar
    show_meeting_view: show_meeting_view
    