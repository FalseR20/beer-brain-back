import { Link, useParams } from "react-router-dom";
import Template from "./Template.tsx";
import { useEffect, useState } from "react";
import NotFound from "./NotFound.tsx";
import getAuthHeader from "../authentication.ts";
import "../css/Event.css";
import { Button, Form, ListGroup, Modal } from "react-bootstrap";
import { BsThreeDotsVertical } from "react-icons/bs";
import { URLS } from "../constants.ts";
import { RxPlus } from "react-icons/rx";
import { Avatar48 } from "./Profile.tsx";

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
  return (
    <Template doAddWrapping={false}>
      <div id={"common-field"} className={"width-60"}>
        <EventHeader event={event} />
        {/*<Members event={event} />*/}
        {/*<Payers event={event} />*/}
        {/*<SettingsElements />*/}
      </div>
    </Template>
  );
}

function EventHeader({ event }: { event: IEvent }) {
  const [showDescriptionModal, setShowDescriptionModal] = useState(false);
  const [description, setDescription] = useState(event.description);
  const [newDescription, setNewDescription] = useState<string | null>(null);

  return (
    <div className={"border border-top-0 rounded-bottom-5 bg-body-tertiary"}>
      <div className={"d-flex flex-row ps-2 pe-3 py-1"}>
        <div
          className={"border rounded-5 my-1 me-3"}
          style={{
            height: "3.5rem",
            width: "3.5rem",
            fontSize: "1.5rem",
            padding: "0.5rem",
            textAlign: "center",
          }}
        >
          {parseInt(event.date.slice(8, 10))}
        </div>
        <div className={"flex-grow-1"}>
          <div className={"d-flex flex-column align-items-start"}>
            <div className={"fs-4"}>{description}</div>
            <div
              className={"fs-6"}
            >{`${event.date}, ${event.members.length} members`}</div>
          </div>
        </div>

        <div className={"pt-1 ms-2"}>
          <a
            id={"name-addon"}
            className={"text-body fs-2 hover-cursor-pointer"}
            onClick={() => setShowDescriptionModal(true)}
          >
            <BsThreeDotsVertical />
          </a>
          <Modal
            show={showDescriptionModal}
            onHide={() => setShowDescriptionModal(false)}
          >
            <Modal.Header closeButton>
              <Modal.Title>Description updating</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Form>
                <Form.Group
                  className="mb-3"
                  controlId="exampleForm.ControlTextarea1"
                >
                  <Form.Label>New description</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={3}
                    defaultValue={description}
                    onChange={(e) => {
                      setNewDescription(e.target.value);
                    }}
                  />
                </Form.Group>
              </Form>
            </Modal.Body>
            <Modal.Footer>
              <Button
                variant="outline-secondary"
                onClick={() => setShowDescriptionModal(false)}
              >
                Close
              </Button>
              <Button
                id={"btn-modal-ok"}
                variant="primary"
                onClick={() => {
                  if (newDescription != description) {
                    console.log(`New description ${newDescription}`);
                    setDescription(newDescription!);
                  }
                  setShowDescriptionModal(false);
                }}
              >
                Save Changes
              </Button>
            </Modal.Footer>
          </Modal>
        </div>
      </div>
    </div>
  );
}

function Members({ event }: { event: IEvent }) {
  return (
    <div className={"mb-1"}>
      <h5>
        {event.date}, {event.members.length} people
      </h5>
      <ListGroup horizontal={true}>
        {event.members.map((member) => {
          // noinspection RequiredAttributes
          return (
            <div
              className={"m-2"} //  border-bottom border-light rounded-2
              key={member.id}
            >
              <Link to={`/user/${member.id}`}>
                <Avatar48 id={member.id} />
              </Link>
            </div>
          );
        })}
        <div className={"m-2"}>
          <RxPlus size={48} />
        </div>
      </ListGroup>
    </div>
  );
}

function Payers({ event }: { event: IEvent }) {
  const membersWithDeposits = event.members.filter(
    (member) => member.deposits.length > 0,
  );
  return (
    <>
      <div className={"d-flex justify-content-between align-items-center"}>
        <h2 className={"my-3"}>Payers</h2>
        <Button variant={"success"}>Add payment</Button>
      </div>
      <div className={"border border-secondary rounded-3 p-2"}>
        <ListGroup className={""} variant={"flush"}>
          {membersWithDeposits.length > 0 ? (
            event.members.map((member) =>
              member.deposits.map((deposit) => (
                <ListGroup.Item key={deposit.id}>
                  <span>
                    {deposit.description} for {deposit.value}
                  </span>
                </ListGroup.Item>
              )),
            )
          ) : (
            <ListGroup.Item>
              <span>Nothing</span>
            </ListGroup.Item>
          )}
        </ListGroup>
      </div>
    </>
  );
}

function SettingsElements() {
  return (
    <>
      <h3 className={"mt-4 mb-2"}> Danger Zone </h3>
      <ListGroup className={"border border-danger rounded-2"} variant={"flush"}>
        <ListGroup.Item className={"d-flex flex-row align-items-center"}>
          <span className={"flex-grow-1"}>Leave this event</span>
          <Button variant={"danger"} className={"my-2"}>
            {" "}
            Leave{" "}
          </Button>
        </ListGroup.Item>
        <ListGroup.Item
          className={
            "d-flex flex-row justify-content-between align-items-center"
          }
        >
          <span className={"flex-grow-1"}>Delete this event</span>
          <Button variant={"danger"} className={"my-2"}>
            {" "}
            Delete event{" "}
          </Button>
        </ListGroup.Item>
      </ListGroup>
    </>
  );
}
