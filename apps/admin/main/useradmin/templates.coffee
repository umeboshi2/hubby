# modular template loading
define (require, exports, module) ->
  $ = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'
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
            
    
  ########################################
  # Templates
  ########################################
  useradmin_sidebar = renderable (model) ->
    div '.listview-list.btn-group-vertical', ->
      for entry in model.entries
        div '.btn.btn-default.' + entry.name, entry.label
        
    
      
  simple_user_entry = renderable (model) ->
    div '.listview-list-entry', ->
      a href:'#useradmin/viewuser/' + model.id, model.name

  simple_group_entry = renderable (model) ->
    div '.listview-list-entry', ->
      a href:'#useradmin/viewgroup/' + model.id, model.name

  simple_user_list = renderable (users) ->
    div '.listview-header', 'Users'
    
  simple_group_list = renderable (groups) ->
    div '.listview-header', 'Groups'


  view_user_page = renderable (model) ->
    div ->
      div '.listview-header', model.name
      p ->
        text "This is the user page for " + model.name
      hr
      div '.btn.btn-default.delete-user-button', 'Delete User'
      
  new_user_form = renderable () ->
    div '.form-group', ->
      label '.control-label', for:'input_name', 'User Name'
      input '#input_name.form-control',
      name:'name', 'data-validation':'name',
      placeholder:'User Name', value: ''
    div '.form-group', ->
      label '.control-label', for:'input_password', 'Password'
      input '#input_password.form-control',
      name:'password', 'data-validation':'password',
      placeholder:'', value:'', type:'password'
    div '.form-group', ->
      label '.control-label', for:'input_confirm', 'Confirm Password'
      input '#input_confirm.form-control',
      name:'confirm', 'data-validation':'confirm',
      placeholder:'', value:'', type:'password'
    input '.btn.btn-default.btn-xs', type:'submit', value:"Add New User"
    
  new_group_form = renderable () ->
    div '.form-group', ->
      label '.control-label', for:'input_name', 'Group Name'
      input '#input_name.form-control',
      name:'name', 'data-validation':'name',
      placeholder:'Group Name', value: ''
    input '.btn.btn-default.btn-xs', type:'submit', value:"Add New Group"

    
         
  ##################################################################
  # ##########################
  ##################################################################    
          
  module.exports =
    useradmin_sidebar: useradmin_sidebar
    simple_user_entry: simple_user_entry
    simple_group_entry: simple_group_entry
    simple_user_list: simple_user_list
    simple_group_list: simple_group_list
    new_user_form: new_user_form
    new_group_form: new_group_form
    view_user_page: view_user_page
    
    
