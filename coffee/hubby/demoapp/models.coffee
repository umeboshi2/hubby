define (require, exports, module) ->
  $ = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'
  ########################################
  # Models
  ########################################
  class SimpleMeetingModel extends Backbone.Model

  class MainMeetingModel extends Backbone.Model
    url: () ->
      'http://hubby.littledebian.org/rest/v0/main/meeting/' + @id
    parse: (response) ->
      response.data
          
  module.exports =
    SimpleMeetingModel: SimpleMeetingModel
    MainMeetingModel: MainMeetingModel
    
