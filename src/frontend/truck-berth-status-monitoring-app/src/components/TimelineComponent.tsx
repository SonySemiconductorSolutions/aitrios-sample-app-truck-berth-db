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
import React, { useEffect, useRef, useState } from "react";
import "vis-timeline/styles/vis-timeline-graph2d.css";
import {
  DataGroup,
  DataItem,
  DataItemCollectionType,
  DataSet,
  Timeline,
  TimelineAlignType,
  TimelineTimeAxisScaleType,
} from "vis-timeline/standalone";
import { MomentInput } from "moment";
import moment from "moment";
import { fetchData } from "../common/Api";
import {
  convertStringToStyles,
  formatToolTipScheduleTime,
} from "../utils/Util";
import { GetStatusResponse, GroupItem, TruckItem } from "../common/ApiResponse";

/**
 * Timeline component which Displays the Truck Berth Status periodically
 *
 * @return {React.FC} React node factory components
 */
const TimelineComponent: React.FC = () => {
  /**
   * Getter and Setter for getStatus API response
   *
   * @type {[GetStatusResponse, React.Dispatch<React.SetStateAction<GetStatusResponse]}
   * @memberof TimelineComponent
   *
   * */
  const [data, setData] = useState<GetStatusResponse>();

  /**
   * Getter and Setter for Tool tip truck number
   *
   * @type {[string, React.Dispatch<React.SetStateAction<string>>]}
   * @memberof TimelineComponent
   *
   * */
  const [tooltipTruckNo, setTooltipTruckNo] = useState("");

  /**
   * Getter and Setter for Tool tip truck schedule Time.
   *
   * @type {[string, React.Dispatch<React.SetStateAction<string>>]}
   * @memberof TimelineComponent
   *
   * */
  const [tooltipScheduleTime, setTooltipScheduleTime] = useState("");

  /**
   * Getter and Setter for Tool tip truck style properties.
   *
   * @type {[Record<string, string>, React.Dispatch<React.SetStateAction<Record<string, string>>>]}
   * @memberof TimelineComponent
   *
   * */
  const [tooltipStyle, setTooltipStyle] = useState<Record<string, string>>({
    color: "#ea6b66",
    "background-color": "#f8cecc",
  });

  /**
   * Getter and Setter for Tool tip visibility*.
   *
   * @type {[boolean, React.Dispatch<React.SetStateAction<boolean>>]}
   * @memberof TimelineComponent
   *
   * */
  const [showTooltip, setShowTooltip] = useState(false);
  /**
   * timeline reference for
   *
   * @type {React.MutableRefObject<Timeline>}
   * @memberof TimelineComponent
   *
   * */
  const timelineRef = useRef<Timeline | null>(null);
  const [grp, setGrp] = useState<GroupItem[]>([
    {
      id: 100,
      content: "Berth 1",
      nestedGroups: [1, 2],
      groupId: 1,
    },
    {
      id: 1,
      content: "Reserve",
      treeLevel: 2,
    },
    {
      id: 2,
      treeLevel: 2,
      content: "Actual",
    },
    /*{
      id: 101,
      content: "Berth 2",
      nestedGroups: [3, 4],
      groupId: 2,
    },
    {
      id: 3,
      treeLevel: 2,
      content: "Reserve",
    },
    {
      id: 4,
      treeLevel: 2,
      content: "Actual",
    }, */
  ]);
  const items: DataSet<DataItem, "id"> = new DataSet([]);

  /**
   *  @description Fetch the API data asynchronously
   *
   */
  const fetchDataFromApi = async () => {
    try {
      const result = await fetchData();
      setData(result.data);
    } catch (error) {
      console.error(error.message);
    }
  };
  useEffect(() => {
    fetchDataFromApi();
    // calls the API periodically
    const interval = setInterval(() => {
      fetchDataFromApi();
    }, 5000);

    return () => clearInterval(interval);

    // fetchDataFromApi();
  }, []);

  useEffect(() => {
    const DATE_TIME_FORMAT = "YYYY-MM-DD HH:mm:ss";
    const today = moment(new Date().toLocaleString()).format(DATE_TIME_FORMAT);
    const options = {
      align: "left" as TimelineAlignType,
      clickToUse: false,
      // height: "100px",
      // width: "1200px",
      // groupHeights: 100,
      start: today, // Set the start date
      end: moment(today).add(1, "days").toString(), // Set the end date
      stack: false,
      orientation: "top",
      margin: {
        item: 10,
      },
      // moment: (date: MomentInput) => {
      //   return moment(date).utcOffset("-06:30");
      // },
      showCurrentTime: false,
      showMajorLabels: true,
      showMinorLabels: true,
      timeAxis: { scale: "minute" as TimelineTimeAxisScaleType, step: 60 },
      format: {
        minorLabels: {
          minute: "HH:mm",
        },
      },
      //   step: 60 * 60 * 1000,
      zoomable: false,
      // zoomFriction: 1,
      // zoomMax: 50,
      // zoomMin: 100,
      // scrollable: true,
      editable: false,
      horizontalScroll: false,
      itemsAlwaysDraggable: false,
      template: (data?: DataItem) => {
        return `<div>
        <div>
        ${data?.content}
        </div>
        <div>
        ${moment(data!.start).format("HH:mm")} - ${moment(data!.end).format(
          "HH:mm"
        )}
        </div>
        </div>`;
      },
      // zIndex: 2,
      //   yAxisOrientation: "left",
      //   type: 'background' as TimelineOptionsEventType
    };
    const groups: DataGroup[] = [];
    groups.push(...grp);

    const container = document.getElementById("timeline-container");

    /**
     * Creating the Timeline component by passing
     * container: HTML Container,
     * items: data to populate in timeline,
     * groups: groups to be shown,
     * options: configurations to display the graph.
     */
    const timeline = new Timeline(container!, items, groups, options);
    //disabling the zoom
    timeline.zoomIn(0);

    timelineRef.current = timeline;

    return () => {
      timeline?.destroy();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (data) {
      setShowTooltip(false);
      //setting the berth name from API response
      let newGrp: GroupItem[] = [];
      data.berths.forEach((element, i) => {
        // grp[i * 3].content = element;
        const groupId = i + 1;
        const berthGroupItem: GroupItem = {
          id: 100 + i,
          content: element,
          nestedGroups: [groupId * 2 - 1, groupId * 2],
          groupId: groupId,
        };
        newGrp.push(berthGroupItem);
        const reservationGroupItem: GroupItem = {
          id: groupId * 2 - 1,
          content: "Reserves",
          treeLevel: 2,
          nestedInGroup: 100 + i,
        };
        newGrp.push(reservationGroupItem);
        const actualGroupItem: GroupItem = {
          id: groupId * 2,
          content: "Actual",
          treeLevel: 2,
          nestedInGroup: 100 + i,
        };
        newGrp.push(actualGroupItem);
      });

      if (grp[0].content !== newGrp[0].content) {
        setGrp(newGrp);
        timelineRef.current?.setGroups(newGrp);
      }

      data["status"].forEach((i: TruckItem) => {
        items.add({
          content: i.content,
          end: i.end,
          group: i.group,
          id: i.id,
          start: i.start,
          style: i.style,
        });
      });

      // Setting the beth data from API response
      timelineRef.current?.setData({ items: items as DataItemCollectionType });

      // setting up call when cursor over the item to show tool tip
      timelineRef.current?.on("itemover", (props) => {
        const itemId: number = props.item;
        const item = items.get(itemId);
        if (item) {
          setTooltipTruckNo(`${item["content"]}`);
          setTooltipScheduleTime(
            formatToolTipScheduleTime(item.start, item.end!)
          );
          setTooltipStyle(convertStringToStyles(item.style!));
          setShowTooltip(true);
        }
      });

      // Handle item out event to hide tooltip on mouse out
      timelineRef.current?.on("itemout", () => {
        setTooltipTruckNo(``);
        setTooltipScheduleTime(``);
        setShowTooltip(false);
        setTooltipStyle({
          color: "#ea6b66",
          "background-color": "#f8cecc",
        });
      });
    }

    return () => {};
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data]);

  return (
    <>
      <div style={{ position: "relative" }}>
        <div className="legend-container">
          <div className="match-legend"></div>
          <div className="match-legend"></div>
          <p>Match</p>
          <div className="not-match-legend"></div>
          <div className="not-match-legend"></div>
          <div className="not-match-legend"></div>
          <p>No Match/Incorrect Reservation</p>
        </div>
        <div
          id="tool-tip"
          style={{
            visibility: showTooltip ? `visible` : `hidden`,
            color: tooltipStyle.color,
            backgroundColor: tooltipStyle["background-color"],
            fontWeight: `bold`,
          }}
        >
          <div>{tooltipTruckNo}</div>
          <div>{tooltipScheduleTime}</div>
        </div>
      </div>
      <div id="timeline-container" style={{ width: "100vw" }}></div>
    </>
  );
};

export default TimelineComponent;
