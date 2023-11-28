import { useParams } from "react-router-dom";
import Template from "../Template.tsx";
import { useEffect, useState } from "react";
import NotFound from "../NotFound.tsx";
import getAuthHeader from "../../authentication.ts";
import "../../css/Event.css";
import { URLS } from "../../constants.ts";
import { IEvent } from "./interfaces.ts";
import { EventHeader } from "./EventHeader.tsx";
import { EventChatBody } from "./EventChatBody.tsx";
import { EventMembers } from "./EventMembers.tsx";
import { EventPayers } from "./EventPayers.tsx";
import { EventSettings } from "./EventSettings.tsx";

export default function Event() {
  const [event, setEvent] = useState<IEvent | undefined>(undefined);
  const params = useParams();
  const event_id = parseInt(params.event_id as string);
  useEffect(() => {
    fetch(URLS.get_full_event(event_id), {
      headers: getAuthHeader(),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setEvent(data!);
      });
  }, [event_id]);

  if (isNaN(event_id)) {
    return <NotFound />;
  } else if (event == undefined) {
    return <Template />;
  } else {
    return <EventValidated event={event} />;
  }
}

function EventValidated({ event }: { event: IEvent }) {
  return (<Template doAddWrapping={false}>
    <div id={"common-field"} className={"width-60"}>
      <EventHeader event={event} />
      <EventChatBody />

      <div style={{ display: "none" }}>
        <EventMembers event={event} />
        <EventPayers event={event} />
        <EventSettings />
      </div>
    </div>
  </Template>);
}
