define (require, exports, module) ->
  $ = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'

  Models = require 'hubby/models'
  MSGBUS = require 'msgbus'
      

  ########################################
  # Collections
  ########################################
  class BaseCollection extends Backbone.Collection
    # wrap the parsing to retrieve the
    # 'data' attribute from the json response
    parse: (response) ->
      return response.data

  class MeetingCollection extends BaseCollection
    model: Models.SimpleMeetingModel
    url: '/rest/v0/main/meeting'

  main_meeting_list = new MeetingCollection
  MSGBUS.reqres.setHandler 'hubby:meetinglist', ->
    main_meeting_list

  module.exports =
    MeetingCollection: MeetingCollection

    
    