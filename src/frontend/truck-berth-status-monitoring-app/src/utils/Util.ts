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

import moment from "moment";
import { DateType } from "vis-timeline";

/**
 * Converting the raw HTML style string to a Mappable List
 *
 * @export
 * @param {string} stylesString Raw HTML style content
 * @return {Record<string, string>} List key value pairs of style properties.
 */
export function convertStringToStyles(
  stylesString: string
): Record<string, string> {
  const stylesArray = stylesString.split(";").filter(Boolean); // Split the string by ';' and remove empty elements
  const stylesObject: Record<string, string> = {};

  stylesArray.forEach((style) => {
    const [property, value] = style.split(":").map((part) => part.trim()); // Split each style into property and value
    if (property && value) {
      stylesObject[property] = value; // Assign property-value pairs to the object
    }
  });

  return stylesObject;
}

export function formatToolTipScheduleTime(start: DateType, end: DateType) {
  const mStart = moment(start);
  const mEnd = moment(end);
  const formatTime = "HH:mm";
  const formatDateTime = "DD MMM HH:mm";
  let format = (mStart.date() !== mEnd.date() || mStart.month() !== mEnd.month()) ? formatDateTime : formatTime;
  let result = `${moment(start).format(format)} - ${moment(end).format(
    format
  )}`;
  return result;
}