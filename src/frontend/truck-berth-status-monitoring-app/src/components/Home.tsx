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
import NotificationListComponent from "./NotificationListComponent";
import TimelineComponent from "./TimelineComponent";

/**
 * Home Screen which consist of Header and Timeline Chart
 *
 * @return {JSX.Element} DOM element
 */
function Home() {
  return (
    <>
      <div className="container">
        <div className="header">
          <h2>Truck Berth Status Monitoring App</h2>
        </div>
        <div className="timeline-body">
          <TimelineComponent></TimelineComponent>
        </div>
        <div className="notification-list">
          <NotificationListComponent></NotificationListComponent>
        </div>
      </div>
    </>
  );
}

export default Home;
