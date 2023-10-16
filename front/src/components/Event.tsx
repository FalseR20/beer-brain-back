import { useParams } from "react-router-dom";
import Template from "./Template.tsx";
import { useEffect, useState } from "react";
import NotFound from "./NotFound.tsx";
import getAuthHeader from "../authentication.ts";
import "../css/Event.css";
import { Col, Container, Form, InputGroup, Row } from "react-bootstrap";
import { BsPencil } from "react-icons/bs";

interface IEvent {
  id: number;
  date: string;
  description: string;
  is_closed: boolean;
  members: IMember[];
}

interface IMember {
  id: number;
  user: number;
  event: number;
  deposits: IDeposit[];
}

interface IDeposit {
  id: number;
  description: string;
  value: number;
  member: number;
}

export default function Event() {
  const [event, setEvent] = useState<IEvent | undefined>(undefined);
  const params = useParams();
  const event_id = parseInt(params.event_id as string);
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/core/events/${event_id}`, {
      headers: getAuthHeader(),
    }).then((response) => response.json()).then((data) => {
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
  function updateDescription(newDescription: string) {
    if (event.description == newDescription) {
      return;
    }
    console.log(`Updated description ${newDescription}`);
    event.description = newDescription;
  }


  return (<Template>
    <InputGroup className={"my-3"} size={"lg"}>
      <InputGroup.Text id={"name-addon"}>
        <BsPencil />
      </InputGroup.Text>
      <Form.Control
        id={"description-input"}
        aria-label={"Description"}
        aria-describedby={"name-addon"}
        defaultValue={event.description}
        onBlur={({ target }) => updateDescription(target.value)}
        onKeyDown={({ key, currentTarget }) => {
          if (key == "Enter") {
            currentTarget.blur();
          }
        }}
      />
    </InputGroup>

    <h2>Bank</h2>
    <Container>
      <Row key={"0"}>
        <Col>Description</Col>
        <Col>Value</Col>
        <Col>User</Col>
      </Row>
      {event.members.map((member) => member.deposits.map((deposit) => <Row key={deposit.id}>
        <Col>{deposit.description}</Col>
        <Col>{deposit.value}</Col>
        <Col>{deposit.id}</Col>
      </Row>))}
    </Container>

    <h2>Event info:</h2>

    <code style={{ whiteSpace: "break-spaces" }}>
      {JSON.stringify(event, null, 3)}
    </code>;

  </Template>);
}
