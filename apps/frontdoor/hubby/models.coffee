define (require, exports, module) ->
  $ = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'
  ########################################
  # Models
  ########################################
  class SimpleMeetingModel extends Backbone.Model
    
  module.exports =
    SimpleMeetingModel: SimpleMeetingModel
    
    

