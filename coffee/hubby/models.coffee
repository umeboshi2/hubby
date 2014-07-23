define (require, exports, module) ->
  $ = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'
  ########################################
  # Models
  ########################################

  class Page extends Backbone.Model
    url: () ->
      '/hubby/pages/' + @id + '.json'

  module.exports =
    Page: Page
    
