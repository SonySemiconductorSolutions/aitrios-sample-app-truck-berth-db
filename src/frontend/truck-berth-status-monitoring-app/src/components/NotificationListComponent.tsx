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
import React, { useEffect, useState } from "react";
import { fetchNotification } from "../common/Api";
import { NotificationItem } from "../common/ApiResponse";

const NotificationListComponent: React.FC = () => {
  const [notificationList, setNotificationList] =
    useState<NotificationItem[]>();
  /**
   *  @description Fetch the Notification List API data asynchronously
   *
   */
  const fetchNotificationFromApi = async (notification_time?: string) => {
    try {
      const result = await fetchNotification(notification_time);
      setNotificationList(
        filterUniqueNotificationListItems(
          notificationList === undefined
            ? result.data
            : result.data.concat(notificationList)
        )
      );
    } catch (error) {
      console.error(error.message);
    }
  };

  /**
   * Filtering unique notification from the added list.
   *
   * @param {NotificationItem[]} arr 
   * @return 
   */
  function filterUniqueNotificationListItems(arr: NotificationItem[]) {
    const unique = new Map();
    arr.forEach((obj) => {
      const key =
        obj.berth_number +
        "|" +
        obj.car_number +
        "|" +
        obj.notification_time +
        "|" +
        obj.notification_type;
      if (!unique.has(key)) {
        unique.set(key, obj);
      }
    });
    return Array.from(unique.values());
  }

  useEffect(() => {
    if (notificationList === undefined) fetchNotificationFromApi();
    // calls the API periodically
    const interval = setInterval(() => {
      fetchNotificationFromApi(
        notificationList !== undefined && notificationList?.length > 0
          ? notificationList[0].notification_time
          : undefined
      );
    }, 5000);

    return () => clearInterval(interval);
  }, [notificationList]);

  return (
    <>
      <div className="notification-list-container">
        {notificationList && notificationList?.length > 0 && (
          <h3 className="notification-header">Notifications</h3>
        )}
        {notificationList?.map((item, index) => (
          <div className={item.class} key={index}>
            <strong>{item.notification_time}</strong>{" "}
            {item.notification_message}
          </div>
        ))}
      </div>
    </>
  );
};

export default NotificationListComponent;
