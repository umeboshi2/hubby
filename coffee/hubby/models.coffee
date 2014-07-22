define (require, exports, module) ->
  $ = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'
  ########################################
  # Models
  ########################################

  class Page extends Backbone.Model
    url: () ->
      '/pages/' + @id + '.json'

  class User extends Backbone.Model
    #url: () ->
    #  'https://api.github.com/users/umeboshi2'
    url: () ->
      '/user.json'
      #'https://api.github.com/users/umeboshi2'
      
  module.exports =
    Page: Page
    User: User
    
