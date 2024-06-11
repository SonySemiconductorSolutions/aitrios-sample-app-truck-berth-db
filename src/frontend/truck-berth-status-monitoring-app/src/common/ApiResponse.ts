/*
------------------------------------------------------------------------
Copyright 2024 Sony Semiconductor Solutions Corp. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
------------------------------------------------------------------------
*/
/**
 * Response structure of "getberthstatus" API
 *
 * @export
 * @interface ApiResponse
 */
export interface ApiResponse {
  /**
   * Data of API response.
   *
   * @type {GetStatusResponse}
   * @memberof ApiResponse
   */
  data: GetStatusResponse;
}

/**
 * Structure of each Truck Berth item
 *
 * @export
 * @interface TruckItem
 */
export interface TruckItem {
  /**
   * Style to update color and background color
   * for each truck berth slot
   *
   * @type {string}
   * @memberof TruckItem
   */
  style: string;
  /**
   * Truck Berth number.
   *
   * @type {string}
   * @memberof TruckItem
   */
  content: string;
  /**
   * Truck Berth slot end time
   *
   * @type {string}
   * @memberof TruckItem
   */
  end: string;
  /**
   * Berth group id
   *
   * @type {number}
   * @memberof TruckItem
   */
  group: number;
  /**
   * Unique ID
   *
   * @type {number}
   * @memberof TruckItem
   */
  id: number;
  /**
   *  Truck Berth slot start time
   *
   * @type {string}
   * @memberof TruckItem
   */
  start: string;
}

/**
 * Structure of response which contains Berth data and
 * Truck Berth Items data
 *
 * @export
 * @interface GetStatusResponse
 */
export interface GetStatusResponse {
  /**
   * List of all actual and reserved truck berth list
   *
   * @type {TruckItem[]}
   * @memberof GetStatusResponse
   */
  status: TruckItem[];
  /**
   * Message of response API.
   *
   * @type {string}
   * @memberof GetStatusResponse
   */
  message: string;
  /**
   * List of all berths in Parking lot
   *
   * @type {string[]}
   * @memberof GetStatusResponse
   */
  berths: string[];
}

/**
 * Response structure of "getnotifications" API
 *
 * @export
 * @interface NotificationResponse
 */
export interface NotificationResponse {
  /**
   * Data of API response.
   *
   * @type {NotificationItem[]}
   * @memberof NotificationResponse
   */
  data: NotificationItem[];
}

/**
 * Structure of each notification item
 *
 * @export
 * @interface NotificationItem
 */
export interface NotificationItem {
  /**
   * Berth Number or Name string
   *
   * @type {string}
   * @memberof NotificationItem
   */
  berth_number: string;
  /**
   * Notification message
   *
   * @type {string}
   * @memberof NotificationItem
   */
  notification_message: string;
  /**
   * style class used to resemblance of the message
   *
   * @type {string}
   * @memberof NotificationItem
   */
  class: string;
  /**
   * Truck Number which is used to display
   *
   * @type {string}
   * @memberof NotificationItem
   */
  car_number: string;
  /**
   * Notification triggered time
   *
   * @type {string}
   * @memberof NotificationItem
   */
  notification_time: string;
  /**
   * Notification type
   *
   * @type {boolean}
   * @memberof NotificationItem
   */
  notification_type: string;
}

/**
 * Group item for Timeline graph.
 *
 * @export
 * @interface GroupItem
 */
export interface GroupItem {
  /**
   * Unique ID in the group.
   *
   * @type {number}
   * @memberof GroupItem
   */
  id: number;
  /**
   * Text to display in y axis header for each row
   *
   * @type {string}
   * @memberof GroupItem
   */
  content: string;
  /**
   * ID's to specify the nested sub group
   *
   * @type {number[]}
   * @memberof GroupItem
   */
  nestedGroups?: number[];
  /**
   * Unique ID of a group
   *
   * @type {number}
   * @memberof GroupItem
   */
  groupId?: number;
  /**
   * Nesting the Subgroup level
   *
   * @type {number}
   * @memberof GroupItem
   */
  treeLevel?: number;
  /**
   * Specifying the group to subgroup item should belong
   *
   * @type {number}
   * @memberof GroupItem
   */
  nestedInGroup?: number;
}
