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
      '/rest/v0/main/meeting/' + @id
      
          
  module.exports =
    SimpleMeetingModel: SimpleMeetingModel
    MainMeetingModel: MainMeetingModel
    

