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

  MSGBUS.reqres.setHandler 'hubby:meetingdetails', (meeting_id) ->
    console.log 'hubby:meetingdetails requested'
    #window.main_meeting_list = main_meeting_list
    #meeting = main_meeting_list.get meeting_id
    meeting = new Models.MainMeetingModel
      id: meeting_id
      url: () ->
        '/rest/v0/main/meeting/' + @id
    #return meeting

  module.exports =
    MeetingCollection: MeetingCollection

    
    