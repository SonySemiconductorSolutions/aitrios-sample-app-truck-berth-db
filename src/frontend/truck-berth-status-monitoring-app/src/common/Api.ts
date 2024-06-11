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
import { ApiResponse, NotificationResponse } from "./ApiResponse";

/** @type {apiUrl} Base URL of the API updates form environment variable*/
const apiUrl: string = import.meta.env.VITE_API_URL;

/**
 * Gets the Truck Berth status from backend API
 *
 * @return {Promise<ApiResponse>} API response from backend service
 */
export const fetchData = async (): Promise<ApiResponse> => {
  try {
    const response = await fetch(`${apiUrl}/getberthstatus`);
    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error("Error fetching data from the API");
  }
};

/**
 * Gets the truck berth Notification from backend API
 *
 * @return {Promise<NotificationResponse>} API response of Notification list from backend service
 */
export const fetchNotification = async (
  notification_time?: string
): Promise<NotificationResponse> => {
  try {
    const response = await fetch(
      `${apiUrl}/getnotifications${
        notification_time !== undefined && notification_time !== null
          ? "?notification_time=" + notification_time
          : ""
      }`
    );
    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error("Error fetching data from the API");
  }
};
