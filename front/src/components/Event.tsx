import { useParams } from "react-router-dom";
import Template from "./Template.tsx";
import { useEffect, useState } from "react";
import NotFound from "./NotFound.tsx";
import getAuthHeader from "../authentication.ts";
import "../css/Event.css";
import { Button, Form, InputGroup, Modal, Table } from "react-bootstrap";
import { BsPencil } from "react-icons/bs";
import { URLS } from "../constants.ts";

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
    fetch(URLS.get_full_event(event_id), {
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
  const [showDescriptionModal, setShowDescriptionModal] = useState(false);
  const [description, setDescription] = useState(event.description);
  const [newDescription, setNewDescription] = useState<string | null>(null);

  return (<Template>
    <InputGroup className={"my-3"} size={"lg"}>
      <Form.Control
        id={"description-input"}
        aria-label={"Description"}
        disabled={true}
        value={description}
      />
      <Button variant={"secondary"} id={"name-addon"} onClick={() => setShowDescriptionModal(true)}>
        <BsPencil />
      </Button>
    </InputGroup>
    <Modal show={showDescriptionModal} onHide={() => setShowDescriptionModal(false)}>
      <Modal.Header closeButton>
        <Modal.Title>Modal heading</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group
            className="mb-3"
            controlId="exampleForm.ControlTextarea1"
          >
            <Form.Label>New description</Form.Label>
            <Form.Control as="textarea" rows={3} defaultValue={description} onChange={(e) => {
              setNewDescription(e.target.value);
            }} />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="outline-secondary" onClick={() => setShowDescriptionModal(false)}>
          Close
        </Button>
        <Button id={"btn-modal-ok"} variant="primary" onClick={() => {
          if (newDescription != description) {
            console.log(`New description ${newDescription}`);
            setDescription(newDescription!);
          }
          setShowDescriptionModal(false);
        }}>
          Save Changes
        </Button>
      </Modal.Footer>
    </Modal>


    <Table>
      <thead>
      <tr>
        <th>Description</th>
        <th>Value</th>
        <th>User</th>
      </tr>
      </thead>
      <tbody>
      {event.members.map((member) => member.deposits.map((deposit) => <tr key={deposit.id}>
        <th>{deposit.description}</th>
        <th>{deposit.value}</th>
        <th>{deposit.id}</th>
      </tr>))}
      </tbody>

    </Table>

    {/*<h2>Event info:</h2>*/}
    {/*<code style={{ whiteSpace: "break-spaces" }}>*/}
    {/*  {JSON.stringify(event, null, 3)}*/}
    {/*</code>;*/}

  </Template>);
}
